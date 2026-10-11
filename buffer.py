
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def models():
    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={
            "Authorization": f"Bearer {os.getenv('API')}"
        },
        timeout=15,
    )
    response.raise_for_status()

    data = response.json()

    with open("models.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Models saved in formatted JSON!")

if __name__ == "__main__":
    models()
