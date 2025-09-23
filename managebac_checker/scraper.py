"""
🎓 ManageBac Assignment Checker Scraper | ManageBac作业检查器爬虫模块
======================================================================

Web scraping functionality for ManageBac Assignment Checker.
ManageBac作业检查器的网页抓取功能模块。
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from playwright.async_api import Page, Browser

from .logging_utils import BilingualLogger


class ManageBacScraper:
    """
    Handles web scraping operations for ManageBac.
    处理ManageBac的网页抓取操作。
    """

    def __init__(self, config, logger: Optional[BilingualLogger] = None):
        """
        Initialize scraper with configuration.
        使用配置初始化爬虫。

        Args:
            config: Configuration instance
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        self.timeout = getattr(config, "timeout", 30000)
        self.debug = config.debug

    async def login(self, page: Page) -> bool:
        """
        Log into ManageBac with provided credentials.
        使用提供的凭据登录ManageBac。

        Args:
            page: The Playwright page instance

        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            nav_msg = (
                f"导航到 {self.config.url}..."
                if self.config.language == "zh"
                else f"Navigating to {self.config.url}..."
            )
            if self.logger:
                self.logger.debug(nav_msg)
            else:
                print(nav_msg)

            await page.goto(self.config.url, wait_until="domcontentloaded")

            # Wait for login form to load
            wait_msg = (
                "等待登录表单加载..."
                if self.config.language == "zh"
                else "Waiting for login form..."
            )
            if self.logger:
                self.logger.debug(wait_msg)
            else:
                print(wait_msg)

            await page.wait_for_selector(
                'input[type="email"], input[name="email"]', timeout=self.timeout
            )

            # Fill in email
            email_selector = 'input[type="email"], input[name="email"]'
            await page.fill(email_selector, self.config.email)

            email_msg = (
                f"已填入邮箱: {self.config.email}"
                if self.config.language == "zh"
                else f"Filled email: {self.config.email}"
            )
            if self.logger:
                self.logger.debug(email_msg)
            else:
                print(email_msg)

            # Fill in password
            password_selector = 'input[type="password"], input[name="password"]'
            await page.fill(password_selector, self.config.password)

            pwd_msg = (
                "已填入密码" if self.config.language == "zh" else "Filled password"
            )
            if self.logger:
                self.logger.debug(pwd_msg)
            else:
                print(pwd_msg)

            # Click login button
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
                ".btn-primary",
            ]

            login_clicked = False
            for selector in login_button_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    print(f"Clicked login button with selector: {selector}")
                    login_clicked = True
                    break
                except:
                    continue

            if not login_clicked:
                print("Warning: Could not find login button, trying form submission...")
                await page.press(password_selector, "Enter")

            # Wait for navigation or error message
            print("Waiting for login to complete...")

            try:
                # Wait for either successful navigation or error message
                await page.wait_for_load_state("domcontentloaded", timeout=self.timeout)

                # Check if we're still on login page (login failed)
                current_url = page.url
                if "login" in current_url.lower() or "signin" in current_url.lower():
                    # Look for error messages
                    error_elements = await page.query_selector_all(
                        '.error, .alert-danger, [class*="error"]'
                    )
                    if error_elements:
                        error_text = await error_elements[0].text_content()
                        print(f"Login failed: {error_text}")
                        return False
                    else:
                        print("Login may have failed (still on login page)")
                        return False

                print(f"Login successful! Current URL: {current_url}")
                return True

            except Exception as e:
                print(f"Error during login: {e}")
                return False

        except Exception as e:
            print(f"Error during login process: {e}")
            return False

    async def explore_page_structure(self, page: Page) -> None:
        """Explore current page structure for debugging."""
        try:
            print("\n=== 页面结构探索 ===")
            print(f"当前URL: {page.url}")

            # Get page title
            title = await page.title()
            print(f"页面标题: {title}")

            # Find possible navigation links
            nav_selectors = [
                "nav a",
                ".nav a",
                ".navbar a",
                ".menu a",
                '[href*="assignment"]',
                '[href*="homework"]',
                '[href*="task"]',
                '[href*="student"]',
                '[href*="dashboard"]',
                '[href*="class"]',
            ]

            print("\n找到的导航链接:")
            for selector in nav_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements[:10]:  # Limit to first 10
                        href = await element.get_attribute("href")
                        text = await element.text_content()
                        if href and text and text.strip():
                            print(f"  - {text.strip()}: {href}")
                except:
                    continue

            # Find possible content areas
            content_selectors = [
                ".content",
                ".main-content",
                ".dashboard",
                ".student-dashboard",
                ".assignments",
                ".homework",
                ".tasks",
                ".todo",
                ".pending",
            ]

            print("\n找到的内容区域:")
            for selector in content_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"  - {selector}: {len(elements)} 个元素")
                except:
                    continue

        except Exception as e:
            print(f"页面结构探索出错: {e}")

    async def navigate_to_assignments(self, page: Page) -> bool:
        """Navigate to assignments page."""
        try:
            print("\n=== 尝试导航到作业页面 ===")

            # Look for assignment-related links
            assignment_link_selectors = [
                'a[href*="tasks_and_deadlines"]',
                'a:has-text("Tasks & Deadlines")',
                'a:has-text("Deadlines")',
                'a[href*="assignment"]',
                'a[href*="homework"]',
                'a[href*="task"]',
                'a:has-text("Assignment")',
                'a:has-text("Homework")',
                'a:has-text("Tasks")',
                'a:has-text("作业")',
                'a:has-text("待办")',
                '.nav a:has-text("Assignment")',
                '.menu a:has-text("Assignment")',
            ]

            for selector in assignment_link_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        href = await element.get_attribute("href")
                        text = (await element.text_content() or "").strip()
                        print(f"找到作业链接: {text}\n -> {href}")
                        await element.click()
                        print(f"点击了作业链接: {text}")
                        await page.wait_for_load_state("domcontentloaded")
                        await page.wait_for_timeout(1500)
                        break
                except Exception as e:
                    if self.debug:
                        print(f"尝试选择器 {selector} 失败: {e}")
                    continue

            # If still not on task page, try direct access
            current_url = page.url
            if not any(
                key in current_url for key in ["tasks", "assignment", "homework"]
            ):
                print("未找到明确的作业链接，尝试其他导航方式...")
                assignment_paths = [
                    "/student/tasks_and_deadlines",
                    "/assignments",
                    "/student/assignments",
                    "/homework",
                    "/tasks",
                    "/dashboard/assignments",
                    "/student/dashboard/assignments",
                ]
                base_url = self.config.url.rstrip("/")
                for path in assignment_paths:
                    try:
                        assignment_url = base_url + path
                        print(f"尝试直接访问: {assignment_url}")
                        await page.goto(assignment_url, wait_until="domcontentloaded")
                        await page.wait_for_timeout(1500)
                        break
                    except Exception as e:
                        if self.debug:
                            print(f"访问 {assignment_url} 失败: {e}")
                        continue

            # Switch to "All" filter
            await self._switch_to_all_filter(page)

            print(f"导航后的URL: {page.url}")
            return True
        except Exception as e:
            print(f"导航到作业页面时出错: {e}")
            return False

    async def _switch_to_all_filter(self, page: Page) -> None:
        """Switch to 'All' filter to show all tasks."""
        try:
            filter_selectors = [
                'a:has-text("All")',
                'button:has-text("All")',
                'a:has-text("全部")',
                'button:has-text("全部")',
                'a[href$="/tasks_and_deadlines"]',
            ]
            for selector in filter_selectors:
                try:
                    el = await page.query_selector(selector)
                    if el:
                        await el.click()
                        await page.wait_for_timeout(800)
                        break
                except:
                    continue
        except Exception as e:
            if self.debug:
                print(f"切换到全部视图失败: {e}")

    async def get_all_assignments(
        self, page: Page, browser: Optional[Browser] = None
    ) -> List[Dict[str, Any]]:
        """Scrape all assignments including submitted and unsubmitted."""
        assignments: List[Dict[str, Any]] = []

        try:
            print("\n=== 抓取全部作业（包含已提交/未提交）===")
            print(f"当前页面: {page.url}")

            # Comprehensive selector collection
            item_selectors = [
                ".assignment",
                ".assignment-item",
                ".task-item",
                ".homework-item",
                'li[class*="assignment"]',
                ".assignment-list li",
                ".homework-list li",
                'tr[class*="assignment"], tr[class*="task"], tr[class*="homework"]',
                '.card:has([class*="due"])',
                'div:has([class*="due"]), div:has([class*="status"])',
            ]

            status_keywords = {
                "submitted": ["submitted", "已提交", "turned in", "已上交"],
                "pending": [
                    "pending",
                    "not submitted",
                    "unsubmitted",
                    "未提交",
                    "待提交",
                    "未上交",
                ],
                "overdue": ["overdue", "逾期", "迟交", "late"],
            }

            type_keywords = {
                "summative": ["summative", "总结性"],
                "formative": ["formative", "形成性"],
            }

            found_elements = []
            for sel in item_selectors:
                try:
                    els = await page.query_selector_all(sel)
                    if els and len(els) > len(found_elements):
                        found_elements = els
                except:
                    continue

            if not found_elements:
                print("未找到结构化列表，回退到基于due类选择：")
                found_elements = await page.query_selector_all(
                    '[class*="due"], [class*="status"]'
                )

            print(f"找到潜在任务元素: {len(found_elements)}")

            # Process each element
            for idx, el in enumerate(found_elements):
                try:
                    text = (await el.text_content() or "").strip()
                    if not text or len(text) < 6:
                        continue
                    low = text.lower()

                    # Extract title
                    title = None
                    for tsel in [
                        ".title",
                        ".assignment-title",
                        ".homework-title",
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "a",
                    ]:
                        try:
                            tnode = await el.query_selector(tsel)
                            if tnode:
                                ttext = (await tnode.text_content() or "").strip()
                                if ttext and len(ttext) > 2:
                                    title = ttext
                                    break
                        except:
                            continue
                    if not title:
                        title = text[:100]

                    # Extract due date
                    due_text = None
                    for dsel in [".due-date", '[class*="due"]', ".date", ".deadline"]:
                        try:
                            dnode = await el.query_selector(dsel)
                            if dnode:
                                dtext = (await dnode.text_content() or "").strip()
                                if dtext:
                                    due_text = dtext
                                    break
                        except:
                            continue
                    if not due_text:
                        m = re.search(
                            r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b[^\n]{0,40}",
                            text,
                            re.I,
                        )
                        if m:
                            due_text = m.group(0).strip()
                        else:
                            due_text = "无截止日期"

                    # Determine status
                    status = "未知"
                    submitted = False
                    overdue = False
                    for key, keys in status_keywords.items():
                        if any(k in low for k in keys):
                            if key == "submitted":
                                status = "Submitted"
                                submitted = True
                            elif key == "pending":
                                status = "Pending"
                            elif key == "overdue":
                                status = "Overdue"
                                overdue = True

                    # Determine type
                    a_type = "Unknown"
                    for tkey, tkeys in type_keywords.items():
                        if any(k in low for k in tkeys):
                            a_type = "Summative" if tkey == "summative" else "Formative"
                            break

                    # Extract course name
                    course = self._extract_course_name(text)

                    # Extract link
                    link = None
                    for lsel in [
                        'a[href*="core_tasks"]',
                        'a[href*="/tasks/"], a[href*="/assignment"]',
                        "a",
                    ]:
                        try:
                            lnode = await el.query_selector(lsel)
                            if lnode:
                                href = await lnode.get_attribute("href")
                                if href and not href.startswith("javascript"):
                                    link = href
                                    break
                        except:
                            continue

                    assignment = {
                        "title": title,
                        "course": course,
                        "type": a_type,
                        "due_date": due_text,
                        "status": status,
                        "submitted": submitted,
                        "overdue": overdue,
                        "link": link,
                        "selector_used": "auto",
                        "element_index": idx,
                        "full_text_preview": text[:300]
                        + ("..." if len(text) > 300 else ""),
                        "found_at": datetime.now().isoformat(),
                    }
                    assignments.append(assignment)
                except Exception as e:
                    if self.debug:
                        print(f"解析元素 {idx} 失败: {e}")
                    continue

            # Optional: fetch details
            if self.config.fetch_details and browser and assignments:
                await self._enrich_assignments_details(assignments, browser)

            # Remove duplicates
            if len(assignments) > 1:
                assignments = self._remove_duplicate_assignments(assignments)

            # Filter noise
            clean = []
            for a in assignments:
                if (
                    len(a.get("title", "").strip()) < 3
                    and a.get("status", "未知") == "未知"
                    and not a.get("course")
                ):
                    continue
                clean.append(a)
            assignments = clean

            print(f"完成抓取：{len(assignments)} 条")
            return assignments
        except Exception as e:
            print(f"抓取全部作业时出错: {e}")
            return assignments

    async def _enrich_assignments_details(
        self, assignments: List[Dict[str, Any]], browser: Browser
    ) -> None:
        """Open assignment detail pages to extract more fields."""
        try:
            count = 0
            for a in assignments:
                if count >= self.config.details_limit:
                    break
                link = a.get("link")
                if not link:
                    continue

                url = link
                if link.startswith("/"):
                    url = self.config.url.rstrip("/") + link

                page = await browser.new_page()
                try:
                    await page.goto(url, wait_until="domcontentloaded")
                    await page.wait_for_timeout(800)

                    desc = await self._safe_inner_text(
                        page,
                        [
                            ".description",
                            ".assignment-description",
                            ".content",
                            ".instructions",
                        ],
                    )
                    teacher = await self._safe_inner_text(
                        page, [".teacher", ".author", 'a[href*="/teachers/"]']
                    )
                    created = await self._safe_inner_text(
                        page, [".created-at", '[class*="created"]']
                    )
                    updated = await self._safe_inner_text(
                        page, [".updated-at", '[class*="updated"]']
                    )
                    attachments = await self._collect_links(
                        page, ['a[href*="/files/"], a:has-text("Download")']
                    )

                    a["details"] = {
                        "description": desc,
                        "teacher": teacher,
                        "created_at": created,
                        "updated_at": updated,
                        "attachments": attachments,
                    }
                    count += 1
                except Exception as e:
                    if self.debug:
                        print(f"详情抓取失败 {url}: {e}")
                finally:
                    await page.close()
        except Exception as e:
            if self.debug:
                print(f"批量详情抓取失败: {e}")

    async def _safe_inner_text(self, page: Page, selectors: List[str]) -> Optional[str]:
        """Safely get text content from selectors."""
        for sel in selectors:
            try:
                el = await page.query_selector(sel)
                if el:
                    t = await el.text_content()
                    if t and t.strip():
                        return t.strip()
            except:
                continue
        return None

    async def _collect_links(
        self, page: Page, selectors: List[str]
    ) -> List[Dict[str, str]]:
        """Collect links from selectors."""
        items = []
        for sel in selectors:
            try:
                els = await page.query_selector_all(sel)
                for el in els[:10]:
                    href = await el.get_attribute("href")
                    text = (await el.text_content() or "").strip()
                    if href and not href.startswith("javascript"):
                        items.append({"text": text, "href": href})
            except:
                continue
        return items

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

    def _remove_duplicate_assignments(
        self, assignments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove duplicate assignment entries."""
        seen_titles = set()
        unique_assignments = []

        for assignment in assignments:
            title_key = assignment["title"][:50].lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_assignments.append(assignment)

        if len(assignments) != len(unique_assignments):
            print(f"去重后：{len(assignments)} -> {len(unique_assignments)} 个作业")

        return unique_assignments
