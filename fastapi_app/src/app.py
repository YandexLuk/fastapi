from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api import users, posts, categories, comments, locations


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users.router)
    app.include_router(posts.router)
    app.include_router(categories.router)
    app.include_router(comments.router)
    app.include_router(locations.router)

    return app