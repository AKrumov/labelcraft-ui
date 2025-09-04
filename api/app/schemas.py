from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: str


class ProjectOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = ""


class DatasetOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
