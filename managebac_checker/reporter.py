"""报告生成功能的兼容封装。"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from .reporting import ReportBuilder
from .models import Assignment
from .logging_utils import BilingualLogger
from .analyzer import _coerce_assignment  # reuse helper


class ReportGenerator:
    """面向旧代码的报告生成器包装。"""

    def __init__(self, config, logger: Optional[BilingualLogger] = None):
        self.config = config
        self.logger = logger
        self.builder = ReportBuilder(
            output_dir=config.output_dir,
            report_formats=getattr(config, "report_formats", ["console", "json"]),
        )

    def build_reports(
        self, assignments: Iterable[Any], analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        assignment_objs: List[Assignment] = [
            _coerce_assignment(item) for item in assignments
        ]
        reports = self.builder.build(assignment_objs, analysis)
        if self.logger:
            for fmt in reports:
                if fmt != "console":
                    self.logger.report_generation(fmt)
        return reports

    def save_reports(self, reports: Dict[str, str]) -> Dict[str, str]:
        saved = self.builder.persist(reports)
        if self.logger:
            for path in saved.values():
                self.logger.report_saved(path)
        return saved

    def generate_reports(
        self, assignments: Iterable[Any], analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        reports = self.build_reports(assignments, analysis)
        return self.save_reports(reports)
