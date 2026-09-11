from ingestion.extract_text import extract_text
from nlp.embedder import get_embedding
from vector_db.vector_store import insert_document, semantic_search

content = "This is a payment update request."
embedding = get_embedding(content)

insert_document("sample.txt", content, embedding)
print("[OK] Document inserted.")

results = semantic_search(get_embedding("payment update"))

print("\n--- Search Results ---")
for row in results:
    print(row)

print("[DEBUG] Number of results:", len(results))
