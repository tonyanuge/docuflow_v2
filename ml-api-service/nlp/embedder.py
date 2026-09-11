from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """Return a vector embedding for the input text."""
    if not text or not isinstance(text, str):
        return []

    embedding = model.encode([text])[0]
    return embedding.tolist()


# -------------------------------------------------------
# NEW: Pure Python cosine similarity for 1D vectors
# -------------------------------------------------------
def cosine_sim_1d(vec_a, vec_b):
    """Cosine similarity for 1D numpy arrays or lists."""
    a = np.array(vec_a)
    b = np.array(vec_b)

    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)

    if norm == 0:
        return 0.0

    return float(dot / norm)


def semantic_search(query: str, documents: list):
    """Semantic search using sklearn cosine similarity."""
    if not documents or not isinstance(documents, list):
        return []

    query_emb = np.array(get_embedding(query)).reshape(1, -1)
    doc_embs = np.array([get_embedding(d) for d in documents])

    scores = cosine_similarity(query_emb, doc_embs)[0]

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {"document": doc, "score": float(score)}
        for doc, score in ranked
    ]
