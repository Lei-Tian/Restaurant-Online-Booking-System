import logging
import typing as t
from datetime import datetime, timedelta, timezone

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
from app.utils.pagination import (
    Page,
    PageLinks,
    get_base_url,
    get_next_url,
    get_prev_url,
)

logger = logging.getLogger(__name__)


def get_location_restaurants_count(request: Request, db: Session) -> t.List[LocationRestaurantCount]:
    result = []
    sql = "SELECT COUNT(location_id), city, state, country FROM location, restaurant where restaurant.location_id = location.id GROUP BY location_id, city, state, country"
    ret_proxy = db.execute(sql)
    for count, city, state, country in ret_proxy.fetchall():
        result.append(LocationRestaurantCount(restaurant_count=count, city=city, state=state, country=country))
    return result


def search_restaurant_tables(
    request: Request, db: Session, current_usersearch_params: SearchIn, offset: int, limit: int
) -> Page[SearchOut]:
    logger.info(f"search restaurant tables[params={current_usersearch_params}|offset={offset}|limit={limit}]...")
    # step1: get location_id by (country, state, city from location table)
    get_loc_sql = f"SELECT id FROM location WHERE city = '{current_usersearch_params.city}' AND state = '{current_usersearch_params.state}' AND country = '{current_usersearch_params.country}'"
    location_id = db.execute(get_loc_sql).fetchall()[0][0]
    results = []
    # step2: utils.crud.get_popular_restaurants(location_id) -> popular_restaurants(a list of restaurant_id) estimate 1200+
    popular_restaurants = crud_utils.get_popular_restaurants(location_id)
    logger.info(f"{len(popular_restaurants)} popular restaurants are found in total.")
    # step3: iterate from restaurant_ids -> find 3 nearest available_windows for each restaurant_id (1100+)
    for restaurantID in popular_restaurants[offset : offset + limit]:
        # step 3.1: get the table ids of a popular restaurant
        get_table_sql = f"SELECT id FROM restaurant_table WHERE restaurant_id = {restaurantID}"
        table_ids = db.execute(get_table_sql).fetchall()
        totalTableCount = len(table_ids)
        for i in range(len(table_ids)):
            table_ids[i] = str(table_ids[i][0])
        table_ids = ", ".join(table_ids)
        # step 3.2: get restaurant info
        get_restaurant_name_sql = f"SELECT name, address, star FROM restaurant WHERE id = {restaurantID}"
        restaurant_name, restaurant_addr, restaurant_star = db.execute(get_restaurant_name_sql).fetchall()[0]
        # step 3.3: get the 3 nearest available_windows (among all tables) of a popular restaurant
        available_windows, timeslots = [], [current_usersearch_params.datetime]
        for delta_hour in range(1, 6):
            timeslots.append(current_usersearch_params.datetime - timedelta(hours=delta_hour))
            timeslots.append(current_usersearch_params.datetime + timedelta(hours=delta_hour))
        for i in range(11):
            searchTime = timeslots[i]
            if isValidSeachTime(searchTime):
                get_table_count_sql = f"SELECT COUNT(restaurant_table_id) FROM table_availability where booking_time = '{searchTime}' AND restaurant_table_id IN ({table_ids})"
                reservedTableCount = db.execute(get_table_count_sql).fetchall()[0][0]
                if reservedTableCount < totalTableCount:
                    available_windows.append(searchTime)
            if len(available_windows) == 3:
                break
        results.append(
            SearchOut(
                id=restaurantID,
                name=restaurant_name,
                address=restaurant_addr,
                star=float(restaurant_star),
                party_size=current_usersearch_params.party_size,
                available_windows=available_windows,
            )
        )
    return Page(
        links=PageLinks(
            base=get_base_url(request),
            self=str(request.url),
            next=get_next_url(request, offset, limit, len(popular_restaurants)),
            prev=get_prev_url(request, offset, limit),
        ),
        total=len(popular_restaurants),
        start=offset,
        limit=limit,
        size=len(results),
        items=results,
    )


