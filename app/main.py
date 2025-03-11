from fastapi import FastAPI, HTTPException
import asyncpg
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Connexion à PostgreSQL
async def get_db():
    return await asyncpg.connect(DATABASE_URL)

# Route pour récupérer tous les artistes
@app.get("/artists/")
async def get_artists():
    conn = await get_db()
    try:
        rows = await conn.fetch("SELECT * FROM artists;")
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# Route pour récupérer un artiste par son ID
@app.get("/artists/{artist_id}")
async def get_artist(artist_id: int):
    conn = await get_db()
    try:
        row = await conn.fetchrow("SELECT * FROM artists WHERE artist_id = $1;", artist_id)
        if not row:
            raise HTTPException(status_code=404, detail="Artist not found")
        return dict(row)
    finally:
        await conn.close()
