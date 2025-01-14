from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None


class EventCreate(EventBase):
    user_id: int


class Event(EventBase):
    id: int  # Identificador único del evento
    user_id: int  # ID del usuario asociado
    created_at: datetime  # Fecha de creación
    updated_at: datetime  # Fecha de última actualización


# Esquema para la actualización de un evento
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None


class FormattedEvent(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    location: Optional[str] = None
    created_at: str
    updated_at: str
