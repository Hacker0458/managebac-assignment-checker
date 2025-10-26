#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ManageBac Assignment Checker - Configuration Tester
🧪 ManageBac作业检查器 - 配置测试器

Quick configuration test utility.
快速配置测试工具。
"""

import sys
import asyncio
from pathlib import Path

# Import the config validator
try:
    from config_validator import ConfigValidator, Colors
except ImportError:
    print("❌ Error: config_validator.py not found!")
    print("❌ 错误：找不到config_validator.py！")
    sys.exit(1)

def print_header():
    """Print application header"""
    print(f"{Colors.PURPLE}{'=' * 50}{Colors.END}")
    print(f"{Colors.PURPLE}{Colors.BOLD}🧪 Configuration Test | 配置测试{Colors.END}")
    print(f"{Colors.PURPLE}{'=' * 50}{Colors.END}")
    print()

def print_quick_help():
    """Print quick help information"""
    print(f"{Colors.CYAN}💡 Quick Help | 快速帮助:{Colors.END}")
    print()
    print("   Configuration issues? Try these commands:")
    print("   配置有问题？试试这些命令：")
    print()
    print(f"   {Colors.GREEN}• Setup wizard:     {Colors.WHITE}python setup_wizard.py{Colors.END}")
    print(f"   {Colors.GREEN}• GUI setup:        {Colors.WHITE}python first_run_setup.py{Colors.END}")
    print(f"   {Colors.GREEN}• Full validation:  {Colors.WHITE}python config_validator.py{Colors.END}")
    print(f"   {Colors.GREEN}• Edit config:      {Colors.WHITE}nano .env{Colors.END}")
    print()

async def run_quick_test():
    """Run a quick configuration test"""
    print_header()

    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print(f"{Colors.RED}❌ No .env file found!{Colors.END}")
        print(f"{Colors.RED}❌ 找不到.env文件！{Colors.END}")
        print()
        print(f"{Colors.YELLOW}🔧 Run setup first: python setup_wizard.py{Colors.END}")
        print(f"{Colors.YELLOW}🔧 先运行设置：python setup_wizard.py{Colors.END}")
        return False

    print(f"{Colors.BLUE}🔍 Running quick configuration test...{Colors.END}")
    print(f"{Colors.BLUE}🔍 正在运行快速配置测试...{Colors.END}")
    print()

    # Run validator with essential tests only
    validator = ConfigValidator('.env')

    # Load config first
    if not validator.load_config():
        print(f"{Colors.RED}❌ Failed to load configuration!{Colors.END}")
        return False

    # Run essential validations
    validator.validate_required_fields()
    validator.validate_managebac_url()
    validator.validate_email_format()
    validator.validate_dependencies()

    # Count results
    success_count = sum(1 for result in validator.results if result.success)
    total_count = len(validator.results)

    # Print results
    print(f"{Colors.BOLD}📊 Quick Test Results:{Colors.END}")
    print("-" * 30)

    for result in validator.results:
        status_icon = f"{Colors.GREEN}✅" if result.success else f"{Colors.RED}❌"
        print(f"{status_icon} {result.test_name}: {result.message}{Colors.END}")

    print("-" * 30)

    if success_count == total_count:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 Quick test passed! ({success_count}/{total_count}){Colors.END}")
        print(f"{Colors.GREEN}🎉 快速测试通过！({success_count}/{total_count}){Colors.END}")
        print()
        print(f"{Colors.CYAN}✨ Your configuration looks good! Try running:{Colors.END}")
        print(f"   {Colors.WHITE}python main_new.py --test{Colors.END}")
        print()
        return True
    else:
        failed_count = total_count - success_count
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {failed_count} issues found.{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  发现 {failed_count} 个问题。{Colors.END}")
        print()
        print_quick_help()
        return False

def main():
    """Main function"""
    try:
        result = asyncio.run(run_quick_test())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Test cancelled by user.{Colors.END}")
        print(f"{Colors.YELLOW}👋 用户取消了测试。{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()