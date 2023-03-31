from sqlalchemy.orm import Session

from . import models, schemas


def create_ride(db: Session, ride: schemas.RideCreate):
    db_ride = models.Ride(**dict(ride))
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)

    return db_ride


def get_all_rides(db: Session):
    db_rides = db.query(models.Ride).all()

    return db_rides
