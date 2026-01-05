import os
import requests

from dotenv import load_dotenv
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
def send_message(session_id: str, message: str):
    payload = {
        "session_id": session_id,
        "message": message
    }

    response = requests.post(
        f"{BACKEND_URL}/chat",
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    return response.json()


print(send_message("test-session", "What is the company's leave policy?"))