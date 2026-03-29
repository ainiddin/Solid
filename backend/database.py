import aiosqlite
import json

DB_PATH = "candidates.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, age INTEGER, city TEXT, school TEXT,
                gpa REAL, achievements TEXT, essay TEXT, motivation TEXT,
                score_json TEXT DEFAULT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        await db.commit()

async def insert_candidate(data: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO candidates (name,age,city,school,gpa,achievements,essay,motivation) VALUES (?,?,?,?,?,?,?,?)",
            (data["name"], data["age"], data["city"], data["school"],
             data["gpa"], data["achievements"], data["essay"], data["motivation"])
        )
        await db.commit()
        return cur.lastrowid

async def get_all_candidates():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM candidates")
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def get_candidate(cid: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM candidates WHERE id=?", (cid,))
        row = await cur.fetchone()
        return dict(row) if row else None

async def save_score(cid: int, score_json: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE candidates SET score_json=? WHERE id=?", (score_json, cid))
        await db.commit()

async def update_status(cid: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE candidates SET status=? WHERE id=?", (status, cid))
        await db.commit()
