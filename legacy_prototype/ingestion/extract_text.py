import docx
import fitz  # PyMuPDF for PDF
import os
from ingestion.ocr import extract_text_from_image
from ingestion.email_parser import extract_text_from_eml



def extract_text_from_pdf(path: str) -> str:
    print(f"[DEBUG] Extracting PDF: {path}")

    text = ""
    doc = fitz.open(path)

    for page_number, page in enumerate(doc, start=1):
        page_text = page.get_text()

        # If text exists → use it (machine-readable PDF)
        if page_text.strip():
            print(f"[DEBUG] Page {page_number}: Text layer found")
            text += page_text
        else:
            # Fallback → scanned PDF → convert to image → OCR
            print(f"[DEBUG] Page {page_number}: No text found, using OCR fallback")

            pix = page.get_pixmap()
            img_path = f"temp_page_{page_number}.png"
            pix.save(img_path)

            text += extract_text_from_image(img_path)

            os.remove(img_path)

    doc.close()
    return text



def extract_text_from_docx(path: str) -> str:
    print(f"[DEBUG] Extracting DOCX: {path}")
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(path: str) -> str:
    print(f"[DEBUG] Extracting TXT: {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text(path: str) -> str:
    """Main entry point for ingestion layer."""
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)

    elif ext == ".docx":
        return extract_text_from_docx(path)

    elif ext == ".txt":
        return extract_text_from_txt(path)
    
    elif ext == ".eml":
        return extract_text_from_eml(path)

    elif ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".heic"]:
        return extract_text_from_image(path)

    else:
        raise ValueError(f"Unsupported file type (for now): {ext}")

