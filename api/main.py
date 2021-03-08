
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.api_v1.routers import route as route_v1
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.user import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.utils.logger import CustomizeLogger
from app.utils.view import register_router

config_path=Path(__file__).with_name("logging_config.json")

def create_app() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api")
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 
    # set app logger
    app.logger = CustomizeLogger.make_logger(config_path)
    return app


app = create_app()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root(request: Request):
    request.app.logger.info("hello nomorewait")
    return {"message": "Hello NoMoreWait"}


@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])
    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])
register_router(app, "v1", [*route_v1.route])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=9000)
