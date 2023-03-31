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


# HTTP POST /rides -> create a new ride
@app.post("/rides")
def publish_ride(ride: schemas.RideCreate, db: Session = Depends(get_db)):
    db_ride = crud.create_ride(db=db, ride=ride)

    return db_ride


# HTTP GET /rides -> get all rides
@app.get("/rides")
def read_rides(db: Session = Depends(get_db)):
    db_rides = crud.get_all_rides(db=db)

    return db_rides


@app.get("/rides/{ride_id}")
def read_ride(ride_id: str, db: Session = Depends(get_db)):
    return crud.get_ride_by_id(db=db, ride_id=ride_id)


@app.post("/users/register", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user.UID)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists with the provided ID!",
        )

    db_user = crud.create_user(db=db, user=user)
    return db_user


@app.get("/healthcheck")
def health_check():
    return {"status": "OK"}
