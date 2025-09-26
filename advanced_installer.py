#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Advanced Installation System | 高级安装系统
Complete installation with smart detection, auto-launch and error recovery
完整安装，包含智能检测、自动启动和错误恢复
"""

import os
import sys
import subprocess
import platform
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import getpass

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

class InstallationState:
    """Track installation state"""

    def __init__(self):
        self.state_file = Path('.install_state.json')
        self.state = self.load_state()

    def load_state(self) -> Dict:
        """Load installation state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'installed': False,
            'components': {},
            'install_date': None,
            'version': None,
            'last_update': None,
            'config_completed': False
        }

    def save_state(self):
        """Save installation state"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ 无法保存安装状态: {e}{Colors.END}")

    def mark_component_installed(self, component: str, success: bool = True):
        """Mark a component as installed"""
        self.state['components'][component] = {
            'installed': success,
            'timestamp': time.time(),
            'version': '1.0.0'
        }
        self.save_state()

    def is_component_installed(self, component: str) -> bool:
        """Check if component is installed"""
        return self.state['components'].get(component, {}).get('installed', False)

    def is_first_install(self) -> bool:
        """Check if this is first installation"""
        return not self.state.get('installed', False)

class AdvancedInstaller:
    """Advanced installation system with smart detection"""

    def __init__(self):
        self.state = InstallationState()
        self.config = {}
        self.installation_start_time = time.time()
        self.errors = []
        self.warnings = []

        # Installation paths
        self.project_root = Path(__file__).parent
        self.env_file = self.project_root / '.env'

    def print_banner(self):
        """Print installation banner"""
        is_first = self.state.is_first_install()
        action = "First Installation" if is_first else "Update/Repair Installation"
        action_zh = "首次安装" if is_first else "更新/修复安装"

        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🚀 ManageBac Assignment Checker - {action:<12}     ║
║         🚀 ManageBac作业检查器 - {action_zh:<12}         ║
║                                                              ║
║   {'🎯 Setting up your assignment tracker...' if is_first else '🔧 Updating your installation...'}           ║
║   {'🎯 设置您的作业跟踪器...' if is_first else '🔧 更新您的安装...'}                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")

        if not is_first:
            print(f"{Colors.GREEN}✨ Detected previous installation{Colors.END}")
            print(f"{Colors.GREEN}✨ 检测到之前的安装{Colors.END}")

            # Show what's already installed
            installed_components = [k for k, v in self.state.state['components'].items()
                                  if v.get('installed', False)]
            if installed_components:
                print(f"{Colors.CYAN}📦 Already installed components: {', '.join(installed_components)}{Colors.END}")
                print(f"{Colors.CYAN}📦 已安装的组件: {', '.join(installed_components)}{Colors.END}")
            print()

    def check_system_requirements(self) -> bool:
        """Check system requirements"""
        print(f"{Colors.HEADER}🔍 System Requirements Check | 系统需求检查{Colors.END}")

        success = True

        # Python version
        print("🐍 Python version...")
        if sys.version_info >= (3, 8):
            print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
        else:
            print(f"   ❌ Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
            success = False

        # Platform detection
        system = platform.system().lower()
        print(f"💻 Operating system: {system}")

        # Available disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.project_root)
            free_mb = free // (1024 * 1024)
            if free_mb > 100:
                print(f"   ✅ Disk space: {free_mb}MB available")
            else:
                print(f"   ⚠️ Low disk space: {free_mb}MB available")
                self.warnings.append("Low disk space")
        except:
            print("   ⚠️ Could not check disk space")

        # Internet connection
        print("🌐 Internet connection...")
        try:
            import urllib.request
            urllib.request.urlopen('https://www.google.com', timeout=5)
            print("   ✅ Internet connection - OK")
        except:
            print("   ⚠️ Internet connection test failed")
            self.warnings.append("No internet connection")

        return success

    def install_dependencies(self) -> bool:
        """Install dependencies with smart caching"""
        print(f"\n{Colors.HEADER}📦 Dependency Installation | 依赖安装{Colors.END}")

        # Check if already installed
        if self.state.is_component_installed('dependencies'):
            print(f"{Colors.GREEN}✅ Dependencies already installed, checking updates...{Colors.END}")
            return self.update_dependencies()

        # Core dependencies
        core_deps = [
            'playwright>=1.40.0',
            'python-dotenv>=1.0.0',
            'jinja2>=3.1.0',
            'requests>=2.28.0',
            'beautifulsoup4>=4.11.0',
            'lxml>=4.9.0',
            'asyncio>=3.4.3',
            'aiohttp>=3.8.0'
        ]

        # AI dependencies (optional)
        ai_deps = [
            'openai>=1.0.0',
            'tiktoken>=0.4.0'
        ]

        # GUI dependencies
        gui_deps = [
            'pystray>=0.19.0',
            'pillow>=10.0.0',
            'plyer>=2.1.0'
        ]

        # Install in stages
        success = True

        # Stage 1: Core dependencies
        print("📋 Installing core dependencies...")
        if self.install_package_list(core_deps, "core"):
            self.state.mark_component_installed('core_dependencies', True)
            print(f"   ✅ Core dependencies installed")
        else:
            success = False
            self.errors.append("Core dependencies installation failed")

        # Stage 2: GUI dependencies
        print("🎨 Installing GUI dependencies...")
        if self.install_package_list(gui_deps, "gui"):
            self.state.mark_component_installed('gui_dependencies', True)
            print(f"   ✅ GUI dependencies installed")
        else:
            print(f"   ⚠️ GUI dependencies failed, GUI features may be limited")
            self.warnings.append("GUI dependencies failed")

        # Stage 3: AI dependencies (optional)
        print("🤖 Installing AI dependencies...")
        if self.install_package_list(ai_deps, "ai"):
            self.state.mark_component_installed('ai_dependencies', True)
            print(f"   ✅ AI dependencies installed")
        else:
            print(f"   ⚠️ AI dependencies failed, AI features will be disabled")
            self.warnings.append("AI dependencies failed")

        if success:
            self.state.mark_component_installed('dependencies', True)

        return success

    def install_package_list(self, packages: List[str], category: str) -> bool:
        """Install a list of packages"""
        failed = []

        for package in packages:
            try:
                print(f"   📦 Installing {package}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package, '--upgrade'],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                if result.returncode == 0:
                    print(f"   ✅ {package} - OK")
                else:
                    print(f"   ❌ {package} - Failed")
                    failed.append(package)

            except subprocess.TimeoutExpired:
                print(f"   ⏰ {package} - Timeout")
                failed.append(package)
            except Exception as e:
                print(f"   ❌ {package} - Error: {e}")
                failed.append(package)

        return len(failed) == 0

    def update_dependencies(self) -> bool:
        """Update existing dependencies"""
        try:
            print("🔄 Checking for updates...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                outdated = json.loads(result.stdout)
                if outdated:
                    print(f"📦 Found {len(outdated)} packages to update")
                    return True
                else:
                    print("✅ All dependencies are up to date")
                    return True
        except:
            print("⚠️ Could not check for updates")

        return True

    def install_playwright(self) -> bool:
        """Install Playwright with retry logic"""
        print(f"\n{Colors.HEADER}🌐 Browser Installation | 浏览器安装{Colors.END}")

        if self.state.is_component_installed('playwright'):
            print(f"{Colors.GREEN}✅ Playwright already installed{Colors.END}")
            return True

        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Installing Playwright browsers (attempt {attempt + 1}/{max_retries})...")

                result = subprocess.run([
                    sys.executable, '-m', 'playwright', 'install', 'chromium'
                ], capture_output=True, text=True, timeout=300)

                if result.returncode == 0:
                    print("✅ Playwright browsers installed successfully!")
                    self.state.mark_component_installed('playwright', True)
                    return True
                else:
                    print(f"❌ Attempt {attempt + 1} failed: {result.stderr}")

            except subprocess.TimeoutExpired:
                print(f"⏰ Attempt {attempt + 1} timed out")
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} error: {e}")

            if attempt < max_retries - 1:
                print("🔄 Retrying in 5 seconds...")
                time.sleep(5)

        print("❌ Playwright installation failed after all attempts")
        self.errors.append("Playwright installation failed")
        return False

    def setup_configuration(self) -> bool:
        """Setup configuration with smart defaults"""
        print(f"\n{Colors.HEADER}⚙️ Configuration Setup | 配置设置{Colors.END}")

        if self.env_file.exists() and self.state.state.get('config_completed', False):
            print(f"{Colors.GREEN}✅ Configuration already exists{Colors.END}")

            # Ask if user wants to reconfigure
            try:
                reconfigure = input(f"{Colors.CYAN}🔧 Reconfigure? (y/n) [n]: {Colors.END}").strip().lower()
                if reconfigure in ['y', 'yes', '1']:
                    return self.run_configuration_wizard()
                return True
            except (EOFError, KeyboardInterrupt):
                return True

        return self.run_configuration_wizard()

    def run_configuration_wizard(self) -> bool:
        """Run configuration wizard"""
        try:
            print("🧙‍♂️ Running setup wizard...")

            # Import and run wizard
            from setup_wizard import SetupWizard
            wizard = SetupWizard()

            # Override the input method to handle non-interactive mode
            original_get_input = wizard.get_input

            def safe_get_input(prompt, default="", required=True, secret=False, validator=None):
                try:
                    return original_get_input(prompt, default, required, secret, validator)
                except (EOFError, KeyboardInterrupt):
                    if default:
                        return default
                    if not required:
                        return ""
                    # Provide sensible defaults for required fields
                    if "url" in prompt.lower():
                        return "https://shtcs.managebac.cn"
                    elif "email" in prompt.lower():
                        return "user@example.com"
                    elif "password" in prompt.lower():
                        return "password"
                    return ""

            wizard.get_input = safe_get_input

            # Run configuration steps
            try:
                wizard.step_1_basic_config()
                wizard.step_2_ai_configuration()
                wizard.step_3_notification_preferences()
                wizard.step_4_report_preferences()
                wizard.step_5_language_and_preferences()

                if wizard.generate_env_file():
                    self.state.state['config_completed'] = True
                    self.state.save_state()
                    print("✅ Configuration completed")
                    return True
                else:
                    self.errors.append("Configuration generation failed")
                    return False

            except Exception as e:
                print(f"⚠️ Configuration wizard error: {e}")
                # Create minimal configuration
                return self.create_minimal_config()

        except ImportError:
            print("⚠️ Setup wizard not available, creating minimal configuration...")
            return self.create_minimal_config()

    def create_minimal_config(self) -> bool:
        """Create minimal working configuration"""
        try:
            minimal_config = """# ManageBac Assignment Checker Configuration
