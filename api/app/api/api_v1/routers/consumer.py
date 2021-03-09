import typing as t

from fastapi import APIRouter, Depends, Request

from app.api.api_v1.crud import consumer
from app.api.api_v1.schemas.consumer import OrderIn, SearchIn, SearchOut, SelectTableIn
from app.api.api_v1.schemas.restaurant import OrderItem

consumer_router = r = APIRouter()


@r.post("/search", response_model=t.List[SearchOut])
async def search_restaurant_tables(
    request: Request,
    search_in: SearchIn,
):
    """
    Find all available restaurants and their available windows
    """
    return consumer.search_restaurant_tables(search_in)


@r.post("/select-table", response_model=OrderItem)
async def select_table(
    request: Request,
    select_table_in: SelectTableIn,
):
    """
    Select a table
    """
    return consumer.select_table(select_table_in)


@r.post("/order", response_model=OrderItem)
async def confirm_order(
    request: Request,
    order_in: OrderIn,
):
    """
    Confirm an order
    """
    return consumer.confirm_order(order_in)
