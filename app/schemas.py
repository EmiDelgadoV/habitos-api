from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

# --- USUARIOS ---

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- AUTH ---

class Token(BaseModel):
    access_token: str
    token_type: str

# --- HÁBITOS ---

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class HabitResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

# --- LOGS ---

class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    date: date
    completed: bool

    class Config:
        from_attributes = True