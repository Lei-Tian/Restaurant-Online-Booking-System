import typing as t

from fastapi import APIRouter, Depends, Request

from app.api.api_v1.crud import consumer
from app.api.api_v1.schemas.consumer import (
    AvailableWindow,
    LocationRestaurantCount,
    OrderIn,
    SearchIn,
    SearchOut,
)
from app.api.api_v1.schemas.restaurant import OrderItem
from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.utils.crud import get_all_locations, get_popular_restaurants

consumer_router = r = APIRouter(
    prefix='/v1/consumer',
    tags=['consumer'],
    dependencies=[Depends(get_db), Depends(get_current_active_user)]
)


@r.get('/support-locations', response_model=t.List[dict])
async def get_all_supported_locations(request: Request):
    return get_all_locations()


@r.get('/popular-restaurants', response_model=t.List[int])
async def get_popular_restaurants_by_location(request: Request, location_id: int):
    return get_popular_restaurants(location_id)


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
    available_window: AvailableWindow,
):
    """
    Select a table
    """
    return consumer.select_table(request, request.state.db, available_window)


@r.post("/order", response_model=OrderItem)
async def confirm_order(
    request: Request,
    order_in: OrderIn,
):
    """
    Confirm an order
    """
    return consumer.confirm_order(request, request.state.db, order_in)
