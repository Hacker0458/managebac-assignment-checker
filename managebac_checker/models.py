"""Data models used by the ManageBac assignment checker."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass(slots=True)
class Assignment:
    identifier: str
    title: str
    course: str
    status: str
    due_date: str
    assignment_type: str = "Unknown"
    priority: str = "low"
    submitted: bool = False
    overdue: bool = False
    link: Optional[str] = None
    description: Optional[str] = None
    raw_text: Optional[str] = None
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.identifier,
            "title": self.title,
            "course": self.course,
            "status": self.status,
            "due_date": self.due_date,
            "type": self.assignment_type,
            "priority": self.priority,
            "submitted": self.submitted,
            "overdue": self.overdue,
            "link": self.link,
            "description": self.description,
            "raw_text": self.raw_text,
            "fetched_at": self.fetched_at.isoformat(),
        }
