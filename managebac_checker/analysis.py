"""Assignment analysis helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Tuple

from .models import Assignment


def analyse_assignments(
    assignments: Iterable[Assignment],
    priority_keywords: Iterable[str],
    *,
    days_ahead: int = 7,
) -> Dict[str, object]:
    assignments = list(assignments)
    priority_keywords = {kw.strip().lower() for kw in priority_keywords if kw.strip()}

    analysis: Dict[str, object] = {
        "total_assignments": len(assignments),
        "by_priority": {"high": 0, "medium": 0, "low": 0},
        "by_course": {},
        "by_due_date": {},
        "by_type": {},
        "grouped_by_status": {
            "submitted": [],
            "pending": [],
            "overdue": [],
            "unknown": [],
        },
        "assignments_by_urgency": {"urgent": [], "soon": [], "later": []},
        "urgent_count": 0,
        "overdue_count": 0,
        "submitted_count": 0,
        "pending_count": 0,
    }

    now = datetime.now(timezone.utc)
    urgent_cutoff = now + timedelta(days=2)
    soon_cutoff = now + timedelta(days=days_ahead)

    for assignment in assignments:
        _increment(analysis["by_course"], assignment.course)
        _increment(analysis["by_type"], assignment.assignment_type)

        analysis["by_priority"][assignment.priority] += 1

        status_key = _normalise_status(
            assignment.status, assignment.submitted, assignment.overdue
        )
        analysis["grouped_by_status"][status_key].append(assignment)
        if status_key == "submitted":
            analysis["submitted_count"] += 1
        elif status_key == "pending":
            analysis["pending_count"] += 1
        elif status_key == "overdue":
            analysis["overdue_count"] += 1

        urgency_key = _classify_urgency(assignment, now, urgent_cutoff, soon_cutoff)
        analysis["assignments_by_urgency"][urgency_key].append(assignment)
        if urgency_key == "urgent":
            analysis["urgent_count"] += 1

        due_key = assignment.due_date or "无截止日期"
        _increment(analysis["by_due_date"], due_key)

    # Derive a flat list of urgent keywords matches (for reporting readability)
    analysis["priority_keywords"] = sorted(priority_keywords)
    return analysis


def _increment(bucket: Dict[str, int], key: str) -> None:
    bucket[key] = bucket.get(key, 0) + 1


def _normalise_status(status: str, submitted: bool, overdue: bool) -> str:
    value = (status or "").lower()
    if submitted or "submitted" in value or "已提交" in value:
        return "submitted"
    if overdue or "overdue" in value or "逾期" in value or "迟" in value:
        return "overdue"
    if "pending" in value or "未提交" in value or "待" in value:
        return "pending"
    return "unknown"


def _classify_urgency(
    assignment: Assignment,
    now: datetime,
    urgent_cutoff: datetime,
    soon_cutoff: datetime,
) -> str:
    due_dt = _parse_due_date(assignment.due_date, reference=now)
    if not due_dt:
        return "later"
    if due_dt <= urgent_cutoff:
        return "urgent"
    if due_dt <= soon_cutoff:
        return "soon"
    return "later"


def _parse_due_date(raw: str, reference: datetime) -> datetime | None:
    if not raw:
        return None

    lowered = raw.lower()
    relative_map: Dict[str, int] = {
        "today": 0,
        "tomorrow": 1,
        "今天": 0,
        "明天": 1,
        "后天": 2,
    }
    for keyword, offset in relative_map.items():
        if keyword in lowered:
            return reference.replace(
                hour=23, minute=59, second=0, microsecond=0
            ) + timedelta(days=offset)

    weekday_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
        "周一": 0,
        "周二": 1,
        "周三": 2,
        "周四": 3,
        "周五": 4,
        "周六": 5,
        "周日": 6,
    }
    for keyword, target_weekday in weekday_map.items():
        if keyword in lowered:
            days_ahead = (target_weekday - reference.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            return reference + timedelta(days=days_ahead)

    # Last resort: try parsing YYYY-MM-DD or DD Month
    normalized = raw.replace("年", "-").replace("月", "-").replace("日", "").strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            parsed = datetime.strptime(normalized, fmt)
            return parsed.replace(tzinfo=reference.tzinfo)
        except ValueError:
            continue

    return None
