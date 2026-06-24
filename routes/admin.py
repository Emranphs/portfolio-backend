from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import AdminLogin, Token
from auth_utils import verify_password, create_access_token

router = APIRouter()

async def admin_login(credentials: AdminLogin, db: AsyncIOMotorDatabase):
    # Find admin user by email
    admin = await db.admin_users.find_one({"email": credentials.email})
    
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(credentials.password, admin['passwordHash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    token = create_access_token(data={"email": admin['email'], "sub": str(admin['_id'])})
    
    return Token(token=token, email=admin['email'])