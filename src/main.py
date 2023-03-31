from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/rides")
def publish_ride(ride: schemas.RideCreate, db: Session = Depends(get_db)):
    db_ride = crud.create_ride(db=db, ride=ride)

    return db_ride


@app.get("/rides")
def read_rides(db: Session = Depends(get_db)):
    db_rides = crud.get_all_rides(db=db)

    return db_rides


@app.get("/healthcheck")
def health_check():
    return {"status": "OK"}
