from ingestion.extract_text import extract_text

path = "sample_scanned.pdf"  # Replace with a scanned or image-only PDF

text = extract_text(path)

print("\n--- Extracted Text from Scanned PDF ---\n")
print(text[:2000])
