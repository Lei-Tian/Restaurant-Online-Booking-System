import typing as t

from fastapi import APIRouter, Depends, Request

from app.api.api_v1.crud import consumer
from app.api.api_v1.schemas.consumer import (
    ConfirmOrderIn,
    LocationRestaurantCount,
    OrderInfoOut,
    OrderItem,
    SearchIn,
    SearchOut,
    SelectTableIn,
)
from app.core.auth import get_current_active_user
from app.db.models.restaurant import Order, Restaurant
from app.db.session import get_db
from app.utils.crud import get_all_locations, get_popular_restaurants
from app.utils.pagination import Page

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


@r.get("/order-info", response_model=OrderInfoOut)
async def get_order_info(request: Request, order_ref_id: str):
    order = request.state.db.query(Order).filter(Order.ref_id == order_ref_id).first()
    restaurant = request.state.db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()
    return OrderInfoOut(**{**order.__dict__, 'restaurant_name': restaurant.name})


@r.post("/search", response_model=Page[SearchOut])
async def search_restaurant_tables(
    request: Request,
    search_in: SearchIn,
    offset: int = 0,
    limit: int = 100,
):
    """
    Find all available restaurants and their available windows
    """
    return consumer.search_restaurant_tables(request, request.state.db, search_in, offset, limit)


@r.post("/select-table", response_model=OrderItem)
async def select_table(
    request: Request,
    select_table_params: SelectTableIn,
):
    """
    Select a table
    """
    return consumer.select_table(request, request.state.db, select_table_params)


@r.post("/order", response_model=OrderItem)
async def confirm_order(
    request: Request,
    order_in: ConfirmOrderIn,
):
    """
    Confirm an order
    """
    return consumer.confirm_order(request, request.state.db, order_in)
