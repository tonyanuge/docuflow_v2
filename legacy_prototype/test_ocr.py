from ingestion.extract_text import extract_text

path = "sample_image.jpg"   # Replace with an actual image

text = extract_text(path)

print("\n--- OCR Extracted Text ---\n")
print(text[:2000])
