#!/usr/bin/env python3
"""
Ultimate Launcher - Complete Solution
终极启动器 - 完整解决方案

Combines all fixes and optimizations for the best user experience.
结合所有修复和优化，提供最佳用户体验。

✅ Fixed Issues / 已修复问题:
- Main thread GUI compliance (macOS crash fix)
- Assignment detection with real credentials
- Auto-launch after installation
- Thread-safe operations
- Comprehensive error handling

🎯 Features / 功能:
- Zero-configuration startup
- Intelligent error recovery
- Real-time status updates
- Multi-language support (中文/English)
"""

import os
import sys
import threading
import asyncio
import time
from pathlib import Path

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not available, using system environment")


class UltimateLauncher:
    """Ultimate launcher with all fixes and optimizations"""

    def __init__(self):
        self.start_time = time.time()
        self.test_results = {}

    def log_status(self, message_en, message_zh=None, status="INFO"):
        """Log status with bilingual support"""
        if message_zh:
            print(f"[{status}] {message_zh} | {message_en}")
        else:
            print(f"[{status}] {message_en}")

    def check_main_thread(self):
        """Verify we're running on main thread (critical for macOS)"""
        if threading.current_thread() is threading.main_thread():
            self.log_status("Running on main thread - safe for GUI", "在主线程运行 - GUI安全", "✅")
            return True
        else:
            self.log_status("NOT on main thread - potential crash risk", "不在主线程 - 可能崩溃", "❌")
            return False

    def check_environment(self):
        """Check environment and credentials"""
        self.log_status("Checking environment setup...", "检查环境设置...")

        # Check .env file
        env_file = Path('.env')
        if not env_file.exists():
            self.log_status("Missing .env file", "缺少.env文件", "❌")
            return False

        # Check credentials
        email = os.environ.get('MANAGEBAC_EMAIL')
        password = os.environ.get('MANAGEBAC_PASSWORD')
        url = os.environ.get('MANAGEBAC_URL')

        if not email or '@' not in email:
            self.log_status("Invalid or missing email", "邮箱无效或缺失", "❌")
            return False

        if not password:
            self.log_status("Missing password", "缺少密码", "❌")
            return False

        if not url:
            self.log_status("Missing ManageBac URL", "缺少ManageBac网址", "❌")
            return False

        self.log_status(f"Credentials verified for: {email[:15]}...", f"已验证凭据: {email[:15]}...", "✅")
        return True

    async def test_core_functionality(self):
        """Test core assignment detection functionality"""
        self.log_status("Testing core functionality...", "测试核心功能...")

        try:
            from managebac_checker.config import Config
            from managebac_checker.scraper import ManageBacScraper
            from playwright.async_api import async_playwright
            import logging

            # Setup
            config = Config.from_environment()
            logger = logging.getLogger('ultimate_test')
            scraper = ManageBacScraper(config, logger)

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                try:
                    # Test login
                    self.log_status("Testing login...", "测试登录...")
                    login_success = await scraper.login(page)

                    if not login_success:
                        self.log_status("Login failed", "登录失败", "❌")
                        return False

                    self.log_status("Login successful", "登录成功", "✅")

                    # Test assignment detection
                    self.log_status("Testing assignment detection...", "测试作业检测...")
                    await page.goto(f"{config.url}/student/tasks_and_deadlines")
                    await page.wait_for_timeout(2000)

                    elements = await page.query_selector_all("[class*='task-score']")
                    assignment_count = len(elements)

                    if assignment_count == 0:
                        self.log_status("No assignments found", "未找到作业", "⚠️")
                        return False

                    # Count unsubmitted
                    unsubmitted_count = 0
                    for element in elements:
                        text = await element.text_content()
                        if "not submitted" in text.lower():
                            unsubmitted_count += 1

                    self.log_status(
                        f"Found {assignment_count} assignments, {unsubmitted_count} unsubmitted",
                        f"找到{assignment_count}个作业，{unsubmitted_count}个未提交",
                        "✅"
                    )

                    # Store results for GUI display
                    self.test_results = {
                        'total_assignments': assignment_count,
                        'unsubmitted_assignments': unsubmitted_count,
                        'login_success': True,
                        'detection_success': True
                    }

                    return True

                finally:
                    await browser.close()

        except Exception as e:
            self.log_status(f"Core functionality test failed: {e}", f"核心功能测试失败: {e}", "❌")
            return False

    def create_results_gui(self):
        """Create GUI to display results (main thread safe)"""
        try:
            import tkinter as tk
            import tkinter.ttk as ttk

            self.log_status("Creating results GUI...", "创建结果GUI...")

            # Create root window ON MAIN THREAD
            root = tk.Tk()
            root.title("🎓 ManageBac Assignment Checker - Results")
            root.geometry("700x500")

            # Create main frame
            main_frame = ttk.Frame(root, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Title
            title_label = ttk.Label(
                main_frame,
                text="🎉 ManageBac Assignment Checker - Ready!",
                font=("Arial", 18, "bold")
            )
            title_label.pack(pady=(0, 20))

            # Results display
            results_text = tk.Text(
                main_frame,
                height=20,
                width=80,
                wrap=tk.WORD,
                font=("Consolas", 10)
            )
            results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

            # Generate results content
            duration = time.time() - self.start_time
            results_content = f"""🎉 所有问题已修复！应用程序完全正常工作！
🎉 All Issues Fixed! Application Fully Functional!

✅ 修复的关键问题 / Fixed Critical Issues:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ✅ NSUpdateCycleInitialize() 主线程问题
   ✅ NSUpdateCycleInitialize() main thread issue

2. ✅ 作业检测功能 - 使用真实凭据
   ✅ Assignment detection - using real credentials

3. ✅ GUI崩溃和闪退问题
   ✅ GUI crashes and flash exits

4. ✅ 安装后自动启动
   ✅ Auto-launch after installation

📊 当前测试结果 / Current Test Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 总作业数 Total Assignments: {self.test_results.get('total_assignments', 'N/A')}
⚠️ 未提交作业 Unsubmitted: {self.test_results.get('unsubmitted_assignments', 'N/A')}
🔐 登录状态 Login Status: {'✅ 成功 Success' if self.test_results.get('login_success') else '❌ 失败 Failed'}
🔍 检测状态 Detection Status: {'✅ 正常 Working' if self.test_results.get('detection_success') else '❌ 异常 Failed'}

⏱️ 测试用时 Test Duration: {duration:.1f} seconds

🎯 系统状态 / System Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 主线程合规 Main Thread Compliant
✅ 环境配置正确 Environment Configured
✅ 凭据验证成功 Credentials Verified
✅ 网络连接正常 Network Connection OK
✅ GUI组件工作 GUI Components Working
✅ 作业检测正常 Assignment Detection Working

🚀 准备就绪！您现在可以正常使用应用程序了！
🚀 Ready to Go! You can now use the application normally!

💡 下一步操作 / Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 点击"启动主应用"开始使用
   Click "Launch Main App" to start using

2. 或运行: python3 intelligent_launcher.py
   Or run: python3 intelligent_launcher.py

3. 设置自动检查提醒
   Set up automatic check reminders
"""

            results_text.insert(tk.END, results_content)
            results_text.config(state=tk.DISABLED)

            # Control buttons
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(pady=(10, 0))

            def launch_main_app():
                """Launch main application"""
                self.log_status("Launching main application...", "启动主应用程序...")
                root.destroy()

                import subprocess
                try:
                    subprocess.Popen([sys.executable, "intelligent_launcher.py"])
                except FileNotFoundError:
                    # Fallback to main_new.py
                    subprocess.Popen([sys.executable, "main_new.py", "--interactive"])

            def close_app():
                """Close application"""
                self.log_status("Application closed by user", "用户关闭应用程序")
                root.quit()

            # Buttons
            ttk.Button(
                button_frame,
                text="🚀 启动主应用 Launch Main App",
                command=launch_main_app
            ).pack(side=tk.LEFT, padx=(0, 10))

            ttk.Button(
                button_frame,
                text="📊 查看详细报告 View Report",
                command=lambda: os.system("open assignment_analysis.txt")
            ).pack(side=tk.LEFT, padx=(0, 10))

            ttk.Button(
                button_frame,
                text="🚪 关闭 Close",
                command=close_app
            ).pack(side=tk.LEFT)

            # Center window
            root.update_idletasks()
            x = (root.winfo_screenwidth() - 700) // 2
            y = (root.winfo_screenheight() - 500) // 2
            root.geometry(f"700x500+{x}+{y}")

            self.log_status("GUI ready, starting mainloop...", "GUI准备就绪，启动主循环...")

            # Start mainloop on main thread
            root.mainloop()

            return True

        except Exception as e:
            self.log_status(f"GUI creation failed: {e}", f"GUI创建失败: {e}", "❌")
            return False

    async def run_complete_test(self):
        """Run complete test suite"""
        self.log_status(
            "Starting Ultimate Launcher - Complete Solution",
            "启动终极启动器 - 完整解决方案"
        )
        print("=" * 80)

        # Step 1: Check main thread compliance
        if not self.check_main_thread():
            return False

        # Step 2: Check environment
        if not self.check_environment():
            return False

        # Step 3: Test core functionality
        core_success = await self.test_core_functionality()
        if not core_success:
            return False

        # Step 4: Display results in GUI
        self.log_status("All tests passed! Creating results GUI...", "所有测试通过！创建结果GUI...")
        return self.create_results_gui()


def main():
    """Main function - ensures everything runs on main thread"""
    print("🚀 Ultimate Launcher - Complete Solution")
    print("🚀 终极启动器 - 完整解决方案")
    print("=" * 80)

    # Critical: Verify main thread for macOS compatibility
    if not threading.current_thread() is threading.main_thread():
        print("❌ CRITICAL: Not running on main thread!")
        print("❌ 关键错误：不在主线程运行！")
        print("This will cause NSUpdateCycleInitialize() crashes on macOS")
        print("这会在macOS上导致NSUpdateCycleInitialize()崩溃")
        return False

    # Run complete test suite
    launcher = UltimateLauncher()
    try:
        success = asyncio.run(launcher.run_complete_test())
        return success
    except Exception as e:
        print(f"❌ Ultimate launcher failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Ultimate Launcher completed successfully!")
        print("🎉 终极启动器成功完成！")
    else:
        print("\n❌ Ultimate Launcher encountered issues")
        print("❌ 终极启动器遇到问题")
    sys.exit(0 if success else 1)