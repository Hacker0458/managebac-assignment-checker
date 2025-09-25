#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ManageBac Assignment Checker - 智能启动器
🤖 ManageBac作业检查器 - 智能启动器

能够自动检测运行环境并选择最适合的启动方式的智能启动器。
Smart launcher that automatically detects the runtime environment and chooses the most appropriate startup method.
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

class Colors:
    """终端颜色常量"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class SmartLauncher:
    def __init__(self):
        self.has_display = self.check_display_available()
        self.has_tkinter = self.check_tkinter_available()
        self.is_configured = self.check_configuration()
        self.project_path = Path(__file__).parent.absolute()

    def check_display_available(self) -> bool:
        """检查是否有可用的显示环境"""
        try:
            if platform.system() == "Darwin":  # macOS
                # Check if we're in a GUI session
                result = subprocess.run(['launchctl', 'managername'],
                                      capture_output=True, text=True, timeout=5)
                return 'Aqua' in result.stdout
            elif platform.system() == "Linux":
                return 'DISPLAY' in os.environ and os.environ.get('DISPLAY') != ''
            elif platform.system() == "Windows":
                return True  # Windows almost always has a display
            return False
        except:
            return False

    def check_tkinter_available(self) -> bool:
        """检查tkinter是否可用"""
        try:
            import tkinter as tk
            # Try to create a root window (but don't show it)
            root = tk.Tk()
            root.withdraw()
            root.destroy()
            return True
        except:
            return False

    def check_configuration(self) -> bool:
        """检查配置文件是否存在且有效"""
        env_file = Path('.env')

        if not env_file.exists():
            return False

        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for required fields
            required_fields = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
            for field in required_fields:
                if f'{field}=' not in content:
                    return False

            # Check for placeholder values
            placeholder_values = [
                'your.email@example.com',
                'your_password',
                'your-school.managebac.cn'
            ]

            for placeholder in placeholder_values:
                if placeholder in content:
                    return False

            return True

        except Exception:
            return False

    def print_banner(self):
        """显示启动横幅"""
        print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}🤖 ManageBac Assignment Checker - 智能启动器{Colors.END}")
        print(f"{Colors.CYAN}🤖 ManageBac作业检查器 - 智能启动器{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 70}{Colors.END}")
        print()

    def show_environment_info(self):
        """显示环境检测信息"""
        print(f"{Colors.BLUE}🔍 环境检测结果：{Colors.END}")
        print(f"   显示环境: {'✅ 可用' if self.has_display else '❌ 不可用'}")
        print(f"   GUI支持: {'✅ 支持' if self.has_tkinter else '❌ 不支持'}")
        print(f"   配置状态: {'✅ 已配置' if self.is_configured else '⚠️ 需要配置'}")
        print(f"   操作系统: {platform.system()} {platform.release()}")
        print()

    def run_command_line_setup(self) -> bool:
        """运行命令行配置向导"""
        print(f"{Colors.YELLOW}🔧 启动命令行配置向导...{Colors.END}")

        # Create a simple interactive setup
        try:
            print(f"\n{Colors.GREEN}请输入您的ManageBac配置信息：{Colors.END}")

            # Get ManageBac URL
            url = input(f"{Colors.BLUE}🏫 学校ManageBac网址 [https://shtcs.managebac.cn]: {Colors.END}").strip()
            if not url:
                url = "https://shtcs.managebac.cn"

            # Get email
            email = input(f"{Colors.BLUE}📧 您的邮箱地址: {Colors.END}").strip()
            if not email:
                print(f"{Colors.RED}❌ 邮箱地址不能为空{Colors.END}")
                return False

            # Get password
            password = input(f"{Colors.BLUE}🔐 您的密码: {Colors.END}").strip()
            if not password:
                print(f"{Colors.RED}❌ 密码不能为空{Colors.END}")
                return False

            # Ask about AI
            ai_choice = input(f"{Colors.BLUE}🤖 是否启用AI辅助功能？(y/n) [n]: {Colors.END}").strip().lower()
            ai_enabled = ai_choice in ['y', 'yes', '是', '1']

            ai_key = ""
            if ai_enabled:
                ai_key = input(f"{Colors.BLUE}🔑 请输入OpenAI API Key: {Colors.END}").strip()
                if not ai_key:
                    print(f"{Colors.YELLOW}⚠️ 未提供API Key，AI功能将被禁用{Colors.END}")
                    ai_enabled = False

            # Create configuration file
            config_content = f"""# ========================================
# ManageBac Assignment Checker Configuration
# ManageBac作业检查器配置文件
# ========================================

# 🔐 ManageBac Credentials | ManageBac凭据
MANAGEBAC_EMAIL={email}
MANAGEBAC_PASSWORD={password}
MANAGEBAC_URL={url}

# 📊 Report Settings | 报告设置
REPORT_FORMAT=console,html
OUTPUT_DIR=./reports
FETCH_DETAILS=true
DETAILS_LIMIT=50

# 📧 Email Notification Settings | 邮件通知设置
ENABLE_EMAIL_NOTIFICATIONS=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=true
NOTIFICATION_RECIPIENTS=

# 🔧 Browser Settings | 浏览器设置
HEADLESS=true
BROWSER_TIMEOUT=30000

