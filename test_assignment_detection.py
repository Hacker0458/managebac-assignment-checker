#!/usr/bin/env python3
"""
Assignment Detection Tester
作业检测测试工具

Tests the assignment detection logic without GUI
测试作业检测逻辑（无GUI版本）
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

import pytest


RUN_INTEGRATION_TESTS = os.getenv("MANAGEBAC_RUN_INTEGRATION_TESTS") == "1"

if not RUN_INTEGRATION_TESTS:
    pytestmark = pytest.mark.skip(
        reason="Manual integration diagnostics disabled without MANAGEBAC_RUN_INTEGRATION_TESTS=1"
    )


def test_config_loading():
    """Test configuration loading"""
    print("🔍 Testing Configuration Loading...")
    print("="*50)

    try:
        from managebac_checker.config import Config
        config = Config(interactive=False)

        print(f"✅ Config loaded successfully")
        print(f"📧 Email: {config.managebac_email[:10] if config.managebac_email else 'Not set'}...")
        print(f"🌐 URL: {config.managebac_url if config.managebac_url else 'Not set'}")
        print(f"🗂️ Output dir: {config.output_dir}")
        print(f"📋 Report format: {config.report_format}")

        # Check if using example credentials
        if (config.managebac_email and 'example.com' in config.managebac_email):
            print("⚠️ WARNING: Still using example credentials!")
            print("💡 Please update .env file with real ManageBac credentials")
            return False
        elif not config.managebac_email:
            print("⚠️ WARNING: No email configured!")
            return False
        else:
            print("✅ Real credentials appear to be configured")
            return True

    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scraper_creation():
    """Test scraper creation"""
    print("\n🕷️ Testing Scraper Creation...")
    print("="*50)

    try:
        from managebac_checker.config import Config
        from managebac_checker.scraper import ManageBacScraper

        config = Config(interactive=False)
        scraper = ManageBacScraper(config)

        print("✅ ManageBacScraper created successfully")
        print(f"🌐 Target URL: {scraper.base_url}")
        print(f"🔐 Email configured: {bool(scraper.email)}")
        print(f"🗝️ Password configured: {bool(scraper.password)}")

        return True

    except Exception as e:
        print(f"❌ Scraper creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_assignment_fetching():
    """Test actual assignment fetching"""
    print("\n📚 Testing Assignment Fetching...")
    print("="*50)

    try:
        from managebac_checker.config import Config
        from managebac_checker.checker import ManageBacChecker

        config = Config(interactive=False)

        # Check credentials first
        if not config.managebac_email or 'example.com' in config.managebac_email:
            print("⚠️ Cannot test fetching with example credentials")
            print("💡 Configure real credentials in .env to test assignment fetching")
            return False

        print("🚀 Creating checker...")
        checker = ManageBacChecker(config)

        print("🔐 Testing authentication...")
        # Run the check
        try:
            result = await checker.check_assignments()

            print(f"📊 Check completed!")
            print(f"✅ Total assignments found: {len(result.get('assignments', []))}")

            assignments = result.get('assignments', [])
            if assignments:
                print(f"📋 Assignment details:")
                for i, assignment in enumerate(assignments[:5], 1):  # Show first 5
                    title = assignment.get('title', 'Unknown')
                    subject = assignment.get('subject', 'Unknown')
                    due_date = assignment.get('due_date', 'Unknown')
                    status = assignment.get('status', 'Unknown')
                    print(f"   {i}. {title} ({subject}) - Due: {due_date} - Status: {status}")

                if len(assignments) > 5:
                    print(f"   ... and {len(assignments) - 5} more")
            else:
                print("⚠️ No assignments found!")
                print("🔍 This could mean:")
                print("   1. No assignments are currently available")
                print("   2. All assignments are completed")
                print("   3. Assignment detection logic needs improvement")
                print("   4. Website structure has changed")

            return len(assignments) > 0

        except Exception as e:
            print(f"❌ Assignment fetching failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"❌ Assignment test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_debug_mode():
    """Test in debug mode to see more details"""
    print("\n🐛 Testing Debug Mode...")
    print("="*50)

    try:
        # Enable debug mode temporarily
        os.environ['DEBUG'] = 'true'

        from managebac_checker.config import Config
        config = Config(interactive=False)

        print(f"✅ Debug mode enabled")
        print(f"🔍 Debug level: {config.debug}")

        return True

    except Exception as e:
        print(f"❌ Debug mode test failed: {e}")
        return False


def check_website_accessibility():
    """Check if ManageBac website is accessible"""
    print("\n🌐 Testing Website Accessibility...")
    print("="*50)

    try:
        import requests
        from managebac_checker.config import Config

        config = Config(interactive=False)

        if not config.managebac_url:
            print("⚠️ No ManageBac URL configured")
            return False

        print(f"🔗 Testing URL: {config.managebac_url}")

        # Test basic connectivity
        response = requests.get(config.managebac_url, timeout=10)
        print(f"✅ Website accessible - Status: {response.status_code}")

        # Check if it looks like ManageBac
        if 'managebac' in response.text.lower():
            print("✅ Appears to be a ManageBac site")
        else:
            print("⚠️ Website doesn't appear to be ManageBac")

        return response.status_code == 200

    except ImportError:
        print("⚠️ requests library not available - cannot test website")
        return False
    except Exception as e:
        print(f"❌ Website accessibility test failed: {e}")
        return False


def run_comprehensive_assignment_test():
    """Run all assignment-related tests"""
    print("🚀 Assignment Detection Comprehensive Test")
    print("🚀 作业检测综合测试")
    print("="*60)

    results = {}

    # Test configuration
    results['config'] = test_config_loading()

    # Test scraper creation
    results['scraper'] = test_scraper_creation()

    # Test website accessibility
    results['website'] = check_website_accessibility()

    # Test debug mode
    results['debug'] = test_debug_mode()

    # Test assignment fetching if other tests pass
    if results['config'] and results['scraper']:
        print("\n🎯 Configuration and scraper OK, testing assignment fetching...")
        try:
            results['assignments'] = asyncio.run(test_assignment_fetching())
        except Exception as e:
            print(f"❌ Assignment fetching test failed: {e}")
            results['assignments'] = False
    else:
        print("⚠️ Skipping assignment fetching due to configuration issues")
        results['assignments'] = False

    # Generate report
    print("\n" + "="*60)
    print("📊 ASSIGNMENT DETECTION TEST REPORT")
    print("📊 作业检测测试报告")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        test_display = {
            'config': 'Configuration Loading',
            'scraper': 'Scraper Creation',
            'website': 'Website Accessibility',
            'debug': 'Debug Mode',
            'assignments': 'Assignment Fetching'
        }.get(test_name, test_name)

        print(f"{status} {test_display}")

    failed_tests = [name for name, passed in results.items() if not passed]

    if not failed_tests:
        print("\n🎉 All tests passed! Assignment detection should work correctly.")
    else:
        print(f"\n⚠️ {len(failed_tests)} test(s) failed:")

        if 'config' in failed_tests:
            print("🔧 Fix: Update .env file with real ManageBac credentials")
        if 'website' in failed_tests:
            print("🔧 Fix: Check internet connection and ManageBac URL")
        if 'assignments' in failed_tests and 'config' not in failed_tests:
            print("🔧 Fix: Assignment detection logic may need updating")
            print("     This could be due to ManageBac website changes")

    print(f"\n💡 Next steps:")
    print(f"1. If config failed: Update .env with real credentials")
    print(f"2. If assignment fetching failed: Run with debug mode for more details")
    print(f"3. For GUI issues: Use 'python3 fixed_gui.py' for testing")

    return len(failed_tests) == 0


if __name__ == "__main__":
    run_comprehensive_assignment_test()