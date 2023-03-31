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
