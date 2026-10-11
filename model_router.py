from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


async def router(message: str) -> str:
    api_key = os.getenv("API")
    if not api_key:
        raise RuntimeError("Missing API key. Add API=... to your .env file or environment.")

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    prompt = f"""
        Compress the following prompt.
        Requirements:
- Max compression
- No information loss
- Prefer keywords over sentences
- Remove articles (a, an, the) when possible
- Merge similar requirements
- Shorten verbose descriptions
- Return only final prompt

Prompt:
{message}
 """
    result = await llm.ainvoke(prompt)
    return result.content