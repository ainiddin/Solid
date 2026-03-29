from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
async def detect_ai_text(essay: str) -> dict:
    prompt = f"""Analyze this essay for signs of AI generation (e.g., ChatGPT).
Return ONLY valid JSON: {{"ai_flag": "Low or Medium or High", "reason": "1-2 sentences"}}

Essay:
{essay}
"""
    resp = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)
