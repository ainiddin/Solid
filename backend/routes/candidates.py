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
    return {"ok": True}