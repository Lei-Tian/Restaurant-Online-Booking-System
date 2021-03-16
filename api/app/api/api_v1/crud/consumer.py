import typing as t
from fastapi import Request
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.api.api_v1.schemas.consumer import (
    LocationRestaurantCount,
    OrderIn,
    SearchIn,
    SearchOut,
    AvailableWindow,
)
from app.api.api_v1.schemas.restaurant import OrderItem
from app.tasks import cancel_order


def get_location_restaurants_count(request: Request, db: Session) -> t.List[LocationRestaurantCount]:
    result = []
    sql = "SELECT COUNT(location_id), city, state, country FROM location, restaurant where restaurant.location_id = location.id GROUP BY location_id, city, state, country"
    ret_proxy = db.execute(sql)
    for count, city, state, country in ret_proxy.fetchall():
        result.append(LocationRestaurantCount(restaurant_count=count, city=city, state=state, country=country))
    return result


def search_restaurant_tables(request: Request, db: Session, current_usersearch_params: SearchIn) -> t.List[SearchOut]:
    pass


def select_table(request: Request, db: Session, available_window: AvailableWindow) -> OrderItem:
    """To reserve a table by a given available_window
    Given available_window,
        if there is no matched row(restaurant_table_id and booking_time) in the TableAvailability table, then insert a new row.
        if there is a matched row in the TableAvailability table,
            if is_available is True, then update it to False using "SELECT FOR UPDATE" to avoid race condition;
            else return failure with a reason
    """
    #TODO:

    order = OrderItem()
    # order will be auto cancelled in 5min
    countdown_in_sec = 60 * 5
    cancel_order.apply_async(args=(order.ref_id,), countdown=countdown_in_sec, task_id=order.ref_id)
    request.app.logger.info(f"cancel order task({order.ref_id}) has been scheduled in {countdown_in_sec}sec")
    return order


def confirm_order(request: Request, db: Session, order_params: OrderIn) -> OrderItem:
    #TODO:

    # cancel the execution of cancel_order task
    celery_app.control.revoke(order_params.ref_id)
    request.app.logger.info(f"cancel_order task({order_params.ref_id}) has been revoked")
