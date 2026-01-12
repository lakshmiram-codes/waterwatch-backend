from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas
from auth import hash_password

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WaterWatch Backend")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/create")
def create_user(user: schemas.UserCreate):
    db = SessionLocal()

    # check duplicate email
    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    
    hashed_pwd = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,  
        role=user.role,
        location=user.location
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }


@app.post("/stations/create")
def create_station(station: schemas.StationCreate):
    db = SessionLocal()

    new_station = models.Station(
        station_name=station.station_name,
        location=station.location,
        ph_level=station.ph_level,
        turbidity=station.turbidity
    )

    db.add(new_station)
    db.commit()
    db.refresh(new_station)
    db.close()

    return {
        "message": "Station created successfully",
        "station_id": new_station.id
    }

@app.post("/reports/create")
def create_report(report: schemas.ReportCreate):
    db = SessionLocal()

    new_report = models.Report(
        user_id=report.user_id,
        station_id=report.station_id,
        issue_description=report.issue_description,
        status="pending"
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    db.close()

    return {
        "message": "Report created successfully",
        "report_id": new_report.id
    }
from auth import verify_password

@app.post("/login", response_model=schemas.LoginResponse)
def login(user: schemas.LoginRequest):
    db = SessionLocal()

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.password):
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    db.close()

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "role": db_user.role
    }


