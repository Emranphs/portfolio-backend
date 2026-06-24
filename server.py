"from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List

# Import models
from models import (
    Project, ProjectCreate, ProjectUpdate,
    Testimonial, TestimonialCreate, TestimonialUpdate,
    Service, ServiceCreate, ServiceUpdate,
    ContactSubmission, ContactSubmissionCreate,
    AdminLogin, Token
)

# Import route handlers
from routes import projects, testimonials, services, contact, admin
from auth_middleware import verify_token

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix=\"/api\")

# Health check route
@api_router.get(\"/\")
async def root():
    return {\"message\": \"Portfolio API is running\"}

# Public Routes - Projects
@api_router.get(\"/projects\", response_model=List[dict])
async def get_projects():
    return await projects.get_all_projects(db)

# Public Routes - Testimonials
@api_router.get(\"/testimonials\", response_model=List[dict])
async def get_testimonials():
    return await testimonials.get_all_testimonials(db)

# Public Routes - Services
@api_router.get(\"/services\", response_model=List[dict])
async def get_services():
    return await services.get_all_services(db)

# Public Routes - Contact
@api_router.post(\"/contact\")
async def submit_contact_form(contact: ContactSubmissionCreate):
    return await contact.submit_contact(contact, db)

# Admin Routes - Authentication
@api_router.post(\"/admin/login\", response_model=Token)
async def login(credentials: AdminLogin):
    return await admin.admin_login(credentials, db)

# Admin Routes - Projects
@api_router.get(\"/admin/projects\", response_model=List[dict])
async def admin_get_projects(user: dict = Depends(verify_token)):
    return await projects.get_all_projects(db)

@api_router.post(\"/admin/projects\")
async def admin_create_project(project: ProjectCreate, user: dict = Depends(verify_token)):
    return await projects.create_project(project, db, user)

@api_router.put(\"/admin/projects/{project_id}\")
async def admin_update_project(project_id: str, project: ProjectUpdate, user: dict = Depends(verify_token)):
    return await projects.update_project(project_id, project, db, user)

@api_router.delete(\"/admin/projects/{project_id}\")
async def admin_delete_project(project_id: str, user: dict = Depends(verify_token)):
    return await projects.delete_project(project_id, db, user)

# Admin Routes - Testimonials
@api_router.get(\"/admin/testimonials\", response_model=List[dict])
async def admin_get_testimonials(user: dict = Depends(verify_token)):
    return await testimonials.get_all_testimonials(db)

@api_router.post(\"/admin/testimonials\")
async def admin_create_testimonial(testimonial: TestimonialCreate, user: dict = Depends(verify_token)):
    return await testimonials.create_testimonial(testimonial, db, user)

@api_router.put(\"/admin/testimonials/{testimonial_id}\")
async def admin_update_testimonial(testimonial_id: str, testimonial: TestimonialUpdate, user: dict = Depends(verify_token)):
    return await testimonials.update_testimonial(testimonial_id, testimonial, db, user)

@api_router.delete(\"/admin/testimonials/{testimonial_id}\")
async def admin_delete_testimonial(testimonial_id: str, user: dict = Depends(verify_token)):
    return await testimonials.delete_testimonial(testimonial_id, db, user)

# Admin Routes - Services
@api_router.get(\"/admin/services\", response_model=List[dict])
async def admin_get_services(user: dict = Depends(verify_token)):
    return await services.get_all_services(db)

@api_router.post(\"/admin/services\")
async def admin_create_service(service: ServiceCreate, user: dict = Depends(verify_token)):
    return await services.create_service(service, db, user)

@api_router.put(\"/admin/services/{service_id}\")
async def admin_update_service(service_id: str, service: ServiceUpdate, user: dict = Depends(verify_token)):
    return await services.update_service(service_id, service, db, user)

@api_router.delete(\"/admin/services/{service_id}\")
async def admin_delete_service(service_id: str, user: dict = Depends(verify_token)):
    return await services.delete_service(service_id, db, user)

# Admin Routes - Contacts
@api_router.get(\"/admin/contacts\", response_model=List[dict])
async def admin_get_contacts(user: dict = Depends(verify_token)):
    return await contact.get_all_contacts(db, user)

@api_router.put(\"/admin/contacts/{contact_id}\")
async def admin_update_contact(contact_id: str, status: str, user: dict = Depends(verify_token)):
    return await contact.update_contact_status(contact_id, status, db, user)

@api_router.delete(\"/admin/contacts/{contact_id}\")
async def admin_delete_contact(contact_id: str, user: dict = Depends(verify_token)):
    return await contact.delete_contact(contact_id, db, user)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[\"*\"],
    allow_methods=[\"*\"],
    allow_headers=[\"*\"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event(\"shutdown\")
async def shutdown_db_client():
    client.close()
"