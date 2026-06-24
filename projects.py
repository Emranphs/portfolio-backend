from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import Project, ProjectCreate, ProjectUpdate
from auth_middleware import verify_token
from bson import ObjectId
from datetime import datetime
from typing import List

router = APIRouter()

# Public route - Get all projects
async def get_all_projects(db: AsyncIOMotorDatabase):
    projects = await db.projects.find().to_list(1000)
    return [{**project, '_id': str(project['_id'])} for project in projects]

# Admin routes - CRUD operations
async def create_project(project: ProjectCreate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    project_dict = project.dict()
    project_dict['createdAt'] = datetime.utcnow()
    project_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": result.inserted_id})
    return {**created_project, '_id': str(created_project['_id'])}

async def update_project(project_id: str, project: ProjectUpdate, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    project_dict = project.dict()
    project_dict['updatedAt'] = datetime.utcnow()
    
    result = await db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": project_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    updated_project = await db.projects.find_one({"_id": ObjectId(project_id)})
    return {**updated_project, '_id': str(updated_project['_id'])}

async def delete_project(project_id: str, db: AsyncIOMotorDatabase, user: dict = Depends(verify_token)):
    if not ObjectId.is_valid(project_id):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    
    result = await db.projects.delete_one({"_id": ObjectId(project_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Project deleted successfully"}