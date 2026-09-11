from ingestion.extract_text import extract_text

path = "sample.pdf"  # change to any file you want

text = extract_text(path)

print("\n--- Extracted Text ---\n")
print(text[:1000])
