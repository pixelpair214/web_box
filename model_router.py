from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json


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








async def optimize_output(question: str, response: str) -> str:
    classifier = ChatOpenAI(
        model="deepseek/deepseek-chat",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API"),
        max_tokens=50
    )

    classification_prompt = f"""
Classify the task based on the question and response.

Categories: coding, education, research, creative,
factual, reasoning, other.
Complexity: low, medium, high.

Return JSON only:
{{"category":"education","complexity":"low"}}

Question: {question}
Response: {response}
"""
    result = await classifier.ainvoke(classification_prompt)
    print("Classification tokens:", result.usage_metadata)
    details = json.loads(result.content)

    token_limits = {"low": 100, "medium": 500, "high": 1000}
    max_tokens = token_limits.get(details["complexity"], 100)

    output_llm = ChatOpenAI(
        model="deepseek/deepseek-chat",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("API"),
        max_tokens=max_tokens
    )

    compression_prompt = f"""
Compress the response for the given category and complexity.
Remove redundancy and preserve essential information.
For coding, preserve code and logic.
Return only the optimized response.

Category: {details["category"]}
Complexity: {details["complexity"]}
Response: {response}
"""
    result = await output_llm.ainvoke(compression_prompt)

    return result.content


