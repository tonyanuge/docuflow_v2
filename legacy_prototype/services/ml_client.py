import requests

API_URL = "http://127.0.0.1:8000"  # define the address of the API service.

def classify_text(text: str):
    playoad = {"text": text}

    try:

        response = requests.post(f"{API_URL}/classify", json=playoad)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}