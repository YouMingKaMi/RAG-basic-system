import sqlite3

conn = sqlite3.connect("storage/documents.db")

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_filename TEXT NOT NULL,
        stored_filename TEXT NOT NULL,
        stored_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL)
""")

conn.commit()
conn.close()

print("Documents database initalization!")