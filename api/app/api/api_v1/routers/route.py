from app.api.api_v1.routers import location, restaurant

route = [
    location.LocationViewSet,
    restaurant.RestaurantViewSet,
    restaurant.RestaurantTableViewSet,
    restaurant.OrderViewSet,
    restaurant.TableAvailabilityViewSet,
]