def isValidSeachTime(searchTime):
    OPEN_HOUR = 10
    CLOSE_HOUR = 23
    if searchTime <= datetime.now():
        return False
    if searchTime.hour > CLOSE_HOUR or searchTime.hour < OPEN_HOUR:
        return False
    return True


def select_table(request: Request, db: Session, select_table_params: SelectTableIn) -> OrderItem:
    """To reserve a table by a given available_window
    Given available_window,
        if there is no matched row(restaurant_table_id and booking_time) in the TableAvailability table, then insert a new row.
        else update is_available to False using "SELECT ... FOR UPDATE" to avoid race condition.

    Given: resetaurant_id=1, booking_time=17:00, Optional table_type=GENERAL
    STEP1: get all tables where restaurant_id=1 -> [1, 2, 3, 4, 5, 6, 7]
        # restaurant_table_ids = get_all_table_ids(restaurant_id=select_table_params.restaurant_id)
    STEP2: check if any[1, 2, 3, 4, 5, 6, 7] is available at 17:00 (no row means available)
    STEP3: let's say restaurant_table_id=6 is available at 17:00, then go to "no matched row" code block
    """
    # create an order
    order_data = {
        "user_id": request.state.current_active_user.id,
        "restaurant_id": select_table_params.restaurant_id,
        "status": OrderStatus.pending,
        "party_size": select_table_params.party_size,
        "booking_time": select_table_params.booking_time,
    }
    order = crud_utils.create_item(db, model=Order, payload=order_data)
    # book table
    get_table_sql = f"select id from restaurant_table where restaurant_id = '{select_table_params.restaurant_id}'"
    table_id_fetch = db.execute(get_table_sql).fetchall()
    # get a list of table ids
    table_id = [item[0] for item in table_id_fetch]
    # convert table id python list into sql list
    table_sql = "("
    for i in range(len(table_id)):
        if i == len(table_id) - 1:
            table_sql = table_sql + str(table_id[i]) + ")"
        else:
            table_sql = table_sql + str(table_id[i]) + ", "
    available_sql = (
        f"select restaurant_table_id, is_available from table_availability where booking_time = '{select_table_params.booking_time}' and restaurant_table_id in "
        + table_sql
        + " FOR UPDATE"
    )
    available_table_fetch = db.execute(available_sql).fetchall()
    # table_id2 is for storing table id table_availability based on booking_time
    table_id2 = list()
    for i in range(len(available_table_fetch)):
        table_id_element, availability = available_table_fetch[i]
        table_id2.append(table_id_element)
        # if available table found, update row in table_availability
    # unshown_table indicates table_id not found in table_availability
    unshown_table = [x for x in table_id if x not in table_id2]
    if len(unshown_table) > 0:
        insert_sql = f"INSERT INTO table_availability (restaurant_table_id, order_id, booking_time, is_available) VALUES ('{unshown_table[0]}', '{order.id}', '{order.booking_time}', FALSE)"
        db.execute(insert_sql)
        db.commit()
        # if it's because tables are all booked
    else:
        raise HTTPException(status_code=404, detail="All booked")
    # order will be auto cancelled in 5min
    countdown_in_sec = 60 * 5
    tasks.cancel_order.apply_async(args=(order.ref_id,), countdown=countdown_in_sec, task_id=order.ref_id)
    logger.info(f"cancel order task({order.ref_id}) has been scheduled in {countdown_in_sec}sec")
    return order


def confirm_order(request: Request, db: Session, confirm_order_params: ConfirmOrderIn) -> OrderItem:
    # update order status
    db.execute(
        f"UPDATE public.order SET status = '{OrderStatus.complete.value.lower()}' where ref_id = '{confirm_order_params.ref_id}'"
    )
    db.commit()
    order = db.query(Order).filter(Order.ref_id == confirm_order_params.ref_id).first()
    # cancel the execution of cancel_order task
    celery_app.control.revoke(confirm_order_params.ref_id)
    logger.info(f"cancel_order task({confirm_order_params.ref_id}) has been revoked")
    return order
