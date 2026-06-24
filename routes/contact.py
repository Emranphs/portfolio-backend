from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import ContactSubmission, ContactSubmissionCreate
from auth_middleware import verify_token
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter()

# Public route - Submit contact form
async def submit_contact(contact: ContactSubmissionCreate, db: AsyncIOMotorDatabase):
    contact_dict = contact.dict()
    contact_dict['status'] = 'unread'
    contact_dict['submittedAt'] = datetime.utcnow()
    
    result = await db.contacts.insert_one(contact_dict)
    return {"message": "Contact form submitted successfully", "id": str(result.inserted_id)}

# Admin routes
async def get_all_contacts(db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    contacts = await db.contacts.find().sort("submittedAt", -1).to_list(1000)
    return [{**contact, '_id': str(contact['_id'])} for contact in contacts]

async def update_contact_status(contact_id: str, status: str, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(status_code=400, detail="Invalid contact ID")
    
    result = await db.contacts.update_one(
        {"_id": ObjectId(contact_id)},
        {"$set": {"status": status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    updated_contact = await db.contacts.find_one({"_id": ObjectId(contact_id)})
    return {**updated_contact, '_id': str(updated_contact['_id'])}

async def delete_contact(contact_id: str, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(status_code=400, detail="Invalid contact ID")
    
    result = await db.contacts.delete_one({"_id": ObjectId(contact_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {"message": "Contact deleted successfully"}