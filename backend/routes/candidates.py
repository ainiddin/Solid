from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend import database as db
import json

router = APIRouter()

class CandidateIn(BaseModel):
    name: str
    age: int
    city: str
    school: str
    gpa: float
    ielts: Optional[str] = None
    program: Optional[str] = None
    achievements: Optional[str] = None
    essay: Optional[str] = None
    motivation: Optional[str] = None

@router.post("/candidates")
async def create_candidate(c: CandidateIn):
    data = c.dict()
    data["certificates"] = "[]"
    candidate_id = await db.insert_candidate(data)
    return {"id": candidate_id}

@router.get("/candidates")
async def get_candidates():
    rows = await db.get_all_candidates()
    for r in rows:
        if r.get("score_json"):
            try:
                parsed = json.loads(r["score_json"])
                r["total_score"] = parsed.get("total_score")
                r["recommendation"] = parsed.get("recommendation")
                r["scoring_logic"] = parsed.get("scoring_logic")
            except:
                r["total_score"] = None
    return rows

@router.get("/candidate/{candidate_id}")
async def get_candidate(candidate_id: int):
    c = await db.get_candidate(candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    return c

@router.patch("/candidate/{candidate_id}/status")
async def update_status(candidate_id: int, status: str):
    await db.update_candidate_status(candidate_id, status)
    return {"ok": True}