import uuid

from pydantic import BaseModel


class RideBase(BaseModel):
    publisher_id: str
    from_location: str
    to_location: str
    passenger_count: int
    doj: str
    price: int


class RideCreate(RideBase):
    pass


class RideResponse(RideBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


# User
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
    pass


class UserLogin(BaseModel):
    UID: int
    password: str
