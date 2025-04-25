# tests/test_db_session.py

import uuid
from app.db import session_store

# def setup_module(module):
    # Override DB_PATH for tests
    # session_store.DB_PATH = ":memory:"

def test_create_and_get_session():
    # test_id = "test-session"
    test_id = f"test-session-{uuid.uuid4()}"
    session_store.create_session(test_id, "Test Title")
    sessions = session_store.get_all_sessions()
    assert any(s["id"] == test_id for s in sessions)

def test_add_and_fetch_messages():
    # session_id = "test-session-2"
    session_id = f"test-session-{uuid.uuid4()}"
    session_store.create_session(session_id)
    session_store.add_message(session_id, "user", "Hello")
    session_store.add_message(session_id, "bot", "Hi there!")

    messages = session_store.get_messages(session_id)
    assert len(messages) >= 2
