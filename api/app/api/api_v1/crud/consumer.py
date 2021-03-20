import typing as t

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app import tasks
from app.api.api_v1.schemas.consumer import (
    ConfirmOrderIn,
    LocationRestaurantCount,
    SearchIn,
    SearchOut,
    SelectTableIn,
)
from app.api.api_v1.schemas.restaurant import OrderItem, TableAvailabilityItem
from app.core.celery_app import celery_app
from app.db.models.restaurant import Order, OrderStatus, TableAvailability
from app.utils import crud as crud_utils


def get_location_restaurants_count(request: Request, db: Session) -> t.List[LocationRestaurantCount]:
    result = []
    sql = "SELECT COUNT(location_id), city, state, country FROM location, restaurant where restaurant.location_id = location.id GROUP BY location_id, city, state, country"
    ret_proxy = db.execute(sql)
    for count, city, state, country in ret_proxy.fetchall():
        result.append(LocationRestaurantCount(restaurant_count=count, city=city, state=state, country=country))
    return result


def search_restaurant_tables(request: Request, db: Session, current_usersearch_params: SearchIn) -> t.List[SearchOut]:
    # step1: get location_id by (country, state, city from location table)
    # step2: utils.crud.get_popular_restaurants(location_id) -> popular_restaurants(a list of restaurant_id) estimate 1200+
    # step3: iterate from restaurant_ids -> find 3 nearest available_windows for each restaurant_id (1100+)
    # return result
    pass


def select_table(request: Request, db: Session, select_table_params: SelectTableIn) -> OrderItem:
    """To reserve a table by a given available_window
    Given available_window,
        if there is no matched row(restaurant_table_id and booking_time) in the TableAvailability table, then insert a new row.
        else update is_available to False using "SELECT ... FOR UPDATE" to avoid race condition.

    Given: resetaurant_id=1, booking_time=17:00, Optional table_type=GENERAL
    STEP1: get all tables where restaurant_id=1 -> [1, 2, 3, 4, 5, 6, 7]
        # restaurant_table_ids = get_all_table_ids(restaurant_id=select_table_params.restaurant_id)
    STEP2: check if any[1, 2, 3, 4, 5, 6, 7] is available at 17:00   (available means no row)
    STEP3: let's say restaurant_table_id=6 is available at 17:00, then go to "no matched row" code block
    """
    # create an order
    order_data = {'user_id': request.state.current_active_user.id, 'status': OrderStatus.pending, 'party_size': select_table_params.party_size} 
    # try to create table availability row
    table_availability_row = db.query(TableAvailability).filter(
        TableAvailability.restaurant_table_id == select_table_params.restaurant_table_id,
        TableAvailability.booking_time == select_table_params.booking_time,
    ).first()
    if table_availability_row:
        # matched row found
        raise HTTPException(status_code=409, detail=f"There is no available spot at {select_table_params.booking_time}")
    else:
        # no matched row
        order = crud_utils.create_item(db, model=Order, payload=order_data)
        table_availability_item = TableAvailabilityItem(
            restaurant_table_id=select_table_params.restaurant_table_id,
            order_id=order.id,
            booking_time=select_table_params.booking_time,
            is_available=False,
        )
        crud_utils.create_item(db, model=TableAvailability, payload=table_availability_item)
    # order will be auto cancelled in 5min
    countdown_in_sec = 60 * 5
    tasks.cancel_order.apply_async(args=(order.ref_id,), countdown=countdown_in_sec, task_id=order.ref_id)
    request.app.logger.info(f"cancel order task({order.ref_id}) has been scheduled in {countdown_in_sec}sec")
    return order


def confirm_order(request: Request, db: Session, confirm_order_params: ConfirmOrderIn) -> OrderItem:
    # update order status
    db.execute(f"UPDATE public.order SET status = '{OrderStatus.complete.value.lower()}' where ref_id = '{confirm_order_params.ref_id}'")
    db.commit()
    order = db.query(Order).filter(Order.ref_id == confirm_order_params.ref_id).first()
    # cancel the execution of cancel_order task
    celery_app.control.revoke(confirm_order_params.ref_id)
    request.app.logger.info(f"cancel_order task({confirm_order_params.ref_id}) has been revoked")
    return order
