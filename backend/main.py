from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WaterWatch Backend")

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

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
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
