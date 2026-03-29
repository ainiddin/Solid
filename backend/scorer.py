import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """You are a candidate screening AI for inVision U (inDrive).

Score the candidate and explain EVERY score in detail so the admissions committee understands exactly why.

Return ONLY valid JSON:
{
  "total_score": <0-100>,
  "dimensions": {
    "skills": {
      "score": <0-25>,
      "reason": "2-3 sentences explaining the score",
      "evidence": "exact quote or fact from candidate data that drove this score",
      "what_would_improve": "what would have made this score higher"
    },
    "motivation": {
      "score": <0-25>,
      "reason": "2-3 sentences explaining the score",
      "evidence": "exact quote or fact from candidate data that drove this score",
      "what_would_improve": "what would have made this score higher"
    },
    "leadership": {
      "score": <0-30>,
      "reason": "2-3 sentences explaining the score",
      "evidence": "exact quote or fact from candidate data that drove this score",
      "what_would_improve": "what would have made this score higher"
    },
    "growth": {
      "score": <0-20>,
      "reason": "2-3 sentences explaining the score",
      "evidence": "exact quote or fact from candidate data that drove this score",
      "what_would_improve": "what would have made this score higher"
    }
  },
  "scoring_logic": "3-4 sentences summarizing the overall scoring decision and how dimensions relate to each other",
  "ai_text_flag": "<Low|Medium|High>",
  "recommendation": "<Strong candidate — shortlist | Promising — review | Needs more context | Not recommended>",
  "key_strengths": ["specific strength with evidence", "specific strength with evidence"],
  "risks": ["specific risk with explanation"],
  "committee_notes": "2-3 actionable questions the committee should ask this candidate in interview"
}

RULES:
- evidence must be a direct reference to something the candidate actually wrote or provided
- Do NOT base any score on demographics, race, or socioeconomic status
- Be honest — if data is weak, say so clearly"""

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