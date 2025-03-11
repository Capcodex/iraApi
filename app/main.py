from fastapi import FastAPI
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Création du pool de connexions
@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/")
def read_root():
    return {"message": "API déployée sur Railway 🚀"}

@app.get("/artists")
async def get_artists():
    async with app.state.db.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM artists")
    return [dict(row) for row in rows]
