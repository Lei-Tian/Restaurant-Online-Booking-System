import typing as t
from datetime import datetime

from pydantic import BaseModel

from app.db.models.restaurant import OrderStatus, RestaurantTableType


class RestaurantBase(BaseModel):
    location_id: int
    name: str
    address: str
    latitude: float
    longitude: float
    zip_code: str
    cuisine: str
    star: float
    is_open: bool
    good_for_kids: t.Optional[bool] = None


class RestaurantItem(RestaurantBase):
    class Config:
        orm_mode = True


class RestaurantTableBase(BaseModel):
    restaurant_id: int
    name: str
    type: RestaurantTableType
    capacity: int


class RestaurantTableItem(RestaurantTableBase):
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    ref_id: str
    status: OrderStatus
    party_size: int
    time_created: datetime
    time_updated: t.Optional[datetime]


class OrderItem(OrderBase):
    class Config:
        orm_mode = True


class TableAvailabilityBase(BaseModel):
    restaurant_table_id: int
    order_id: int
    booking_time: datetime
    is_available: bool


class TableAvailabilityItem(TableAvailabilityBase):
    class Config:
        orm_mode = True
