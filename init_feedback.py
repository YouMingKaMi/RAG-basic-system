import sqlite3
from app.config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER UNIQUE NOT NULL,
        rating INTEGER NOT NULL CHECK (rating IN (0, 1)),
        rating_content TEXT,
        created_at TEXT NOT NULL
    )
""")

conn.commit()
conn.close()