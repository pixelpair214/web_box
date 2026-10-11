import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import model_router

load_dotenv()

api_key = os.getenv("API")
if not api_key:
    raise RuntimeError("Missing API key. Add API=... to your .env file or environment.")

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


async def chat(message: str) -> str:
    response = await llm.ainvoke(message)
    return response.content


async def main():
    while True:
        message = await asyncio.to_thread(input, "user: ")
        if message.lower().strip() in ["exit", "bye"]:
            break
        task = await model_router.router(message)
        result = await chat(task)
        print(f"agent:{task}")
        print(f"ai: {result}")


if __name__ == "__main__":
    asyncio.run(main())
