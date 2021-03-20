import typing as t
from datetime import datetime

from pydantic import BaseModel

from app.api.api_v1.schemas.location import LocationBase
from app.db.models.restaurant import RestaurantTableType


class LocationRestaurantCount(LocationBase):
    restaurant_count: int


class ConfirmOrderIn(BaseModel):
    ref_id: str


class SearchIn(BaseModel):
    country: str
    state: str
    city: str
    datetime: datetime
    party_size: int
    cuisine: t.Optional[str]
    min_star: t.Optional[int]
    good_for_kids: t.Optional[bool]


class AvailableWindow(BaseModel):
    booking_time: datetime


class SelectTableIn(AvailableWindow):
    restaurant_id: int
    party_size: int
    table_type: t.Optional[RestaurantTableType]


class SearchOut(BaseModel):
    restaurant_id: int
    restaurant_name: str
    available_windows: t.List[AvailableWindow]
