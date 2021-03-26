
import logging
import time
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from starlette.requests import Request

from app.api.api_v1.routers import route as route_v1
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.consumer import consumer_router
from app.api.api_v1.routers.user import users_router
from app.core import config
from app.core.auth import get_current_active_user
from app.db.session import SessionLocal, get_db
from app.tasks import greeting
from app.utils.logger import CustomizeLogger
from app.utils.view import register_router

logger = logging.getLogger(__name__)
config_path=Path(__file__).with_name("logging_config.json")

def create_app(serve_static: bool = False) -> FastAPI:
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
    CustomizeLogger.make_logger(config_path)
    # serve static files
    if serve_static: serve_static_files(app)
    return app


def serve_static_files(app):
    app.mount("/static", StaticFiles(directory='public/static'), name="static")
    app.mount("/assets", StaticFiles(directory='public/assets'), name="assets")
    templates = Jinja2Templates(directory='public')
    @app.get("/{catchall:path}", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})


app = create_app()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.middleware("http")
async def log_session_middleware(request: Request, call_next):
    logger.info(f"[REQ IN]: url={request.url}")
    start_time = time.time()
    response = await call_next(request)
    logger.info(f"[RES OUT]: total_time={time.time() - start_time:.6f}s")
    return response


@app.on_event('startup')
async def on_startup():
    caches.set(CACHE_KEY, RedisCacheBackend(config.REDIS_URI))


@app.on_event('shutdown')
async def on_shutdown():
    await close_caches


@app.get("/api/")
async def root(request: Request):
    logger.info("hello nomorewait")
    return {"message": "Hello NoMoreWait"}


@app.get("/api/v1/task")
async def example_task(request: Request):
    greeting.apply_async(args=("Hello NoMoreWait!",), countdown=5)
    return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_db), Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api")
app.include_router(consumer_router, prefix="/api")
register_router(app, "v1", [*route_v1.route])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=9000)
