from datetime import datetime

from fastapi import HTTPException
from pytz import timezone

from app.core.db import get_db


class EventService:

    @staticmethod
    async def get_all_events():
        """Fetch all events and format the dates to the local timezone (Toronto)."""
        pool = await get_db()
        async with pool.acquire() as conn:
            sql = """
                SELECT id, user_id, title, description, start_time, end_time, location, created_at, updated_at 
                FROM events;
            """
            rows = await conn.fetch(sql)
            events = []

            local_tz = timezone("America/Toronto")

            for row in rows:
                event = dict(row)
                # Convert datetime to local timezone and format to a readable string
                event["start_time"] = (
                    event["start_time"]
                    .astimezone(local_tz)
                    .strftime("%Y-%m-%d %I:%M %p")
                )  # Example: 2025-01-13 09:00 AM
                event["end_time"] = (
                    event["end_time"].astimezone(local_tz).strftime("%Y-%m-%d %I:%M %p")
                )  # Example: 2025-01-13 10:00 AM
                event["created_at"] = (
                    event["created_at"]
                    .astimezone(local_tz)
                    .strftime("%Y-%m-%d %I:%M %p")
                )  # Example: 2025-01-12 08:30 PM
                event["updated_at"] = (
                    event["updated_at"]
                    .astimezone(local_tz)
                    .strftime("%Y-%m-%d %I:%M %p")
                )  # Example: 2025-01-12 09:00 PM
                events.append(event)

            return events

    @staticmethod
    async def create_event(
        user_id: int,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        location: str,
    ):
        # Validate that the datetimes are offset-aware (contain timezone information)
        if start_time.tzinfo is None:
            raise ValueError(
                "start_time must include timezone information (offset-aware)"
            )
        if end_time.tzinfo is None:
            raise ValueError(
                "end_time must include timezone information (offset-aware)"
            )

        pool = await get_db()
        async with pool.acquire() as conn:
            sql = """
                INSERT INTO events (user_id, title, description, start_time, end_time, location)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id, user_id, title, description, start_time, end_time, location, created_at, updated_at;
            """
            row = await conn.fetchrow(
                sql, user_id, title, description, start_time, end_time, location
            )
            if not row:
                raise HTTPException(
                    status_code=400, detail="Could not create the event"
                )
            return dict(row)
