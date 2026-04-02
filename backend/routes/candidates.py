<<<<<<< HEAD
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
=======
from fastapi import APIRouter, HTTPException
from typing import List
import json
from backend.models import CandidateIn
from backend import database as db

router = APIRouter()

@router.post("/candidates", status_code=201)
async def create_candidate(body: CandidateIn):
    cid = await db.insert_candidate(body.model_dump())
    return {"id": cid, "message": "Candidate saved"}

@router.post("/candidates/batch", status_code=201)
async def create_candidates_batch(body: List[CandidateIn]):
    ids = []
    for candidate in body:
        cid = await db.insert_candidate(candidate.model_dump())
        ids.append(cid)
    return {"ids": ids, "message": f"{len(ids)} candidates saved"}

@router.get("/candidates")
async def list_candidates():
    rows = await db.get_all_candidates()
    result = []
    for r in rows:
        entry = {k: v for k, v in r.items() if k not in ("essay", "motivation", "achievements")}
        if r.get("score_json"):
            s = json.loads(r["score_json"])
            entry["total_score"] = s.get("total_score")
            entry["recommendation"] = s.get("recommendation")
            entry["ai_text_flag"] = s.get("ai_text_flag")
            entry["scoring_logic"] = s.get("scoring_logic")
        result.append(entry)
    return result

@router.get("/candidate/{cid}")
async def get_candidate(cid: int):
    row = await db.get_candidate(cid)
    if not row:
        raise HTTPException(404, "Not found")
    if row.get("score_json"):
        row["score_data"] = json.loads(row["score_json"])
    return row

@router.patch("/candidate/{cid}/status")
async def set_status(cid: int, status: str):
    if status not in ("shortlisted", "rejected", "pending"):
        raise HTTPException(400, "Invalid status")
    await db.update_status(cid, status)
>>>>>>> 74f7674ba2fbf83ea646c78da1fc74bac6f7205d
    return {"ok": True}