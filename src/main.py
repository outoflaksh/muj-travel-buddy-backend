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


# Rides API
@app.get("/rides", response_model=list[schemas.RideResponse])
def read_rides(db: Session = Depends(get_db)):
    db_rides = crud.get_all_rides(db=db)

    return db_rides


@app.get("/rides/{ride_id}", response_model=schemas.RideResponse)
def read_ride(ride_id: str, db: Session = Depends(get_db)):
    return crud.get_ride_by_id(db=db, ride_id=ride_id)


# Users API
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


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Requested user not found!",
        )

    return db_user


@app.get("/users/{user_id}/rides")
def read_rides_for_user(user_id: int, db: Session = Depends(get_db)):
    rides = crud.get_rides_by_publisher_id(db=db, publisher_id=user_id)

    return rides


@app.post("/users/{user_id}/rides")
def publish_ride_for_user(
    user_id: int, ride: schemas.RideCreate, db: Session = Depends(get_db)
):
    db_ride = crud.create_ride(db=db, ride=ride, user_id=user_id)

    return db_ride


@app.post("/users/{user_id}/requests")
def create_ride_request(
    user_id: int, ride_request: schemas.RideRequestCreate, db: Session = Depends(get_db)
):
    if not (crud.get_user_by_id(user_id=ride_request.publisher_id, db=db)):
        raise HTTPException(status_code=400, detail="Ride or Publisher doesn't exist!")
    return crud.create_ride_request(
        db=db, ride_request=ride_request, requestee_id=user_id
    )


@app.get("/healthcheck")
def health_check():
    return {"status": "OK"}
