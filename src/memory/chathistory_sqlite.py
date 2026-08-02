"""
SQLite-backed persistent memory and document metadata storage.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict

import os

DB_PATH = Path(os.environ.get("SQLITE_DB_PATH", "adaptive_rag.db"))

def init_db():
    """Initialize the SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for chat messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    
    # Table for document metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize DB on module import
init_db()


class SQLiteChatMessageHistory(BaseChatMessageHistory):
    """SQLite-backed chat history storage."""

    def __init__(self, session_id: str):
        self.session_id = session_id

    @property
    def messages(self) -> List[BaseMessage]:
        """Retrieve all messages for this session from the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT message FROM messages WHERE session_id = ? ORDER BY id ASC',
            (self.session_id,)
        )
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append(json.loads(row[0]))
        
        return messages_from_dict(items)

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the database."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        msg_dict = message_to_dict(message)
        cursor.execute(
            'INSERT INTO messages (session_id, message) VALUES (?, ?)',
            (self.session_id, json.dumps(msg_dict))
        )
        conn.commit()
        conn.close()

    def clear(self) -> None:
        """Clear all messages for this session."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM messages WHERE session_id = ?',
            (self.session_id,)
        )
        conn.commit()
        conn.close()


class DocumentManager:
    """Manages document metadata in SQLite."""
    
    @staticmethod
    def add_document(filename: str, description: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO documents (filename, description) VALUES (?, ?)',
            (filename, description)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_documents() -> List[Dict]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, filename, description FROM documents ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [{"id": r[0], "filename": r[1], "description": r[2]} for r in rows]
    
    @staticmethod
    def delete_document(filename: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM documents WHERE filename = ?', (filename,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_all():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM documents')
        conn.commit()
        conn.close()
