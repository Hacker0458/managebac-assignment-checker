"""基于 Playwright 的 ManageBac 作业抓取器。"""

from __future__ import annotations

import logging
from typing import Iterable, List, Optional, Tuple

from playwright.async_api import Browser, Page

from .config import Config
from .models import Assignment


class ManageBacScraper:
    """封装登录、导航及作业信息提取的逻辑。"""

    _ASSIGNMENT_CONTAINER_SELECTORS = [
        # 基于真实DOM分析的精确选择器（2025-10-26更新）
        "div.task-agenda",                    # ManageBac 任务区域容器
        "div.line.task-node",                 # ManageBac 任务节点行
        "[class*='assignment']",               # 包含assignment的所有类名（10个元素）
        "div.task-node",                      # 任务节点简化选择器
        
        # 回退选择器（兼容旧版本或不同学校的ManageBac）
        "div.assignment",
        "div.assignment-card",
        "div.task-item",
        "li.assignment",
        "li.assignment-item",
        "tr.assignment",
        "tr.task",
        "div[data-assignment-id]",
    ]

    _TITLE_SELECTORS = [
        # 基于真实DOM分析（2025-10-26更新）
        ".details h4.title a",                # ManageBac 标题链接
        "h4.title a",                         # 标题简化选择器
        ".title a",                           # 更通用的标题
        
        # 回退选择器
        "a.assignment-title",
        "a.title",
        "h3",
        "h4",
        "h5",
        "strong",
    ]

    _COURSE_SELECTORS = [
        # 基于真实DOM分析（2025-10-26更新）
        ".details .label-and-due",            # 包含标签和截止日期的区域
        ".class-info",                        # 课程信息区域
        
        # 回退选择器
        "span.course",
        "div.course",
        "span.subject",
        "div.subject",
    ]

    _DUE_SELECTORS = [
        # 基于真实DOM分析（2025-10-26更新）
        ".label-and-due .due",                # ManageBac 截止日期
        ".date-badge",                        # 日期徽章
        
        # 回退选择器
        "span.due",
        "span.due-date",
        "td.due",
        "div.due-date",
        "time",
    ]

    _STATUS_SELECTORS = [
        "span.status",
        "span.badge",
        "div.status",
    ]

    def __init__(self, config: Config, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

    async def login(self, page: Page) -> bool:
        self.logger.info("Navigating to %s", self.config.url)
        await page.goto(
            self.config.url, wait_until="domcontentloaded", timeout=self.config.timeout
        )
        await page.wait_for_timeout(500)

        email_selector = "input[type=email], input[name=email]"
        password_selector = "input[type=password], input[name=password]"
        await page.fill(email_selector, self.config.email)
        await page.fill(password_selector, self.config.password)

        login_buttons = [
            "button[type=submit]",
            "input[type=submit]",
            "button:has-text('Login')",
            "button:has-text('Sign in')",
        ]
        for selector in login_buttons:
            try:
                await page.click(selector, timeout=1_500)
                break
            except Exception:
                continue
        else:
            self.logger.warning(
                "Could not locate login button, submitting form with Enter key"
            )
            await page.press(password_selector, "Enter")

        try:
            await page.wait_for_load_state("networkidle", timeout=self.config.timeout)
        except Exception:
            self.logger.debug("networkidle wait timed out; continuing")

        current_url = page.url.lower()
        if "login" in current_url or "signin" in current_url:
            self.logger.error("Login appears to have failed (%s)", current_url)
            return False

        self.logger.info("Login successful")
        return True

    async def navigate_to_assignments(self, page: Page) -> None:
        """
        导航到作业页面
        
        重要：ManageBac的作业页面包含多个section（Upcoming, Overdue, Completed）
        我们需要确保所有section的内容都被加载
        """
        candidates = [
            ("a:has-text('Tasks & Deadlines')", "Tasks & Deadlines"),
            ("a:has-text('Assignments')", "Assignments"),
            ("a:has-text('Tasks')", "Tasks"),
            ("a:has-text('作业')", "作业"),
            ("a[href*='tasks']", "href tasks"),
            ("a[href*='assignments']", "href assignments"),
        ]
        for selector, label in candidates:
            try:
                link = await page.query_selector(selector)
                if not link:
                    continue
                self.logger.debug("Clicking navigation link: %s (%s)", label, selector)
                await link.click()
                await page.wait_for_load_state(
                    "domcontentloaded", timeout=self.config.timeout
                )
                await page.wait_for_timeout(1_000)
                if any(
                    keyword in page.url
                    for keyword in ("tasks", "assignment", "homework")
                ):
                    # 成功到达作业页面，现在尝试展开所有section
                    await self._expand_all_sections(page)
                    return
            except Exception as exc:
                self.logger.debug("Navigation via %s failed: %s", selector, exc)

        base = self.config.url.rstrip("/")
        fallback_paths = [
            "/student/tasks_and_deadlines",
            "/student/assignments",
            "/assignments",
            "/tasks",
        ]
        for path in fallback_paths:
            target = base + path
            self.logger.debug("Trying fallback navigation to %s", target)
            try:
                await page.goto(
                    target, wait_until="domcontentloaded", timeout=self.config.timeout
                )
                await page.wait_for_timeout(1_000)
                if any(
                    keyword in page.url
                    for keyword in ("tasks", "assignment", "homework")
                ):
                    await self._expand_all_sections(page)
                    return
            except Exception as exc:
                self.logger.debug("Fallback navigation to %s failed: %s", target, exc)

        self.logger.warning(
            "Unable to confirm assignment page navigation; continuing with current page"
        )
        # 即使导航失败，也尝试展开sections
        await self._expand_all_sections(page)

    async def _expand_all_sections(self, page: Page) -> None:
        """
        展开所有作业section（Upcoming, Overdue, Completed等）
        
        ManageBac可能使用折叠的sections来组织作业，我们需要点击展开它们
        """
        self.logger.info("尝试展开所有作业sections...")
        
        # 尝试点击各种可能的展开按钮/标签
        expand_selectors = [
            "a:has-text('Overdue')",           # Overdue tab/link
            "button:has-text('Overdue')",      # Overdue button
            "[data-section='overdue']",        # Overdue section
            ".section-toggle",                  # Generic section toggle
            ".expand-button",                   # Expand button
            "a:has-text('Show all')",          # Show all link
            "button:has-text('Show all')",     # Show all button
        ]
        
        for selector in expand_selectors:
            try:
                elements = await page.query_selector_all(selector)
                for element in elements:
                    try:
                        await element.click(timeout=1000)
                        await page.wait_for_timeout(500)
                        self.logger.debug("Clicked expand element: %s", selector)
                    except Exception:
                        pass
            except Exception:
                pass
        
        # 滚动页面以触发lazy loading
        try:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(500)
            self.logger.debug("Scrolled page to trigger lazy loading")
        except Exception as e:
            self.logger.debug("Failed to scroll page: %s", e)
        
        self.logger.info("完成section展开尝试")

    async def collect_assignments(self, page: Page) -> List[Assignment]:
        """
        收集页面上的所有作业
        
        重要改进：不再在找到第一个匹配的selector后就停止，而是尝试所有selector
        并收集所有唯一的作业，确保不会遗漏任何作业。
        """
        assignments: List[Assignment] = []
        seen_ids: set[str] = set()

        # 尝试所有selector，收集所有可能的作业元素（不要提前break）
        for selector in self._ASSIGNMENT_CONTAINER_SELECTORS:
            try:
                handles = await page.query_selector_all(selector)
            except Exception as e:
                self.logger.debug("Selector %s query failed: %s", selector, e)
                handles = []
            
            if not handles:
                self.logger.debug("Selector %s yielded 0 elements", selector)
                continue

            self.logger.info("✅ Selector '%s' found %d elements", selector, len(handles))
            
            for handle in handles:
                assignment = await self._extract_assignment(handle)
                if not assignment:
                    continue
                
                # 使用唯一标识符去重
                if assignment.identifier in seen_ids:
                    self.logger.debug("Skipping duplicate assignment: %s", assignment.title)
                    continue
                
                seen_ids.add(assignment.identifier)
                assignments.append(assignment)
                self.logger.debug("Collected assignment: %s (course: %s, due: %s)", 
                                assignment.title, assignment.course, assignment.due_date)

        # 如果所有selector都没有找到作业，尝试fallback方法
        if not assignments:
            self.logger.warning("⚠️ No assignments found with selectors, trying fallback method")
            assignments = await self._text_fallback(page)
        else:
            self.logger.info("📚 Total unique assignments collected: %d", len(assignments))

        # 应用配置的过滤规则
        assignments = self._filter_assignments(assignments)
        self.logger.info("📋 After filtering: %d assignments remaining", len(assignments))

        # 按截止日期和标题排序
        assignments.sort(key=lambda a: (a.due_date or "", a.title))
        return assignments

    async def _extract_assignment(self, handle) -> Optional[Assignment]:
        try:
            raw_text = (await handle.inner_text()).strip()
        except Exception:
            return None
        if len(raw_text) < 5:
            return None

        title = await self._first_text(handle, self._TITLE_SELECTORS)
        if not title:
            title = raw_text.splitlines()[0].strip()

        course = await self._first_text(handle, self._COURSE_SELECTORS) or "未知课程"
        due_date = await self._first_text(handle, self._DUE_SELECTORS) or "无截止日期"
        status = await self._first_text(
            handle, self._STATUS_SELECTORS
        ) or self._infer_status(raw_text)
        assignment_type = self._infer_type(raw_text)
        submitted, overdue = self._classify_state(status, raw_text)
        link = await self._first_attr(handle, "a", "href")
        identifier = f"{title.lower()}::{due_date.lower()}"
        priority = self._priority_from_text(title, raw_text)

        return Assignment(
            identifier=identifier,
            title=title.strip(),
            course=course.strip(),
            status=status.strip(),
            due_date=due_date.strip(),
            assignment_type=assignment_type,
            priority=priority,
            submitted=submitted,
            overdue=overdue,
            link=link,
            raw_text=raw_text,
        )

    async def _first_text(self, handle, selectors: Iterable[str]) -> Optional[str]:
        for selector in selectors:
            try:
                element = await handle.query_selector(selector)
            except Exception:
                element = None
            if element:
                try:
                    text = await element.text_content()
                except Exception:
                    text = None
                if text and text.strip():
                    return text.strip()
        return None

    async def _first_attr(self, handle, selector: str, attr: str) -> Optional[str]:
        try:
            element = await handle.query_selector(selector)
        except Exception:
            return None
        if not element:
            return None
        try:
            value = await element.get_attribute(attr)
        except Exception:
            return None
        return value

    def _infer_status(self, raw_text: str) -> str:
        lowered = raw_text.lower()
        if any(token in lowered for token in ("submitted", "turned in", "已提交")):
            return "Submitted"
        if any(token in lowered for token in ("overdue", "late", "逾期")):
            return "Overdue"
        if any(token in lowered for token in ("pending", "未提交", "待")):
            return "Pending"
        return "Unknown"

    def _classify_state(self, status: str, raw_text: str) -> Tuple[bool, bool]:
        text = f"{status} {raw_text}".lower()
        submitted = any(token in text for token in ("submitted", "turned in", "已提交"))
        overdue = any(token in text for token in ("overdue", "late", "逾期"))
        return submitted, overdue

    def _infer_type(self, raw_text: str) -> str:
        lowered = raw_text.lower()
        if "summative" in lowered or "总结" in lowered:
            return "Summative"
        if "formative" in lowered or "形成" in lowered:
            return "Formative"
        if "essay" in lowered:
            return "Essay"
        return "Unknown"

    def _priority_from_text(self, title: str, raw_text: str) -> str:
        text = f"{title} {raw_text}".lower()
        for keyword in self.config.priority_keywords:
            if keyword.lower() in text:
                return "high"
        if any(token in text for token in ("quiz", "assignment", "homework")):
            return "medium"
        return "low"

    def _filter_assignments(self, assignments: List[Assignment]) -> List[Assignment]:
        """
        根据配置过滤作业列表
        
        Args:
            assignments: 原始作业列表
            
        Returns:
            过滤后的作业列表
        """
        if not assignments:
            return assignments
        
        filtered = []
        stats = {
            'submitted': 0,
            'overdue': 0,
            'upcoming': 0,
            'filtered_out': 0
        }
        
        for assignment in assignments:
            # 根据submitted状态过滤
            if assignment.submitted:
                stats['submitted'] += 1
                if not self.config.include_submitted:
                    stats['filtered_out'] += 1
                    self.logger.debug("Filtered out (submitted): %s", assignment.title)
                    continue
            
            # 根据overdue状态过滤
            if assignment.overdue:
                stats['overdue'] += 1
                if not self.config.include_overdue:
                    stats['filtered_out'] += 1
                    self.logger.debug("Filtered out (overdue): %s", assignment.title)
                    continue
            
            # 未提交且未过期的作业视为upcoming
            if not assignment.submitted and not assignment.overdue:
                stats['upcoming'] += 1
                if not self.config.include_upcoming:
                    stats['filtered_out'] += 1
                    self.logger.debug("Filtered out (upcoming): %s", assignment.title)
                    continue
            
            filtered.append(assignment)
        
        # 记录过滤统计
        self.logger.info(
            "Filter stats - Submitted: %d, Overdue: %d, Upcoming: %d, Filtered out: %d",
            stats['submitted'], stats['overdue'], stats['upcoming'], stats['filtered_out']
        )
        
        return filtered

    async def _text_fallback(self, page: Page) -> List[Assignment]:
        """
        文本回退方法：当CSS选择器无法找到作业时的备用方案
        
        重要改进：移除了原来的blocks[:20]限制，现在会处理所有可能的作业文本
        """
        content = await page.inner_text("body")
        blocks = [
            line.strip() for line in content.splitlines() if len(line.strip()) > 10
        ]
        
        self.logger.info("Text fallback: analyzing %d text blocks", len(blocks))
        
        assignments: List[Assignment] = []
        seen_identifiers: set[str] = set()
        
        # 移除了[:20]限制，处理所有可能包含作业信息的文本块
        for block in blocks:
            if not any(
                token in block.lower() for token in ("due", "截止", "submit", "提交", "assignment", "homework", "作业")
            ):
                continue
            
            # 使用更长的标识符以提高唯一性
            identifier = block[:60].lower()
            
            # 避免重复
            if identifier in seen_identifiers:
                continue
            seen_identifiers.add(identifier)
            
            # Try to extract date from text
            due_date = "无截止日期"
            import re

            date_patterns = [
                r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
                r"(\d{2}/\d{2}/\d{4})",  # MM/DD/YYYY
                r"(\d{2}-\d{2}-\d{4})",  # MM-DD-YYYY
                r"(\d{1,2}/\d{1,2}/\d{2,4})",  # M/D/YY or MM/DD/YYYY
                r"([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})",  # Oct 26, 2025
            ]

            for pattern in date_patterns:
                match = re.search(pattern, block)
                if match:
                    due_date = match.group(1)
                    break

            # Try to extract course name
            course = "未知课程"
            course_patterns = [
                r"AP\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",  # AP courses
                r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",  # Course names
                r"(数学|物理|化学|生物|英语|语文|历史|地理|政治)",  # Chinese subjects
                r"(Math|Physics|Chemistry|Biology|English|History|Geography|Computer Science|Calculus|Macroeconomics)",  # English subjects
            ]

            for pattern in course_patterns:
                match = re.search(pattern, block)
                if match:
                    course = match.group(1)
                    break

            assignments.append(
                Assignment(
                    identifier=identifier,
                    title=block[:80],
                    course=course,
                    status="Pending",
                    due_date=due_date,
                    raw_text=block,
                    assignment_type="Unknown",
                    priority=self._priority_from_text(block, block),
                )
            )
        
        self.logger.info("Text fallback collected %d potential assignments", len(assignments))
        return assignments


async def run_scraper(config: Config, logger: logging.Logger) -> List[Assignment]:
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(
            headless=config.headless, args=config.browser_args
        )
        page: Page = await browser.new_page()
        page.set_default_timeout(config.timeout)

        scraper = ManageBacScraper(config, logger)
        try:
            if not await scraper.login(page):
                return []
            await scraper.navigate_to_assignments(page)
            await page.wait_for_timeout(1_500)
            assignments = await scraper.collect_assignments(page)
            if config.fetch_details and assignments:
                await _enrich_details(
                    scraper, page, assignments, limit=config.details_limit
                )
            return assignments
        finally:
            await browser.close()


async def _enrich_details(
    scraper: ManageBacScraper, page: Page, assignments: List[Assignment], *, limit: int
) -> None:
    enriched = 0
    for assignment in assignments:
        if enriched >= limit or not assignment.link:
            continue
        try:
            await page.goto(
                assignment.link,
                wait_until="domcontentloaded",
                timeout=scraper.config.timeout,
            )
            await page.wait_for_timeout(600)
            description = await page.inner_text("main", timeout=2_000)
            assignment.description = description.strip()
            enriched += 1
        except Exception as exc:
            scraper.logger.debug("Failed to enrich %s: %s", assignment.title, exc)