# 🐛 Debug Settings | 调试设置
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/managebac_checker.log

# 🎨 UI Settings | 界面设置
HTML_THEME=auto
INCLUDE_CHARTS=true
CHART_COLOR_SCHEME=default

# 🤖 AI Assistant Settings | AI助手设置
AI_ENABLED={'true' if ai_enabled else 'false'}
OPENAI_API_KEY={ai_key}
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=500

# 🌐 Language Settings | 语言设置
LANGUAGE=zh
"""

            with open('.env', 'w', encoding='utf-8') as f:
                f.write(config_content)

            print(f"\n{Colors.GREEN}✅ 配置文件创建成功！{Colors.END}")
            return True

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠️ 用户取消配置{Colors.END}")
            return False
        except Exception as e:
            print(f"\n{Colors.RED}❌ 配置失败: {e}{Colors.END}")
            return False

    def launch_application(self, force_cli=False) -> bool:
        """启动应用程序"""
        if not force_cli and self.has_display and self.has_tkinter:
            # Try GUI mode
            print(f"{Colors.GREEN}🎨 启动GUI模式...{Colors.END}")

            # Try different GUI launchers in order of preference
            gui_files = ['gui_launcher.py', 'professional_gui.py', 'enhanced_gui.py']

            for gui_file in gui_files:
                if Path(gui_file).exists():
                    try:
                        result = subprocess.run([sys.executable, gui_file],
                                              timeout=5, capture_output=True)
                        if result.returncode == 0:
                            print(f"{Colors.GREEN}✅ GUI启动成功{Colors.END}")
                            return True
                    except subprocess.TimeoutExpired:
                        # GUI is running, this is actually success
                        print(f"{Colors.GREEN}✅ GUI已启动{Colors.END}")
                        return True
                    except Exception as e:
                        print(f"{Colors.YELLOW}⚠️ {gui_file} 启动失败: {e}{Colors.END}")
                        continue

        # Fallback to command line mode
        print(f"{Colors.BLUE}💻 启动命令行模式...{Colors.END}")

        cli_files = ['main_new.py', 'main.py']
        for cli_file in cli_files:
            if Path(cli_file).exists():
                try:
                    subprocess.run([sys.executable, cli_file])
                    return True
                except Exception as e:
                    print(f"{Colors.RED}❌ {cli_file} 启动失败: {e}{Colors.END}")
                    continue

        return False

    def show_usage_help(self):
        """显示使用帮助"""
        print(f"\n{Colors.CYAN}💡 使用帮助：{Colors.END}")
        print(f"{Colors.WHITE}如果遇到问题，请尝试以下方法：{Colors.END}")
        print()
        print(f"{Colors.GREEN}1. 重新配置:{Colors.END}")
        print(f"   python smart_launcher.py --setup")
        print()
        print(f"{Colors.GREEN}2. 强制命令行模式:{Colors.END}")
        print(f"   python smart_launcher.py --cli")
        print()
        print(f"{Colors.GREEN}3. 检查环境:{Colors.END}")
        print(f"   python smart_launcher.py --check")
        print()
        print(f"{Colors.GREEN}4. 创建桌面快捷方式:{Colors.END}")
        print(f"   python create_desktop_shortcut.py")
        print()

    def run(self, args=None):
        """主运行方法"""
        if args is None:
            args = sys.argv[1:]

        # Handle command line arguments
        if '--setup' in args or '-s' in args:
            self.print_banner()
            success = self.run_command_line_setup()
            if success:
                self.is_configured = True
                print(f"\n{Colors.GREEN}是否立即启动应用程序？(y/n) [y]: {Colors.END}", end='')
                launch_now = input().strip().lower()
                if launch_now in ['', 'y', 'yes', '是', '1']:
                    return self.launch_application()
            return success

        elif '--cli' in args or '-c' in args:
            self.print_banner()
            if not self.is_configured:
                print(f"{Colors.RED}❌ 应用程序尚未配置{Colors.END}")
                return False
            return self.launch_application(force_cli=True)

        elif '--check' in args:
            self.print_banner()
            self.show_environment_info()
            return True

        elif '--help' in args or '-h' in args:
            self.print_banner()
            self.show_usage_help()
            return True

        # Default behavior: smart launch
        self.print_banner()
        self.show_environment_info()

        # Configuration check
        if not self.is_configured:
            print(f"{Colors.YELLOW}⚠️ 应用程序尚未配置{Colors.END}")
            print(f"{Colors.BLUE}现在开始配置...{Colors.END}")
            print()

            success = self.run_command_line_setup()
            if not success:
                self.show_usage_help()
                return False

            self.is_configured = True
            print()

        # Launch application
        print(f"{Colors.GREEN}🚀 启动应用程序...{Colors.END}")
        success = self.launch_application()

        if not success:
            print(f"{Colors.RED}❌ 应用程序启动失败{Colors.END}")
            self.show_usage_help()

        return success

def main():
    """主函数"""
    try:
        launcher = SmartLauncher()
        success = launcher.run()
        return 0 if success else 1
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 用户退出{Colors.END}")
        return 0
    except Exception as e:
        print(f"\n{Colors.RED}❌ 启动器错误: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())