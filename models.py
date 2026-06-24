from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ProjectBase(BaseModel):
    title: str
    description: str
    overview: str
    features: List[str]
    technologies: List[str]
    impact: str
    image: str
    liveUrl: Optional[str] = None
    caseStudyUrl: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class TestimonialBase(BaseModel):
    name: str
    position: str
    company: str
    content: str
    rating: int = Field(ge=1, le=5)
    image: str

class TestimonialCreate(TestimonialBase):
    pass

class TestimonialUpdate(TestimonialBase):
    pass

class Testimonial(TestimonialBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class ServiceBase(BaseModel):
    title: str
    description: str
    icon: str

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass

class Service(ServiceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class ContactSubmissionBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactSubmissionCreate(ContactSubmissionBase):
    pass

class ContactSubmission(ContactSubmissionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    status: str = "unread"
    submittedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class AdminUserBase(BaseModel):
    email: EmailStr

class AdminUserCreate(AdminUserBase):
    password: str

class AdminUser(AdminUserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    passwordHash: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    email: str