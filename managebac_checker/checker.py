"""
主要的ManageBac检查器类
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


class ManageBacChecker:
    """ManageBac作业检查器主类"""
    
    def __init__(self):
        """初始化检查器"""
        self.config = Config()
        self.scraper = ManageBacScraper(self.config)
        self.analyzer = AssignmentAnalyzer(self.config)
        self.reporter = ReportGenerator(self.config)
        self.notifications = NotificationManager(self.config)
    
    async def run(self):
        """运行主要的检查流程"""
        print("=== ManageBac Assignment Checker ===")
        print(f"目标URL: {self.config.url}")
        print(f"邮箱: {self.config.email}")
        print(f"无头模式: {self.config.headless}")
        print()
        
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=self.config.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            try:
                # 创建新页面
                page = await browser.new_page()
                
                # 设置视口大小
                await page.set_viewport_size({'width': 1280, 'height': 720})
                
                # 尝试登录
                if not await self.scraper.login(page):
                    print("登录失败。请检查您的凭据。")
                    return
                
                # 等待页面完全加载
                await page.wait_for_timeout(3000)
                
                # 如果开启了调试模式，先探索页面结构
                if self.config.debug or not self.config.headless:
                    await self.scraper.explore_page_structure(page)
                
                # 尝试导航到作业页面
                navigation_success = await self.scraper.navigate_to_assignments(page)
                
                if navigation_success:
                    print("\n成功导航到作业页面，等待内容加载...")
                    await page.wait_for_timeout(3000)
                    
                    # 如果导航成功，再次探索页面结构
                    if self.config.debug:
                        await self.scraper.explore_page_structure(page)
                
                # 抓取全部作业（包含已提交/未提交）
                assignments = await self.scraper.get_all_assignments(page, browser)
                
                # 分析作业数据
                analysis = self.analyzer.analyze_assignments(assignments)
                
                # 生成多种格式的报告
                reports = self.reporter.generate_reports(assignments, analysis)
                
                # 显示控制台结果
                self._display_console_results(assignments, analysis)
                
                # 保存报告文件
                saved_files = self.reporter.save_reports(reports)
                
                # 发送邮件通知（如果启用）
                if self.config.is_notification_enabled() and assignments:
                    await self.notifications.send_email_notification(assignments, analysis)
                
                # 显示总结信息
                self._display_summary(assignments, analysis, saved_files)

                # 如果生成了HTML报告，提示用默认浏览器打开
                if 'html' in saved_files:
                    print(f"\n➡️  自动打开HTML报告...")
                    try:
                        webbrowser.open(saved_files['html'])
                    except Exception as e:
                        if self.config.debug:
                            print(f"无法自动打开浏览器: {e}")
                
            finally:
                await browser.close()
    
    def _display_console_results(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any]) -> None:
        """在控制台显示结果"""
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
            priority = self.analyzer._calculate_priority(assignment)
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[priority]
            urgency = self.analyzer._calculate_urgency(assignment, datetime.now())
            urgency_emoji = {'urgent': '🔥', 'soon': '⚠️', 'later': '🟢'}[urgency]
            
            print(f"\n   {i}. {urgency_emoji} {assignment['title'][:80]}")
            print(f"      ⏰ 截止: {assignment['due_date']}")
            print(f"      📊 状态: {assignment['status']} | {priority_emoji} {priority.upper()}优先级")
            
            if self.config.debug and 'selector_used' in assignment:
                print(f"      🔧 检测方式: {assignment['selector_used']}")
        
        print(f"\n⚠️  【重要提醒】")
        print("   • 请及时登录ManageBac网站确认作业状态")
        print("   • 以上结果可能包含已提交但系统未更新的作业")
        print("   • 建议优先处理紧急和高优先级的作业")
    
    def _display_summary(self, assignments: List[Dict[str, Any]], analysis: Dict[str, Any], saved_files: Dict[str, str]) -> None:
        """显示总结信息"""
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
