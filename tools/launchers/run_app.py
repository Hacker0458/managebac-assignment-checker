#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ManageBac Assignment Checker - 简单启动器
🚀 ManageBac作业检查器 - 简单启动器

为小白用户设计的简单启动脚本。
Simple launcher script designed for novice users.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import time

# Color constants for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Print application header"""
    print(f"{Colors.PURPLE}{'=' * 60}{Colors.END}")
    print(f"{Colors.PURPLE}{Colors.BOLD}🚀 ManageBac Assignment Checker - 启动器{Colors.END}")
    print(f"{Colors.PURPLE}🚀 ManageBac作业检查器 - 启动器{Colors.END}")
    print(f"{Colors.PURPLE}{'=' * 60}{Colors.END}")
    print()

def check_configuration():
    """Check if configuration exists and is valid"""
    env_file = Path('.env')

    if not env_file.exists():
        return False, "配置文件不存在"

    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required fields
        required_fields = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
        missing_fields = []

        for field in required_fields:
            if f'{field}=' not in content:
                missing_fields.append(field)

        if missing_fields:
            return False, f"缺少必需配置: {', '.join(missing_fields)}"

        # Check for placeholder values
        placeholder_values = [
            'your.email@example.com',
            'your_password',
            'your-school.managebac.cn'
        ]

        for placeholder in placeholder_values:
            if placeholder in content:
                return False, "配置文件包含占位符值，需要填写真实信息"

        return True, "配置文件检查通过"

    except Exception as e:
        return False, f"配置文件读取错误: {str(e)}"

def run_setup():
    """Run configuration setup"""
    print(f"{Colors.CYAN}🔧 启动配置向导...{Colors.END}")

    # Try GUI setup first
    if Path('first_run_setup.py').exists():
        try:
            result = subprocess.run([sys.executable, 'first_run_setup.py'],
                                  capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return True
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ GUI配置向导启动失败: {e}{Colors.END}")

    # Fallback to command line setup with proper input handling
    if Path('setup_wizard.py').exists():
        try:
            # Run setup wizard in interactive mode
            result = subprocess.run([sys.executable, 'setup_wizard.py'],
                                  timeout=600)  # 10 minutes timeout
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"{Colors.YELLOW}⚠️ 配置向导超时{Colors.END}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ 配置向导启动失败: {e}{Colors.END}")

    return False

def show_gui_options():
    """Show GUI options for running the application"""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Ask user how they want to run the application
        choice = messagebox.askyesnocancel(
            "选择运行方式 | Choose Run Mode",
            "如何运行ManageBac作业检查器？\nHow would you like to run ManageBac Assignment Checker?\n\n"
            "点击'是'使用GUI界面（推荐）\nClick 'Yes' for GUI Mode (Recommended)\n\n"
            "点击'否'使用命令行模式\nClick 'No' for Command Line Mode\n\n"
            "点击'取消'退出\nClick 'Cancel' to Exit"
        )

        root.destroy()
        return choice

    except Exception as e:
        print(f"{Colors.YELLOW}⚠️ GUI选项显示失败: {e}{Colors.END}")
        return None

def run_application(mode='gui'):
    """Run the application in specified mode"""
    if mode == 'gui':
        print(f"{Colors.GREEN}🎨 启动GUI模式...{Colors.END}")

        # Try GUI launcher first
        if Path('gui_launcher.py').exists():
            try:
                subprocess.run([sys.executable, 'gui_launcher.py'])
                return True
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️ GUI启动失败: {e}{Colors.END}")

        # Try professional GUI
        if Path('professional_gui.py').exists():
            try:
                subprocess.run([sys.executable, 'professional_gui.py'])
                return True
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️ 专业GUI启动失败: {e}{Colors.END}")

    else:  # command line mode
        print(f"{Colors.BLUE}💻 启动命令行模式...{Colors.END}")

        if Path('main_new.py').exists():
            try:
                subprocess.run([sys.executable, 'main_new.py'])
                return True
            except Exception as e:
                print(f"{Colors.RED}❌ 命令行模式启动失败: {e}{Colors.END}")

    return False

def show_help_info():
    """Show help information for users"""
    print(f"\n{Colors.CYAN}💡 使用帮助 | Help Information:{Colors.END}")
    print(f"{Colors.WHITE}如果遇到问题，您可以尝试以下解决方案：{Colors.END}")
    print()
    print(f"{Colors.GREEN}1. 重新配置:{Colors.END}")
    print(f"   python setup_wizard.py")
    print()
    print(f"{Colors.GREEN}2. 测试配置:{Colors.END}")
    print(f"   python test_config.py")
    print()
    print(f"{Colors.GREEN}3. 完整验证:{Colors.END}")
    print(f"   python config_validator.py")
    print()
    print(f"{Colors.GREEN}4. 手动启动GUI:{Colors.END}")
    print(f"   python gui_launcher.py")
    print()
    print(f"{Colors.GREEN}5. 手动启动命令行:{Colors.END}")
    print(f"   python main_new.py")
    print()

def main():
    """Main function"""
    print_header()

    # Check configuration
    print(f"{Colors.BLUE}🔍 检查配置...{Colors.END}")
    config_valid, config_message = check_configuration()
    print(f"   {config_message}")

    if not config_valid:
        print(f"\n{Colors.YELLOW}⚠️ 需要先配置应用程序{Colors.END}")

        # Ask if user wants to configure now
        try:
            root = tk.Tk()
            root.withdraw()

            setup_now = messagebox.askyesno(
                "需要配置 | Setup Required",
                "应用程序尚未配置完成。\nThe application is not configured yet.\n\n"
                "是否现在进行配置？\nWould you like to configure it now?\n\n"
                "点击'是'开始配置\nClick 'Yes' to start setup\n"
                "点击'否'手动配置\nClick 'No' for manual setup"
            )

            root.destroy()

            if setup_now:
                success = run_setup()
                if success:
                    print(f"\n{Colors.GREEN}✅ 配置完成！{Colors.END}")
                    # Re-check configuration
                    config_valid, config_message = check_configuration()
                    print(f"   {config_message}")
                else:
                    print(f"\n{Colors.RED}❌ 配置失败{Colors.END}")
                    show_help_info()
                    return
            else:
                print(f"\n{Colors.CYAN}请手动编辑.env文件完成配置{Colors.END}")
                show_help_info()
                return

        except Exception as e:
            print(f"{Colors.RED}❌ 配置对话框显示失败: {e}{Colors.END}")
            show_help_info()
            return

    if config_valid:
        print(f"\n{Colors.GREEN}✅ 配置检查通过，准备启动应用程序...{Colors.END}")

        # Show run options
        run_choice = show_gui_options()

        if run_choice is True:  # GUI mode
            success = run_application('gui')
        elif run_choice is False:  # Command line mode
            success = run_application('cli')
        else:  # Cancelled or error
            print(f"\n{Colors.YELLOW}👋 用户取消操作{Colors.END}")
            return

        if not success:
            print(f"\n{Colors.RED}❌ 应用程序启动失败{Colors.END}")
            show_help_info()
        else:
            print(f"\n{Colors.GREEN}✅ 应用程序启动成功！{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 用户中断操作{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ 启动器出现错误: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()