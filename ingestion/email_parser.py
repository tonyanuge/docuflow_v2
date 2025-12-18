import email
from email import policy

def extract_text_from_eml(path: str) -> str:
    print(f"[DEBUG] Extracting email (EML): {path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        msg = email.message_from_file(f, policy=policy.default)

    text = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_content()
    else:
        text = msg.get_content()

    return text
