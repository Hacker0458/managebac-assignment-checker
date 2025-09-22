#!/usr/bin/env python3
"""
ManageBac Assignment Checker

Automated tool to log into ManageBac and check for unsubmitted assignments.
"""

import os
import sys
import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from playwright.async_api import async_playwright, Page, Browser
from dotenv import load_dotenv


class ManageBacChecker:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.email = os.getenv('MANAGEBAC_EMAIL')
        self.password = os.getenv('MANAGEBAC_PASSWORD')
        self.url = os.getenv('MANAGEBAC_URL', 'https://shtcs.managebac.cn')
        self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', '30000'))
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        
        # 报告和通知配置
        self.report_format = os.getenv('REPORT_FORMAT', 'console,json').split(',')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', './reports'))
        self.enable_notifications = os.getenv('ENABLE_NOTIFICATIONS', 'false').lower() == 'true'
        
        # 邮件通知配置
        self.smtp_server = os.getenv('SMTP_SERVER', '')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL', '')
        
        # 过滤和分析配置
        self.days_ahead = int(os.getenv('DAYS_AHEAD', '7'))  # 查看未来N天的作业
        self.priority_keywords = os.getenv('PRIORITY_KEYWORDS', 'exam,test,project,essay').split(',')
        
        # 详情抓取配置
        self.fetch_details = os.getenv('FETCH_DETAILS', 'false').lower() == 'true'
        self.details_limit = int(os.getenv('DETAILS_LIMIT', '10'))
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate required environment variables
        if not self.email or not self.password:
            print("Error: MANAGEBAC_EMAIL and MANAGEBAC_PASSWORD must be set in .env file")
            sys.exit(1)
    
    async def login(self, page: Page) -> bool:
        """
        Log into ManageBac with provided credentials.
        
        Args:
            page: The Playwright page instance
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            print(f"Navigating to {self.url}...")
            await page.goto(self.url, wait_until="domcontentloaded")
            
            # Wait for login form to load
            print("Waiting for login form...")
            await page.wait_for_selector('input[type="email"], input[name="email"]', timeout=self.timeout)
            
            # Fill in email
            email_selector = 'input[type="email"], input[name="email"]'
            await page.fill(email_selector, self.email)
            print(f"Filled email: {self.email}")
            
            # Fill in password
            password_selector = 'input[type="password"], input[name="password"]'
            await page.fill(password_selector, self.password)
            print("Filled password")
            
            # Click login button
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
                '.btn-primary'
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
                await page.press(password_selector, 'Enter')
            
            # Wait for navigation or error message
            print("Waiting for login to complete...")
            
            try:
                # Wait for either successful navigation or error message
                await page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
                
                # Check if we're still on login page (login failed)
                current_url = page.url
                if 'login' in current_url.lower() or 'signin' in current_url.lower():
                    # Look for error messages
                    error_elements = await page.query_selector_all('.error, .alert-danger, [class*="error"]')
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
        """
        探索当前页面结构，用于调试和了解页面内容。
        """
        try:
            print("\n=== 页面结构探索 ===")
            print(f"当前URL: {page.url}")
            
            # 获取页面标题
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 查找可能的导航链接
            nav_selectors = [
                'nav a', '.nav a', '.navbar a', '.menu a',
                '[href*="assignment"]', '[href*="homework"]', '[href*="task"]',
                '[href*="student"]', '[href*="dashboard"]', '[href*="class"]'
            ]
            
            print("\n找到的导航链接:")
            for selector in nav_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    for element in elements[:10]:  # 限制显示前10个
                        href = await element.get_attribute('href')
                        text = await element.text_content()
                        if href and text and text.strip():
                            print(f"  - {text.strip()}: {href}")
                except:
                    continue
            
            # 查找可能包含作业的区域
            content_selectors = [
                '.content', '.main-content', '.dashboard', '.student-dashboard',
                '.assignments', '.homework', '.tasks', '.todo', '.pending'
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
        """
        尝试导航到作业页面，并尽量切换到“全部/All”视图，方便抓取已提交与未提交。
        """
        try:
            print("\n=== 尝试导航到作业页面 ===")
            
            # 优先寻找“Tasks & Deadlines”或“全部/All”入口
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
                '.menu a:has-text("Assignment")'
            ]
            
            for selector in assignment_link_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        href = await element.get_attribute('href')
                        text = (await element.text_content() or '').strip()
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
            
            # 如果仍未到任务页面，尝试直接访问常见路径
            current_url = page.url
            if not any(key in current_url for key in ['tasks', 'assignment', 'homework']):
                print("未找到明确的作业链接，尝试其他导航方式...")
                assignment_paths = [
                    '/student/tasks_and_deadlines',
                    '/assignments', '/student/assignments', '/homework', '/tasks',
                    '/dashboard/assignments', '/student/dashboard/assignments'
                ]
                base_url = self.url.rstrip('/')
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
            
            # 页面上切换“全部/All”筛选
            await self._switch_to_all_filter(page)
            
            print(f"导航后的URL: {page.url}")
            return True
        except Exception as e:
            print(f"导航到作业页面时出错: {e}")
            return False
    
    async def _switch_to_all_filter(self, page: Page) -> None:
        """尽量点击“全部/All”标签或过滤器，让列表显示所有任务。"""
        try:
            filter_selectors = [
                'a:has-text("All")', 'button:has-text("All")',
                'a:has-text("全部")', 'button:has-text("全部")',
                'a[href$="/tasks_and_deadlines"]'
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
        """
        尝试导航到作业页面。
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print("\n=== 尝试导航到作业页面 ===")
            
            # 尝试找到作业相关的链接
            assignment_link_selectors = [
                'a[href*="assignment"]',
                'a[href*="homework"]',
                'a[href*="task"]',
                'a:has-text("Assignment")',
                'a:has-text("Homework")',
                'a:has-text("Tasks")',
                'a:has-text("作业")',
                'a:has-text("待办")',
                '.nav a:has-text("Assignment")',
                '.menu a:has-text("Assignment")'
            ]
            
            for selector in assignment_link_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        href = await element.get_attribute('href')
                        text = await element.text_content()
                        print(f"找到作业链接: {text} -> {href}")
                        
                        # 点击链接
                        await element.click()
                        print(f"点击了作业链接: {text}")
                        
                        # 等待页面加载
                        await page.wait_for_load_state("domcontentloaded")
                        await page.wait_for_timeout(2000)  # 等待2秒确保内容加载
                        
                        current_url = page.url
                        print(f"导航后的URL: {current_url}")
                        return True
                        
                except Exception as e:
                    if self.debug:
                        print(f"尝试选择器 {selector} 失败: {e}")
                    continue
            
            print("未找到明确的作业链接，尝试其他导航方式...")
            
            # 尝试直接访问常见的作业页面URL路径
            assignment_paths = [
                '/assignments',
                '/student/assignments',
                '/homework',
                '/tasks',
                '/dashboard/assignments',
                '/student/dashboard/assignments'
            ]
            
            base_url = self.url.rstrip('/')
            for path in assignment_paths:
                try:
                    assignment_url = base_url + path
                    print(f"尝试直接访问: {assignment_url}")
                    
                    await page.goto(assignment_url, wait_until="domcontentloaded")
                    await page.wait_for_timeout(2000)
                    
                    # 检查是否成功导航（没有404错误等）
                    title = await page.title()
                    if '404' not in title and 'error' not in title.lower():
                        print(f"成功访问: {assignment_url}")
                        return True
                        
                except Exception as e:
                    if self.debug:
                        print(f"访问 {assignment_url} 失败: {e}")
                    continue
            
            print("无法找到作业页面，将在当前页面搜索作业信息...")
            return False
            
        except Exception as e:
            print(f"导航到作业页面时出错: {e}")
            return False
    
    async def get_all_assignments(self, page: Page, browser: Optional[Browser] = None) -> List[Dict[str, Any]]:
        """
        抓取“全部作业”，包括已提交与未提交，并尽可能提取详情。
        如果配置了 FETCH_DETAILS=true，会打开部分作业详情页抓取更多字段。
        """
        assignments: List[Dict[str, Any]] = []
        
        try:
            print("\n=== 抓取全部作业（包含已提交/未提交）===")
            print(f"当前页面: {page.url}")
            
            # 更全面的选择器集合，优先选择包含任务条目的容器元素
            item_selectors = [
                '.assignment', '.assignment-item', '.task-item', '.homework-item',
                'li[class*="assignment"]', '.assignment-list li', '.homework-list li',
                'tr[class*="assignment"], tr[class*="task"], tr[class*="homework"]',
                '.card:has([class*="due"])',
                # 容器内带有截止日期/状态的块
                'div:has([class*="due"]), div:has([class*="status"])'
            ]
            
            status_keywords = {
                'submitted': ['submitted', '已提交', 'turned in', '已上交'],
                'pending': ['pending', 'not submitted', 'unsubmitted', '未提交', '待提交', '未上交'],
                'overdue': ['overdue', '逾期', '迟交', 'late']
            }
            
            type_keywords = {
                'summative': ['summative', '总结性'],
                'formative': ['formative', '形成性']
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
                found_elements = await page.query_selector_all('[class*="due"], [class*="status"]')
            
            print(f"找到潜在任务元素: {len(found_elements)}")
            
            # 遍历每个元素，提取信息
            for idx, el in enumerate(found_elements):
                try:
                    text = (await el.text_content() or '').strip()
                    if not text or len(text) < 6:
                        continue
                    low = text.lower()
                    
                    # 标题
                    title = None
                    for tsel in ['.title', '.assignment-title', '.homework-title', 'h1', 'h2', 'h3', 'h4', 'a']:
                        try:
                            tnode = await el.query_selector(tsel)
                            if tnode:
                                ttext = (await tnode.text_content() or '').strip()
                                if ttext and len(ttext) > 2:
                                    title = ttext
                                    break
                        except:
                            continue
                    if not title:
                        # 回退：截取前100字符作为标题
                        title = text[:100]
                    
                    # 截止日期
                    due_text = None
                    for dsel in ['.due-date', '[class*="due"]', '.date', '.deadline']:
                        try:
                            dnode = await el.query_selector(dsel)
                            if dnode:
                                dtext = (await dnode.text_content() or '').strip()
                                if dtext:
                                    due_text = dtext
                                    break
                        except:
                            continue
                    if not due_text:
                        # 简单从整体文本中查找“at”模式
                        m = re.search(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b[^\n]{0,40}', text, re.I)
                        if m:
                            due_text = m.group(0).strip()
                        else:
                            due_text = '无截止日期'
                    
                    # 状态
                    status = '未知'
                    submitted = False
                    overdue = False
                    for key, keys in status_keywords.items():
                        if any(k in low for k in keys):
                            if key == 'submitted':
                                status = 'Submitted'
                                submitted = True
                            elif key == 'pending':
                                status = 'Pending'
                            elif key == 'overdue':
                                status = 'Overdue'
                                overdue = True
                    
                    # 类型
                    a_type = 'Unknown'
                    for tkey, tkeys in type_keywords.items():
                        if any(k in low for k in tkeys):
                            a_type = 'Summative' if tkey == 'summative' else 'Formative'
                            break
                    
                    # 课程名称（从局部或整段文本中提取）
                    course = self._extract_course_name(text)
                    
                    # 链接
                    link = None
                    for lsel in ['a[href*="core_tasks"]', 'a[href*="/tasks/"], a[href*="/assignment"]', 'a']:
                        try:
                            lnode = await el.query_selector(lsel)
                            if lnode:
                                href = await lnode.get_attribute('href')
                                if href and not href.startswith('javascript'):
                                    link = href
                                    break
                        except:
                            continue
                    
                    assignment = {
                        'title': title,
                        'course': course,
                        'type': a_type,
                        'due_date': due_text,
                        'status': status,
                        'submitted': submitted,
                        'overdue': overdue,
                        'link': link,
                        'selector_used': 'auto',
                        'element_index': idx,
                        'full_text_preview': text[:300] + ('...' if len(text) > 300 else ''),
                        'found_at': datetime.now().isoformat()
                    }
                    assignments.append(assignment)
                except Exception as e:
                    if self.debug:
                        print(f"解析元素 {idx} 失败: {e}")
                    continue
            
            # 可选：抓取详情
            if self.fetch_details and browser and assignments:
                await self._enrich_assignments_details(assignments, browser)
            
            # 去重
            if len(assignments) > 1:
                assignments = self._remove_duplicate_assignments(assignments)
            
            # 过滤不合理噪声（仅文本非常短且无状态、无课程、无类型）
            clean = []
            for a in assignments:
                if len(a.get('title', '').strip()) < 3 and a.get('status', '未知') == '未知' and not a.get('course'):
                    continue
                clean.append(a)
            assignments = clean
            
            print(f"完成抓取：{len(assignments)} 条")
            return assignments
        except Exception as e:
            print(f"抓取全部作业时出错: {e}")
            return assignments
    
    async def _enrich_assignments_details(self, assignments: List[Dict[str, Any]], browser: Browser) -> None:
        """打开部分作业详情页，提取更多字段。"""
        try:
            count = 0
            for a in assignments:
                if count >= self.details_limit:
                    break
                link = a.get('link')
                if not link:
                    continue
                # 拼接完整URL
                url = link
                if link.startswith('/'):
                    url = self.url.rstrip('/') + link
                
                page = await browser.new_page()
                try:
                    await page.goto(url, wait_until='domcontentloaded')
                    await page.wait_for_timeout(800)
                    # 详情字段尝试提取
                    desc = await self._safe_inner_text(page, ['.description', '.assignment-description', '.content', '.instructions'])
                    teacher = await self._safe_inner_text(page, ['.teacher', '.author', 'a[href*="/teachers/"]'])
                    created = await self._safe_inner_text(page, ['.created-at', '[class*="created"]'])
                    updated = await self._safe_inner_text(page, ['.updated-at', '[class*="updated"]'])
                    attachments = await self._collect_links(page, ['a[href*="/files/"], a:has-text("Download")'])
                    
                    a['details'] = {
                        'description': desc,
                        'teacher': teacher,
                        'created_at': created,
                        'updated_at': updated,
                        'attachments': attachments
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
    
    async def _collect_links(self, page: Page, selectors: List[str]) -> List[Dict[str, str]]:
        items = []
        for sel in selectors:
            try:
                els = await page.query_selector_all(sel)
                for el in els[:10]:
                    href = await el.get_attribute('href')
                    text = (await el.text_content() or '').strip()
                    if href and not href.startswith('javascript'):
                        items.append({'text': text, 'href': href})
            except:
                continue
        return items
    
    async def get_unsubmitted_assignments(self, page: Page) -> List[Dict[str, Any]]:
        """
        从ManageBac提取未提交的作业。
        
        Args:
            page: The Playwright page instance
            
        Returns:
            List of dictionaries containing assignment information
        """
        assignments = []
        
        try:
            print("\n=== 开始搜索作业 ===")
            print(f"当前页面: {page.url}")
            
            # 首先尝试更全面的作业选择器
            assignment_selectors = [
                # 通用作业容器
                '.assignment', '[data-assignment]', '.task-item', '.homework-item', '.assignment-item',
                # 表格行
                'tr[class*="assignment"]', 'tr[class*="homework"]', 'tr[class*="task"]',
                # 卡片式布局
                '.card', '.assignment-card', '.homework-card',
                # 列表项
                'li[class*="assignment"]', '.assignment-list li', '.homework-list li',
                # 通用容器
                '[class*="pending"]', '[class*="due"]', '[class*="overdue"]', '[class*="unsubmitted"]'
            ]
            
            print(f"尝试 {len(assignment_selectors)} 种不同的选择器...")
            
            # 尝试找到作业容器
            for i, selector in enumerate(assignment_selectors):
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        print(f"✓ 选择器 {i+1}: '{selector}' 找到 {len(elements)} 个元素")
                        
                        for j, element in enumerate(elements[:20]):  # 限制处理前20个元素
                            try:
                                # 获取元素的所有文本内容
                                element_text = await element.text_content()
                                if not element_text or len(element_text.strip()) < 5:
                                    continue
                                
                                element_text = element_text.strip()
                                
                                # 尝试提取结构化信息
                                title_selectors = [
                                    '.title', '.assignment-title', '.homework-title', '.task-title',
                                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                                    '.name', '.subject', '.description',
                                    'strong', 'b', '.bold',
                                    'a[href*="assignment"]'
                                ]
                                
                                due_date_selectors = [
                                    '.due-date', '.date', '.deadline', '.due',
                                    '[class*="date"]', '[class*="due"]', '[class*="deadline"]',
                                    '.time', '.datetime'
                                ]
                                
                                status_selectors = [
                                    '.status', '.assignment-status', '.homework-status',
                                    '.state', '.progress', '.completion',
                                    '[class*="status"]', '[class*="state"]',
                                    '.badge', '.label', '.tag'
                                ]
                                
                                title = "未知作业"
                                due_date = "无截止日期"
                                status = "状态未知"
                                
                                # 提取标题
                                for title_selector in title_selectors:
                                    try:
                                        title_element = await element.query_selector(title_selector)
                                        if title_element:
                                            title_text = await title_element.text_content()
                                            if title_text and len(title_text.strip()) > 2:
                                                title = title_text.strip()
                                                break
                                    except:
                                        continue
                                
                                # 如果没找到标题，使用元素文本的前100个字符
                                if title == "未知作业" and len(element_text) > 10:
                                    title = element_text[:100] + ("..." if len(element_text) > 100 else "")
                                
                                # 提取截止日期
                                for due_selector in due_date_selectors:
                                    try:
                                        due_element = await element.query_selector(due_selector)
                                        if due_element:
                                            due_text = await due_element.text_content()
                                            if due_text and due_text.strip():
                                                due_date = due_text.strip()
                                                break
                                    except:
                                        continue
                                
                                # 提取状态
                                for status_selector in status_selectors:
                                    try:
                                        status_element = await element.query_selector(status_selector)
                                        if status_element:
                                            status_text = await status_element.text_content()
                                            if status_text and status_text.strip():
                                                status = status_text.strip()
                                                break
                                    except:
                                        continue
                                
                                # 检查是否为未提交的作业
                                unsubmitted_keywords = [
                                    'not submitted', 'unsubmitted', 'pending', 'overdue',
                                    '未提交', '待提交', '未完成', '逾期', '延期',
                                    'todo', 'to do', 'incomplete', 'missing'
                                ]
                                
                                is_unsubmitted = False
                                full_text = f"{title} {due_date} {status} {element_text}".lower()
                                
                                for keyword in unsubmitted_keywords:
                                    if keyword in full_text:
                                        is_unsubmitted = True
                                        break
                                
                                # 如果没有明确的状态信息，且包含作业相关关键词，也认为是潜在的作业
                                if not is_unsubmitted and status == "状态未知":
                                    assignment_keywords = ['assignment', 'homework', 'task', '作业', '任务']
                                    if any(keyword in full_text for keyword in assignment_keywords):
                                        is_unsubmitted = True
                                        status = "可能未提交"
                                
                                if is_unsubmitted:
                                    assignment_info = {
                                        'title': title,
                                        'due_date': due_date,
                                        'status': status,
                                        'selector_used': selector,
                                        'element_index': j,
                                        'full_text_preview': element_text[:200] + ("..." if len(element_text) > 200 else ""),
                                        'found_at': datetime.now().isoformat()
                                    }
                                    assignments.append(assignment_info)
                                    
                                    if self.debug:
                                        print(f"  找到作业 {len(assignments)}: {title}")
                                    
                            except Exception as e:
                                if self.debug:
                                    print(f"处理元素 {j+1} 时出错: {e}")
                                continue
                        
                        if assignments:
                            print(f"通过选择器 '{selector}' 找到 {len(assignments)} 个作业")
                            break  # 找到作业后停止搜索
                        
                except Exception as e:
                    if self.debug:
                        print(f"选择器 '{selector}' 失败: {e}")
                    continue
            
            # 如果仍然没有找到作业，尝试全页面文本搜索
            if not assignments:
                print("\n未找到结构化作业元素，进行全页面文本搜索...")
                await self._search_page_text_for_assignments(page, assignments)
            
            # 去重处理
            if len(assignments) > 1:
                assignments = self._remove_duplicate_assignments(assignments)
            
            return assignments
            
        except Exception as e:
            print(f"搜索作业时出错: {e}")
            return assignments
    
    async def _search_page_text_for_assignments(self, page: Page, assignments: List[Dict[str, Any]]) -> None:
        """
        在页面文本中搜索作业相关信息。
        """
        try:
            # 获取页面所有可见文本
            page_content = await page.content()
            
            # 检查是否包含作业相关关键词
            assignment_keywords = [
                'assignment', 'homework', 'task', 'due', 'submit', 'pending',
                '作业', '任务', '提交', '截止', '待办', '未完成'
            ]
            
            if any(keyword in page_content.lower() for keyword in assignment_keywords):
                print("页面包含作业相关内容，尝试提取...")
                
                # 获取所有可见的文本元素
                text_elements = await page.query_selector_all('p, div, span, li, td, th')
                print(f"找到 {len(text_elements)} 个文本元素")
                
                for element in text_elements[:100]:  # 限制处理前100个元素
                    try:
                        text = await element.text_content()
                        if not text or len(text.strip()) < 10:
                            continue
                            
                        text = text.strip()
                        text_lower = text.lower()
                        
                        # 检查是否包含作业相关关键词
                        has_assignment_keyword = any(keyword in text_lower for keyword in assignment_keywords)
                        
                        if has_assignment_keyword and len(text) > 20 and len(text) < 500:
                            # 尝试判断是否为未提交的作业
                            unsubmitted_indicators = [
                                'not submitted', 'unsubmitted', 'pending', 'overdue', 'todo',
                                '未提交', '待提交', '未完成', '逾期', '待办'
                            ]
                            
                            is_unsubmitted = any(indicator in text_lower for indicator in unsubmitted_indicators)
                            
                            if is_unsubmitted or ('due' in text_lower and 'submit' in text_lower):
                                assignments.append({
                                    'title': text[:100] + ("..." if len(text) > 100 else ""),
                                    'due_date': '从文本提取',
                                    'status': '可能未提交',
                                    'selector_used': 'text_search',
                                    'full_text_preview': text,
                                    'found_at': datetime.now().isoformat()
                                })
                                
                                if len(assignments) >= 10:  # 限制文本搜索结果数量
                                    break
                                    
                    except:
                        continue
                        
                print(f"文本搜索找到 {len([a for a in assignments if a.get('selector_used') == 'text_search'])} 个潜在作业")
                
        except Exception as e:
            print(f"页面文本搜索出错: {e}")
    
    def _remove_duplicate_assignments(self, assignments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        移除重复的作业条目。
        """
        seen_titles = set()
        unique_assignments = []
        
        for assignment in assignments:
            title_key = assignment['title'][:50].lower().strip()  # 使用前50个字符作为去重键
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_assignments.append(assignment)
        
        if len(assignments) != len(unique_assignments):
            print(f"去重后：{len(assignments)} -> {len(unique_assignments)} 个作业")
        
        return unique_assignments
    
    def analyze_assignments(self, assignments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析作业数据，生成统计信息。
        """
        if not assignments:
            return {
                'total_assignments': 0,
                'by_priority': {'high': 0, 'medium': 0, 'low': 0},
                'by_course': {},
                'by_due_date': {},
                'by_type': {},
                'urgent_count': 0,
                'overdue_count': 0,
                'submitted_count': 0,
                'pending_count': 0,
                'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
                'grouped_by_status': {'submitted': [], 'pending': [], 'overdue': [], 'unknown': []}
            }
        
        analysis = {
            'total_assignments': len(assignments),
            'by_priority': {'high': 0, 'medium': 0, 'low': 0},
            'by_course': {},
            'by_due_date': {},
            'by_type': {},
            'urgent_count': 0,  # 48小时内
            'overdue_count': 0,
            'submitted_count': 0,
            'pending_count': 0,
            'assignments_by_urgency': {'urgent': [], 'soon': [], 'later': []},
            'grouped_by_status': {'submitted': [], 'pending': [], 'overdue': [], 'unknown': []}
        }
        
        now = datetime.now()
        
        for assignment in assignments:
            # 课程统计
            course = assignment.get('course') or self._extract_course_name(assignment.get('title', ''))
            if course not in analysis['by_course']:
                analysis['by_course'][course] = 0
            analysis['by_course'][course] += 1
            
            # 类型统计
            a_type = assignment.get('type', 'Unknown')
            analysis['by_type'][a_type] = analysis['by_type'].get(a_type, 0) + 1
            
            # 优先级分析
            priority = self._calculate_priority(assignment)
            analysis['by_priority'][priority] += 1
            
            # 状态分组
            status = (assignment.get('status') or '未知').lower()
            if 'submitted' in status or assignment.get('submitted'):
                analysis['grouped_by_status']['submitted'].append(assignment)
                analysis['submitted_count'] += 1
            elif 'overdue' in status or assignment.get('overdue'):
                analysis['grouped_by_status']['overdue'].append(assignment)
                analysis['overdue_count'] += 1
            elif 'pending' in status or '未提交' in status:
                analysis['grouped_by_status']['pending'].append(assignment)
                analysis['pending_count'] += 1
            else:
                analysis['grouped_by_status']['unknown'].append(assignment)
            
            # 时间紧急度分析
            urgency = self._calculate_urgency(assignment, now)
            analysis['assignments_by_urgency'][urgency].append(assignment)
            if urgency == 'urgent':
                analysis['urgent_count'] += 1
            
            # 截止日期统计
            due_date_str = assignment.get('due_date', '无截止日期')
            analysis['by_due_date'][due_date_str] = analysis['by_due_date'].get(due_date_str, 0) + 1
        
        return analysis
    
    def _extract_course_name(self, title: str) -> str:
        """从作业标题中提取课程名称。"""
        # 尝试从标题中提取AP课程名称
        ap_match = re.search(r'AP\s+([^\n(]+)', title)
        if ap_match:
            return f"AP {ap_match.group(1).strip()}"
        
        # 查找课程相关关键词
        course_keywords = {
            'Computer Science': ['CS', 'Computer', 'Programming'],
            'Mathematics': ['Math', 'Calculus', 'Algebra', 'BC'],
            'Economics': ['Economics', 'Macro', 'Micro'],
            'History': ['History', 'US History'],
            'Psychology': ['Psychology', 'Psych'],
            'English': ['English', 'Literature', 'Writing']
        }
        
        title_lower = title.lower()
        for course, keywords in course_keywords.items():
            if any(keyword.lower() in title_lower for keyword in keywords):
                return course
        
        return '未知课程'
    
    def _calculate_priority(self, assignment: Dict[str, Any]) -> str:
        """计算作业优先级。"""
        title = assignment.get('title', '').lower()
        status = assignment.get('status', '').lower()
        
        # 高优先级关键词
        high_priority_keywords = ['summative', 'exam', 'test', 'project', 'essay', 'final']
        if any(keyword in title or keyword in status for keyword in high_priority_keywords):
            return 'high'
        
        # 中优先级关键词
        medium_priority_keywords = ['homework', 'assignment', 'quiz']
        if any(keyword in title or keyword in status for keyword in medium_priority_keywords):
            return 'medium'
        
        return 'low'
    
    def _calculate_urgency(self, assignment: Dict[str, Any], now: datetime) -> str:
        """计算作业紧急程度。"""
        due_date_str = assignment.get('due_date', '')
        
        # 尝试解析截止日期
        try:
            # 简单的日期解析（可以进一步优化）
            if 'sunday' in due_date_str.lower() or 'monday' in due_date_str.lower():
                # 近期作业
                return 'urgent'
            elif 'tuesday' in due_date_str.lower() or 'wednesday' in due_date_str.lower():
                return 'soon'
            else:
                return 'later'
        except:
            return 'later'
    
    def generate_reports(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        生成多种格式的报告。
        """
        report_data = {
            'assignments': assignments,
            'analysis': analysis,
            'generated_at': datetime.now().isoformat(),
            'student_email': self.email
        }
        
        reports = {}
        
        for format_type in self.report_format:
            format_type = format_type.strip().lower()
            
            if format_type == 'json':
                reports['json'] = self._generate_json_report(report_data)
            elif format_type == 'html':
                reports['html'] = self._generate_html_report(report_data)
            elif format_type == 'markdown':
                reports['markdown'] = self._generate_markdown_report(report_data)
            elif format_type == 'console':
                reports['console'] = self._generate_console_report(report_data)
        
        return reports
    
    def _generate_json_report(self, data: Dict[str, Any]) -> str:
        """生成JSON格式报告。"""
        try:
            return json.dumps(data, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            return f"{{\"error\": \"生成JSON报告失败: {e}\"}}"
    
    def _generate_html_report(self, data: Dict[str, Any]) -> str:
        """生成HTML格式报告（包含全部作业：未提交/已提交/逾期）。"""
        assignments = data['assignments']
        analysis = data['analysis']
        generated_at = data['generated_at']
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="light" />
    <title>ManageBac作业检查报告</title>
    <style>
        :root {{ color-scheme: light; }}
        html, body {{ background:#f7fafc; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 24px; color:#111827; }}
        a {{ color:#1d4ed8; text-decoration:none; }}
        a:hover {{ text-decoration:underline; }}
        .container {{ max-width: 1100px; margin: 0 auto; background-color: #ffffff; padding: 28px; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.06); border:1px solid #e5e7eb; }}
        h1 {{ color: #111827; border-bottom: 4px solid #2563eb; padding-bottom: 10px; margin-top:0; }}
        h2 {{ color: #111827; margin-top: 28px; }}
        h3 {{ color:#111827; }}
        .summary {{ background-color: #f3f4f6; padding: 18px; border-radius: 10px; margin: 18px 0; border:1px solid #e5e7eb; }}
        .urgent {{ background-color: #ef4444; color: #ffffff; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .soon {{ background-color: #f59e0b; color: #111827; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .later {{ background-color: #10b981; color: #ffffff; padding: 10px; border-radius: 10px; margin: 6px 0; }}
        .assignment {{ border-left: 6px solid #2563eb; padding: 14px; margin: 10px 0; background-color: #ffffff; border:1px solid #e5e7eb; border-radius:8px; color:#111827; }}
        .high-priority {{ border-left-color: #ef4444; }}
        .medium-priority {{ border-left-color: #f59e0b; }}
        .low-priority {{ border-left-color: #10b981; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 18px 0; }}
        .stat-item {{ text-align: center; padding: 16px; background-color: #2563eb; color: white; border-radius: 10px; box-shadow: inset 0 -4px 0 rgba(0,0,0,0.1); }}
        .kpi-bar {{ background:#e5e7eb; height:10px; border-radius:999px; overflow:hidden; }}
        .kpi-fill {{ height:10px; background:#2563eb; }}
        .kpi-fill.red {{ background:#ef4444; }}
        .kpi-fill.yellow {{ background:#f59e0b; }}
        .kpi-fill.green {{ background:#10b981; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size:14px; }}
        th, td {{ border: 1px solid #e5e7eb; padding: 10px; text-align: left; color:#111827; }}
        th {{ background-color: #2563eb; color: #ffffff; }}
        .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 12px; }}
        .badge {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; margin-left:6px; }}
        .badge.high {{ background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }}
        .badge.medium {{ background:#fef3c7; color:#92400e; border:1px solid #fde68a; }}
        .badge.low {{ background:#d1fae5; color:#065f46; border:1px solid #a7f3d0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 ManageBac作业检查报告</h1>
        
        <div class="summary">
            <h2>📈 概览统计</h2>
            <div class="stats">
                <div class="stat-item">
                    <h3>{analysis['total_assignments']}</h3>
                    <p>总任务</p>
                    <div class="kpi-bar" title="总任务">
                        <div class="kpi-fill" style="width:100%"></div>
                    </div>
                </div>
                <div class="stat-item">
                    <h3>{analysis['urgent_count']}</h3>
                    <p>紧急任务</p>
                    <div class="kpi-bar" title="紧急任务">
                        <div class="kpi-fill red" style="width:{(analysis['urgent_count'] / max(analysis['total_assignments'],1)) * 100:.0f}%"></div>
                    </div>
                </div>
                <div class="stat-item">
                    <h3>{len(analysis['by_course'])}</h3>
                    <p>涉及课程</p>
                    <div class="kpi-bar" title="课程覆盖">
                        <div class="kpi-fill green" style="width:{(len(analysis['by_course'])/max(len(analysis['by_course']),1)) * 100:.0f}%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <h2>😨 紧急作业</h2>
        <p>以下为近期（规则：按日期文本粗略判断）更紧急的任务：</p>
        """
        
        # 添加紧急作业
        for assignment in analysis['assignments_by_urgency']['urgent']:
            html += f'''
        <div class="assignment urgent">
            <strong>🔥 {assignment['title'][:100]}</strong><br>
            <em>截止日期: {assignment['due_date']}</em><br>
            <small>状态: {assignment['status']}</small>
        </div>
            '''
        
        # 添加课程统计
        html += """
        <h2>📚 课程统计</h2>
        <table>
            <tr><th>课程</th><th>作业数量</th></tr>
        """
        
        for course, count in analysis['by_course'].items():
            html += f"<tr><td>{course}</td><td>{count}</td></tr>"
        
        html += """
        </table>
        
        <h2>📋 作业分类</h2>
        <div>
            <h3>🟠 未提交（Pending） - {len(analysis['grouped_by_status']['pending'])} 个</h3>
        </div>
        
        """
        
        # Pending 列表
        for i, assignment in enumerate(analysis['grouped_by_status']['pending'], 1):
            priority = self._calculate_priority(assignment)
            priority_class = f"{priority}-priority"
            priority_text = {'high': '🔴 高', 'medium': '🟡 中', 'low': '🟢 低'}[priority]
            html += f'''
        <div class="assignment {priority_class}">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em> |
            <em>优先级: {priority_text}</em>
        </div>
            '''
        
        html += """
        <div style="margin-top:20px;">
            <h3>✅ 已提交（Submitted） - {len(analysis['grouped_by_status']['submitted'])} 个</h3>
        </div>
        """
        
        for i, assignment in enumerate(analysis['grouped_by_status']['submitted'], 1):
            html += f'''
        <div class="assignment low-priority">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em>
        </div>
            '''
        
        html += """
        <div style="margin-top:20px;">
            <h3>⛔ 逾期（Overdue） - {len(analysis['grouped_by_status']['overdue'])} 个</h3>
        </div>
        """
        
        for i, assignment in enumerate(analysis['grouped_by_status']['overdue'], 1):
            html += f'''
        <div class="assignment urgent">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> |
            <em>类型: {assignment.get('type','Unknown')}</em> |
            <em>截止日期: {assignment['due_date']}</em> |
            <em>状态: {assignment['status']}</em>
        </div>
            '''
        
        html += """
        <h2>📋 所有作业详情（完整列表）</h2>
        """
        
        # 添加所有作业
        for i, assignment in enumerate(assignments, 1):
            priority = self._calculate_priority(assignment)
            priority_class = f"{priority}-priority"
            priority_text = {'high': '🔴 高', 'medium': '🟡 中', 'low': '🟢 低'}[priority]
            
            html += f'''
        <div class="assignment {priority_class}">
            <strong>{i}. {assignment['title'][:150]}</strong><br>
            <em>课程: {assignment.get('course','未知')}</em> | 
            <em>类型: {assignment.get('type','Unknown')}</em> | 
            <em>截止日期: {assignment['due_date']}</em> | 
            <em>状态: {assignment['status']}</em> | 
            <em>优先级: {priority_text}</em>
        </div>
            '''
        
        html += f"""
        <div class="footer">
            <p>报告生成时间: {generated_at}</p>
            <p>由 ManageBac Assignment Checker 自动生成</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """生成Markdown格式报告（包含全部作业：未提交/已提交/逾期）。"""
        assignments = data['assignments']
        analysis = data['analysis']
        generated_at = data['generated_at']
        
        md = f"""# 📚 ManageBac作业检查报告

生成时间: {generated_at}

## 📈 概览统计

- 待办作业总数: {analysis['total_assignments']}
- 紧急作业: {analysis['urgent_count']}
- 已提交: {analysis['submitted_count']} | 未提交: {analysis['pending_count']} | 逾期: {analysis['overdue_count']}
- 涉及课程: {len(analysis['by_course'])}

### 优先级分布
- 🔴 高: {analysis['by_priority']['high']}
- 🟡 中: {analysis['by_priority']['medium']}
- 🟢 低: {analysis['by_priority']['low']}

## 😨 紧急作业

"""
        
        if analysis['assignments_by_urgency']['urgent']:
            for assignment in analysis['assignments_by_urgency']['urgent']:
                md += f"- 🔥 {assignment['title'][:100]} — {assignment['due_date']}\n"
        else:
            md += "暂无紧急作业\n"
        
        md += "\n## 📚 课程统计\n\n"
        for course, count in analysis['by_course'].items():
            md += f"- {course}: {count} 个作业\n"
        
        md += "\n## 📋 作业分类\n\n### 🟠 未提交（Pending）\n\n"
        
        for i, assignment in enumerate(analysis['grouped_by_status']['pending'], 1):
            priority = self._calculate_priority(assignment)
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
            md += f"- {i}. {assignment['title'][:100]}\n  - 课程: {assignment.get('course','未知')}\n  - 类型: {assignment.get('type','Unknown')}\n  - 截止日期: {assignment['due_date']}\n  - 状态: {assignment['status']}\n  - 优先级: {priority_emoji} {priority.upper()}\n"
        
        md += "\n### ✅ 已提交（Submitted）\n\n"
        for i, assignment in enumerate(analysis['grouped_by_status']['submitted'], 1):
            md += f"- {i}. {assignment['title'][:100]} — {assignment['due_date']} (课程: {assignment.get('course','未知')}, 类型: {assignment.get('type','Unknown')})\n"
        
        md += "\n### ⛔ 逾期（Overdue）\n\n"
        for i, assignment in enumerate(analysis['grouped_by_status']['overdue'], 1):
            md += f"- {i}. {assignment['title'][:100]} — {assignment['due_date']} (课程: {assignment.get('course','未知')}, 类型: {assignment.get('type','Unknown')})\n"
        
        md += "\n## 📋 所有作业详情（完整列表）\n\n"
        
        for i, assignment in enumerate(assignments, 1):
            priority = self._calculate_priority(assignment)
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
            md += f"""### {i}. {assignment['title'][:100]}

- 课程: {assignment.get('course','未知')}
- 类型: {assignment.get('type','Unknown')}
- 截止日期: {assignment['due_date']}
- 状态: {assignment['status']}
- 优先级: {priority_emoji} {priority.upper()}

"""
        
        md += "\n---\n*报告由 ManageBac Assignment Checker 自动生成*"
        
        return md
    
    def _generate_console_report(self, data: Dict[str, Any]) -> str:
        """生成控制台格式报告。"""
        # 这个将在主运行方法中处理
        return "console_output_handled_in_main_method"
    
    def save_reports(self, reports: Dict[str, str]) -> Dict[str, str]:
        """
        保存报告到文件。
        """
        saved_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type, content in reports.items():
            if format_type == 'console':
                continue
                
            file_extension = {
                'json': 'json',
                'html': 'html',
                'markdown': 'md'
            }.get(format_type, 'txt')
            
            filename = f"managebac_report_{timestamp}.{file_extension}"
            filepath = self.output_dir / filename
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files[format_type] = str(filepath)
                print(f"\n💾 {format_type.upper()}报告已保存: {filepath}")
            except Exception as e:
                print(f"\n⚠️  保存{format_type}报告失败: {e}")
        
        return saved_files
    
    async def send_email_notification(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> bool:
        """
        发送邮件通知。
        """
        if not self.enable_notifications or not all([self.smtp_server, self.email_user, self.email_password, self.notification_email]):
            return False
        
        try:
            # 创建邮件内容
            subject = f"📚 ManageBac作业提醒 - {analysis['total_assignments']}个待办作业"
            
            # 生成简单的HTML邮件内容
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2 style="color: #2c3e50;">📚 ManageBac作业提醒</h2>
                    <p>您好！以下是您的作业总结：</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>📈 概览统计</h3>
                        <ul>
                            <li><strong>待办作业</strong>: {analysis['total_assignments']} 个</li>
                            <li><strong>紧急作业</strong>: {analysis['urgent_count']} 个</li>
                            <li><strong>涉及课程</strong>: {len(analysis['by_course'])} 个</li>
                        </ul>
                    </div>
            """
            
            if analysis['urgent_count'] > 0:
                html_content += """
                    <div style="background-color: #e74c3c; color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h3>😨 紧急作业</h3>
                        <ul>
                """
                
                for assignment in analysis['assignments_by_urgency']['urgent'][:5]:  # 只显示前5个
                    html_content += f"<li><strong>{assignment['title'][:50]}...</strong> - {assignment['due_date']}</li>"
                
                html_content += "</ul></div>"
            
            html_content += """
                    <p style="margin-top: 20px; font-size: 14px; color: #7f8c8d;">
                        请及时登录ManageBac查看详情并完成作业。
                    </p>
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #95a5a6;">
                        此邮件由 ManageBac Assignment Checker 自动发送<br>
                        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </body>
            </html>
            """
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = self.notification_email
            
            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.sendmail(self.email_user, self.notification_email, msg.as_string())
            
            print(f"\n📧 邮件通知已发送到: {self.notification_email}")
            return True
            
        except Exception as e:
            print(f"\n⚠️  发送邮件通知失败: {e}")
            return False
    
    def _display_console_results(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> None:
        """
        在控制台显示结果。
        """
        print("\n" + "═"*80)
        print(f"\n📚 【ManageBac作业检查报告】 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═"*80)
        
        # 概览统计
        print(f"\n📈 【概览统计】")
        print(f"   📋 待办作业总数: {analysis['total_assignments']} 个")
        print(f"   😨 紧急作业: {analysis['urgent_count']} 个")
        print(f"   📚 涉及课程: {len(analysis['by_course'])} 个")
        
        # 优先级分布
        print(f"\n   优先级分布:")
        print(f"     🔴 高优先级: {analysis['by_priority']['high']} 个")
        print(f"     🟡 中优先级: {analysis['by_priority']['medium']} 个")
        print(f"     🟢 低优先级: {analysis['by_priority']['low']} 个")
        
        if not assignments:
            print(f"\n✅ 【好消息】 未找到未提交的作业！")
            print("\n这可能意味着：")
            print("• 所有作业都已提交 ✅")
            print("• 页面结构发生了变化，需要更新脚本")
            print("• 需要手动导航到正确的作业页面")
            return
        
        # 紧急作业
        urgent_assignments = analysis['assignments_by_urgency']['urgent']
        if urgent_assignments:
            print(f"\n🔥 【紧急作业 - 需要立即关注！】")
            for i, assignment in enumerate(urgent_assignments[:5], 1):  # 只显示前5个
                print(f"   {i}. 🔥 {assignment['title'][:60]}")
                print(f"      ⏰ 截止: {assignment['due_date']} | 状态: {assignment['status']}")
        
        # 课程统计
        if analysis['by_course']:
            print(f"\n📚 【课程分布】")
            for course, count in sorted(analysis['by_course'].items(), key=lambda x: x[1], reverse=True):
                print(f"   • {course}: {count} 个作业")
        
        # 所有作业列表
        print(f"\n📋 【所有作业详情】")
        for i, assignment in enumerate(assignments, 1):
            priority = self._calculate_priority(assignment)
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
            urgency = self._calculate_urgency(assignment, datetime.now())
            urgency_emoji = {'urgent': '🔥', 'soon': '⚠️', 'later': '🟢'}[urgency]
            
            print(f"\n   {i}. {urgency_emoji} {assignment['title'][:80]}")
            print(f"      ⏰ 截止: {assignment['due_date']}")
            print(f"      📊 状态: {assignment['status']} | {priority_emoji} {priority.upper()}优先级")
            
            if self.debug and 'selector_used' in assignment:
                print(f"      🔧 检测方式: {assignment['selector_used']}")
        
        print(f"\n⚠️  【重要提醒】")
        print("   • 请及时登录ManageBac网站确认作业状态")
        print("   • 以上结果可能包含已提交但系统未更新的作业")
        print("   • 建议优先处理紧急和高优先级的作业")
    
    def _display_summary(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any], saved_files: Dict[str, str]) -> None:
        """
        显示总结信息。
        """
        print(f"\n\n📁 【报告文件生成】")
        if saved_files:
            for format_type, filepath in saved_files.items():
                print(f"   • {format_type.upper()}报告: {filepath}")
                
                # 提供打开指令
                if format_type == 'html':
                    print(f"     ↳ 浏览器打开: open '{filepath}'")
                elif format_type == 'json':
                    print(f"     ↳ 查看内容: cat '{filepath}'")
                elif format_type == 'markdown':
                    print(f"     ↳ 查看内容: cat '{filepath}'")
        else:
            print("   没有生成额外的报告文件")
        
        # 显示下次运行建议
        print(f"\n🔄 【后续操作建议】")
        if assignments:
            if analysis['urgent_count'] > 0:
                print(f"   😨 优先处理 {analysis['urgent_count']} 个紧急作业")
            print("   ⏰ 建议每日运行此脚本检查更新")
            print("   📚 访问 ManageBac 网站完成作业提交")
        else:
            print("   🎉 太棒了！没有待办作业")
            print("   ⏰ 建议明天再次检查")
        
        print(f"\n⏱️  检查完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("═"*80)
        print("🚀 ManageBac Assignment Checker - 让作业管理更简单！")
        print("═"*80)
    async def run(self):
        """
        Main method to run the ManageBac checker.
        """
        print("=== ManageBac Assignment Checker ===")
        print(f"Target URL: {self.url}")
        print(f"Email: {self.email}")
        print(f"Headless mode: {self.headless}")
        print()
        
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            try:
                # Create new page
                page = await browser.new_page()
                
                # Set viewport size
                await page.set_viewport_size({'width': 1280, 'height': 720})
                
                # Attempt login
                if not await self.login(page):
                    print("Login failed. Please check your credentials.")
                    return
                
                # 等待页面完全加载
                await page.wait_for_timeout(3000)
                
                # 如果开启了调试模式或页面探索，先探索页面结构
                if self.debug or not self.headless:
                    await self.explore_page_structure(page)
                
                # 尝试导航到作业页面
                navigation_success = await self.navigate_to_assignments(page)
                
                if navigation_success:
                    print("\n成功导航到作业页面，等待内容加载...")
                    await page.wait_for_timeout(3000)
                    
                    # 如果导航成功，再次探索页面结构
                    if self.debug:
                        await self.explore_page_structure(page)
                
                # 抓取全部作业（包含已提交/未提交）
                assignments = await self.get_all_assignments(page, browser)
                
                # 分析作业数据
                analysis = self.analyze_assignments(assignments)
                
                # 生成多种格式的报告
                reports = self.generate_reports(assignments, analysis)
                
        # 显示控制台结果
                self._display_console_results(assignments, analysis)
                
                # 保存报告文件
                saved_files = self.save_reports(reports)
                
                # 发送邮件通知（如果启用）
                if self.enable_notifications and assignments:
                    await self.send_email_notification(assignments, analysis)
                
                # 显示总结信息
                self._display_summary(assignments, analysis, saved_files)

                # 如果生成了HTML报告，提示用默认浏览器打开
                if 'html' in saved_files:
                    print(f"\n➡️  自动打开HTML报告...")
                    try:
                        import webbrowser
                        webbrowser.open(saved_files['html'])
                    except Exception as e:
                        if self.debug:
                            print(f"无法自动打开浏览器: {e}")
                
            finally:
                await browser.close()


async def main():
    """Main entry point."""
    checker = ManageBacChecker()
    await checker.run()


if __name__ == '__main__':
    asyncio.run(main())