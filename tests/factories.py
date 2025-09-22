"""Test helpers for building assignment objects."""

from __future__ import annotations

from managebac_checker.models import Assignment


def make_assignment(**overrides):
    counter = make_assignment.counter
    make_assignment.counter += 1
    base = {
        "identifier": f"id-{counter}",
        "title": f"Assignment {counter}",
        "course": "Mathematics",
        "status": "Pending",
        "due_date": "2025-01-01",
        "assignment_type": "Summative",
        "priority": "medium",
    }
    base.update(overrides)
    return Assignment(**base)


make_assignment.counter = 1
