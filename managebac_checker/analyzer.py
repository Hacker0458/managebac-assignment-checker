"""
🎓 ManageBac Assignment Checker Analyzer | ManageBac作业检查器分析器
====================================================================

Assignment analysis functionality for ManageBac Assignment Checker.
ManageBac作业检查器的作业分析功能模块。
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional

from .logging_utils import BilingualLogger


class AssignmentAnalyzer:
    """
    Handles assignment analysis and statistics generation.
    处理作业分析和统计生成。
    """

    def __init__(self, config, logger: Optional[BilingualLogger] = None):
        """
        Initialize analyzer with configuration.
        使用配置初始化分析器。
        """
        self.config = config
        self.logger = logger
        self.priority_keywords = getattr(
            config, "priority_keywords", ["exam", "test", "project", "essay"]
        )
        self.language = config.language

    def analyze_assignments(self, assignments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze assignment data and generate statistics."""
        if not assignments:
            return self._empty_analysis()

        analysis = {
            "total_assignments": len(assignments),
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_course": {},
            "by_due_date": {},
            "by_type": {},
            "urgent_count": 0,
            "overdue_count": 0,
            "submitted_count": 0,
            "pending_count": 0,
            "assignments_by_urgency": {"urgent": [], "soon": [], "later": []},
            "grouped_by_status": {
                "submitted": [],
                "pending": [],
                "overdue": [],
                "unknown": [],
            },
        }

        now = datetime.now()

        for assignment in assignments:
            # Course statistics
            course = assignment.get("course") or self._extract_course_name(
                assignment.get("title", "")
            )
            if course not in analysis["by_course"]:
                analysis["by_course"][course] = 0
            analysis["by_course"][course] += 1

            # Type statistics
            a_type = assignment.get("type", "Unknown")
            analysis["by_type"][a_type] = analysis["by_type"].get(a_type, 0) + 1

            # Priority analysis
            priority = self._calculate_priority(assignment)
            analysis["by_priority"][priority] += 1

            # Status grouping
            status = (assignment.get("status") or "未知").lower()
            if "submitted" in status or assignment.get("submitted"):
                analysis["grouped_by_status"]["submitted"].append(assignment)
                analysis["submitted_count"] += 1
            elif "overdue" in status or assignment.get("overdue"):
                analysis["grouped_by_status"]["overdue"].append(assignment)
                analysis["overdue_count"] += 1
            elif "pending" in status or "未提交" in status:
                analysis["grouped_by_status"]["pending"].append(assignment)
                analysis["pending_count"] += 1
            else:
                analysis["grouped_by_status"]["unknown"].append(assignment)

            # Urgency analysis
            urgency = self._calculate_urgency(assignment, now)
            analysis["assignments_by_urgency"][urgency].append(assignment)
            if urgency == "urgent":
                analysis["urgent_count"] += 1

            # Due date statistics
            due_date_str = assignment.get("due_date", "无截止日期")
            analysis["by_due_date"][due_date_str] = (
                analysis["by_due_date"].get(due_date_str, 0) + 1
            )

        return analysis

    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure."""
        return {
            "total_assignments": 0,
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "by_course": {},
            "by_due_date": {},
            "by_type": {},
            "urgent_count": 0,
            "overdue_count": 0,
            "submitted_count": 0,
            "pending_count": 0,
            "assignments_by_urgency": {"urgent": [], "soon": [], "later": []},
            "grouped_by_status": {
                "submitted": [],
                "pending": [],
                "overdue": [],
                "unknown": [],
            },
        }

    def _extract_course_name(self, title: str) -> str:
        """Extract course name from assignment title."""
        # Try to extract AP course names
        ap_match = re.search(r"AP\s+([^\n(]+)", title)
        if ap_match:
            return f"AP {ap_match.group(1).strip()}"

        # Look for course-related keywords
        course_keywords = {
            "Computer Science": ["CS", "Computer", "Programming"],
            "Mathematics": ["Math", "Calculus", "Algebra", "BC"],
            "Economics": ["Economics", "Macro", "Micro"],
            "History": ["History", "US History"],
            "Psychology": ["Psychology", "Psych"],
            "English": ["English", "Literature", "Writing"],
        }

        title_lower = title.lower()
        for course, keywords in course_keywords.items():
            if any(keyword.lower() in title_lower for keyword in keywords):
                return course

        return "未知课程"

    def _calculate_priority(self, assignment: Dict[str, Any]) -> str:
        """Calculate assignment priority."""
        title = assignment.get("title", "").lower()
        status = assignment.get("status", "").lower()

        # High priority keywords
        high_priority_keywords = [
            "summative",
            "exam",
            "test",
            "project",
            "essay",
            "final",
        ]
        if any(
            keyword in title or keyword in status for keyword in high_priority_keywords
        ):
            return "high"

        # Medium priority keywords
        medium_priority_keywords = ["homework", "assignment", "quiz"]
        if any(
            keyword in title or keyword in status
            for keyword in medium_priority_keywords
        ):
            return "medium"

        return "low"

    def _calculate_urgency(self, assignment: Dict[str, Any], now: datetime) -> str:
        """Calculate assignment urgency."""
        due_date_str = assignment.get("due_date", "")

        # Try to parse due date
        try:
            # Simple date parsing (can be further optimized)
            if "sunday" in due_date_str.lower() or "monday" in due_date_str.lower():
                return "urgent"
            elif (
                "tuesday" in due_date_str.lower() or "wednesday" in due_date_str.lower()
            ):
                return "soon"
            else:
                return "later"
        except:
            return "later"
