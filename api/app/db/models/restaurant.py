import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import (
    Boolean,
    DateTime,
    Enum,
    Float,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy_utils import generic_repr

from app.db.session import Base


@generic_repr
class Restaurant(Base):
    __tablename__ = "restaurant"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("location.id", ondelete="SET NULL"))
    name = Column(String, nullable=False)
    address = Column(Text)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(8, 6))
    zip_code = Column(String(15))
    cuisine = Column(String(30))
    star = Column(Float)
    is_open = Column(Boolean)
    good_for_kids = Column(Boolean)

    # relationships
    location = relationship("Location", back_populates="restaurants")
    restaurant_tables = relationship("RestaurantTable", back_populates="restaurant")

    __table_args__ = (
        CheckConstraint("star >= 0 AND star <= 5", name='check_star_value'),
    )


class RestaurantTableType(enum.Enum):
    general = "GENERAL"
    outdoor = "OUTDOOR"
    window = "WINDOW"


@generic_repr
class RestaurantTable(Base):
    __tablename__ = "restaurant_table"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"))
    type = Column(Enum(RestaurantTableType))
    capacity = Column(Integer)

    # relationships
    restaurant = relationship("Restaurant", back_populates="restaurant_tables")
    table_availabilities = relationship("TableAvailability", back_populates="restaurant_table")

    __table_args__ = (
        CheckConstraint(capacity > 0, name='check_table_capacity_value'),
    )


class OrderStatus(enum.Enum):
    complete = "COMPLETE"
    pending = "PENDING"
    cancelled = "CANCELLED"


@generic_repr
class Order(Base):
    __tablename__ = "order"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    status = Column(Enum(OrderStatus))
    party_size = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    user = relationship("User", back_populates="orders")
    table_availabilities = relationship("TableAvailability", back_populates="order")

    __table_args__ = (
        CheckConstraint(party_size > 0, name='check_table_party_size_value'),
    )


@generic_repr
class TableAvailability(Base):
    __tablename__ = "table_availability"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    restaurant_table_id = Column(Integer, ForeignKey("restaurant_table.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("order.id", ondelete="SET NULL"))
    booking_time = Column(DateTime(timezone=True))
    is_available = Column(Boolean)

    # relationships
    restaurant_table = relationship("RestaurantTable", back_populates="table_availabilities")
    order = relationship("Order", back_populates="table_availabilities")