#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ManageBac Assignment Checker - 启动助手
🚀 ManageBac作业检查器 - 启动助手

处理设置完成后的启动逻辑，为小白用户提供友好的启动选项。
Launch helper that handles post-setup launch logic with user-friendly options for novice users.
"""

import os
import sys
import time
import platform
import subprocess
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

class LaunchHelper:
    def __init__(self):
        self.project_path = Path(__file__).parent.absolute()
        self.system = platform.system()

    def print_success_banner(self):
        """显示成功横幅"""
        print(f"\n{Colors.GREEN}{'=' * 70}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 配置完成！Configuration Complete!{Colors.END}")
        print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
        print(f"{Colors.WHITE}ManageBac作业检查器已成功配置！{Colors.END}")
        print(f"{Colors.WHITE}ManageBac Assignment Checker is successfully configured!{Colors.END}")
        print(f"{Colors.GREEN}{'=' * 70}{Colors.END}")
        print()

    def show_launch_options(self):
        """显示启动选项"""
        print(f"{Colors.CYAN}🚀 选择启动方式 | Choose Launch Method:{Colors.END}")
        print()
        print(f"{Colors.GREEN}1. 🎨 立即启动GUI界面 (推荐){Colors.END}")
        print(f"{Colors.WHITE}   Start GUI interface now (Recommended){Colors.END}")
        print()
        print(f"{Colors.BLUE}2. 💻 启动命令行模式{Colors.END}")
        print(f"{Colors.WHITE}   Start command line mode{Colors.END}")
        print()
        print(f"{Colors.PURPLE}3. 🖥️ 创建桌面快捷方式{Colors.END}")
        print(f"{Colors.WHITE}   Create desktop shortcut{Colors.END}")
        print()
        print(f"{Colors.YELLOW}4. ⏭️ 稍后手动启动{Colors.END}")
        print(f"{Colors.WHITE}   Start manually later{Colors.END}")
        print()

    def get_user_choice(self, timeout_seconds=15):
        """获取用户选择，带超时"""
        try:
            print(f"{Colors.CYAN}请选择选项 (1-4) [默认: 1, {timeout_seconds}秒后自动选择]: {Colors.END}", end='', flush=True)

            # Try to get input with a basic timeout approach
            import select
            if hasattr(select, 'select'):  # Unix-like systems
                ready, _, _ = select.select([sys.stdin], [], [], timeout_seconds)
                if ready:
                    choice = sys.stdin.readline().strip()
                else:
                    print(f"\n{Colors.YELLOW}⏰ 超时，自动选择GUI模式{Colors.END}")
                    choice = '1'
            else:  # Windows or systems without select
                choice = input()

            # Validate and normalize choice
            if choice in ['1', '', 'gui', 'g']:
                return 1
            elif choice in ['2', 'cli', 'c']:
                return 2
            elif choice in ['3', 'shortcut', 's']:
                return 3
            elif choice in ['4', 'later', 'l']:
                return 4
            else:
                print(f"{Colors.YELLOW}⚠️ 无效选择，使用默认选项{Colors.END}")
                return 1

        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.YELLOW}⚠️ 用户中断，稍后启动{Colors.END}")
            return 4
        except:
            # Fallback for systems where select doesn't work
            return 1

    def launch_gui(self):
        """启动GUI模式"""
        print(f"\n{Colors.GREEN}🎨 启动GUI界面...{Colors.END}")

        gui_files = [
            'smart_launcher.py',
            'gui_launcher.py',
            'professional_gui.py',
            'enhanced_gui.py'
        ]

        for gui_file in gui_files:
            if (self.project_path / gui_file).exists():
                try:
                    print(f"{Colors.BLUE}   正在启动 {gui_file}...{Colors.END}")

                    # Launch GUI in background
                    if self.system == "Windows":
                        subprocess.Popen([sys.executable, gui_file],
                                       creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen([sys.executable, gui_file])

                    print(f"{Colors.GREEN}✅ GUI界面启动成功！{Colors.END}")
                    print(f"{Colors.WHITE}   GUI interface launched successfully!{Colors.END}")
                    return True

                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️ {gui_file} 启动失败: {e}{Colors.END}")
                    continue

        print(f"{Colors.RED}❌ GUI启动失败，尝试命令行模式{Colors.END}")
        return self.launch_cli()

    def launch_cli(self):
        """启动命令行模式"""
        print(f"\n{Colors.BLUE}💻 启动命令行模式...{Colors.END}")

        cli_files = ['main_new.py', 'main.py']

        for cli_file in cli_files:
            if (self.project_path / cli_file).exists():
                try:
                    print(f"{Colors.BLUE}   正在启动 {cli_file}...{Colors.END}")
                    subprocess.run([sys.executable, cli_file])
                    print(f"{Colors.GREEN}✅ 程序执行完成{Colors.END}")
                    return True

                except Exception as e:
                    print(f"{Colors.RED}❌ {cli_file} 启动失败: {e}{Colors.END}")
                    continue

        print(f"{Colors.RED}❌ 命令行模式启动失败{Colors.END}")
        return False

    def create_desktop_shortcut(self):
        """创建桌面快捷方式"""
        print(f"\n{Colors.PURPLE}🖥️ 创建桌面快捷方式...{Colors.END}")

        if (self.project_path / 'create_desktop_shortcut.py').exists():
            try:
                subprocess.run([sys.executable, 'create_desktop_shortcut.py'])
                print(f"{Colors.GREEN}✅ 桌面快捷方式创建成功！{Colors.END}")

                # Ask if user wants to launch now
                print(f"\n{Colors.CYAN}是否立即启动应用程序？(y/n) [y]: {Colors.END}", end='')
                launch_now = input().strip().lower()

                if launch_now in ['', 'y', 'yes', '是', '1']:
                    return self.launch_gui()
                else:
                    print(f"{Colors.GREEN}✅ 您可以通过桌面快捷方式启动程序{Colors.END}")
                    return True

            except Exception as e:
                print(f"{Colors.RED}❌ 桌面快捷方式创建失败: {e}{Colors.END}")
                return False
        else:
            print(f"{Colors.YELLOW}⚠️ 未找到桌面快捷方式创建器{Colors.END}")
            return False

    def show_manual_launch_info(self):
        """显示手动启动信息"""
        print(f"\n{Colors.YELLOW}📋 手动启动方法：{Colors.END}")
        print(f"{Colors.WHITE}您可以使用以下任一方法启动程序：{Colors.END}")
        print()
        print(f"{Colors.GREEN}1. 智能启动器 (推荐):{Colors.END}")
        print(f"   python smart_launcher.py")
        print()
        print(f"{Colors.GREEN}2. 简单启动器:{Colors.END}")
        print(f"   python run_app.py")
        print()
        print(f"{Colors.GREEN}3. 一键启动脚本:{Colors.END}")
        print(f"   python start.py")
        print()
        print(f"{Colors.GREEN}4. 直接启动GUI:{Colors.END}")
        print(f"   python gui_launcher.py")
        print()
        print(f"{Colors.GREEN}5. 直接启动命令行:{Colors.END}")
        print(f"   python main_new.py")
        print()

    def run_post_setup_launch(self):
        """运行设置后启动流程"""
        self.print_success_banner()
        self.show_launch_options()

        choice = self.get_user_choice()

        if choice == 1:  # GUI模式
            success = self.launch_gui()
        elif choice == 2:  # CLI模式
            success = self.launch_cli()
        elif choice == 3:  # 桌面快捷方式
            success = self.create_desktop_shortcut()
        else:  # 稍后启动
            self.show_manual_launch_info()
            success = True

        # Final message
        if success and choice != 4:
            print(f"\n{Colors.GREEN}🎯 感谢使用ManageBac作业检查器！{Colors.END}")
            print(f"{Colors.WHITE}Thank you for using ManageBac Assignment Checker!{Colors.END}")

        return success

def main():
    """主函数，可独立运行"""
    try:
        helper = LaunchHelper()
        return helper.run_post_setup_launch()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 用户退出{Colors.END}")
        return True
    except Exception as e:
        print(f"\n{Colors.RED}❌ 启动助手错误: {e}{Colors.END}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)