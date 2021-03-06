import os

PROJECT_NAME = "nomorewait"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin@localhost/nomorewait")

API_V1_STR = "/api/v1"