from ingestion.extract_text import extract_text

path = "sample_email.eml"

text = extract_text(path)

print("\n--- Extracted Email Text ---\n")
print(text)
