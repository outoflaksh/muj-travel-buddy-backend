import uuid

from sqlalchemy.orm import Session

from . import models, schemas, utils


def create_ride(db: Session, ride: schemas.RideCreate):
    db_ride = models.Ride(**dict(ride))
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)

    return db_ride


def get_all_rides(db: Session):
    db_rides = db.query(models.Ride).all()

    return db_rides


def get_ride_by_id(db: Session, ride_id: str):
    return db.query(models.Ride).filter(models.Ride.id == uuid.UUID(ride_id)).first()


# users
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
