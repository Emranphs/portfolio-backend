"""
Seed script - run once to create admin user in MongoDB
Usage: python seed_data.py
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from auth_utils import hash_password
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

ADMIN_EMAIL = "emranphs@gmail.com"
ADMIN_PASSWORD = "Emranphs37250@"

async def seed():
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'portfolio')
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    # Check if admin already exists
    existing = await db.admin_users.find_one({"email": ADMIN_EMAIL})
    if existing:
        print(f"Admin already exists: {ADMIN_EMAIL}")
    else:
        hashed = hash_password(ADMIN_PASSWORD)
        await db.admin_users.insert_one({
            "email": ADMIN_EMAIL,
            "passwordHash": hashed,
        })
        print(f"✅ Admin created: {ADMIN_EMAIL}")

    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
