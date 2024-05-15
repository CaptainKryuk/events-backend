from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from app.api import root_router


def create_app() -> FastAPI:
    _app = FastAPI(
        debug=True,
        docs_url='/docs'
    )

    _app.include_router(router=root_router)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # type:ignore
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return _app

app = create_app()