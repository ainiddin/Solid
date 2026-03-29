from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
SYSTEM_PROMPT = """You are a candidate screening AI for inVision U (inDrive).
Score the candidate 0-100 across these weighted dimensions:
- skills (max 25): academic/technical background
- motivation (max 25): clarity of purpose and values alignment
- leadership (max 30): real leadership signals, not just titles
- growth (max 20): trajectory and learning mindset

Return ONLY valid JSON exactly matching this schema:
{
  "total_score": <number>,
  "dimensions": {
    "skills":     {"score": <number>, "reason": "<1-2 sentences>"},
    "motivation": {"score": <number>, "reason": "<1-2 sentences>"},
    "leadership": {"score": <number>, "reason": "<1-2 sentences>"},
    "growth":     {"score": <number>, "reason": "<1-2 sentences>"}
  },
  "ai_text_flag": "<Low|Medium|High>",
  "recommendation": "<Strong candidate — shortlist | Promising — review | Needs more context | Not recommended>",
  "key_strengths": ["<strength1>", "<strength2>"],
  "risks": ["<risk1>"]
}

IMPORTANT: Do NOT base any score on demographics, race, or socioeconomic status."""

async def score_candidate(candidate: dict) -> dict:
    user_prompt = f"Candidate data:\n{json.dumps(candidate, ensure_ascii=False, indent=2)}"
    resp = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content)
