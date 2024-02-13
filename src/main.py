from fastapi import FastAPI, APIRouter


def _include_routers(app: FastAPI, *routers: APIRouter) -> None:
    for router in routers:
        app.include_router(router)


def _create_app() -> FastAPI:
    app = FastAPI()
    return app
