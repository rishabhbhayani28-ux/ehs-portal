from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserOut(UserBase):
    id: int
    is_admin: bool
    is_active: bool

    class Config:
        orm_mode = True

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Incident schemas
class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentOut(IncidentBase):
    id: int
    date_reported: datetime
    reported_by_id: int

    class Config:
        orm_mode = True

# Action schemas
class ActionBase(BaseModel):
    description: str
    status: str = "Open"

class ActionCreate(ActionBase):
    due_date: Optional[datetime] = None

class ActionOut(ActionBase):
    id: int
    due_date: Optional[datetime] = None
    incident_id: int

    class Config:
        orm_mode = True
