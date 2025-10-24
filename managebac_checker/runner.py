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
from .cache import AssignmentCache
from .config import Config
from .logging_utils import setup_logging
from .models import Assignment
from .notifications import send_email_notification
from .performance import get_global_monitor
from .reporting import ReportBuilder
from .scraper import run_scraper


class Runner:
    def __init__(
        self,
        overrides: Optional[Dict] = None,
        config: Optional[Config] = None,
        enable_cache: bool = True,
        enable_performance_monitoring: bool = True,
    ) -> None:
        load_dotenv()
        self.config = config or Config.from_environment(overrides or {})
        self.logger = setup_logging(self.config.debug)
        self.cache = AssignmentCache() if enable_cache else None
        self.monitor = get_global_monitor() if enable_performance_monitoring else None

    async def execute(self) -> Dict[str, object]:
        self.logger.info("Starting ManageBac assignment check")

        # 尝试从缓存加载
        assignments = None
        if self.cache:
            if self.monitor:
                async with self.monitor.measure_async("cache_load"):
                    assignments = self.cache.get(self.config.email, self.config.url)
            else:
                assignments = self.cache.get(self.config.email, self.config.url)

            if assignments:
                self.logger.info("Loaded %d assignments from cache", len(assignments))

        # 如果缓存未命中，进行抓取
        if not assignments:
            if self.monitor:
                async with self.monitor.measure_async("scraping"):
                    assignments = await run_scraper(self.config, self.logger)
            else:
                assignments = await run_scraper(self.config, self.logger)

            if not assignments:
                self.logger.warning("No assignments found")
            elif self.cache:
                # 保存到缓存
                self.cache.set(self.config.email, self.config.url, assignments)

        # 分析作业
        if self.monitor:
            with self.monitor.measure("analysis"):
                analysis = analyse_assignments(
                    assignments,
                    self.config.priority_keywords,
                    days_ahead=self.config.days_ahead,
                )
        else:
            analysis = analyse_assignments(
                assignments,
                self.config.priority_keywords,
                days_ahead=self.config.days_ahead,
            )

        # 生成报告
        if self.monitor:
            with self.monitor.measure("report_generation"):
                report_builder = ReportBuilder(
                    output_dir=self.config.output_dir,
                    report_formats=self.config.report_formats,
                )
                reports = report_builder.build(assignments, analysis)
                saved_files = report_builder.persist(reports)
        else:
            report_builder = ReportBuilder(
                output_dir=self.config.output_dir,
                report_formats=self.config.report_formats,
            )
            reports = report_builder.build(assignments, analysis)
            saved_files = report_builder.persist(reports)

        # 发送通知
        if self.config.enable_notifications and assignments:
            if self.monitor:
                with self.monitor.measure("notifications"):
                    self._send_notifications(assignments, analysis)
            else:
                self._send_notifications(assignments, analysis)

        console_report = reports.get("console")
        if console_report:
            self.logger.info("\n%s", console_report)

        # 打印性能统计
        if self.monitor and self.config.debug:
            self.monitor.print_stats()

        result = {
            "assignments": assignments,
            "analysis": analysis,
            "reports": reports,
            "saved_files": saved_files,
        }

        # 添加性能和缓存统计
        if self.monitor:
            result["performance_stats"] = self.monitor.get_stats()
        if self.cache:
            result["cache_stats"] = self.cache.get_stats()

        return result

    def _send_notifications(
        self, assignments: List[Assignment], analysis: Dict[str, object]
    ) -> None:
        urgent = analysis["assignments_by_urgency"]["urgent"]
        if not urgent:
            self.logger.info(
                "Email notifications enabled but no urgent assignments detected"
            )
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
            self.logger.info(
                "Email notification sent to %s", self.config.notification_email
            )
        except Exception as exc:
            self.logger.error("Failed to send notification: %s", exc)


def run_sync(overrides: Optional[Dict] = None) -> Dict[str, object]:
    runner = Runner(overrides)
    return asyncio.run(runner.execute())
