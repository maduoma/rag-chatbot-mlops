# tests/test_db_session.py

from app.db import session_store

def test_create_and_get_session():
    test_id = "test-session"
    session_store.create_session(test_id, "Test Title")
    sessions = session_store.get_all_sessions()
    assert any(s["id"] == test_id for s in sessions)

def test_add_and_fetch_messages():
    session_id = "test-session-2"
    session_store.create_session(session_id)
    session_store.add_message(session_id, "user", "Hello")
    session_store.add_message(session_id, "bot", "Hi there!")

    messages = session_store.get_messages(session_id)
    assert len(messages) >= 2
