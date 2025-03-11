from fastapi import FastAPI
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API déployée sur Railway 🚀"}

# Exemple de route pour récupérer les artistes
@app.get("/artists")
async def get_artists():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM artists")
    await conn.close()
    return [dict(row) for row in rows]
