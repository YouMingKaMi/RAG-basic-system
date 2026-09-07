import sqlite3
from datetime import datetime


db_loc = "storage/documents.db"

def get_connection():
    conn = sqlite3.connect(db_loc)
    return conn

def create_document(original_filename, stored_filename, stored_path, file_size, status):
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO documents(original_filename,stored_filename,stored_path,file_size,status,created_at)
                VALUES (?,?,?,?,?,?)
""", (original_filename, stored_filename, stored_path, file_size, status, datetime.now().isoformat()))
    
    document_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return document_id

def search_all_document():
    conn = sqlite3.connect(db_loc)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM documents")

    rows = cur.fetchall()

    conn.close()
    return [dict(row) for row in rows]

def search_one_document(document_id: int):
    conn = sqlite3.connect(db_loc)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE id = ?", (document_id,))

    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)


def create_chunks(conn, document_id: int, chunks: list[str]):
    cur = conn.cursor()

    for chunk_id, chunk in enumerate(chunks, start=1):
        cur.execute("""
            INSERT INTO chunks(document_id, chunk_id, content, created_at)
                    VALUES(?,?,?,?)
                    """,(document_id, chunk_id, chunk, datetime.now().isoformat()))

def delete_chunks(conn, document_id: int):
    cur = conn.cursor()
    cur.execute("DELETE FROM chunks WHERE document_id = ?",(document_id,))

def update_document_status(conn, document_id: int, status: str):
    cur = conn.cursor()

    cur.execute("""
            UPDATE documents SET status = ? WHERE id = ?
                """,(status, document_id))

def search_chunks_by_keyword(keyword:str):
    if not keyword.strip():
        return []
    conn = sqlite3.connect(db_loc)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM chunks WHERE content LIKE ?",(f"%{keyword}%", ))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_chunks_by_document(document_id: int):
    conn = sqlite3.connect(db_loc)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_id",(document_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_chunk_content(document_id: int, chunk_id: int):
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    cur.execute("SELECT content FROM chunks WHERE document_id = ? AND chunk_id = ? ",(document_id, chunk_id))
    result = cur.fetchone()
    if result is None:
        conn.close()
        return None
    (content,) = result
    conn.close()
    return content

def get_session_content(session_id: int)->list:
    conn = sqlite3.connect(db_loc)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM message WHERE session_id = ? ORDER BY id
        """,(session_id,))
    rows = cur.fetchall()
    conn.close()
    message = []
    roles = [dict(row)["role"] for row in rows]
    contents = [dict(row)["content"] for row in rows]
    for role, content in zip(roles, contents):
        message.append({
            "role": role,
            "content":content
        })
    return message

def add_session_content(session_id: int, question: dict, answer: dict):
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    for dic in [question, answer] :
        cur.execute("""
            INSERT INTO message(session_id, role, content, created_at)
                VALUES(?,?,?,?)
            """,(session_id, dic["role"], dic["content"], datetime.now().isoformat() ))
    conn.commit()
    conn.close()

def create_new_session() -> int:
    conn = sqlite3.connect(db_loc)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sessions(created_at)
            VALUES(?)
        """,(datetime.now().isoformat(),))
    session_id = cur.lastrowid
    conn.commit()
    conn.close()
    return session_id

def add_rating(message_id: int, rating: int, rating_content: str):
    with sqlite3.connect(db_loc) as conn:
        conn.execute("""
            INSERT INTO feedback(message_id, rating, rating_content, created_at)
                VALUES(?,?,?,?)
        """,(message_id, rating, rating_content, datetime.now().isoformat()))

def message_exists(message_id: int):
    with sqlite3.connect(db_loc) as conn:
        cur = conn.execute("SELECT * FROM message WHERE id = ?",(message_id,))
        row = cur.fetchone()
        return row is not None

def rating_exists(message_id: int):
    with sqlite3.connect(db_loc) as conn:
        cur =conn.execute("SELECT * FROM feedback WHERE message_id = ?",(message_id,))
        row = cur.fetchone()
        return row is not None

def update_rating(message_id: int, rating: int, rating_content: str):
    with sqlite3.connect(db_loc) as conn:
        conn.execute("UPDATE feedback SET rating = ?, rating_content = ? WHERE message_id = ?",(rating, rating_content, message_id))


