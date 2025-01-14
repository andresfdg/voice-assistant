from typing import List

from fastapi import APIRouter

# from app.services.user import UserService
from app.modules.event.schemas import Event, EventCreate, FormattedEvent
from app.modules.event.services import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[FormattedEvent])
async def get_users():
    events = await EventService.get_all_events()
    return events


@router.post("/", response_model=Event)
async def create_event(event_data: EventCreate):
    """Crea un nuevo evento."""
    event = await EventService.create_event(
        user_id=event_data.user_id,
        title=event_data.title,
        description=event_data.description,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        location=event_data.location,
    )
    return event
