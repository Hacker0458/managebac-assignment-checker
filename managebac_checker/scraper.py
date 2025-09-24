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
        "a.assignment-title",
        "a.title",
        "h3",
        "h4",
        "h5",
        "strong",
    ]

    _COURSE_SELECTORS = [
        "span.course",
        "div.course",
        "span.subject",
        "div.subject",
    ]

    _DUE_SELECTORS = [
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
        await page.goto(self.config.url, wait_until="domcontentloaded", timeout=self.config.timeout)
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
            self.logger.warning("Could not locate login button, submitting form with Enter key")
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
                await page.wait_for_load_state("domcontentloaded", timeout=self.config.timeout)
                await page.wait_for_timeout(1_000)
                if any(keyword in page.url for keyword in ("tasks", "assignment", "homework")):
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
                await page.goto(target, wait_until="domcontentloaded", timeout=self.config.timeout)
                await page.wait_for_timeout(1_000)
                if any(keyword in page.url for keyword in ("tasks", "assignment", "homework")):
                    return
            except Exception as exc:
                self.logger.debug("Fallback navigation to %s failed: %s", target, exc)

        self.logger.warning(
            "Unable to confirm assignment page navigation; continuing with current page"
        )

    async def collect_assignments(self, page: Page) -> List[Assignment]:
        assignments: List[Assignment] = []
        seen_ids: set[str] = set()

        for selector in self._ASSIGNMENT_CONTAINER_SELECTORS:
            try:
                handles = await page.query_selector_all(selector)
            except Exception:
                handles = []
            if not handles:
                continue

            self.logger.debug("Selector %s yielded %d elements", selector, len(handles))
            for handle in handles:
                assignment = await self._extract_assignment(handle)
                if not assignment:
                    continue
                if assignment.identifier in seen_ids:
                    continue
                seen_ids.add(assignment.identifier)
                assignments.append(assignment)

            if assignments:
                break

        if not assignments:
            self.logger.info("Falling back to text-based scan")
            assignments = await self._text_fallback(page)

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
        status = await self._first_text(handle, self._STATUS_SELECTORS) or self._infer_status(
            raw_text
        )
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

    async def _text_fallback(self, page: Page) -> List[Assignment]:
        content = await page.inner_text("body")
        blocks = [line.strip() for line in content.splitlines() if len(line.strip()) > 10]
        assignments: List[Assignment] = []
        for block in blocks[:20]:
            if not any(token in block.lower() for token in ("due", "截止", "submit", "提交")):
                continue
            identifier = block[:40].lower()
            # Try to extract date from text
            due_date = "无截止日期"
            import re

            date_patterns = [
                r"(\d{4}-\d{2}-\d{2})",  # YYYY-MM-DD
                r"(\d{2}/\d{2}/\d{4})",  # MM/DD/YYYY
                r"(\d{2}-\d{2}-\d{4})",  # MM-DD-YYYY
                r"(\d{1,2}/\d{1,2}/\d{2,4})",  # M/D/YY or MM/DD/YYYY
            ]

            for pattern in date_patterns:
                match = re.search(pattern, block)
                if match:
                    due_date = match.group(1)
                    break

            # Try to extract course name
            course = "未知课程"
            course_patterns = [
                r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",  # Course names
                r"(数学|物理|化学|生物|英语|语文|历史|地理|政治)",  # Chinese subjects
                r"(Math|Physics|Chemistry|Biology|English|History|Geography)",  # English subjects
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
                await _enrich_details(scraper, page, assignments, limit=config.details_limit)
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
                assignment.link, wait_until="domcontentloaded", timeout=scraper.config.timeout
            )
            await page.wait_for_timeout(600)
            description = await page.inner_text("main", timeout=2_000)
            assignment.description = description.strip()
            enriched += 1
        except Exception as exc:
            scraper.logger.debug("Failed to enrich %s: %s", assignment.title, exc)
