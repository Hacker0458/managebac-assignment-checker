#!/usr/bin/env python3
"""
Ultimate User Experience Launcher
终极用户体验启动器

Features:
- Animated startup sequences
- Smart environment detection
- Interactive help system
- Multi-language support
- Comprehensive error recovery
- Beautiful progress indicators
"""

import os
import sys
import time
import subprocess
import platform
from pathlib import Path
from typing import Optional, List, Dict, Any
import json


class UltimateUserExperience:
    """Ultimate user experience with comprehensive features"""

    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.working_dir = Path.cwd()

        # Language detection
        self.language = self._detect_language()

        # Load messages
        self.messages = self._load_messages()

        # State tracking
        self.startup_state = {
            "first_run": not Path(".install_state.json").exists(),
            "previous_launches": 0,
            "last_successful_launch": None,
            "preferred_method": None
        }

        self._load_startup_state()

    def _detect_language(self) -> str:
        """Detect user's preferred language"""
        # Check environment variables
        for var in ['LANG', 'LANGUAGE', 'LC_ALL']:
            if var in os.environ:
                lang = os.environ[var].lower()
                if 'zh' in lang or 'chinese' in lang:
                    return 'zh'

        # Check system locale
        try:
            import locale
            system_lang = locale.getdefaultlocale()[0]
            if system_lang and ('zh' in system_lang.lower() or 'chinese' in system_lang.lower()):
                return 'zh'
        except:
            pass

        return 'en'  # Default to English

    def _load_messages(self) -> Dict[str, Dict[str, str]]:
        """Load localized messages"""
        return {
            'en': {
                'welcome': '🎓 Welcome to ManageBac Assignment Checker',
                'starting': '🚀 Starting application...',
                'detecting': '🔍 Detecting optimal launch method...',
                'checking_deps': '📦 Checking dependencies...',
                'launching': '✨ Launching application...',
                'success': '✅ Application started successfully!',
                'error': '❌ Error occurred',
                'retry': '🔄 Retrying...',
                'help': '💡 Need help? Press H for help menu',
                'first_time': '🌟 First time setup detected',
                'returning_user': '👋 Welcome back!',
                'optimizing': '⚡ Optimizing for your system...',
                'ready': '🎯 Ready to launch!'
            },
            'zh': {
                'welcome': '🎓 欢迎使用 ManageBac 作业检查器',
                'starting': '🚀 正在启动应用程序...',
                'detecting': '🔍 正在检测最佳启动方式...',
                'checking_deps': '📦 正在检查依赖项...',
                'launching': '✨ 正在启动应用程序...',
                'success': '✅ 应用程序启动成功！',
                'error': '❌ 发生错误',
                'retry': '🔄 正在重试...',
                'help': '💡 需要帮助？按 H 键打开帮助菜单',
                'first_time': '🌟 检测到首次设置',
                'returning_user': '👋 欢迎回来！',
                'optimizing': '⚡ 正在为您的系统优化...',
                'ready': '🎯 准备启动！'
            }
        }

    def _load_startup_state(self):
        """Load previous startup state"""
        state_file = Path(".app_state.json")
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.startup_state.update(state)
            except Exception as e:
                print(f"⚠️ Could not load startup state: {e}")

    def _save_startup_state(self):
        """Save startup state for next time"""
        state_file = Path(".app_state.json")
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.startup_state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save startup state: {e}")

    def get_message(self, key: str) -> str:
        """Get localized message"""
        return self.messages[self.language].get(key, key)

    def show_animated_welcome(self):
        """Show animated welcome screen"""
        print("\n" + "="*70)

        # Animated title
        title = self.get_message('welcome')
        for i, char in enumerate(title):
            print(char, end='', flush=True)
            time.sleep(0.03)
        print()

        # System info
        print(f"💻 System: {self.system} | Python: {self.python_version.major}.{self.python_version.minor}")
        print(f"📁 Working Directory: {self.working_dir.name}")

        # User status
        if self.startup_state['first_run']:
            print(f"🌟 {self.get_message('first_time')}")
        else:
            print(f"👋 {self.get_message('returning_user')}")
            launches = self.startup_state['previous_launches']
            print(f"📊 Previous launches: {launches}")

        print("="*70)
        print(f"{self.get_message('help')}")
        print()

    def show_progress_bar(self, message: str, duration: float = 2.0):
        """Show animated progress bar"""
        print(f"{message}", end=" ")

        bar_length = 30
        for i in range(bar_length + 1):
            progress = i / bar_length
            filled = int(progress * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            percentage = int(progress * 100)

            print(f"\r{message} [{bar}] {percentage}%", end="", flush=True)
            time.sleep(duration / bar_length)

        print(" ✅")

    def detect_optimal_launch_method(self) -> List[Dict[str, Any]]:
        """Detect the best launch methods for this system"""
        self.show_progress_bar(self.get_message('detecting'))

        methods = []

        # Check for optimized installer (preferred)
        if Path("优化安装器.py").exists():
            methods.append({
                "name": "Optimized Installer | 优化安装器",
                "command": ["python3", "优化安装器.py"],
                "priority": 10,
                "description": "Best user experience with auto-launch"
            })

        # Check for intelligent launcher
        if Path("intelligent_launcher.py").exists():
            methods.append({
                "name": "Intelligent Launcher | 智能启动器",
                "command": ["python3", "intelligent_launcher.py"],
                "priority": 9,
                "description": "Smart environment detection"
            })

        # Check for ultimate installer
        if Path("ultimate_installer.py").exists():
            methods.append({
                "name": "Ultimate Installer | 终极安装器",
                "command": ["python3", "ultimate_installer.py"],
                "priority": 8,
                "description": "Complete installation system"
            })

        # Check for GUI launcher
        if Path("gui_launcher.py").exists():
            methods.append({
                "name": "GUI Launcher | GUI启动器",
                "command": ["python3", "gui_launcher.py"],
                "priority": 7,
                "description": "Direct GUI application"
            })

        # Check for professional GUI module
        if Path("managebac_checker").exists():
            methods.append({
                "name": "Professional GUI Module | 专业GUI模块",
                "command": ["python3", "-m", "managebac_checker.professional_gui"],
                "priority": 6,
                "description": "Direct module launch"
            })

        # Sort by priority
        methods.sort(key=lambda x: x['priority'], reverse=True)

        return methods

    def check_dependencies(self) -> Dict[str, bool]:
        """Check system dependencies"""
        self.show_progress_bar(self.get_message('checking_deps'))

        deps = {}

        # Check Python version
        deps['python_version'] = self.python_version >= (3, 8)

        # Check required modules
        required_modules = ['tkinter', 'pathlib', 'json', 'subprocess']
        for module in required_modules:
            try:
                __import__(module)
                deps[f'module_{module}'] = True
            except ImportError:
                deps[f'module_{module}'] = False

        # Check for package files
        deps['package_exists'] = Path("managebac_checker").exists()
        deps['config_exists'] = Path("config.py").exists() or Path("managebac_checker/config.py").exists()

        return deps

    def launch_application(self, method: Dict[str, Any]) -> bool:
        """Launch application using specified method"""
        print(f"\n🚀 {method['name']}")
        print(f"📝 {method['description']}")

        self.show_progress_bar(self.get_message('launching'), 1.5)

        try:
            # Import enhanced error handling if available
            try:
                from enhanced_error_handler import handle_error, log_info
                log_info(f"Launching application with method: {method['name']}")
            except ImportError:
                pass

            # Launch the application
            process = subprocess.Popen(
                method['command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Wait a moment to see if it starts successfully
            time.sleep(2)

            if process.poll() is None:
                # Process is still running - success!
                print(f"✅ {self.get_message('success')}")

                # Update startup state
                self.startup_state['last_successful_launch'] = time.time()
                self.startup_state['preferred_method'] = method['name']
                self.startup_state['previous_launches'] += 1
                self._save_startup_state()

                return True
            else:
                # Process exited - check for errors
                stdout, stderr = process.communicate()
                if stderr:
                    print(f"❌ Launch failed: {stderr}")
                return False

        except Exception as e:
            print(f"❌ Failed to launch: {e}")
            try:
                from enhanced_error_handler import handle_error
                handle_error(e, f"Application Launch - {method['name']}", "ERROR")
            except ImportError:
                pass
            return False

    def show_help_menu(self):
        """Show interactive help menu"""
        print("\n" + "="*60)
        print("📚 ManageBac Assignment Checker - Help Menu")
        print("📚 ManageBac 作业检查器 - 帮助菜单")
        print("="*60)

        help_items = [
            ("1", "Quick Start | 快速开始", "Launch with best method | 使用最佳方式启动"),
            ("2", "Manual Launch | 手动启动", "Choose launch method | 选择启动方式"),
            ("3", "System Check | 系统检查", "Check dependencies | 检查依赖项"),
            ("4", "Troubleshooting | 故障排除", "Common solutions | 常见解决方案"),
            ("5", "Documentation | 文档", "Open user guide | 打开用户指南"),
            ("Q", "Quit | 退出", "Exit application | 退出应用程序")
        ]

        for key, title, desc in help_items:
            print(f"{key:>2}. {title}")
            print(f"     {desc}")

        print("="*60)

        choice = input("\n👉 Select option | 选择选项: ").strip().upper()

        if choice == "1":
            return "quick_start"
        elif choice == "2":
            return "manual_launch"
        elif choice == "3":
            return "system_check"
        elif choice == "4":
            return "troubleshooting"
        elif choice == "5":
            return "documentation"
        elif choice == "Q":
            return "quit"
        else:
            print("❌ Invalid choice | 无效选择")
            return None

    def show_troubleshooting(self):
        """Show troubleshooting guide"""
        print("\n" + "="*60)
        print("🔧 Troubleshooting Guide | 故障排除指南")
        print("="*60)

        issues = [
            {
                "problem": "Application won't start | 应用程序无法启动",
                "solutions": [
                    "Check Python version (3.8+ required) | 检查Python版本（需要3.8+）",
                    "Install dependencies: pip install -r requirements.txt",
                    "Try different launch method | 尝试不同的启动方式"
                ]
            },
            {
                "problem": "GUI crashes or flashes | GUI闪退或闪烁",
                "solutions": [
                    "Check display server (X11/Wayland) | 检查显示服务器",
                    "Verify tkinter: python3 -m tkinter | 验证tkinter",
                    "Run in compatibility mode | 使用兼容模式运行"
                ]
            },
            {
                "problem": "Dependencies missing | 缺少依赖项",
                "solutions": [
                    "Run installer script | 运行安装器脚本",
                    "Manual install: pip install <package> | 手动安装包",
                    "Check virtual environment | 检查虚拟环境"
                ]
            }
        ]

        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. {issue['problem']}")
            for j, solution in enumerate(issue['solutions'], 1):
                print(f"   {j}) {solution}")

        print("\n💡 Still having issues? | 仍有问题？")
        print("   • Check logs in ./logs/ directory | 查看./logs/目录中的日志")
        print("   • Report issue on GitHub | 在GitHub上报告问题")
        print("   • Run system diagnostic | 运行系统诊断")

    def run(self):
        """Main application flow"""
        try:
            # Show welcome screen
            self.show_animated_welcome()

            # Check for immediate help request
            print("Press ENTER to continue or H for help...")
            user_input = input().strip().upper()

            if user_input == 'H':
                action = self.show_help_menu()
                if action == "quit":
                    print("👋 Goodbye! | 再见！")
                    return
                elif action == "system_check":
                    deps = self.check_dependencies()
                    print("\n📊 System Check Results:")
                    for dep, status in deps.items():
                        status_icon = "✅" if status else "❌"
                        print(f"   {status_icon} {dep}")
                    input("\nPress ENTER to continue...")
                elif action == "troubleshooting":
                    self.show_troubleshooting()
                    input("\nPress ENTER to continue...")

            # Detect launch methods
            methods = self.detect_optimal_launch_method()

            if not methods:
                print("❌ No launch methods available | 没有可用的启动方式")
                print("💡 Please run the installer first | 请先运行安装器")
                return

            # Check dependencies
            deps = self.check_dependencies()
            critical_deps_ok = all([
                deps.get('python_version', False),
                deps.get('module_tkinter', False),
                deps.get('package_exists', False)
            ])

            if not critical_deps_ok:
                print("❌ Critical dependencies missing | 缺少关键依赖项")
                print("💡 Please run the installer to fix dependencies")
                print("💡 请运行安装器来修复依赖项")
                return

            # Show optimization message
            print(f"\n⚡ {self.get_message('optimizing')}")
            time.sleep(1)
            print(f"🎯 {self.get_message('ready')}")

            # Try launch methods in order of priority
            for method in methods:
                if self.launch_application(method):
                    print(f"\n🎉 Application launched successfully with {method['name']}")
                    print("🎉 应用程序启动成功")
                    return
                else:
                    print(f"⚠️ Method failed, trying next option...")
                    time.sleep(1)

            # If all methods failed
            print("\n❌ All launch methods failed | 所有启动方式都失败了")
            print("🔧 Please check the troubleshooting guide")
            print("🔧 请查看故障排除指南")

        except KeyboardInterrupt:
            print("\n🛑 Launch cancelled by user | 用户取消启动")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            try:
                from enhanced_error_handler import handle_error
                handle_error(e, "Ultimate User Experience", "CRITICAL")
            except ImportError:
                import traceback
                traceback.print_exc()


def main():
    """Main function"""
    launcher = UltimateUserExperience()
    launcher.run()


if __name__ == "__main__":
    main()