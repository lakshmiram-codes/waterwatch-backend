from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    location: Optional[str] = None

class StationCreate(BaseModel):
    station_name: str
    location: str
    ph_level: float
    turbidity: float


class ReportCreate(BaseModel):
    user_id: int
    station_id: int
    issue_description: str


class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
    role: str
