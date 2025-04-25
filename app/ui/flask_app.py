# app/ui/flask_app.py
from app.db.session_store import init_db
from flask import Flask
from app.ui.routes import ui_blueprint

def create_app():
    init_db()
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'data/raw'
    app.secret_key = 'super-secret-key'  # Use environment variable in prod

    app.register_blueprint(ui_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