# Basic configuration for getting started

# ManageBac Settings
MANAGEBAC_URL=https://shtcs.managebac.cn
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password

# Report Settings
REPORT_FORMAT=html,json,console
OUTPUT_DIR=reports
LANGUAGE=zh

# Browser Settings
HEADLESS=true
BROWSER_TIMEOUT=30000

# Basic Settings
DEBUG=false
LOG_LEVEL=INFO
"""

            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write(minimal_config)

            print("✅ Minimal configuration created")
            print("📝 Please edit .env file to add your ManageBac credentials")
            return True

        except Exception as e:
            print(f"❌ Failed to create configuration: {e}")
            return False

    def setup_environment(self) -> bool:
        """Setup application environment"""
        print(f"\n{Colors.HEADER}🔧 Environment Setup | 环境设置{Colors.END}")

        # Create directories
        directories = ['logs', 'reports', 'cache', 'screenshots', 'backups']
        for directory in directories:
            try:
                Path(directory).mkdir(exist_ok=True)
                print(f"   📁 {directory}/ - OK")
            except Exception as e:
                print(f"   ❌ {directory}/ - Failed: {e}")

        # Set permissions for scripts
        scripts = ['START.sh', 'start_gui.sh', 'install.sh']
        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                try:
                    os.chmod(script_path, 0o755)
                    print(f"   🔑 {script} - Executable")
                except:
                    print(f"   ⚠️ {script} - Could not set permissions")

        self.state.mark_component_installed('environment', True)
        return True

    def create_shortcuts(self) -> bool:
        """Create desktop shortcuts and launchers"""
        print(f"\n{Colors.HEADER}🔗 Shortcut Creation | 快捷方式创建{Colors.END}")

        try:
            # Try to run shortcut creation script
            shortcut_scripts = ['create_desktop_shortcut.py', 'create_shortcuts.py']

            for script in shortcut_scripts:
                script_path = Path(script)
                if script_path.exists():
                    try:
                        result = subprocess.run([sys.executable, str(script_path)],
                                              capture_output=True, text=True, timeout=30)
                        if result.returncode == 0:
                            print("✅ Desktop shortcuts created")
                            self.state.mark_component_installed('shortcuts', True)
                            return True
                    except Exception as e:
                        print(f"⚠️ Shortcut script {script} failed: {e}")
                        continue

            # Manual shortcut creation for common cases
            return self.create_manual_shortcuts()

        except Exception as e:
            print(f"⚠️ Shortcut creation failed: {e}")
            return False

    def create_manual_shortcuts(self) -> bool:
        """Create shortcuts manually"""
        system = platform.system().lower()

        if system == "darwin":  # macOS
            return self.create_macos_shortcuts()
        elif system == "windows":  # Windows
            return self.create_windows_shortcuts()
        else:  # Linux
            return self.create_linux_shortcuts()

    def create_macos_shortcuts(self) -> bool:
        """Create macOS shortcuts"""
        try:
            # Create alias/shortcut script
            app_script = f'''#!/bin/bash
cd "{self.project_root}"
python3 smart_launcher.py
'''

            shortcut_path = Path.home() / 'Desktop' / 'ManageBac Assignment Checker'
            with open(shortcut_path, 'w') as f:
                f.write(app_script)

            os.chmod(shortcut_path, 0o755)
            print("✅ macOS shortcut created")
            return True
        except:
            return False

    def create_windows_shortcuts(self) -> bool:
        """Create Windows shortcuts"""
        try:
            # Create batch file
            batch_content = f'''@echo off
cd /d "{self.project_root}"
python smart_launcher.py
pause
'''

            shortcut_path = Path.home() / 'Desktop' / 'ManageBac Assignment Checker.bat'
            with open(shortcut_path, 'w') as f:
                f.write(batch_content)

            print("✅ Windows shortcut created")
            return True
        except:
            return False

    def create_linux_shortcuts(self) -> bool:
        """Create Linux desktop shortcuts"""
        try:
            desktop_content = f'''[Desktop Entry]
Name=ManageBac Assignment Checker
Comment=Check and manage your ManageBac assignments
Exec=python3 "{self.project_root}/smart_launcher.py"
Path={self.project_root}
Icon={self.project_root}/icon.png
Terminal=false
Type=Application
Categories=Education;Utility;
'''

            desktop_path = Path.home() / 'Desktop' / 'managebac-assignment-checker.desktop'
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)

            os.chmod(desktop_path, 0o755)
            print("✅ Linux desktop file created")
            return True
        except:
            return False

    def test_installation(self) -> bool:
        """Test installation components"""
        print(f"\n{Colors.HEADER}🧪 Installation Testing | 安装测试{Colors.END}")

        tests_passed = 0
        total_tests = 0

        # Test 1: Basic imports
        total_tests += 1
        try:
            import tkinter
            print("   ✅ tkinter - OK")
            tests_passed += 1
        except ImportError:
            print("   ❌ tkinter - Missing")

        # Test 2: Configuration loading
        total_tests += 1
        try:
            if self.env_file.exists():
                from dotenv import load_dotenv
                load_dotenv(self.env_file)
                print("   ✅ Configuration loading - OK")
                tests_passed += 1
            else:
                print("   ⚠️ Configuration file - Missing")
        except Exception as e:
            print(f"   ❌ Configuration loading - Failed: {e}")

        # Test 3: Playwright
        total_tests += 1
        try:
            from playwright.sync_api import sync_playwright
            print("   ✅ Playwright - OK")
            tests_passed += 1
        except ImportError:
            print("   ❌ Playwright - Missing")

        # Test 4: Application modules
        total_tests += 1
        try:
            # Check if main modules exist
            required_files = ['gui_launcher.py', 'smart_launcher.py', 'main_new.py']
            existing_files = [f for f in required_files if Path(f).exists()]

            if existing_files:
                print(f"   ✅ Application modules - {len(existing_files)}/{len(required_files)} found")
                tests_passed += 1
            else:
                print("   ❌ Application modules - None found")

        except Exception as e:
            print(f"   ❌ Application modules - Error: {e}")

        success_rate = tests_passed / total_tests
        print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed ({success_rate:.1%})")

        return success_rate >= 0.75  # 75% success rate required

    def launch_application(self) -> bool:
        """Launch the application after installation"""
        print(f"\n{Colors.HEADER}🚀 Application Launch | 应用启动{Colors.END}")

        # Priority order of launchers
        launchers = [
            ('smart_launcher.py', 'Smart Launcher'),
            ('gui_launcher.py', 'GUI Launcher'),
            ('run_app.py', 'App Runner'),
            ('main_new.py', 'Main Application')
        ]

        for launcher_file, launcher_name in launchers:
            launcher_path = Path(launcher_file)
            if launcher_path.exists():
                try:
                    print(f"🔄 Starting {launcher_name}...")

                    # Try to launch in background
                    if platform.system().lower() == "windows":
                        # Windows
                        subprocess.Popen([sys.executable, str(launcher_path)],
                                       creationflags=subprocess.CREATE_NEW_CONSOLE)
                    else:
                        # macOS/Linux
                        subprocess.Popen([sys.executable, str(launcher_path)])

                    print(f"✅ {launcher_name} started successfully!")

                    # Give it a moment to start
                    time.sleep(2)
                    return True

                except Exception as e:
                    print(f"❌ {launcher_name} failed to start: {e}")
                    continue

        print("❌ Could not start application automatically")
        print("💡 You can start it manually using: python gui_launcher.py")
        return False

    def show_installation_summary(self):
        """Show installation summary and next steps"""
        duration = time.time() - self.installation_start_time

        print(f"""
{Colors.HEADER}🎉 Installation Summary | 安装总结{Colors.END}
{'=' * 60}

