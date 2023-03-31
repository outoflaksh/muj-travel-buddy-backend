from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, UUID
from sqlalchemy.orm import relationship

from uuid import uuid4

from .database import Base


class Ride(Base):
    __tablename__ = "rides"

    id = Column(UUID, default=uuid4, primary_key=True, index=True)
    publisher_id = Column(Integer, ForeignKey("users.UID"))
    from_location = Column(String)
    to_location = Column(String)
    doj = Column(String)
    passenger_count = Column(Integer)
    price = Column(Integer)

    publisher = relationship("User", back_populates="rides")


class User(Base):
    __tablename__ = "users"

    UID = Column(Integer, primary_key=True, index=True)
    user_type = Column(String)
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    designation = Column(String)
    phone = Column(Integer)
    rating = Column(Integer)
    hashed_password = Column(String)

    rides = relationship("Ride", back_populates="publisher")


class RideRequest(Base):
    __tablename__ = "riderequests"

    request_id = Column(Integer, primary_key=True, autoincrement=True)
    publisher_id = Column(Integer, ForeignKey("users.UID"))
    requestee_id = Column(Integer, ForeignKey("users.UID"))
    ride_id = Column(String, ForeignKey("rides.id"))
    request_status = Column(String, default="pending")
