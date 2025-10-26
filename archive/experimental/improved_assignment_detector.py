#!/usr/bin/env python3
"""
Improved Assignment Detector
改进的作业检测器

Based on analysis of actual ManageBac page structure
基于实际ManageBac页面结构的分析
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


async def test_improved_assignment_detection():
    """Test improved assignment detection based on page analysis"""
    print("🔍 Testing Improved Assignment Detection...")
    print("🔍 测试改进的作业检测...")
    print("="*60)

    try:
        from managebac_checker.config import Config
        from managebac_checker.scraper import ManageBacScraper
        from playwright.async_api import async_playwright

        # Setup
        logger = logging.getLogger(__name__)
        config = Config.from_environment()

        print(f"🔐 Using account: {config.email}")
        print(f"🌐 Target URL: {config.url}")

        # Create scraper
        scraper = ManageBacScraper(config, logger)

        # Use Playwright
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

                    # Navigate to assignments/tasks page
                    print("📚 Navigating to tasks page...")
                    try:
                        await page.goto(f"{config.url}/student/tasks_and_deadlines",
                                      wait_until="domcontentloaded")
                        await page.wait_for_timeout(2000)
                        print("✅ Tasks page loaded")
                    except Exception as e:
                        print(f"⚠️ Could not navigate to tasks page: {e}")
                        print("Staying on current page...")

                    # Try improved selectors based on page analysis
                    assignment_selectors = [
                        # Based on actual page structure analysis
                        ".f-task-score",  # Found in page
                        "[class*='task-score']",
                        ".badge-label:contains('Homework')",
                        "[class*='homework']",
                        ".js-tasks-tab .card",  # Tasks tab cards
                        ".panel .card",  # Panel cards
                        "[data-test*='task']",
                        "[data-test*='assignment']",
                        # Generic fallbacks
                        ".task-item",
                        ".assignment-item",
                        ".homework-item",
                        ".card:has(.badge-label)",
                        ".panel-body .item"
                    ]

                    assignments_found = []
                    all_assignments_data = []

                    print("🔍 Searching with improved selectors...")
                    for i, selector in enumerate(assignment_selectors, 1):
                        try:
                            elements = await page.query_selector_all(selector)
                            if elements:
                                print(f"✅ Selector {i}: Found {len(elements)} elements with '{selector}'")

                                # Extract details from each element
                                for j, element in enumerate(elements[:5]):  # Limit to first 5 for testing
                                    try:
                                        text = await element.text_content()
                                        html = await element.inner_html()

                                        if text and text.strip():
                                            assignment_data = {
                                                'selector': selector,
                                                'index': j,
                                                'text': text.strip()[:200],  # First 200 chars
                                                'has_homework_keyword': 'homework' in text.lower() or '作业' in text,
                                                'has_due_keyword': any(word in text.lower() for word in ['due', 'deadline', '截止', '到期']),
                                                'html_snippet': html[:100] if html else ''
                                            }
                                            all_assignments_data.append(assignment_data)
                                            print(f"    📋 Element {j+1}: {text.strip()[:100]}...")

                                    except Exception as e:
                                        print(f"    ⚠️ Error extracting element {j}: {e}")

                                assignments_found.extend(elements)
                                break  # Use first working selector
                            else:
                                print(f"❌ Selector {i}: No elements found with '{selector}'")

                        except Exception as e:
                            print(f"❌ Error with selector '{selector}': {e}")

                    # Analysis and reporting
                    print(f"\n📊 Assignment Detection Results:")
                    print(f"   Total elements found: {len(assignments_found)}")
                    print(f"   Assignment data extracted: {len(all_assignments_data)}")

                    if all_assignments_data:
                        print(f"\n📋 Assignment Details:")
                        homework_count = 0
                        due_count = 0

                        for data in all_assignments_data:
                            print(f"\n   📝 Assignment found:")
                            print(f"      Selector: {data['selector']}")
                            print(f"      Text: {data['text']}")
                            print(f"      Has homework keywords: {data['has_homework_keyword']}")
                            print(f"      Has due date keywords: {data['has_due_keyword']}")

                            if data['has_homework_keyword']:
                                homework_count += 1
                            if data['has_due_keyword']:
                                due_count += 1

                        print(f"\n📈 Summary Statistics:")
                        print(f"   📚 Items with homework keywords: {homework_count}")
                        print(f"   📅 Items with due date keywords: {due_count}")
                        print(f"   🎯 Potential assignments: {len(all_assignments_data)}")

                        # Save detailed analysis
                        with open('assignment_analysis.txt', 'w', encoding='utf-8') as f:
                            f.write("ManageBac Assignment Analysis\n")
                            f.write("="*50 + "\n\n")
                            for data in all_assignments_data:
                                f.write(f"Selector: {data['selector']}\n")
                                f.write(f"Text: {data['text']}\n")
                                f.write(f"HTML: {data['html_snippet']}\n")
                                f.write("-" * 30 + "\n")
                        print(f"💾 Detailed analysis saved to assignment_analysis.txt")

                    else:
                        print("⚠️ No assignment elements found with any selector")
                        print("🔍 Let's check the current page URL and title:")
                        current_url = page.url
                        current_title = await page.title()
                        print(f"   📄 Current URL: {current_url}")
                        print(f"   📝 Current Title: {current_title}")

                    return len(all_assignments_data) > 0

                else:
                    print("❌ Login failed")
                    return False

            finally:
                await browser.close()

    except Exception as e:
        print(f"❌ Improved assignment detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main function"""
    print("🚀 Starting Improved Assignment Detection Test")
    print("🚀 开始改进的作业检测测试")
    print("="*60)

    # Setup logging
    logging.basicConfig(level=logging.WARNING)  # Reduce log noise

    success = await test_improved_assignment_detection()

    print(f"\n🏁 Test Result: {'SUCCESS' if success else 'NEEDS_IMPROVEMENT'}")
    print(f"🏁 测试结果：{'成功' if success else '需要改进'}")

    if success:
        print("✅ Assignment detection is working with your account!")
        print("✅ 作业检测在您的账户上正常工作！")
    else:
        print("⚠️ Assignment detection needs refinement for your account")
        print("⚠️ 您的账户的作业检测需要进一步改进")
        print("💡 Check assignment_analysis.txt for detailed findings")
        print("💡 查看assignment_analysis.txt获取详细结果")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)