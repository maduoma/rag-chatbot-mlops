# tests/test_db_session.py
import uuid
import os
from app.db import session_store

# Track session IDs created during tests
test_session_ids = []

def setup_module(module):
    # Use a separate test database instead of the main one
    # This is the best approach to avoid contaminating the UI
    session_store.DB_PATH = "data/test_chat_sessions.db"
    
    # If test DB exists, remove it for a clean start
    if os.path.exists(session_store.DB_PATH):
        os.remove(session_store.DB_PATH)
    
    # Initialize the test database
    session_store.init_db()

def teardown_module(module):
    # Clean up - delete the test DB after all tests
    if os.path.exists(session_store.DB_PATH):
        os.remove(session_store.DB_PATH)

def test_create_and_get_session():
    test_id = f"test-session-{uuid.uuid4()}"
    test_session_ids.append(test_id)  # Track for cleanup
    session_store.create_session(test_id, "Test Title")
    sessions = session_store.get_all_sessions()
    assert any(s["id"] == test_id for s in sessions)

def test_add_and_fetch_messages():
    session_id = f"test-session-{uuid.uuid4()}"
    test_session_ids.append(session_id)  # Track for cleanup
    session_store.create_session(session_id)
    session_store.add_message(session_id, "user", "Hello")
    session_store.add_message(session_id, "bot", "Hi there!")

    messages = session_store.get_messages(session_id)
    assert len(messages) >= 2



# # tests/test_db_session.py

# import os
# import uuid
# import sqlite3
# from datetime import datetime
# from app.db import session_store

# # Store original values to restore later
# orig_db_path = None

# def setup_module(module):
#     global orig_db_path
#     # Save original values
#     orig_db_path = session_store.DB_PATH
    
#     # Use a file-based test database instead of in-memory
#     # More reliable than in-memory for cross-function testing
#     test_db_path = "test_sessions.db"
    
#     # Remove existing test DB if it exists
#     if os.path.exists(test_db_path):
#         os.remove(test_db_path)
    
#     # Set the session_store to use our test database
#     session_store.DB_PATH = test_db_path
    
#     # Initialize the database
#     conn = sqlite3.connect(test_db_path)
#     cursor = conn.cursor()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS sessions (
#         id TEXT PRIMARY KEY,
#         title TEXT,
#         created_at TEXT
#     )
#     ''')
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS messages (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         session_id TEXT,
#         sender TEXT,
#         content TEXT,
#         created_at TEXT,
#         FOREIGN KEY (session_id) REFERENCES sessions (id)
#     )
#     ''')
#     conn.commit()
#     conn.close()

# def teardown_module(module):
#     global orig_db_path
    
#     # Clean up the test database
#     if os.path.exists(session_store.DB_PATH):
#         try:
#             os.remove(session_store.DB_PATH)
#         except:
#             pass
    
#     # Restore original settings
#     if orig_db_path:
#         session_store.DB_PATH = orig_db_path

# def test_create_and_get_session():
#     test_id = f"test-session-{uuid.uuid4()}"
#     session_store.create_session(test_id, "Test Title")
#     sessions = session_store.get_all_sessions()
#     assert any(s["id"] == test_id for s in sessions)

# def test_add_and_fetch_messages():
#     session_id = f"test-session-{uuid.uuid4()}"
#     session_store.create_session(session_id)
#     session_store.add_message(session_id, "user", "Hello")
#     session_store.add_message(session_id, "bot", "Hi there!")
    
#     messages = session_store.get_messages(session_id)
#     assert len(messages) >= 2

# tests/test_db_session.py
# import uuid
# import os
# from app.db import session_store

# # Track session IDs created during tests
# test_session_ids = []

# def setup_module(module):
#     # Use a separate test database instead of the main one
#     # This is the best approach to avoid contaminating the UI
#     session_store.DB_PATH = "data/test_chat_sessions.db"
    
#     # If test DB exists, remove it for a clean start
#     if os.path.exists(session_store.DB_PATH):
#         os.remove(session_store.DB_PATH)
    
#     # Initialize the test database
#     session_store.init_db()

# def teardown_module(module):
#     # Clean up - delete the test DB after all tests
#     if os.path.exists(session_store.DB_PATH):
#         os.remove(session_store.DB_PATH)

# def test_create_and_get_session():
#     test_id = f"test-session-{uuid.uuid4()}"
#     test_session_ids.append(test_id)  # Track for cleanup
#     session_store.create_session(test_id, "Test Title")
#     sessions = session_store.get_all_sessions()
#     assert any(s["id"] == test_id for s in sessions)

# def test_add_and_fetch_messages():
#     session_id = f"test-session-{uuid.uuid4()}"
#     test_session_ids.append(session_id)  # Track for cleanup
#     session_store.create_session(session_id)
#     session_store.add_message(session_id, "user", "Hello")
#     session_store.add_message(session_id, "bot", "Hi there!")

#     messages = session_store.get_messages(session_id)
#     assert len(messages) >= 2

