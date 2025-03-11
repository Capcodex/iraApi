from fastapi import FastAPI
import os
import asyncpg
from fastapi.responses import JSONResponse

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

# Création du pool de connexions
@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(DATABASE_URL)
        print("Connexion réussie à la base de données")
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise e  # Reraise the exception to stop the application

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/")
def read_root():
    return {"message": "API déployée sur Railway 🚀"}

# Exemple de route pour récupérer les artistes
@app.get("/artists")
async def get_artists():
    try:
        async with app.state.db.acquire() as conn:
            rows = await conn.fetch("SELECT id, name FROM artists LIMIT 100")
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des artistes : {e}")
        return JSONResponse(status_code=500, content={"message": "Erreur serveur lors de la récupération des artistes"})
