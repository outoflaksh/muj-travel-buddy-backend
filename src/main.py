from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Union

from . import crud, models, schemas, utils
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rides API
@app.get("/rides", response_model=List[schemas.RideResponse])
def read_rides(
    db: Session = Depends(get_db),
    from_location: Union[str, None] = None,
    to_location: Union[str, None] = None,
    doj: Union[str, None] = None,
    price: Union[str, None] = None,
):
    db_rides = crud.get_all_rides(db, from_location, to_location, doj, price)

    return db_rides


@app.get("/rides/{ride_id}", response_model=schemas.RideResponse)
def read_ride(ride_id: str, db: Session = Depends(get_db)):
    return crud.get_ride_by_id(db=db, ride_id=ride_id)


# Show all requests where current user was publisher
@app.get("/rides/{ride_id}/requests")
def read_requests_for_user(ride_id: str, db: Session = Depends(get_db)):
    return crud.fetch_requests_for_ride(ride_id=ride_id, db=db)


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


@app.post("/users/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user.UID)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found!",
        )

    if utils.verify_hash(user.password, db_user.hashed_password):
        db_user.token = utils.create_access_token(db_user.as_dict())
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


# Request to be added in a ride by some other user
@app.post("/users/{user_id}/requests")
def create_ride_request(
    user_id: int, ride_request: schemas.RideRequestCreate, db: Session = Depends(get_db)
):
    if not (crud.get_user_by_id(user_id=ride_request.publisher_id, db=db)):
        raise HTTPException(status_code=400, detail="Ride or Publisher doesn't exist!")
    return crud.create_ride_request(
        db=db, ride_request=ride_request, requestee_id=user_id
    )


# Show all requests where current user was publisher
@app.get("/users/{user_id}/requests")
def read_requests_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.fetch_requests_for_user(publisher_id=user_id, db=db)


# Change status of a ride request
@app.put("/users/{user_id}/requests/{ride_id}")
def update_request_status(
    user_id: int,
    ride_id: str,
    request_body: schemas.RideRequestUpdate,
    db: Session = Depends(get_db),
):
    if (
        crud.get_ride_request(
            ride_id=ride_id, requestee_id=request_body.requestee_id, db=db
        ).publisher_id
        != user_id
    ):
        raise HTTPException(status_code=401, detail="Not the owner!")

    return crud.update_request_status(
        action=request_body.action,
        ride_id=ride_id,
        requestee_id=request_body.requestee_id,
        db=db,
    )


# Get requests made by a user
@app.get("/requests")
def read_requests_for_requestee(requestee_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(user_id=requestee_id, db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Requestee user not found!")

    return crud.get_requests_by_requestee(requestee_id=requestee_id, db=db)


@app.get("/healthcheck")
def health_check():
    return {"status": "OK"}
