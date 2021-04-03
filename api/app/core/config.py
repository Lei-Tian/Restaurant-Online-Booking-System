import os

PROJECT_NAME = "nomorewait"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/nomorewait")
REDIS_URI = os.getenv("REDIS_URL", "redis://localhost")

API_V1_STR = "/api/v1"
