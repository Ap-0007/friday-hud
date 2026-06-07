"""
Memory tools — persistent neural archive for F.R.I.D.A.Y.
Allows the assistant to remember facts about the user and past projects.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neural_archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact_key TEXT UNIQUE,
            fact_value TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def remember_fact(key: str, value: str, **kwargs) -> str:
    """
    Save a fact to the permanent archive. 
    Example: remember_fact("coffee_preference", "Black, no sugar")
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO neural_archive (fact_key, fact_value, timestamp)
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return f"Information archived, boss. I'll remember that {key} is {value}."
    except Exception as e:
        return f"Neural link error while archiving: {str(e)}"

def recall_fact(query: str, **kwargs) -> str:
    """
    Search the neural archive for matching facts.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Escape special characters for SQL LIKE
        escaped_query = query.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        like_pattern = f"%{escaped_query}%"

        cursor.execute('''
            SELECT fact_key, fact_value FROM neural_archive
            WHERE fact_key LIKE ? ESCAPE '\\' OR fact_value LIKE ? ESCAPE '\\'
        ''', (like_pattern, like_pattern))
        results = cursor.fetchall()
        conn.close()

        if not results:
            return f"I've searched the archives, boss, but I found no record of '{query}'."

        summary = [f"{k}: {v}" for k, v in results]
        return "Archive retrieval complete. Here's what I found:\n" + "\n".join(summary)
    except Exception as e:
        return f"Error retrieving from archive: {str(e)}"

def list_all_memories(**kwargs) -> str:
    """List everything currently stored in the memory archive."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT fact_key, fact_value FROM neural_archive')
        results = cursor.fetchall()
        conn.close()

        if not results:
            return "The archive is currently empty, boss."

        summary = [f"- {k}: {v}" for k, v in results]
        return "Current neural archive contents:\n" + "\n".join(summary)
    except Exception as e:
        return f"System error reading archive: {str(e)}"

def register(mcp):
    init_db()
    mcp.tool()(remember_fact)
    mcp.tool()(recall_fact)
    mcp.tool()(list_all_memories)
