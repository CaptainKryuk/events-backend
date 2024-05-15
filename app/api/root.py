from fastapi import APIRouter
from .users import router as users_router
from .events import router as events_router


root_router = APIRouter(prefix='/api/v1')
root_router.include_router(prefix='/users', router=users_router)
root_router.include_router(prefix='/events', router=events_router)