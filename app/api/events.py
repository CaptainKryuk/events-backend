import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import get_pgsql_session
from app.db.models import Event

router = APIRouter()


class EventCreateData(BaseModel):
    author_id: int
    invited_id: int
    name: str
    event_date: datetime.date

class EventListEntity(BaseModel):
    id: int
    author_id: int
    invited_id: int
    event_date: datetime.date | None = Field(None)
    name: str


@router.get('/list')
async def events_list(
    user_id: int,
    session: AsyncSession = Depends(get_pgsql_session),
):
    my_events = (await session.execute(select(Event).where(Event.author_id == user_id))).scalars().all()
    invited_events = (await session.execute(select(Event).where(Event.invited_id == user_id))).scalars().all()

    return {
        'my_events': [EventListEntity.model_validate(x, from_attributes=True) for x in my_events],
        'invited_events': [EventListEntity.model_validate(x, from_attributes=True) for x in invited_events],
    }



@router.post('/create')
async def create_event(
    data: EventCreateData,
    session: AsyncSession = Depends(get_pgsql_session),
):
    event = Event(
        author_id=data.author_id,
        invited_id=data.invited_id,
        event_date=data.event_date,
        name=data.name
    )
    session.add(event)
    await session.commit()