import typing as t
from datetime import datetime

from pydantic import BaseModel

from app.api.api_v1.schemas.location import LocationBase
from app.api.api_v1.schemas.restaurant import OrderItem
from app.db.models.restaurant import RestaurantTableType


class LocationRestaurantCount(LocationBase):
    restaurant_count: int


class OrderActionIn(BaseModel):
    ref_id: str


class ConfirmOrderIn(OrderActionIn):
    pass


class CancelOrderIn(OrderActionIn):
    pass


class SearchIn(BaseModel):
    country: str
    state: str
    city: str
    datetime: datetime
    party_size: int
    cuisine: t.Optional[str]
    min_star: t.Optional[int]
    good_for_kids: t.Optional[bool]


class SearchOut(BaseModel):
    id: int
    name: str
    address: str
    star: float
    party_size: int
    available_windows: t.List[datetime]


class SelectTableIn(BaseModel):
    restaurant_id: int
    party_size: int
    booking_time: datetime
    table_type: t.Optional[RestaurantTableType]


class OrderInfoOut(OrderItem):
    restaurant_name: str
