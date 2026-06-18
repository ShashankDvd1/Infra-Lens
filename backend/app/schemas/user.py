from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .project import ProjectListResponse

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Saved Opportunity Schemas
class SavedOpportunityCreate(BaseModel):
    project_id: UUID
    notes: Optional[str] = None

class SavedOpportunityResponse(BaseModel):
    id: UUID
    project_id: UUID
    notes: Optional[str]
    created_at: datetime
    project: Optional[ProjectListResponse] = None

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
