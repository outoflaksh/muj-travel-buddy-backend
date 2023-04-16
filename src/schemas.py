import uuid

from pydantic import BaseModel

# User schemas
class UserBase(BaseModel):
    UID: int
    fname: str
    lname: str
    email: str
    designation: str
    user_type: str
    phone: int


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    UID: int
    password: str


class RideRequestCreate(BaseModel):
    publisher_id: int
    ride_id: str


class RideRequestResponse(RideRequestCreate):
    ride_status: str


# Ride schemas
class RideBase(BaseModel):
    from_location: str
    to_location: str
    passenger_count: int
    doj: str
    price: int


class RideCreate(RideBase):
    pass


class RideResponse(RideBase):
    id: uuid.UUID
    publisher_id: int
    publisher: UserResponse

    class Config:
        orm_mode = True


class RideRequestUpdate(BaseModel):
    action: str
    requestee_id: int


class TokenData(BaseModel):
    username: str
