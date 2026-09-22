import requests
import dotenv
import os


dotenv.load_dotenv()

api = os.getenv("OPENROUTER_API_KEY")

print("Key loaded:", api is not None)

url = "https://openrouter.ai/api/v1/chat/completions"

name = "deepseek/deepseek-chat"

while True:
    print("User : ", end=" ")
    message = input()

    if message == "exit":
        break

    response = requests.post(
        url=url,
        headers={
            "Authorization": f"Bearer {api}",
            "Content-Type": "application/json"
        },
        json={
            "model": name,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )

    data = response.json()

    if "choices" in data:
        print(data["choices"][0]["message"]["content"])
    else:
        print(data)