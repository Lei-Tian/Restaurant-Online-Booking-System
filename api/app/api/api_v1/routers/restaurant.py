import app.db.models.restaurant as restaurant_model
import app.db.schemas.restaurant as restaurant_schema
from app.utils.view import ModelViewSet


class RestaurantViewSet(ModelViewSet):
    ENDPOINT = "restaurant"
    MODEL = restaurant_model.Restaurant
    GET_SCHEMA_OUT = restaurant_schema.RestaurantItem
    POST_SCHEMA_IN = restaurant_schema.RestaurantBase
    PATCH_SCHEMA_IN = restaurant_schema.RestaurantBase


class RestaurantTableViewSet(ModelViewSet):
    ENDPOINT = "restaurant-table"
    MODEL = restaurant_model.RestaurantTable
    GET_SCHEMA_OUT = restaurant_schema.RestaurantTableItem
    POST_SCHEMA_IN = restaurant_schema.RestaurantTableBase
    PATCH_SCHEMA_IN = restaurant_schema.RestaurantTableBase


class OrderViewSet(ModelViewSet):
    ENDPOINT = "order"
    MODEL = restaurant_model.Order
    GET_SCHEMA_OUT = restaurant_schema.OrderItem
    POST_SCHEMA_IN = restaurant_schema.OrderBase
    PATCH_SCHEMA_IN = restaurant_schema.OrderBase


class TableAvailabilityViewSet(ModelViewSet):
    ENDPOINT = "table-availability"
    MODEL = restaurant_model.TableAvailability
    GET_SCHEMA_OUT = restaurant_schema.TableAvailabilityItem
    POST_SCHEMA_IN = restaurant_schema.TableAvailabilityBase
    PATCH_SCHEMA_IN = restaurant_schema.TableAvailabilityBase