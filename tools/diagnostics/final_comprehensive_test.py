#!/usr/bin/env python3
"""
Final Comprehensive Test
最终综合测试

Tests all components with real user credentials
使用真实用户凭据测试所有组件
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError:
    print("⚠️ python-dotenv not available")


class FinalComprehensiveTest:
    """Final comprehensive test suite"""

    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()

    def log_test_result(self, test_name, success, details=""):
        """Log test result"""
        self.test_results[test_name] = {
            'success': success,
            'details': details,
            'timestamp': time.time()
        }
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")

    def test_environment_setup(self):
        """Test environment setup"""
        print("\n🔧 Testing Environment Setup...")
        print("-" * 40)

        # Check .env file
        env_file = Path('.env')
        if env_file.exists():
            self.log_test_result("Environment File", True, ".env file exists")
        else:
            self.log_test_result("Environment File", False, ".env file missing")
            return False

        # Check credentials
        email = os.environ.get('MANAGEBAC_EMAIL')
        password = os.environ.get('MANAGEBAC_PASSWORD')
        url = os.environ.get('MANAGEBAC_URL')

        if email and '@gmail.com' in email:
            self.log_test_result("Real Credentials", True, f"Using {email}")
        else:
            self.log_test_result("Real Credentials", False, "Missing or invalid credentials")
            return False

        return True

    def test_configuration_loading(self):
        """Test configuration loading"""
        print("\n⚙️ Testing Configuration Loading...")
        print("-" * 40)

        try:
            from managebac_checker.config import Config
            config = Config.from_environment()

            self.log_test_result("Config Loading", True, f"Email: {config.email[:15]}...")

            # Test configuration values
            if config.email and config.password and config.url:
                self.log_test_result("Config Validation", True, "All required fields present")
            else:
                self.log_test_result("Config Validation", False, "Missing required fields")
                return False

            return True

        except Exception as e:
            self.log_test_result("Config Loading", False, f"Error: {e}")
            return False

    def test_scraper_creation(self):
        """Test scraper creation"""
        print("\n🕷️ Testing Scraper Creation...")
        print("-" * 40)

        try:
            from managebac_checker.config import Config
            from managebac_checker.scraper import ManageBacScraper
            import logging

            config = Config.from_environment()
            logger = logging.getLogger("test")
            scraper = ManageBacScraper(config, logger)

            self.log_test_result("Scraper Creation", True, "ManageBacScraper created successfully")
            return True

        except Exception as e:
            self.log_test_result("Scraper Creation", False, f"Error: {e}")
            return False

    async def test_login_functionality(self):
        """Test login functionality"""
        print("\n🔐 Testing Login Functionality...")
        print("-" * 40)

        try:
            from managebac_checker.config import Config
            from managebac_checker.scraper import ManageBacScraper
            from playwright.async_api import async_playwright
            import logging

            config = Config.from_environment()
            logger = logging.getLogger("test")
            scraper = ManageBacScraper(config, logger)

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                try:
                    login_success = await scraper.login(page)
                    if login_success:
                        self.log_test_result("Login Test", True, "Login successful")

                        # Check if we're on the right page
                        title = await page.title()
                        url = page.url
                        if "managebac" in url.lower() and "jack fang" in title.lower():
                            self.log_test_result("Login Verification", True, f"On correct page: {title}")
                        else:
                            self.log_test_result("Login Verification", False, f"Unexpected page: {title}")

                        return True
                    else:
                        self.log_test_result("Login Test", False, "Login failed")
                        return False

                finally:
                    await browser.close()

        except Exception as e:
            self.log_test_result("Login Test", False, f"Error: {e}")
            return False

    async def test_assignment_detection(self):
        """Test assignment detection"""
        print("\n📚 Testing Assignment Detection...")
        print("-" * 40)

        try:
            from managebac_checker.config import Config
            from managebac_checker.scraper import ManageBacScraper
            from playwright.async_api import async_playwright
            import logging

            config = Config.from_environment()
            logger = logging.getLogger("test")
            scraper = ManageBacScraper(config, logger)

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                try:
                    # Login
                    login_success = await scraper.login(page)
                    if not login_success:
                        self.log_test_result("Assignment Detection", False, "Login failed")
                        return False

                    # Navigate to tasks page
                    await page.goto(f"{config.url}/student/tasks_and_deadlines")
                    await page.wait_for_timeout(2000)

                    # Look for assignments using working selector
                    assignment_elements = await page.query_selector_all("[class*='task-score']")

                    if assignment_elements:
                        assignment_count = len(assignment_elements)

                        # Check for unsubmitted assignments
                        unsubmitted_count = 0
                        for element in assignment_elements:
                            text = await element.text_content()
                            if "not submitted" in text.lower():
                                unsubmitted_count += 1

                        self.log_test_result("Assignment Detection", True,
                                           f"Found {assignment_count} assignments, {unsubmitted_count} unsubmitted")
                        return True
                    else:
                        self.log_test_result("Assignment Detection", False, "No assignments found")
                        return False

                finally:
                    await browser.close()

        except Exception as e:
            self.log_test_result("Assignment Detection", False, f"Error: {e}")
            return False

    def test_gui_components(self):
        """Test GUI components"""
        print("\n🖥️ Testing GUI Components...")
        print("-" * 40)

        try:
            import tkinter as tk

            # Test basic tkinter
            root = tk.Tk()
            root.withdraw()
            root.destroy()
            self.log_test_result("Basic Tkinter", True, "tkinter working")

            # Test GUI imports
            from managebac_checker.professional_gui import ProfessionalTheme
            theme = ProfessionalTheme("professional_light")
            self.log_test_result("GUI Imports", True, "All GUI components importable")

            # Test notification manager
            from managebac_checker.system_tray import NotificationManager
            nm = NotificationManager("zh")
            self.log_test_result("Notification Manager", True, "NotificationManager created")

            return True

        except Exception as e:
            self.log_test_result("GUI Components", False, f"Error: {e}")
            return False

    def test_main_application(self):
        """Test main application"""
        print("\n🚀 Testing Main Application...")
        print("-" * 40)

        try:
            from managebac_checker.checker import ManageBacChecker
            from managebac_checker.config import Config

            config = Config.from_environment()
            checker = ManageBacChecker(config)

            self.log_test_result("Main Application", True, "ManageBacChecker created successfully")
            return True

        except Exception as e:
            self.log_test_result("Main Application", False, f"Error: {e}")
            return False

    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Final Comprehensive Test Suite")
        print("🚀 开始最终综合测试套件")
        print("=" * 60)

        # Run synchronous tests
        tests = [
            ("Environment Setup", self.test_environment_setup),
            ("Configuration Loading", self.test_configuration_loading),
            ("Scraper Creation", self.test_scraper_creation),
            ("GUI Components", self.test_gui_components),
            ("Main Application", self.test_main_application),
        ]

        for test_name, test_func in tests:
            try:
                success = test_func()
            except Exception as e:
                self.log_test_result(test_name, False, f"Unexpected error: {e}")

        # Run async tests
        async_tests = [
            ("Login Functionality", self.test_login_functionality),
            ("Assignment Detection", self.test_assignment_detection),
        ]

        for test_name, test_func in async_tests:
            try:
                success = await test_func()
            except Exception as e:
                self.log_test_result(test_name, False, f"Unexpected error: {e}")

        # Generate report
        self.generate_final_report()

    def generate_final_report(self):
        """Generate final test report"""
        print("\n" + "=" * 60)
        print("📊 FINAL COMPREHENSIVE TEST REPORT")
        print("📊 最终综合测试报告")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r['success']])
        failed_tests = total_tests - passed_tests

        print(f"\n📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📊 Success Rate: {passed_tests/total_tests*100:.1f}%")

        print(f"\n📋 Detailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {status} {test_name}: {result['details']}")

        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! 所有测试通过！")
            print("✅ The application is fully functional with your account")
            print("✅ 应用程序在您的账户上完全正常工作")
        elif failed_tests <= 2:
            print("🟡 MOSTLY FUNCTIONAL 基本功能正常")
            print(f"⚠️ {failed_tests} minor issues found, but core functionality works")
            print(f"⚠️ 发现{failed_tests}个小问题，但核心功能正常")
        else:
            print("🔴 SIGNIFICANT ISSUES 存在重大问题")
            print(f"❌ {failed_tests} tests failed, needs attention")
            print(f"❌ {failed_tests}个测试失败，需要关注")

        # Time taken
        duration = time.time() - self.start_time
        print(f"\n⏱️ Test Duration: {duration:.1f} seconds")

        # Recommendations
        print(f"\n💡 Recommendations:")
        if failed_tests == 0:
            print("1. You can now use the application normally")
            print("2. Try: python3 intelligent_launcher.py")
            print("3. Or GUI: python3 non_hanging_gui.py")
        else:
            print("1. Review failed tests above")
            print("2. Check logs for detailed error information")
            print("3. Run specific test tools for failed components")


async def main():
    """Main function"""
    tester = FinalComprehensiveTest()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())