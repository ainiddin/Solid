from fastapi import APIRouter, UploadFile, File
from typing import List
import fitz  # pymupdf
import json

router = APIRouter()

@router.post("/upload-certificates")
async def upload_certificates(files: List[UploadFile] = File(...)):
    results = []
    for f in files:
        content = await f.read()
        text = ""
        if f.content_type == "application/pdf":
            try:
                doc = fitz.open(stream=content, filetype="pdf")
                for page in doc:
                    text += page.get_text()
                doc.close()
            except:
                text = ""
        results.append({
            "name": f.filename,
            "text": text.strip()[:2000]  # мак 2000 символ
        })
    return {"certificates": results}
