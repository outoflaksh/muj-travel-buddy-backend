from pydantic import BaseModel


class RideCreate(BaseModel):
    publisher_id: str
    from_location: str
    to_location: str
    passenger_count: int
    doj: str
    price: int
