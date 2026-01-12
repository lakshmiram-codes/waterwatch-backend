from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from database import Base
from datetime import datetime
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # ✅
    role = Column(String)
    location = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    station_name = Column(String)
    location = Column(String)
    ph_level = Column(String)
    turbidity = Column(String)
    last_updated = Column(TIMESTAMP, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    issue_description = Column(Text)
    status = Column(String)
    reported_at = Column(TIMESTAMP, default=datetime.utcnow)
