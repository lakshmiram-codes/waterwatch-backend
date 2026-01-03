from pydantic import BaseModel, EmailStr
from typing import Optional

# -------- USERS --------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    location: Optional[str] = None

# -------- STATIONS --------
class StationCreate(BaseModel):
    station_name: str
    location: str
    ph_level: float
    turbidity: float

# -------- REPORTS --------
class ReportCreate(BaseModel):
    user_id: int
    station_id: int
    issue_description: str
