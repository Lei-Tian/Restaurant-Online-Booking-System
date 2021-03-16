import typing as t

from fastapi import APIRouter, Depends, Request

from app.api.api_v1.crud import consumer
from app.api.api_v1.schemas.consumer import (
    LocationRestaurantCount,
    OrderIn,
    SearchIn,
    SearchOut,
    SelectTableIn,
)
from app.api.api_v1.schemas.restaurant import OrderItem
from app.core.auth import get_current_active_user
from app.db.session import get_db

consumer_router = r = APIRouter(
    prefix='/v1/consumer',
    tags=['consumer'],
    dependencies=[Depends(get_db), Depends(get_current_active_user)]
)


@r.get("/location-restaurants-count", response_model=t.List[LocationRestaurantCount])
async def location_restaurants_count(request: Request):
    """
    Find all locations and their restaurants count
    """
    return consumer.get_location_restaurants_count(request, request.state.db)


@r.post("/search", response_model=t.List[SearchOut])
async def search_restaurant_tables(
    request: Request,
    search_in: SearchIn,
):
    """
    Find all available restaurants and their available windows
    """
    return consumer.search_restaurant_tables(request, request.state.db, search_in)


@r.post("/select-table", response_model=OrderItem)
async def select_table(
    request: Request,
    select_table_in: SelectTableIn,
):
    """
    Select a table
    """
    return consumer.select_table(request, request.state.db, select_table_in)


@r.post("/order", response_model=OrderItem)
async def confirm_order(
    request: Request,
    order_in: OrderIn,
):
    """
    Confirm an order
    """
    return consumer.confirm_order(request, request.state.db, order_in)
