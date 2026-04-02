from fastapi import APIRouter, HTTPException
import json
from backend import database as db
from backend.scorer import score_candidate
from backend.ai_detector import detect_ai_text

router = APIRouter()

def sanitize(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(i) for i in obj]
    return obj

@router.post("/score/{cid}")
async def run_score(cid: int):
    row = await db.get_candidate(cid)
    if not row:
        raise HTTPException(404, "Candidate not found")

    ai_check = await detect_ai_text(row["essay"] + " " + row["motivation"])
    candidate_payload = {k: v for k, v in row.items()
                         if k not in ("id", "score_json", "status")}

    result = await score_candidate(candidate_payload)
    result["ai_text_flag"] = ai_check.get("ai_flag", result.get("ai_text_flag", "Unknown"))
    result["ai_flag_reason"] = ai_check.get("reason", "")
    result["human_in_the_loop"] = "This score is advisory only. Final decisions must be made by the admissions committee."

    result = sanitize(result)
    await db.save_score(cid, json.dumps(result, ensure_ascii=False))
    return result