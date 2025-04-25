# app/ui/routes.py
from app.db.session_store import DB_PATH, create_session, add_message, get_messages, get_all_sessions, delete_session as db_delete_session, update_message
from flask import session as flask_session
from app.utils.helpers import infer_title_from_query
from uuid import uuid4
import sqlite3
from flask import request, jsonify
from app.ingestion.document_loader import load_document
from app.vectorstore.faiss_store import LocalVectorStore
from app.ingestion.chunker import split_text
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.llm.rag_chain import RAGPipeline
rag_pipeline = RAGPipeline()


ui_blueprint = Blueprint(
    "ui", __name__, template_folder="templates", static_folder="static")


@ui_blueprint.route('/')
def index():
    sessions = get_all_sessions()
    session_id = flask_session.get('chat_session_id')
    messages = get_messages(session_id) if session_id else []

    flash_msg = request.args.get('msg')
    if flash_msg:
        flash(flash_msg, 'success')

    return render_template('index.html', messages=messages, sessions=sessions)


@ui_blueprint.route('/upload', methods=['GET', 'POST'], endpoint='upload')
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            if request.headers.get('accept') == 'application/json':
                return jsonify({"success": False, "message": "No file part"})
            flash("No file part", "danger")
            return redirect(request.url)

        file = request.files.get('file')
        if not file or file.filename == '':
            if request.headers.get('accept') == 'application/json':
                return jsonify({"success": False, "message": "No file selected"})
            flash("No file selected", "danger")
            return redirect(request.url)

        if file and file.filename.endswith(('.pdf', '.txt', '.csv', '.docx')):
            filename = secure_filename(file.filename)
            os.makedirs('data/raw', exist_ok=True)
            upload_path = os.path.join('data/raw', filename)
            file.save(upload_path)

            try:
                text = load_document(upload_path)
                chunks = split_text(text)
                store = LocalVectorStore()
                store.add_texts(chunks)

                if request.headers.get('accept') == 'application/json':
                    return jsonify({"success": True, "message": "File uploaded and indexed successfully!"})
                flash("File uploaded and indexed successfully!", "success")
            except Exception as e:
                if request.headers.get('accept') == 'application/json':
                    return jsonify({"success": False, "message": f"Error indexing file: {str(e)}"})
                flash(f"Error indexing file: {str(e)}", "danger")

            return redirect(url_for('ui.index'))
        else:
            if request.headers.get('accept') == 'application/json':
                return jsonify({"success": False, "message": "Unsupported file type"})
            flash("Unsupported file type", "danger")

    return render_template('upload.html')

# Add this new function to update session titles


def update_session_title(session_id: str, title: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
    rows_affected = c.rowcount
    print(f"DEBUG: Title update affected {rows_affected} rows")
    conn.commit()
    conn.close()

# Update the chat route


@ui_blueprint.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query')
    title = infer_title_from_query(query)

    if 'chat_session_id' not in flask_session:
        session_id = str(uuid4())
        flask_session['chat_session_id'] = session_id
        create_session(session_id, title)
        print(f"DEBUG: Created new session {session_id} with title {title}")
    else:
        session_id = flask_session['chat_session_id']
        # If this is the first message, update the session title
        messages = get_messages(session_id)
        if len(messages) == 0:
            update_session_title(session_id, title)
            print(f"DEBUG: Updated session {session_id} title to {title}")

    # Rest remains the same
    add_message(session_id, 'user', query)

    answer = rag_pipeline.run(query)
    add_message(session_id, 'bot', answer)

    sessions = get_all_sessions()
    messages = get_messages(session_id)
    return render_template('index.html', answer=answer, messages=messages, sessions=sessions)


@ui_blueprint.route('/session/<session_id>')
def view_session(session_id):
    flask_session['chat_session_id'] = session_id
    messages = get_messages(session_id)
    sessions = get_all_sessions()
    return render_template('index.html', messages=messages, sessions=sessions)

# Keep only one definition of this route/function


@ui_blueprint.route('/session/delete/<session_id>', methods=['POST'])
def delete_session(session_id):
    db_delete_session(session_id)
    if flask_session.get('chat_session_id') == session_id:
        flask_session.pop('chat_session_id')
    flash("Session deleted", "success")
    return redirect(url_for('ui.index'))


@ui_blueprint.route("/resend", methods=["POST"])
def resend():
    try:
        data = request.get_json()
        new_query = data["query"]
        message_id = data.get("message_id")
        session_id = flask_session.get('chat_session_id')

        if not session_id or not message_id:
            return jsonify({"success": False, "message": "Missing session or message ID"})

        # Update the original user message
        update_message(message_id, "user", new_query)

        # Rerun RAG with new query
        new_answer = rag_pipeline.run(new_query)

        # Update bot message (assumes next message after user is bot)
        update_message(message_id + 1, "bot", new_answer)

        return jsonify({
            "success": True,
            "new_query": new_query,
            "new_answer": new_answer
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Update the chat-stream route


@ui_blueprint.route('/chat-stream', methods=['POST'])
def chat_stream():
    query = request.json.get('query')
    session_id = flask_session.get('chat_session_id')

    if not session_id:
        title = infer_title_from_query(query)
        session_id = str(uuid4())
        flask_session['chat_session_id'] = session_id
        create_session(session_id, title)
    else:
        # If this is the first message, update the session title
        messages = get_messages(session_id)
        if len(messages) == 0:
            title = infer_title_from_query(query)
            update_session_title(session_id, title)

    # Rest remains the same
    add_message(session_id, 'user', query)
    answer = rag_pipeline.run(query)
    add_message(session_id, 'bot', answer)

    return jsonify({
        "success": True,
        "answer": answer,
        "query": query,
        "session_id": session_id
    })

# Add this new route to your routes.py file


@ui_blueprint.route('/new-chat')
def new_chat():
    # Create a new session
    new_session_id = str(uuid4())
    flask_session['chat_session_id'] = new_session_id
    create_session(new_session_id, "New Conversation")  # Add a default title

    # Redirect to index with empty chat
    return redirect(url_for('ui.index'))
