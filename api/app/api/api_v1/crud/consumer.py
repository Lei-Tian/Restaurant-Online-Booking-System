import typing as t

from sqlalchemy.orm import Session

from app.api.api_v1.schemas.consumer import OrderIn, SearchIn, SearchOut, SelectTableIn
from app.api.api_v1.schemas.restaurant import OrderItem
from app.db.models.user import User


def search_restaurant_tables(current_user: User, db: Session, current_usersearch_params: SearchIn) -> t.List[SearchOut]:
    pass


def select_table(current_user: User, db: Session, select_table_params: SelectTableIn) -> OrderItem:
    pass


def confirm_order(current_user: User, db: Session, order_params: OrderIn) -> OrderItem:
    pass
