from services.search_client import semantic_search

documents = [
    "Customer wants to update payment date",
    "This is an urgent request for support",
    "Loan modification extension needed",
    "Please review attached file"
]

result = semantic_search("urgent payment update", documents)

print("\n--- Semantic Search Results ---")
for r in result:
    print(f"{r['score']:.3f}  |  {r['document']}")
