from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend import database as db
from backend.routes import candidates, score

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield

app = FastAPI(title="inVision U Screening API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router)
app.include_router(score.router)

FRONTEND = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.get('/')
async def candidate_page():
    return FileResponse(os.path.join(FRONTEND, 'candidate.html'))

@app.get('/admin')
async def admin_page():
    return FileResponse(os.path.join(FRONTEND, 'admin.html'))