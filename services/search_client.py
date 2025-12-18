import requests

API_URL = "http://127.0.0.1:8000"

def embed_text(text: str):
    payload = {"text": text}
    response = requests.post(f"{API_URL}/embed", json=payload)
    response.raise_for_status()
    return response.json()["embedding"]


def semantic_search(query: str, documents: list[str]):
    payload ={
        "query": query,
        "documents": documents
    }
    response = requests.post(f"{API_URL}/semantic-search", json=payload)
    response.raise_for_status()
    return response.json()["results"]