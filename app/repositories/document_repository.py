import sqlite3
from datetime import datetime

def get_connection():
    conn = sqlite3.connect("storage/documents.db")
    return conn

def create_document(original_filename, stored_filename, stored_path, file_size, status):
    conn = sqlite3.connect("storage/documents.db")
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
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM documents")

    rows = cur.fetchall()

    conn.close()
    return [dict(row) for row in rows]

def search_one_document(document_id: int):
    conn = sqlite3.connect("storage/documents.db")
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
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM chunks WHERE content LIKE ?",(f"%{keyword}%", ))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_chunks_by_document(document_id: int):
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_id",(document_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_chunk_content(document_id: int, chunk_id: int):
    conn = sqlite3.connect("storage/documents.db")
    cur = conn.cursor()
    cur.execute("SELECT content FROM chunks WHERE document_id = ? AND chunk_id = ? ",(document_id, chunk_id))
    result = cur.fetchone()
    if result is None:
        conn.close()
        return None
    (content,) = result
    conn.close()
    return content

if __name__ == "__main__":
    create_document("hhh","dhi.db","what",1,"h")