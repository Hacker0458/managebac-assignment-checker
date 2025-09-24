"""High level orchestration for the assignment checker."""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency guard

    def load_dotenv():
        return None


from .analysis import analyse_assignments
from .config import Config
from .logging_utils import setup_logging
from .models import Assignment
from .notifications import send_email_notification
from .reporting import ReportBuilder
from .scraper import run_scraper


class Runner:
    def __init__(self, overrides: Optional[Dict] = None, config: Optional[Config] = None) -> None:
        load_dotenv()
        self.config = config or Config.from_environment(overrides or {})
        self.logger = setup_logging(self.config.debug)

    async def execute(self) -> Dict[str, object]:
        self.logger.info("Starting ManageBac assignment check")
        assignments = await run_scraper(self.config, self.logger)
        if not assignments:
            self.logger.warning("No assignments found")

        analysis = analyse_assignments(
            assignments,
            self.config.priority_keywords,
            days_ahead=self.config.days_ahead,
        )

        report_builder = ReportBuilder(
            output_dir=self.config.output_dir, report_formats=self.config.report_formats
        )
        reports = report_builder.build(assignments, analysis)
        saved_files = report_builder.persist(reports)

        if self.config.enable_notifications and assignments:
            self._send_notifications(assignments, analysis)

        console_report = reports.get("console")
        if console_report:
            self.logger.info("\n%s", console_report)

        return {
            "assignments": assignments,
            "analysis": analysis,
            "reports": reports,
            "saved_files": saved_files,
        }

    def _send_notifications(
        self, assignments: List[Assignment], analysis: Dict[str, object]
    ) -> None:
        urgent = analysis["assignments_by_urgency"]["urgent"]
        if not urgent:
            self.logger.info("Email notifications enabled but no urgent assignments detected")
            return

        try:
            send_email_notification(
                smtp_server=self.config.smtp_server,
                smtp_port=self.config.smtp_port,
                username=self.config.email_user,
                password=self.config.email_password,
                recipient=self.config.notification_email,
                subject=f"ManageBac 作业提醒 - {len(urgent)} 个紧急任务",
                urgent_assignments=urgent,
                total_count=analysis["total_assignments"],
            )
            self.logger.info("Email notification sent to %s", self.config.notification_email)
        except Exception as exc:
            self.logger.error("Failed to send notification: %s", exc)


def run_sync(overrides: Optional[Dict] = None) -> Dict[str, object]:
    runner = Runner(overrides)
    return asyncio.run(runner.execute())
