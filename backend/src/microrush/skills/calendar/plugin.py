"""Calendar plugin for Micro Rush."""

from datetime import datetime, timedelta
from typing import Optional
from ..plugins import Plugin


# Simple calendar integration — replace with actual calendar API
class CalendarPlugin(Plugin):
    """
    Calendar monitoring and proactive scheduling.

    Capabilities:
    - View today's meetings
    - Calculate travel time and suggest departure
    - Send reminders before meetings
    - Proactively suggest scheduling based on free time
    """

    name = "calendar"
    description = "Smart calendar with proactive traffic awareness"
    version = "0.1.0"

    def __init__(self):
        self._meetings: list[dict] = []

    def add_meeting(self, title: str, start_time: datetime, end_time: datetime, location: str | None = None) -> dict:
        """Add a meeting to track."""
        meeting = {
            "id": len(self._meetings) + 1,
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
        }
        self._meetings.append(meeting)
        return meeting

    def execute(self, context: dict) -> dict:
        """
        Handle calendar-related requests.

        Context keys:
        - action: "get_next_meeting" | "departure_time" | "free_time"
        - query: optional search terms
        """
        action = context.get("action", "get_next_meeting")

        if action == "get_next_meeting":
            return self._get_next_meeting()
        elif action == "departure_time":
            return self._calculate_departure(context.get("meeting_id"))
        elif action == "free_time":
            return self._find_free_time(context.get("duration_minutes", 60))
        else:
            return {"error": f"Unknown action: {action}"}

    def _get_next_meeting(self) -> dict:
        """Get the next upcoming meeting."""
        now = datetime.utcnow()
        upcoming = [m for m in self._meetings if m["start_time"] > now]
        if not upcoming:
            return {"result": "No upcoming meetings"}
        next_meeting = min(upcoming, key=lambda m: m["start_time"])
        return {"result": next_meeting}

    def _calculate_departure(self, meeting_id: int) -> dict:
        """
        Calculate when to leave for a meeting based on traffic.

        TODO: Integrate real traffic API (Google Maps, etc.)
        """
        meeting = next((m for m in self._meetings if m["id"] == meeting_id), None)
        if not meeting:
            return {"error": "Meeting not found"}

        # Placeholder traffic calculation
        if meeting.get("location"):
            travel_minutes = 20  # TODO: Real traffic lookup
            buffer_minutes = 10
            departure_time = meeting["start_time"] - timedelta(minutes=travel_minutes + buffer_minutes)
            return {
                "result": f"Leave by {departure_time.strftime('%H:%M')} for your {meeting['title']} at {meeting['location']}",
                "departure_time": departure_time,
                "travel_minutes": travel_minutes,
            }

        return {"result": f"Meeting '{meeting['title']}' at {meeting['start_time'].strftime('%H:%M')}, no location set"}

    def _find_free_time(self, duration_minutes: int = 60) -> dict:
        """Find the next available free time slot."""
        now = datetime.utcnow()
        free_slots = []
        sorted_meetings = sorted(self._meetings, key=lambda m: m["start_time"])

        # Simple logic: find gaps between meetings
        if not sorted_meetings:
            return {"result": f"You're free now for {duration_minutes}+ minutes"}

        current = now
        for meeting in sorted_meetings:
            if meeting["start_time"] > current:
                gap = (meeting["start_time"] - current).total_seconds() / 60
                if gap >= duration_minutes:
                    free_slots.append({"start": current, "end": meeting["start_time"]})
                current = meeting["end_time"]

        if free_slots:
            slot = free_slots[0]
            return {
                "result": f"Free {slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')}"
            }

        return {"result": "No free slots found in the next 24 hours"}