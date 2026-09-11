import sqlite3
import sqlite_vec
import numpy as np
import os

DB_PATH = "vector_db/docuflow.db"

def get_connection():
    os.makedirs("vector_db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    conn.enable_load_extension(True)

    # Load vec0.dll from the project folder
    dll_path = os.path.join("vector_db", "vec0.dll")

    try:
        conn.load_extension(dll_path)
        print(f"[DEBUG] Loaded sqlite-vec from: {dll_path}")
    except Exception as e:
        print("[ERROR] Failed loading vec0.dll:", e)
        raise e

    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create main table with metadata
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        content TEXT,
        embedding BLOB
    )
    """)

    # Create vector index table (dimension = 384 for MiniLM-L6-V2)
    cur.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS documents_idx USING vec0(
        embedding FLOAT[384]
    )
    """)

    conn.commit()
    conn.close()

def insert_document(filename: str, content: str, embedding: list):
    print("\n[DEBUG] --- insert_document called ---")
    print("[DEBUG] filename:", filename)

    # Convert embedding → numpy array
    emb_array = np.array(embedding, dtype=np.float32)

    # Normalize (cosine search compatibility)
    emb_norm = emb_array / np.linalg.norm(emb_array)

    # Convert to bytes
    emb_bytes = emb_norm.tobytes()

    conn = get_connection()
    cur = conn.cursor()

    # Main document table (OK)
    cur.execute(
        "INSERT INTO documents (filename, content, embedding) VALUES (?, ?, ?)",
        (filename, content, emb_bytes)
    )

    doc_id = cur.lastrowid

    # Index table — MUST use bytes rather than list for your build
    cur.execute(
        "INSERT INTO documents_idx (rowid, embedding) VALUES (?, ?)",
        (doc_id, emb_bytes)
    )

    conn.commit()
    conn.close()

    print("[OK] Document inserted.")
    return doc_id


    # ----------------------------------------------


def semantic_search(query_embedding: list, limit=5):
    conn = get_connection()
    cur = conn.cursor()

    # Normalize the query embedding
    qe = np.array(query_embedding, dtype=np.float32)
    qe_norm = qe / np.linalg.norm(qe)
    q = qe_norm.tobytes()

    cur.execute("""
        SELECT 
            documents.filename,
            documents.content,
            documents_idx.distance
        FROM documents_idx
        JOIN documents
            ON documents_idx.rowid = documents.id
        WHERE documents_idx.embedding MATCH ? AND k = ?
        ORDER BY documents_idx.distance ASC
        LIMIT ?
    """, (q, limit, limit))

    results = cur.fetchall()
    conn.close()
    return results




