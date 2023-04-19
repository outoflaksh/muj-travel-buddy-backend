import uuid

from sqlalchemy import and_
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

from . import models, schemas, utils


# Users CRUD
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        UID=user.UID,
        fname=user.fname,
        lname=user.lname,
        email=user.email,
        designation=user.designation,
        user_type=user.user_type,
        phone=user.phone,
        hashed_password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.UID == user_id).first()


def create_ride(db: Session, ride: schemas.RideCreate, user_id: int):
    db_ride = models.Ride(**dict(ride), publisher_id=user_id)
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)

    return db_ride


# Rides CRUD
def get_all_rides(db: Session, *filters):
    db_rides = db.query(models.Ride).filter(models.Ride.passenger_count > 0)

    if filters[0]:
        db_rides = db_rides.filter(models.Ride.from_location == filters[0])
    if filters[1]:
        db_rides = db_rides.filter(models.Ride.to_location == filters[1])
    if filters[2]:
        db_rides = db_rides.filter(models.Ride.doj == filters[2])
    if filters[3]:
        db_rides = db_rides.filter(models.Ride.price <= filters[3])

    return db_rides.all()


def get_ride_by_id(db: Session, ride_id: str):
    db_ride = db.query(models.Ride).filter(models.Ride.id == uuid.UUID(ride_id)).first()

    return db_ride


def get_rides_by_publisher_id(db: Session, publisher_id: int):
    return db.query(models.Ride).filter(models.Ride.publisher_id == publisher_id).all()


# Ride Requests CRUD
def create_ride_request(
    db: Session, ride_request: schemas.RideRequestCreate, requestee_id: int
):
    db_request = models.RideRequest(**dict(ride_request), requestee_id=requestee_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request


def get_ride_request(db: Session, ride_id: str, requestee_id: int):
    db_request = (
        db.query(models.RideRequest)
        .filter(
            and_(
                models.RideRequest.ride_id == ride_id,
                models.RideRequest.requestee_id == requestee_id,
            )
        )
        .first()
    )

    return db_request


def fetch_requests_for_user(db: Session, publisher_id: int):
    return (
        db.query(models.RideRequest)
        .filter(models.RideRequest.publisher_id == publisher_id)
        .all()
    )


def fetch_requests_for_ride(db: Session, ride_id: str):
    return (
        db.query(models.RideRequest).filter(models.RideRequest.ride_id == ride_id).all()
    )


def update_request_status(db: Session, action: str, ride_id: str, requestee_id: int):
    db_request = get_ride_request(db, ride_id, requestee_id)
    if action == "accept":
        db_request.request_status = "accepted"
        db_ride = get_ride_by_id(db, str(db_request.ride_id))
        db_ride.passenger_count -= 1

    elif action == "reject":
        db_request.request_status = "rejected"

    db.commit()
    db.refresh(db_request)

    return db_request


def get_requests_by_requestee(requestee_id: int, db: Session):
    return (
        db.query(models.RideRequest)
        .filter(models.RideRequest.requestee_id == requestee_id)
        .all()
    )
