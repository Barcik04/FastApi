from fastapi import FastAPI, HTTPException
from src.db import db   # ← relative import because main.py is inside the same package

app = FastAPI(title="FastAPI + Postgres (no ORM)")

@app.on_event("startup")
async def on_startup():
    await db.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await db.disconnect()

@app.get("/")
def root():
    return {"ok": True}

@app.get("/db/ping")
async def db_ping():
    try:
        val = await db.fetchval("SELECT 1;")
        return {"db_ok": val == 1}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/db/time")
async def db_time():
    try:
        now = await db.fetchval("SELECT NOW();")
        return {"now": now}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

