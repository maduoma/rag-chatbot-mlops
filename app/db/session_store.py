# app/db/session_store.py

import sqlite3
from datetime import datetime
from typing import List, Dict

DB_PATH = "data/chat_sessions.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        title TEXT,
        created_at TEXT
    )''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        sender TEXT,
        content TEXT,
        created_at TEXT,
        FOREIGN KEY(session_id) REFERENCES sessions(id)
    )''')
    conn.commit()
    conn.close()

def create_session(session_id: str, title: str = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (id, title, created_at) VALUES (?, ?, ?)", (
        session_id, title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}", datetime.now().isoformat()))
    conn.commit()
    conn.close()

def add_message(session_id: str, sender: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (session_id, sender, content, created_at) VALUES (?, ?, ?, ?)", (
        session_id, sender, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_messages(session_id: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, sender, content, created_at FROM messages WHERE session_id = ? ORDER BY created_at", (session_id,))
    messages = [{"id": row[0], "sender": row[1], "content": row[2], "created_at": row[3]} for row in c.fetchall()]
    conn.close()
    return messages


def get_all_sessions() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title FROM sessions ORDER BY created_at DESC")
    sessions = [{"id": row[0], "title": row[1]} for row in c.fetchall()]
    conn.close()
    return sessions

def delete_session(session_id: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    c.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def update_message(msg_id: int, sender: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE messages SET content = ? WHERE id = ? AND sender = ?", (content, msg_id, sender))
    conn.commit()
    conn.close()
