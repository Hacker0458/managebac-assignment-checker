#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 Ultimate Installer | 终极安装器
The definitive installation solution with multiple modes and smart fallbacks
具有多种模式和智能后备方案的终极安装解决方案
"""

import os
import sys
import subprocess
import platform
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

class Colors:
    """Console colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class UltimateInstaller:
    """The ultimate installation solution"""

    def __init__(self):
        self.platform = platform.system().lower()
        self.python_version = sys.version_info
        self.install_methods = self.get_available_install_methods()
        self.args = self.parse_arguments()

    def parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(
            description="ManageBac Assignment Checker - Ultimate Installer",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Installation Modes:
  gui       - Graphical installation (recommended)
  wizard    - Interactive command-line wizard
  advanced  - Advanced command-line installer
  quick     - Quick installation with defaults
  repair    - Repair existing installation

Examples:
  python ultimate_installer.py          # Auto-detect best mode + auto-launch
  python ultimate_installer.py --mode gui
  python ultimate_installer.py --mode quick --no-auto-launch
  python ultimate_installer.py --repair
            """
        )

        parser.add_argument(
            '--mode', '-m',
            choices=['auto', 'gui', 'wizard', 'advanced', 'quick'],
            default='auto',
            help='Installation mode (default: auto-detect)'
        )

        parser.add_argument(
            '--no-auto-launch',
            action='store_true',
            help='Disable automatic application launch after installation'
        )

        parser.add_argument(
            '--repair', '-r',
            action='store_true',
            help='Repair existing installation'
        )

        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Verbose output'
        )

        parser.add_argument(
            '--no-deps',
            action='store_true',
            help='Skip dependency installation'
        )

        parser.add_argument(
            '--offline',
            action='store_true',
            help='Offline installation mode (skip network operations)'
        )

        parser.add_argument(
            '--config-file',
            type=str,
            help='Path to configuration file'
        )

        return parser.parse_args()

    def get_available_install_methods(self) -> Dict[str, Dict[str, Any]]:
        """Get available installation methods"""
        methods = {}

        # GUI installer
        try:
            import tkinter
            methods['gui'] = {
                'available': True,
                'priority': 1,
                'description': 'Graphical installation wizard',
                'description_zh': '图形化安装向导',
                'module': 'enhanced_setup_gui',
                'class': 'EnhancedSetupGUI',
                'requirements': ['tkinter']
            }
        except ImportError:
            methods['gui'] = {
                'available': False,
                'priority': 1,
                'description': 'Graphical installation wizard (tkinter not available)',
                'description_zh': '图形化安装向导（tkinter不可用）',
                'requirements': ['tkinter']
            }

        # Advanced installer
        methods['advanced'] = {
            'available': True,
            'priority': 2,
            'description': 'Advanced command-line installer',
            'description_zh': '高级命令行安装器',
            'module': 'advanced_installer',
            'class': 'AdvancedInstaller',
            'requirements': []
        }

        # Interactive wizard
        methods['wizard'] = {
            'available': True,
            'priority': 3,
            'description': 'Interactive setup wizard',
            'description_zh': '交互式设置向导',
            'module': 'setup_wizard',
            'class': 'SetupWizard',
            'requirements': []
        }

        # Quick installer
        methods['quick'] = {
            'available': True,
            'priority': 4,
            'description': 'Quick installation with defaults',
            'description_zh': '使用默认设置快速安装',
            'function': self.quick_install,
            'requirements': []
        }

        return methods

    def print_banner(self):
        """Print installation banner"""
        print(f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     🌟 ManageBac Assignment Checker - Ultimate Installer     ║
║         🌟 ManageBac作业检查器 - 终极安装器                    ║
║                                                                ║
║   🚀 Smart installation with multiple modes and fallbacks     ║
║   🚀 多模式智能安装，具有后备方案                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}Platform: {self.platform.title()} | Python: {self.python_version.major}.{self.python_version.minor}{Colors.END}
""")

    def show_available_methods(self):
        """Show available installation methods"""
        print(f"{Colors.HEADER}📋 Available Installation Methods | 可用的安装方法:{Colors.END}\n")

        for method, config in self.install_methods.items():
            status = "✅" if config['available'] else "❌"
            print(f"   {status} {method.upper():<10} - {config['description']}")
            print(f"      {'':>10}   {config['description_zh']}")
            if not config['available'] and 'requirements' in config:
                missing = ', '.join(config['requirements'])
                print(f"      {'':>10}   {Colors.YELLOW}Missing: {missing}{Colors.END}")
            print()

    def detect_best_method(self) -> str:
        """Detect the best installation method"""
        if self.args.mode != 'auto':
            return self.args.mode

        # Check for previous installations
        if self.is_repair_needed():
            print(f"{Colors.YELLOW}🔧 Detected existing installation with issues, suggesting repair mode{Colors.END}")
            return 'advanced'

        # Check for GUI availability
        if self.install_methods['gui']['available']:
            print(f"{Colors.GREEN}🎨 GUI mode available, using graphical installer{Colors.END}")
            return 'gui'

        # Check if running in interactive terminal
        if sys.stdin.isatty() and sys.stdout.isatty():
            print(f"{Colors.BLUE}💬 Interactive terminal detected, using wizard mode{Colors.END}")
            return 'wizard'

        # Fallback to advanced
        print(f"{Colors.CYAN}🔧 Using advanced command-line installer{Colors.END}")
        return 'advanced'

    def is_repair_needed(self) -> bool:
        """Check if repair is needed"""
        # Check for common issues
        indicators = [
            Path('.install_state.json').exists() and not Path('.env').exists(),
            Path('.env').exists() and Path('.env').stat().st_size == 0,
            # Add more repair indicators
        ]
        return any(indicators)

    def run_installation_method(self, method: str) -> bool:
        """Run specific installation method"""
        if method not in self.install_methods:
            print(f"{Colors.RED}❌ Unknown installation method: {method}{Colors.END}")
            return False

        config = self.install_methods[method]

        if not config['available']:
            print(f"{Colors.RED}❌ Installation method '{method}' is not available{Colors.END}")
            return False

        print(f"{Colors.CYAN}🚀 Starting installation with method: {method.upper()}{Colors.END}")
        print(f"{Colors.CYAN}🚀 使用方法开始安装: {method.upper()}{Colors.END}\n")

        try:
            if 'function' in config:
                # Direct function call
                return config['function']()
            elif 'module' in config and 'class' in config:
                # Import and instantiate class
                module_name = config['module']
                class_name = config['class']

                try:
                    module = __import__(module_name)
                    installer_class = getattr(module, class_name)
                    installer = installer_class()

                    if hasattr(installer, 'run'):
                        return installer.run()
                    else:
                        print(f"{Colors.RED}❌ Installer class missing 'run' method{Colors.END}")
                        return False

                except ImportError as e:
                    print(f"{Colors.RED}❌ Could not import {module_name}: {e}{Colors.END}")
                    return False
                except AttributeError as e:
                    print(f"{Colors.RED}❌ Could not find {class_name} in {module_name}: {e}{Colors.END}")
                    return False

            else:
                print(f"{Colors.RED}❌ Invalid installation method configuration{Colors.END}")
                return False

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🛑 Installation cancelled by user{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}❌ Installation failed: {e}{Colors.END}")
            if self.args.verbose:
                import traceback
                traceback.print_exc()
            return False

    def quick_install(self) -> bool:
        """Quick installation with defaults"""
        print(f"{Colors.CYAN}⚡ Quick Installation Mode | 快速安装模式{Colors.END}")
        print(f"{Colors.YELLOW}Using default settings for fastest installation{Colors.END}")
        print(f"{Colors.YELLOW}使用默认设置进行最快安装{Colors.END}\n")

        steps = [
            ("检查系统要求", self.check_system_quick),
            ("安装核心依赖", self.install_core_deps),
            ("安装浏览器", self.install_browser_quick),
            ("创建配置", self.create_minimal_config),
            ("设置环境", self.setup_basic_environment),
            ("测试安装", self.test_basic_installation)
        ]

        for step_name, step_func in steps:
            print(f"{Colors.BLUE}🔄 {step_name} | {step_name}{Colors.END}", end=" ... ")
            try:
                if step_func():
                    print(f"{Colors.GREEN}✅{Colors.END}")
                else:
                    print(f"{Colors.RED}❌{Colors.END}")
                    return False
            except Exception as e:
                print(f"{Colors.RED}❌ {str(e)}{Colors.END}")
                return False

        print(f"\n{Colors.GREEN}🎉 Quick installation completed successfully!{Colors.END}")
        print(f"{Colors.GREEN}🎉 快速安装成功完成！{Colors.END}")

        # 默认自动启动，除非用户明确禁用
        if not self.args.no_auto_launch:
            self.launch_application()

        return True

    def check_system_quick(self) -> bool:
        """Quick system check"""
        return self.python_version >= (3, 8)

    def install_core_deps(self) -> bool:
        """Install core dependencies"""
        if self.args.no_deps:
            return True

        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'python-dotenv>=1.0.0',
                'requests>=2.28.0'
            ], capture_output=True, text=True, timeout=120)
            return result.returncode == 0
        except:
            return False

    def install_browser_quick(self) -> bool:
        """Quick browser installation"""
        if self.args.offline:
            return True

        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 'playwright>=1.40.0'
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                result = subprocess.run([
                    sys.executable, '-m', 'playwright', 'install', 'chromium'
                ], capture_output=True, text=True, timeout=180)
                return result.returncode == 0

            return False
        except:
            return False

    def create_minimal_config(self) -> bool:
        """Create minimal configuration"""
        try:
            config_content = """# ManageBac Assignment Checker - Quick Setup
MANAGEBAC_URL=https://shtcs.managebac.cn
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password
REPORT_FORMAT=html,console
OUTPUT_DIR=reports
LANGUAGE=zh
HEADLESS=true
DEBUG=false
"""

            if self.args.config_file and Path(self.args.config_file).exists():
                # Use provided config file
                import shutil
                shutil.copy(self.args.config_file, '.env')
            else:
                # Create default config
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(config_content)

            return True
        except:
            return False

    def setup_basic_environment(self) -> bool:
        """Setup basic environment"""
        try:
            directories = ['logs', 'reports']
            for directory in directories:
                Path(directory).mkdir(exist_ok=True)
            return True
        except:
            return False

    def test_basic_installation(self) -> bool:
        """Test basic installation"""
        try:
            # Test basic imports
            import os
            from pathlib import Path
            return Path('.env').exists()
        except:
            return False

    def launch_application(self):
        """Launch the application"""
        print(f"\n{Colors.CYAN}🚀 Launching application | 启动应用程序{Colors.END}")

        launchers = ['smart_launcher.py', 'gui_launcher.py', 'run_app.py', 'main_new.py']

        for launcher in launchers:
            launcher_path = Path(launcher)
            if launcher_path.exists():
                try:
                    if self.platform == 'windows':
                        subprocess.Popen([sys.executable, str(launcher_path)],
                                       creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        subprocess.Popen([sys.executable, str(launcher_path)])

                    print(f"{Colors.GREEN}✅ Application launched with {launcher}{Colors.END}")
                    return True
                except Exception as e:
                    continue

        print(f"{Colors.YELLOW}⚠️ Could not auto-launch. Run manually: python gui_launcher.py{Colors.END}")
        print(f"{Colors.YELLOW}⚠️ 无法自动启动。请手动运行: python gui_launcher.py{Colors.END}")
        return False

    def run_with_fallback(self) -> bool:
        """Run installation with automatic fallback"""
        method = self.detect_best_method()

        # Handle repair mode
        if self.args.repair:
            print(f"{Colors.YELLOW}🔧 Repair mode activated{Colors.END}")
            method = 'advanced'

        print(f"{Colors.CYAN}Selected method: {method.upper()}{Colors.END}")

        # Try primary method
        if self.run_installation_method(method):
            return True

        # Fallback logic
        print(f"{Colors.YELLOW}⚠️ Primary method '{method}' failed, trying fallbacks...{Colors.END}")

        # Get fallback methods in priority order
        available_methods = [
            (m, config) for m, config in self.install_methods.items()
            if config['available'] and m != method
        ]

        available_methods.sort(key=lambda x: x[1]['priority'])

        for fallback_method, config in available_methods:
            print(f"{Colors.CYAN}🔄 Trying fallback: {fallback_method.upper()}{Colors.END}")
            if self.run_installation_method(fallback_method):
                print(f"{Colors.GREEN}✅ Installation successful with fallback method: {fallback_method.upper()}{Colors.END}")
                return True

        print(f"{Colors.RED}❌ All installation methods failed{Colors.END}")
        return False

    def show_help_and_troubleshooting(self):
        """Show help and troubleshooting information"""
        print(f"""
{Colors.HEADER}🆘 Troubleshooting | 故障排除:{Colors.END}

{Colors.CYAN}Common Issues | 常见问题:{Colors.END}

1. {Colors.YELLOW}Permission Errors | 权限错误:{Colors.END}
   • macOS/Linux: sudo python ultimate_installer.py
   • Windows: Run as Administrator
   • 或使用: --user flag with pip

2. {Colors.YELLOW}Network Issues | 网络问题:{Colors.END}
   • Use VPN or proxy
   • Try: --offline flag for offline installation
   • Use mirror: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple

3. {Colors.YELLOW}Dependencies | 依赖问题:{Colors.END}
   • Create virtual environment: python -m venv venv
   • Use: --no-deps to skip dependency installation

4. {Colors.YELLOW}GUI Not Available | GUI不可用:{Colors.END}
   • Install tkinter: sudo apt-get install python3-tk (Ubuntu/Debian)
   • Use command line: --mode wizard or --mode advanced

{Colors.CYAN}Manual Installation | 手动安装:{Colors.END}
   pip install -r requirements.txt
   python -m playwright install chromium
   cp config.example.env .env
   python main_new.py

{Colors.CYAN}Get Help | 获取帮助:{Colors.END}
   • Documentation: README.md
   • Issues: https://github.com/your-repo/issues
   • Email: support@example.com

{Colors.GREEN}For more verbose output, use: --verbose{Colors.END}
""")

    def run(self) -> bool:
        """Main run method"""
        self.print_banner()

        # Show help if requested
        if '--help' in sys.argv or '-h' in sys.argv:
            return True

        # Show available methods if verbose
        if self.args.verbose:
            self.show_available_methods()

        try:
            success = self.run_with_fallback()

            if not success:
                print(f"\n{Colors.RED}{'='*60}{Colors.END}")
                print(f"{Colors.RED}💥 Installation Failed | 安装失败{Colors.END}")
                print(f"{Colors.RED}{'='*60}{Colors.END}")
                self.show_help_and_troubleshooting()

            return success

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}🛑 Installation cancelled by user{Colors.END}")
            print(f"{Colors.YELLOW}🛑 用户取消安装{Colors.END}")
            return False
        except Exception as e:
            print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
            if self.args.verbose:
                import traceback
                traceback.print_exc()
            return False

def main():
    """Main entry point"""
    installer = UltimateInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()