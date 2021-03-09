import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.api.api_v1.schemas.consumer import (
    OrderFailOut,
    OrderIn,
    OrderSuccessOut,
    SearchedAvailableRestaurant,
    SearchIn,
    SelectTableFailOut,
    SelectTableIn,
    SelectTableSuccessOut,
)
from app.core.auth import get_current_active_user
from app.db.session import get_db

consumer_router = r = APIRouter()


@r.post("/search", response_model=t.List[SearchedAvailableRestaurant])
async def search_restaurant_tables(
    request: Request,
    search_in: SearchIn,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Find all available restaurants and their available windows
    """
    return []


@r.post("/select-table", response_model=t.Union[SelectTableSuccessOut, SelectTableFailOut])
async def select_table(
    request: Request,
    select_table_in: SelectTableIn,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Select a table
    """
    return


@r.post("/order", response_model=t.Union[OrderSuccessOut, OrderFailOut])
async def confirm_order(
    request: Request,
    select_table_in: OrderIn,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Confirm an order
    """
    return
