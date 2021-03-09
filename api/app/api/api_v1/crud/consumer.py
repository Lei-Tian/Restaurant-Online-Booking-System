from app.api.api_v1.schemas.consumer import OrderIn, SearchIn, SearchOut, SelectTableIn
from app.api.api_v1.schemas.restaurants import OrderItem


def search_restaurant_tables(search_params: SearchIn) -> SearchOut:
    pass


def select_table(select_table_params: SelectTableIn) -> OrderItem:
    pass


def confirm_order(order_params: OrderIn) -> OrderItem:
    pass
