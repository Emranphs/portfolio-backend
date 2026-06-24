from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Service, ServiceCreate, ServiceUpdate
from auth_middleware import verify_token
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter()

# Public route - Get all services
async def get_all_services(db: AsyncIOMotorDatabase):
    services = await db.services.find().to_list(1000)
    return [{**service, '_id': str(service['_id'])} for service in services]

# Admin routes - CRUD operations
async def create_service(service: ServiceCreate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    service_dict = service.dict()
    service_dict['createdAt'] = datetime.utcnow()
    service_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.services.insert_one(service_dict)
    created_service = await db.services.find_one({"_id": result.inserted_id})
    return {**created_service, '_id': str(created_service['_id'])}

async def update_service(service_id: str, service: ServiceUpdate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Invalid service ID")
    
    service_dict = service.dict()
    service_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.services.update_one(
        {"_id": ObjectId(service_id)},
        {"$set": service_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    updated_service = await db.services.find_one({"_id": ObjectId(service_id)})
    return {**updated_service, '_id': str(updated_service['_id'])}

async def delete_service(service_id: str, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Invalid service ID")
    
    result = await db.services.delete_one({"_id": ObjectId(service_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    
    return {"message": "Service deleted successfully"}