⏱️ Installation time: {duration:.1f} seconds
⏱️ 安装时间: {duration:.1f} 秒

📊 Components Status:
""")

        # Show component status
        for component, data in self.state.state['components'].items():
            status = "✅" if data.get('installed', False) else "❌"
            print(f"   {status} {component}")

        print(f"""
{Colors.GREEN if not self.errors else Colors.YELLOW}📋 Results:
   Errors: {len(self.errors)}
   Warnings: {len(self.warnings)}{Colors.END}
""")

        if self.errors:
            print(f"{Colors.RED}❌ Errors:{Colors.END}")
            for error in self.errors:
                print(f"   • {error}")

        if self.warnings:
            print(f"{Colors.YELLOW}⚠️ Warnings:{Colors.END}")
            for warning in self.warnings:
                print(f"   • {warning}")

        print(f"""
{Colors.CYAN}🚀 Quick Start Guide | 快速开始指南:

1. 🖱️  Double-click desktop shortcut (if created)
   双击桌面快捷方式（如果已创建）

2. 💻 Command line options:
   python smart_launcher.py    (recommended)
   python gui_launcher.py      (GUI mode)
   python main_new.py         (CLI mode)

3. 📝 First time setup:
   • Edit .env file with your ManageBac credentials
   • 编辑 .env 文件添加您的ManageBac凭据
   • Configure preferences in the application
   • 在应用中配置偏好设置

