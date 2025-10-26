#!/usr/bin/env python3
"""
Fixed Assignment Detection Tester
修复的作业检测测试工具

Tests the assignment detection logic with correct API usage
使用正确的API测试作业检测逻辑
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️ python-dotenv not available, relying on system environment")


def setup_test_logging():
    """Setup logging for testing"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_assignment.log')
        ]
    )
    return logging.getLogger(__name__)


def test_config_loading():
    """Test configuration loading with correct attribute names"""
    print("🔍 Testing Configuration Loading...")
    print("="*50)

    try:
        from managebac_checker.config import Config

        # First try to load from environment
        try:
            config = Config.from_environment()
            print(f"✅ Config loaded from environment")
        except ValueError as e:
            print(f"⚠️ Environment config failed: {e}")
            print("📝 Checking .env file...")

            # Check .env file
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    env_content = f.read()
                    print("📄 .env file contents (redacted):")
                    for line in env_content.split('\n'):
                        if '=' in line and not line.strip().startswith('#'):
                            key, value = line.split('=', 1)
                            if 'PASSWORD' in key.upper():
                                print(f"   {key}=***")
                            elif 'EMAIL' in key.upper() and 'example.com' in value:
                                print(f"   {key}={value} ⚠️ (example credential)")
                            else:
                                print(f"   {key}={value}")

                # Try with manual values from .env
                os.environ.setdefault('MANAGEBAC_EMAIL', 'test@example.com')
                os.environ.setdefault('MANAGEBAC_PASSWORD', 'test')
                config = Config.from_environment()
                print(f"✅ Config loaded with defaults")

        print(f"📧 Email: {config.email[:15] if config.email else 'Not set'}...")
        print(f"🌐 URL: {config.url}")
        print(f"🗂️ Output dir: {config.output_dir}")
        print(f"📋 Report formats: {config.report_formats}")
        print(f"🔒 Headless mode: {config.headless}")

        # Check if using example credentials
        if config.email and 'example.com' in config.email:
            print("⚠️ WARNING: Still using example credentials!")
            print("💡 Please update .env file with real ManageBac credentials")
            return False, config
        elif not config.email:
            print("⚠️ WARNING: No email configured!")
            return False, config
        else:
            print("✅ Real credentials appear to be configured")
            return True, config

    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_scraper_creation():
    """Test scraper creation with correct parameters"""
    print("\n🕷️ Testing Scraper Creation...")
    print("="*50)

    try:
        from managebac_checker.config import Config
        from managebac_checker.scraper import ManageBacScraper

        # Setup logger
        logger = setup_test_logging()

        # Load config
        try:
            config = Config.from_environment()
        except ValueError:
            os.environ.setdefault('MANAGEBAC_EMAIL', 'test@example.com')
            os.environ.setdefault('MANAGEBAC_PASSWORD', 'test')
            config = Config.from_environment()

        # Create scraper with correct parameters
        scraper = ManageBacScraper(config, logger)

        print("✅ ManageBacScraper created successfully")
        print(f"🌐 Target URL: {config.url}")
        print(f"🔐 Email configured: {bool(config.email)}")
        print(f"🗝️ Password configured: {bool(config.password)}")

        return True, scraper, config

    except Exception as e:
        print(f"❌ Scraper creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None


async def test_assignment_fetching_manual():
    """Test assignment fetching with manual debugging"""
    print("\n📚 Testing Assignment Fetching (Manual Debug)...")
    print("="*50)

    try:
        from managebac_checker.config import Config
        from managebac_checker.scraper import ManageBacScraper
        from playwright.async_api import async_playwright

        # Setup
        logger = setup_test_logging()

        try:
            config = Config.from_environment()
        except ValueError:
            print("⚠️ Using test credentials - real test requires actual ManageBac account")
            return False

        if 'example.com' in config.email:
            print("⚠️ Cannot test with example credentials")
            return False

        print(f"🔐 Testing with email: {config.email[:15]}...")

        # Create scraper
        scraper = ManageBacScraper(config, logger)

        # Use Playwright directly for better debugging
        async with async_playwright() as p:
            print("🚀 Launching browser...")
            browser = await p.chromium.launch(headless=config.headless)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                print("🔐 Attempting login...")
                login_success = await scraper.login(page)

                if login_success:
                    print("✅ Login successful!")

                    print("🔍 Looking for assignments...")

                    # Try multiple approaches to find assignments
                    assignment_selectors = [
                        "div.assignment",
                        "div.assignment-card",
                        "div.task-item",
                        "li.assignment",
                        "li.assignment-item",
                        "tr.assignment",
                        ".task",
                        ".assignment",
                        "[data-assignment]",
                        ".homework",
                        ".homework-item"
                    ]

                    assignments_found = []

                    for selector in assignment_selectors:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            print(f"✅ Found {len(elements)} elements with selector: {selector}")
                            assignments_found.extend(elements)

                    if assignments_found:
                        print(f"📊 Total assignment elements found: {len(assignments_found)}")

                        # Try to extract details from first few
                        for i, element in enumerate(assignments_found[:3]):
                            text = await element.text_content()
                            print(f"   Assignment {i+1}: {text[:100]}...")

                    else:
                        print("⚠️ No assignment elements found with standard selectors")
                        print("🔍 Let's check the page content...")

                        # Check page title and URL
                        title = await page.title()
                        url = page.url
                        print(f"📄 Page title: {title}")
                        print(f"🔗 Current URL: {url}")

                        # Look for any content that might be assignments
                        page_content = await page.content()
                        assignment_keywords = ["作业", "assignment", "homework", "task", "due", "deadline"]

                        for keyword in assignment_keywords:
                            if keyword in page_content.lower():
                                print(f"✅ Found keyword '{keyword}' in page content")
                            else:
                                print(f"❌ Keyword '{keyword}' not found in page content")

                        # Check if we're actually on the right page
                        if "managebac" not in url.lower():
                            print("⚠️ Warning: Not on a ManageBac page after login")

                        print("🔍 Saving page content for manual inspection...")
                        with open('debug_page_content.html', 'w', encoding='utf-8') as f:
                            f.write(page_content)
                        print("💾 Page content saved to debug_page_content.html")

                    return len(assignments_found) > 0

                else:
                    print("❌ Login failed")
                    return False

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Assignment fetching test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_checker_class():
    """Test the main checker class"""
    print("\n🔍 Testing Main Checker Class...")
    print("="*50)

    try:
        from managebac_checker.checker import ManageBacChecker
        from managebac_checker.config import Config

        # Setup config
        try:
            config = Config.from_environment()
        except ValueError:
            os.environ.setdefault('MANAGEBAC_EMAIL', 'test@example.com')
            os.environ.setdefault('MANAGEBAC_PASSWORD', 'test')
            config = Config.from_environment()

        # Create checker
        checker = ManageBacChecker(config)
        print("✅ ManageBacChecker created successfully")

        return True, checker

    except Exception as e:
        print(f"❌ Checker class test failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


async def run_comprehensive_assignment_test():
    """Run all assignment-related tests"""
    print("🚀 Fixed Assignment Detection Test")
    print("🚀 修复的作业检测测试")
    print("="*60)

    results = {}

    # Test configuration
    config_ok, config = test_config_loading()
    results['config'] = config_ok

    # Test scraper creation
    scraper_ok, scraper, _ = test_scraper_creation()
    results['scraper'] = scraper_ok

    # Test checker class
    checker_ok, checker = test_checker_class()
    results['checker'] = checker_ok

    # Test assignment fetching if configuration is OK
    if config_ok and scraper_ok and config and 'example.com' not in config.email:
        print("\n🎯 Real credentials found, testing assignment fetching...")
        results['assignments'] = await test_assignment_fetching_manual()
    else:
        print("⚠️ Skipping assignment fetching test")
        if not config_ok:
            print("   Reason: Configuration issues")
        elif config and 'example.com' in config.email:
            print("   Reason: Using example credentials")
        results['assignments'] = False

    # Generate report
    print("\n" + "="*60)
    print("📊 FIXED ASSIGNMENT DETECTION TEST REPORT")
    print("📊 修复的作业检测测试报告")
    print("="*60)

    test_names = {
        'config': 'Configuration Loading 配置加载',
        'scraper': 'Scraper Creation 爬虫创建',
        'checker': 'Checker Class 检查器类',
        'assignments': 'Assignment Fetching 作业获取'
    }

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        display_name = test_names.get(test_name, test_name)
        print(f"{status} {display_name}")

    failed_tests = [name for name, passed in results.items() if not passed]

    if not failed_tests:
        print("\n🎉 All tests passed!")
        print("🎉 所有测试通过！")
    else:
        print(f"\n⚠️ {len(failed_tests)} test(s) failed:")
        print(f"⚠️ {len(failed_tests)}个测试失败：")

        if 'config' in failed_tests:
            print("   🔧 Fix: Update .env with real ManageBac credentials")
            print("   🔧 修复：在.env中更新真实的ManageBac凭据")

        if 'assignments' in failed_tests and 'config' not in failed_tests:
            print("   🔧 Fix: Check debug_page_content.html for website structure")
            print("   🔧 修复：检查debug_page_content.html了解网站结构")

    print(f"\n💡 Recommendations 建议:")
    print(f"1. Update .env file with real credentials 使用真实凭据更新.env文件")
    print(f"2. Check debug_page_content.html if fetching failed 如果获取失败请检查调试文件")
    print(f"3. Verify ManageBac website hasn't changed structure 验证ManageBac网站结构未变化")

    return len(failed_tests) == 0


if __name__ == "__main__":
    success = asyncio.run(run_comprehensive_assignment_test())
    print(f"\n🏁 Test completed: {'SUCCESS' if success else 'ISSUES FOUND'}")
    print(f"🏁 测试完成：{'成功' if success else '发现问题'}")
    sys.exit(0 if success else 1)