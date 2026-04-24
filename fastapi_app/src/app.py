from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api import users, posts, categories, comments, locations, authorization
from core.config import settings
from core.logging_config import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(root_path=settings.ROOT_PATH)

    origins = [o.strip() for o in settings.ORIGINS.split(",") if o.strip()] or ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(authorization.router)
    app.include_router(users.router)
    app.include_router(posts.router)
    app.include_router(categories.router)
    app.include_router(comments.router)
    app.include_router(locations.router)

    return app