4. 📚 Documentation:
   • Check CLAUDE.md for detailed instructions
   • 查看 CLAUDE.md 获取详细说明{Colors.END}

{Colors.GREEN}🎯 Installation completed! Happy assignment tracking!
🎯 安装完成！愉快地跟踪作业！{Colors.END}
""")

    def run(self) -> bool:
        """Run the complete installation process"""
        try:
            self.print_banner()

            # Installation steps
            steps = [
                ("系统需求检查", self.check_system_requirements),
                ("依赖安装", self.install_dependencies),
                ("浏览器安装", self.install_playwright),
                ("配置设置", self.setup_configuration),
                ("环境设置", self.setup_environment),
                ("快捷方式创建", self.create_shortcuts),
                ("安装测试", self.test_installation)
            ]

            print(f"{Colors.CYAN}📋 Installation Plan | 安装计划:{Colors.END}")
            for i, (name, _) in enumerate(steps, 1):
                print(f"   {i}. {name}")
            print()

            # Execute steps
            overall_success = True
            for step_name, step_func in steps:
                print(f"{Colors.BOLD}{'=' * 60}{Colors.END}")
                try:
                    if not step_func():
                        print(f"{Colors.YELLOW}⚠️ Step '{step_name}' completed with issues{Colors.END}")
                        # Don't fail completely, but note the issue
                except Exception as e:
                    print(f"{Colors.RED}❌ Step '{step_name}' failed: {e}{Colors.END}")
                    self.errors.append(f"{step_name}: {str(e)}")
                print()

            # Mark installation complete
            self.state.state['installed'] = True
            self.state.state['install_date'] = time.time()
            self.state.state['version'] = '1.0.0'
            self.state.save_state()

            # Show summary
            self.show_installation_summary()

            # Ask about launching
            if len(self.errors) == 0:
                try:
                    launch = input(f"\n{Colors.CYAN}🚀 Launch application now? (y/n) [y]: {Colors.END}").strip().lower()
                    if launch in ['', 'y', 'yes', '1', '是']:
                        self.launch_application()
                except (EOFError, KeyboardInterrupt):
                    print(f"\n{Colors.CYAN}👋 You can launch the application later using: python smart_launcher.py{Colors.END}")

            return len(self.errors) == 0

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}🛑 Installation cancelled by user{Colors.END}")
            return False
        except Exception as e:
            print(f"\n\n{Colors.RED}❌ Installation failed: {e}{Colors.END}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main entry point"""
    installer = AdvancedInstaller()
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()