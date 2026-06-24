from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Testimonial, TestimonialCreate, TestimonialUpdate
from auth_middleware import verify_token
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter()

# Public route - Get all testimonials
async def get_all_testimonials(db: AsyncIOMotorDatabase):
    testimonials = await db.testimonials.find().to_list(1000)
    return [{**testimonial, '_id': str(testimonial['_id'])} for testimonial in testimonials]

# Admin routes - CRUD operations
async def create_testimonial(testimonial: TestimonialCreate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    testimonial_dict = testimonial.dict()
    testimonial_dict['createdAt'] = datetime.utcnow()
    testimonial_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.testimonials.insert_one(testimonial_dict)
    created_testimonial = await db.testimonials.find_one({"_id": result.inserted_id})
    return {**created_testimonial, '_id': str(created_testimonial['_id'])}

async def update_testimonial(testimonial_id: str, testimonial: TestimonialUpdate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(testimonial_id):
        raise HTTPException(status_code=400, detail="Invalid testimonial ID")
    
    testimonial_dict = testimonial.dict()
    testimonial_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.testimonials.update_one(
        {"_id": ObjectId(testimonial_id)},
        {"$set": testimonial_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    updated_testimonial = await db.testimonials.find_one({"_id": ObjectId(testimonial_id)})
    return {**updated_testimonial, '_id': str(updated_testimonial['_id'])}

async def delete_testimonial(testimonial_id: str, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(testimonial_id):
        raise HTTPException(status_code=400, detail="Invalid testimonial ID")
    
    result = await db.testimonials.delete_one({"_id": ObjectId(testimonial_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    return {"message": "Testimonial deleted successfully"}