"""
🎓 ManageBac Assignment Checker | ManageBac作业检查器
=====================================================

Main checker class that orchestrates the entire assignment checking process.
主要的检查器类，协调整个作业检查流程。
"""

import asyncio
import webbrowser
from datetime import datetime
from typing import List, Dict, Any, Optional

from playwright.async_api import async_playwright, Browser

from .config import Config
from .scraper import ManageBacScraper
from .analyzer import AssignmentAnalyzer
from .reporter import ReportGenerator
from .notifications import NotificationManager
from .logging_utils import BilingualLogger, setup_logging


class ManageBacChecker:
    """
    ManageBac Assignment Checker main class.
    ManageBac作业检查器主类。
    """

    def __init__(
        self, config: Optional[Config] = None, logger: Optional[BilingualLogger] = None
    ):
        """
        Initialize the checker.
        初始化检查器。

        Args:
            config: Configuration instance
            logger: Logger instance
        """
        self.config = config or Config()
        self.logger = logger or setup_logging(
            level=self.config.log_level,
            log_file=self.config.log_file,
            language=self.config.language,
        )

        # Initialize components | 初始化组件
        self.scraper = ManageBacScraper(self.config, self.logger)
        self.analyzer = AssignmentAnalyzer(self.config, self.logger)
        self.reporter = ReportGenerator(self.config, self.logger)
        self.notifications = NotificationManager(self.config, self.logger)

    async def run(self) -> None:
        """
        Run the main checking process.
        运行主要的检查流程。
        """
        try:
            # Log startup
            self.logger.startup()

            # Display startup info
            self._display_startup_info()

            async with async_playwright() as p:
                # Launch browser | 启动浏览器
                browser = await self._launch_browser(p)

                try:
                    # Create new page | 创建新页面
                    page = await browser.new_page()

                    # Configure page | 配置页面
                    await self._configure_page(page)

                    # Login to ManageBac | 登录ManageBac
                    if not await self._perform_login(page):
                        return

                    # Navigate and scrape | 导航并抓取
                    assignments = await self._scrape_assignments(page, browser)

                    # Process and report | 处理并报告
                    await self._process_and_report(assignments)

                finally:
                    await browser.close()

            # Log completion
            self.logger.completion()

        except Exception as e:
            self.logger.error_occurred(str(e))
            raise

    async def _launch_browser(self, playwright) -> Browser:
        """Launch browser with appropriate settings."""
        self.logger.debug(
            "启动浏览器..." if self.config.language == "zh" else "Launching browser..."
        )

        return await playwright.chromium.launch(
            headless=self.config.headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
            ],
        )

    async def _configure_page(self, page) -> None:
        """Configure page settings."""
        # Set viewport size
        await page.set_viewport_size({"width": 1280, "height": 720})

        # Set user agent if configured
        if hasattr(self.config, "user_agent") and self.config.user_agent:
            await page.set_extra_http_headers({"User-Agent": self.config.user_agent})

    async def _perform_login(self, page) -> bool:
        """Perform login to ManageBac."""
        self.logger.login_start()

        success = await self.scraper.login(page)

        if success:
            self.logger.login_success()
            # Wait for page to fully load
            await page.wait_for_timeout(3000)
        else:
            error_msg = (
                "登录失败，请检查您的凭据"
                if self.config.language == "zh"
                else "Login failed, please check your credentials"
            )
            self.logger.error_occurred(error_msg)
            self._display_error(error_msg)

        return success

    async def _scrape_assignments(self, page, browser) -> List[Dict[str, Any]]:
        """Scrape assignments from ManageBac."""
        self.logger.scraping_start()

        # Debug mode exploration
        if self.config.debug or not self.config.headless:
            await self.scraper.explore_page_structure(page)

        # Navigate to assignments page
        navigation_success = await self.scraper.navigate_to_assignments(page)

        if navigation_success:
            success_msg = (
                "成功导航到作业页面"
                if self.config.language == "zh"
                else "Successfully navigated to assignments page"
            )
            self.logger.info(success_msg)
            await page.wait_for_timeout(3000)

            if self.config.debug:
                await self.scraper.explore_page_structure(page)

        # Get all assignments
        assignments = await self.scraper.get_all_assignments(page, browser)

        self.logger.assignments_found(len(assignments))
        return assignments

    async def _process_and_report(self, assignments: List[Dict[str, Any]]) -> None:
        """Process assignments and generate reports."""
        # Analyze assignments | 分析作业
        self.logger.analysis_start()
        analysis = self.analyzer.analyze_assignments(assignments)

        # Generate reports | 生成报告
        for format_type in self.config.get_report_formats():
            self.logger.report_generation(format_type)

        reports = self.reporter.generate_reports(assignments, analysis)

        # Display console results | 显示控制台结果
        self._display_console_results(assignments, analysis)

        # Save report files | 保存报告文件
        saved_files = self.reporter.save_reports(reports)

        for format_type, path in saved_files.items():
            self.logger.report_saved(path)

        # Send notifications | 发送通知
        await self._send_notifications(assignments, analysis)

        # Display summary | 显示总结
        self._display_summary(assignments, analysis, saved_files)

        # Auto-open HTML report | 自动打开HTML报告
        await self._auto_open_report(saved_files)

    async def _send_notifications(
        self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]
    ) -> None:
        """Send email notifications if enabled."""
        if self.config.is_notification_enabled() and assignments:
            try:
                recipients = ", ".join(self.config.get_notification_recipients())
                await self.notifications.send_email_notification(assignments, analysis)
                self.logger.notification_sent(recipients)
            except Exception as e:
                error_msg = (
                    f"邮件发送失败: {e}"
                    if self.config.language == "zh"
                    else f"Failed to send email: {e}"
                )
                self.logger.error_occurred(error_msg)

    async def _auto_open_report(self, saved_files: Dict[str, str]) -> None:
        """Auto-open HTML report in browser."""
        if "html" in saved_files:
            try:
                open_msg = (
                    "自动打开HTML报告..."
                    if self.config.language == "zh"
                    else "Auto-opening HTML report..."
                )
                print(f"\n➡️  {open_msg}")
                webbrowser.open(saved_files["html"])
            except Exception as e:
                if self.config.debug:
                    error_msg = (
                        f"无法自动打开浏览器: {e}"
                        if self.config.language == "zh"
                        else f"Cannot auto-open browser: {e}"
                    )
                    self.logger.debug(error_msg)

    def _display_startup_info(self) -> None:
        """Display startup information."""
        if self.config.language == "zh":
            print("=== 🎓 ManageBac作业检查器 ===")
            print(f"目标URL: {self.config.url}")
            print(f"邮箱: {self.config.email}")
            print(f"语言: {'中文' if self.config.language == 'zh' else 'English'}")
            print(f"无头模式: {'是' if self.config.headless else '否'}")
            print(f"调试模式: {'是' if self.config.debug else '否'}")
        else:
            print("=== 🎓 ManageBac Assignment Checker ===")
            print(f"Target URL: {self.config.url}")
            print(f"Email: {self.config.email}")
            print(
                f"Language: {'Chinese' if self.config.language == 'zh' else 'English'}"
            )
            print(f"Headless: {'Yes' if self.config.headless else 'No'}")
            print(f"Debug: {'Yes' if self.config.debug else 'No'}")
        print()

    def _display_error(self, message: str) -> None:
        """Display error message."""
        print(f"❌ {message}")

    def _display_console_results(
        self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]
    ) -> None:
        """Display results in console."""
        separator = "═" * 80
        print(f"\n{separator}")

        if self.config.language == "zh":
            print(
                f"\n📚 【ManageBac作业检查报告】 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(separator)

            # Overview statistics
            print(f"\n📈 【概览统计】")
            print(f"   📋 待办作业总数: {analysis['total_assignments']} 个")
            print(f"   😨 紧急作业: {analysis['urgent_count']} 个")
            print(f"   📚 涉及课程: {len(analysis['by_course'])} 个")

            # Priority distribution
            print(f"\n   优先级分布:")
            print(f"     🔴 高优先级: {analysis['by_priority']['high']} 个")
            print(f"     🟡 中优先级: {analysis['by_priority']['medium']} 个")
            print(f"     🟢 低优先级: {analysis['by_priority']['low']} 个")
        else:
            print(
                f"\n📚 【ManageBac Assignment Report】 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(separator)

            # Overview statistics
            print(f"\n📈 【Overview Statistics】")
            print(f"   📋 Total assignments: {analysis['total_assignments']}")
            print(f"   😨 Urgent assignments: {analysis['urgent_count']}")
            print(f"   📚 Courses involved: {len(analysis['by_course'])}")

            # Priority distribution
            print(f"\n   Priority distribution:")
            print(f"     🔴 High priority: {analysis['by_priority']['high']}")
            print(f"     🟡 Medium priority: {analysis['by_priority']['medium']}")
            print(f"     🟢 Low priority: {analysis['by_priority']['low']}")

        if not assignments:
            if self.config.language == "zh":
                print(f"\n✅ 【好消息】 未找到未提交的作业！")
                print("\n这可能意味着：")
                print("• 所有作业都已提交 ✅")
                print("• 页面结构发生了变化，需要更新脚本")
                print("• 需要手动导航到正确的作业页面")
            else:
                print(f"\n✅ 【Good News】 No unsubmitted assignments found!")
                print("\nThis might mean:")
                print("• All assignments have been submitted ✅")
                print("• Page structure has changed, script needs updating")
                print("• Manual navigation to correct assignment page needed")
            return

        # Urgent assignments
        urgent_assignments = analysis["assignments_by_urgency"]["urgent"]
        if urgent_assignments:
            urgent_title = (
                "🔥 【紧急作业 - 需要立即关注！】"
                if self.config.language == "zh"
                else "🔥 【Urgent Assignments - Immediate Attention Required!】"
            )
            print(f"\n{urgent_title}")
            for i, assignment in enumerate(urgent_assignments[:5], 1):
                print(f"   {i}. 🔥 {assignment['title'][:60]}")
                due_status = (
                    f"截止: {assignment['due_date']} | 状态: {assignment['status']}"
                    if self.config.language == "zh"
                    else f"Due: {assignment['due_date']} | Status: {assignment['status']}"
                )
                print(f"      ⏰ {due_status}")

        # Course statistics
        if analysis["by_course"]:
            course_title = (
                "📚 【课程分布】"
                if self.config.language == "zh"
                else "📚 【Course Distribution】"
            )
            print(f"\n{course_title}")
            for course, count in sorted(
                analysis["by_course"].items(), key=lambda x: x[1], reverse=True
            ):
                count_text = (
                    f"{count} 个作业"
                    if self.config.language == "zh"
                    else f"{count} assignments"
                )
                print(f"   • {course}: {count_text}")

        # All assignments list
        all_title = (
            "📋 【所有作业详情】"
            if self.config.language == "zh"
            else "📋 【All Assignment Details】"
        )
        print(f"\n{all_title}")

        for i, assignment in enumerate(assignments, 1):
            priority = self.analyzer._calculate_priority(assignment)
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[priority]
            urgency = self.analyzer._calculate_urgency(assignment, datetime.now())
            urgency_emoji = {"urgent": "🔥", "soon": "⚠️", "later": "🟢"}[urgency]

            print(f"\n   {i}. {urgency_emoji} {assignment['title'][:80]}")

            due_text = (
                f"截止: {assignment['due_date']}"
                if self.config.language == "zh"
                else f"Due: {assignment['due_date']}"
            )
            print(f"      ⏰ {due_text}")

            if self.config.language == "zh":
                priority_text = f"{priority.upper()}优先级"
                status_text = (
                    f"状态: {assignment['status']} | {priority_emoji} {priority_text}"
                )
            else:
                priority_text = f"{priority.upper()} priority"
                status_text = (
                    f"Status: {assignment['status']} | {priority_emoji} {priority_text}"
                )
            print(f"      📊 {status_text}")

            if self.config.debug and "selector_used" in assignment:
                debug_text = (
                    f"检测方式: {assignment['selector_used']}"
                    if self.config.language == "zh"
                    else f"Detection method: {assignment['selector_used']}"
                )
                print(f"      🔧 {debug_text}")

        # Important reminders
        if self.config.language == "zh":
            print(f"\n⚠️  【重要提醒】")
            print("   • 请及时登录ManageBac网站确认作业状态")
            print("   • 以上结果可能包含已提交但系统未更新的作业")
            print("   • 建议优先处理紧急和高优先级的作业")
        else:
            print(f"\n⚠️  【Important Reminders】")
            print("   • Please login to ManageBac website to confirm assignment status")
            print(
                "   • Results may include submitted assignments not yet updated in system"
            )
            print("   • Recommend prioritizing urgent and high-priority assignments")

    def _display_summary(
        self,
        assignments: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        saved_files: Dict[str, str],
    ) -> None:
        """Display summary information."""
        if self.config.language == "zh":
            print(f"\n\n📁 【报告文件生成】")
            if saved_files:
                for format_type, filepath in saved_files.items():
                    print(f"   • {format_type.upper()}报告: {filepath}")

                    if format_type == "html":
                        print(f"     ↳ 浏览器打开: open '{filepath}'")
                    elif format_type in ["json", "markdown"]:
                        print(f"     ↳ 查看内容: cat '{filepath}'")
            else:
                print("   没有生成额外的报告文件")

            print(f"\n🔄 【后续操作建议】")
            if assignments:
                if analysis["urgent_count"] > 0:
                    print(f"   😨 优先处理 {analysis['urgent_count']} 个紧急作业")
                print("   ⏰ 建议每日运行此脚本检查更新")
                print("   📚 访问 ManageBac 网站完成作业提交")
            else:
                print("   🎉 太棒了！没有待办作业")
                print("   ⏰ 建议明天再次检查")
        else:
            print(f"\n\n📁 【Report Files Generated】")
            if saved_files:
                for format_type, filepath in saved_files.items():
                    print(f"   • {format_type.upper()} report: {filepath}")

                    if format_type == "html":
                        print(f"     ↳ Open in browser: open '{filepath}'")
                    elif format_type in ["json", "markdown"]:
                        print(f"     ↳ View content: cat '{filepath}'")
            else:
                print("   No additional report files generated")

            print(f"\n🔄 【Next Steps Recommended】")
            if assignments:
                if analysis["urgent_count"] > 0:
                    print(
                        f"   😨 Prioritize {analysis['urgent_count']} urgent assignments"
                    )
                print("   ⏰ Recommend running this script daily for updates")
                print("   📚 Visit ManageBac website to complete assignments")
            else:
                print("   🎉 Great! No pending assignments")
                print("   ⏰ Recommend checking again tomorrow")

        print(f"\n⏱️  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═" * 80)

        if self.config.language == "zh":
            print("🚀 ManageBac Assignment Checker - 让作业管理更简单！")
        else:
            print(
                "🚀 ManageBac Assignment Checker - Making assignment management easier!"
            )
        print("═" * 80)
