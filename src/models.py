from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    UUID,
    BigInteger,
)
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
    phone = Column(String)
    rating = Column(Integer)
    hashed_password = Column(String)

    rides = relationship("Ride", back_populates="publisher")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class RideRequest(Base):
    __tablename__ = "riderequests"

    publisher_id = Column(Integer, ForeignKey("users.UID"))
    requestee_id = Column(Integer, ForeignKey("users.UID"), primary_key=True)
    ride_id = Column(UUID, ForeignKey("rides.id"), primary_key=True)
    request_status = Column(String, default="pending")
