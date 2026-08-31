import sqlite3

conn = sqlite3.connect("storage/llm_history.db")

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS message(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
""")

conn.commit()
conn.close()