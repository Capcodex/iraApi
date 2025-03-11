import asyncpg
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Lire l'URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
