import sqlite3
from datetime import datetime

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

    result = cur.fetchall()

    conn.close()
    return result

def search_one_document(document_id: int):
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    cur.execute("SELECT * FROM documents WHERE id = ?", (document_id,))

    result = cur.fetchone()

    conn.close()
    return result


def create_chunks(document_id: int, chunks: list[str]):
    conn = sqlite3.connect("storage/documents.db")
    cur = conn.cursor()

    for chunk_id, chunk in enumerate(chunks, start=1):
        cur.execute("""
            INSERT INTO chunks(document_id, chunk_id, content, created_at)
                    VALUES(?,?,?,?)
                    """,(document_id, chunk_id, chunk, datetime.now().isoformat()))

    conn.commit()    
    conn.close()

def delete_chunks(document_id: int):
    conn = sqlite3.connect("storage/documents.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM chunks WHERE document_id = ?",(document_id,))

    conn.commit()
    conn.close()

def update_document_status(document_id: int, status: str):
    conn = sqlite3.connect("storage/documents.db")
    cur = conn.cursor()

    cur.execute("""
            UPDATE documents SET status = ? WHERE id = ?
                """,(status, document_id))
        
    conn.commit()
    conn.close()

def search_chunks_by_keyword(keyword:str):
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM chunks WHERE content LIKE ?",(f"%{keyword}%", ))
    result = cur.fetchall()
    conn.close()
    return result

def get_chunks_by_document(document_id: int):
    conn = sqlite3.connect("storage/documents.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_id",(document_id,))
    result = cur.fetchall()
    conn.close()
    return result

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

