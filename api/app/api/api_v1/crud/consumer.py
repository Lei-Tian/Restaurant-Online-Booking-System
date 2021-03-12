import typing as t

from sqlalchemy.orm import Session

from app.api.api_v1.schemas.consumer import (
    LocationRestaurantCount,
    OrderIn,
    SearchIn,
    SearchOut,
    SelectTableIn,
)
from app.api.api_v1.schemas.restaurant import OrderItem
from app.db.models.user import User


def get_location_restaurants_count(current_user: User, db: Session) -> t.List[LocationRestaurantCount]:
    ret_proxy = db.execute("select * from restaurant")
    return []

def search_restaurant_tables(current_user: User, db: Session, current_usersearch_params: SearchIn) -> t.List[SearchOut]:
    pass


def select_table(current_user: User, db: Session, select_table_params: SelectTableIn) -> OrderItem:
    pass


def confirm_order(current_user: User, db: Session, order_params: OrderIn) -> OrderItem:
    pass
