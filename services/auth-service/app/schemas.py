from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserCreate):
    id: str
    hashed_password: str
    role: str = "user"  # Defaultna uloga

class UserLogin(BaseModel):
    email: EmailStr
    password: str