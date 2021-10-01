from fastapi import APIRouter

api_router = APIRouter(prefix="/api", tags=["api"])
from . import control, statistics, search
api_router.include_router(control.api)
api_router.include_router(search.api)
api_router.include_router(statistics.api)


@api_router.get('/hello')
def api_hello():
    return "hello from api"
