import app.db.models.location as location_model
import app.db.schemas.location as location_schema
from app.utils.view import ModelViewSet


class LocationViewSet(ModelViewSet):
    ENDPOINT = "location"
    MODEL = location_model.Location
    GET_SCHEMA_OUT = location_schema.LocationItem
    POST_SCHEMA_IN = location_schema.LocationBase
    PATCH_SCHEMA_IN = location_schema.LocationBase
