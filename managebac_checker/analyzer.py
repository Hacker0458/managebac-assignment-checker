"""作业分析兼容层。"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from .analysis import analyse_assignments
from .models import Assignment
from .logging_utils import BilingualLogger


def _coerce_assignment(item: Any) -> Assignment:
    if isinstance(item, Assignment):
        return item
    if isinstance(item, dict):
        identifier = (
            item.get("identifier")
            or item.get("id")
            or item.get("title", "assignment").lower()
        )
        return Assignment(
            identifier=identifier,
            title=item.get("title", "未命名作业"),
            course=item.get("course", "未知课程"),
            status=item.get("status", "Unknown"),
            due_date=item.get("due_date", "无截止日期"),
            assignment_type=item.get("type", "Unknown"),
            priority=item.get("priority", "low"),
            submitted=bool(item.get("submitted", False)),
            overdue=bool(item.get("overdue", False)),
            link=item.get("link"),
            description=item.get("description"),
            raw_text=item.get("raw_text"),
        )
    raise TypeError("Unsupported assignment payload")


class AssignmentAnalyzer:
    """薄封装，复用新的 analyse_assignments 实现。"""

    def __init__(self, config, logger: Optional[BilingualLogger] = None):
        self.config = config
        self.logger = logger

    def analyze_assignments(self, assignments: Iterable[Any]) -> Dict[str, Any]:
        if self.logger:
            self.logger.analysis_start()
        assignment_objs: List[Assignment] = [
            _coerce_assignment(item) for item in assignments
        ]
        result = analyse_assignments(
            assignment_objs,
            self.config.priority_keywords,
            days_ahead=getattr(self.config, "days_ahead", 7),
        )
        if self.logger:
            self.logger.debug(f"分析完成，共 {result['total_assignments']} 个作业")
        return result
