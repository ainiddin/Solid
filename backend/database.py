import aiosqlite
import json

DB_PATH = "candidates.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, age INTEGER, city TEXT, school TEXT,
                gpa REAL, ielts TEXT, program TEXT,
                achievements TEXT, essay TEXT, motivation TEXT,
                certificates TEXT DEFAULT '[]',
                score_json TEXT DEFAULT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        for col, typ in [("ielts","TEXT"),("program","TEXT"),("certificates","TEXT")]:
            try:
                await db.execute(f"ALTER TABLE candidates ADD COLUMN {col} {typ}")
            except:
                pass
        await db.commit()

async def insert_candidate(data: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO candidates (name,age,city,school,gpa,ielts,program,achievements,essay,motivation,certificates) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (data.get("name"), data.get("age"), data.get("city"), data.get("school"),
             data.get("gpa"), data.get("ielts"), data.get("program"),
             data.get("achievements"), data.get("essay"), data.get("motivation"),
             data.get("certificates","[]"))
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

async def update_candidate_status(cid: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE candidates SET status=? WHERE id=?", (status, cid))
        await db.commit()

async def update_status(cid: int, status: str):
    await update_candidate_status(cid, status)