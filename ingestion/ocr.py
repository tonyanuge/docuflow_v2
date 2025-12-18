import pytesseract
from PIL import Image
import os

# Tell pytesseract exactly where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(path: str) -> str:
    print(f"[DEBUG] OCR: Extracting text from image: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"OCR Error: File not found: {path}")

    try:
        img = Image.open(path)
    except Exception as e:
        raise ValueError(f"OCR Error: Cannot open image: {e}")

    # Perform OCR
    text = pytesseract.image_to_string(img)

    print(f"[DEBUG] OCR: Extracted {len(text)} characters")
    return text
