#!/usr/bin/env python3
"""
Comprehensive Diagnostic Tool
综合诊断工具

Diagnoses both GUI crash issues and assignment detection problems
诊断GUI闪退问题和作业检测问题
"""

import os
import sys
import time
import subprocess
import traceback
from pathlib import Path
import platform


class ComprehensiveDiagnostic:
    """Comprehensive diagnostic for all major issues"""

    def __init__(self):
        self.working_dir = Path.cwd()
        self.system = platform.system()
        self.python_version = sys.version_info
        self.issues_found = []
        self.solutions = []

    def log_issue(self, category, description, severity="WARNING"):
        """Log an issue found during diagnosis"""
        self.issues_found.append({
            "category": category,
            "description": description,
            "severity": severity
        })
        icon = "🔴" if severity == "CRITICAL" else "🟡" if severity == "WARNING" else "ℹ️"
        print(f"{icon} [{category}] {description}")

    def log_solution(self, solution):
        """Log a suggested solution"""
        self.solutions.append(solution)
        print(f"💡 Solution: {solution}")

    def check_basic_environment(self):
        """Check basic Python environment"""
        print("\n🔍 Checking Basic Environment...")
        print("="*50)

        # Python version
        if self.python_version >= (3, 8):
            print(f"✅ Python version: {self.python_version.major}.{self.python_version.minor}")
        else:
            self.log_issue("Environment", f"Python version too old: {self.python_version}", "CRITICAL")
            self.log_solution("Upgrade to Python 3.8+")

        # Working directory
        print(f"📁 Working directory: {self.working_dir}")

        # Check for required files
        required_files = [
            "managebac_checker/",
            ".env",
            "requirements.txt"
        ]

        for file_path in required_files:
            path = Path(file_path)
            if path.exists():
                print(f"✅ {file_path} exists")
            else:
                self.log_issue("Files", f"Missing {file_path}", "WARNING")

    def check_gui_specific_issues(self):
        """Check for GUI-specific problems"""
        print("\n🖥️ Checking GUI Issues...")
        print("="*50)

        # Test tkinter import
        try:
            import tkinter as tk
            print("✅ tkinter import successful")

            # Test basic tkinter window
            try:
                root = tk.Tk()
                root.withdraw()  # Hide the window
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                print(f"✅ tkinter window test successful (screen: {screen_width}x{screen_height})")
            except Exception as e:
                self.log_issue("GUI", f"tkinter window creation failed: {e}", "CRITICAL")
                self.log_solution("Check display server and GUI permissions")

        except ImportError as e:
            self.log_issue("GUI", f"tkinter not available: {e}", "CRITICAL")
            self.log_solution("Install tkinter: apt-get install python3-tk (Linux) or reinstall Python with tkinter")

        # Check for macOS specific issues
        if self.system == "Darwin":
            print("🍎 macOS specific checks...")

            # Check for GUI frameworks
            try:
                result = subprocess.run(['python3', '-c', 'import tkinter; print("tkinter OK")'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print("✅ macOS tkinter working in subprocess")
                else:
                    self.log_issue("macOS", f"tkinter subprocess failed: {result.stderr}", "WARNING")
            except subprocess.TimeoutExpired:
                self.log_issue("macOS", "tkinter subprocess timed out", "WARNING")
                self.log_solution("Check for hanging GUI processes")

    def test_professional_gui_import(self):
        """Test professional GUI module import"""
        print("\n📱 Testing Professional GUI Import...")
        print("="*50)

        try:
            # Test basic import
            from managebac_checker.professional_gui import ProfessionalManageBacGUI
            print("✅ ProfessionalManageBacGUI import successful")

            # Test theme import
            from managebac_checker.professional_gui import ProfessionalTheme
            theme = ProfessionalTheme("professional_light")
            print("✅ ProfessionalTheme creation successful")

            # Test notification manager
            from managebac_checker.system_tray import NotificationManager
            notification_manager = NotificationManager("zh")
            print("✅ NotificationManager creation successful")

        except ImportError as e:
            self.log_issue("GUI Import", f"Cannot import GUI modules: {e}", "CRITICAL")
            self.log_solution("Check managebac_checker package installation")
        except Exception as e:
            self.log_issue("GUI Init", f"GUI component initialization failed: {e}", "WARNING")
            self.log_solution("Check dependencies and system compatibility")

    def test_gui_startup_sequence(self):
        """Test the exact GUI startup sequence that's failing"""
        print("\n🚀 Testing GUI Startup Sequence...")
        print("="*50)

        try:
            # Import enhanced error handler if available
            try:
                from enhanced_error_handler import get_error_handler, handle_error, log_info
                print("✅ Enhanced error handler available")
            except ImportError:
                print("⚠️ Enhanced error handler not available, using fallback")

            # Test the exact same sequence as professional_gui main()
            print("📋 Step 1: Import main function...")
            from managebac_checker.professional_gui import main
            print("✅ main function imported")

            print("📋 Step 2: Test in subprocess with timeout...")
            # Create a simple test script
            test_script = '''
import sys
import signal
def timeout_handler(signum, frame):
    print("❌ GUI startup timed out")
    sys.exit(1)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)  # 10 second timeout

try:
    from managebac_checker.professional_gui import ProfessionalManageBacGUI
    print("✅ Creating GUI instance...")
    app = ProfessionalManageBacGUI()
    print("✅ GUI instance created successfully")
    print("🎯 GUI initialization completed - would start mainloop here")
    sys.exit(0)
except Exception as e:
    print(f"❌ GUI creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''

            with open('temp_gui_test.py', 'w') as f:
                f.write(test_script)

            try:
                result = subprocess.run([sys.executable, 'temp_gui_test.py'],
                                      capture_output=True, text=True, timeout=15)

                print("📤 GUI test output:")
                print(result.stdout)

                if result.stderr:
                    print("📤 GUI test errors:")
                    print(result.stderr)

                if result.returncode == 0:
                    print("✅ GUI startup sequence successful")
                else:
                    self.log_issue("GUI Startup", f"GUI creation failed with code {result.returncode}", "CRITICAL")
                    self.log_solution("Check the error output above for specific failure points")

            except subprocess.TimeoutExpired:
                self.log_issue("GUI Startup", "GUI startup timed out (likely hanging)", "CRITICAL")
                self.log_solution("GUI is hanging - check for modal dialogs or blocking operations")
            finally:
                # Clean up temp file
                if Path('temp_gui_test.py').exists():
                    Path('temp_gui_test.py').unlink()

        except Exception as e:
            self.log_issue("GUI Test", f"GUI startup test failed: {e}", "CRITICAL")
            traceback.print_exc()

    def check_assignment_detection(self):
        """Check assignment detection logic"""
        print("\n📚 Checking Assignment Detection...")
        print("="*50)

        # Check .env configuration
        env_file = Path('.env')
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()

                if 'your-email@example.com' in content or 'your-password' in content:
                    self.log_issue("Config", "Using example credentials in .env file", "CRITICAL")
                    self.log_solution("Update .env file with real ManageBac credentials")
                else:
                    print("✅ .env file appears to have real credentials")

                # Check required fields
                required_fields = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
                for field in required_fields:
                    if field in content and f'{field}=' in content:
                        print(f"✅ {field} present in .env")
                    else:
                        self.log_issue("Config", f"Missing {field} in .env", "CRITICAL")

            except Exception as e:
                self.log_issue("Config", f"Cannot read .env file: {e}", "CRITICAL")
        else:
            self.log_issue("Config", ".env file not found", "CRITICAL")
            self.log_solution("Create .env file with ManageBac credentials")

        # Test scraper import
        try:
            from managebac_checker.scraper import ManageBacScraper
            print("✅ ManageBacScraper import successful")
        except ImportError as e:
            self.log_issue("Scraper", f"Cannot import scraper: {e}", "CRITICAL")

        # Test config loading
        try:
            from managebac_checker.config import Config
            config = Config(interactive=False)
            print("✅ Config loading successful")

            # Check if config has valid values
            if hasattr(config, 'managebac_email') and config.managebac_email:
                if 'example.com' not in config.managebac_email:
                    print(f"✅ Email configured: {config.managebac_email[:10]}...")
                else:
                    self.log_issue("Config", "Still using example email", "WARNING")
            else:
                self.log_issue("Config", "No email configured", "CRITICAL")

        except Exception as e:
            self.log_issue("Config", f"Config loading failed: {e}", "WARNING")
            self.log_solution("Check .env file format and values")

    def test_assignment_fetch(self):
        """Test actual assignment fetching if credentials are available"""
        print("\n🔍 Testing Assignment Fetch...")
        print("="*50)

        try:
            from managebac_checker.config import Config
            config = Config(interactive=False)

            if (hasattr(config, 'managebac_email') and
                config.managebac_email and
                'example.com' not in config.managebac_email):

                print("🔐 Real credentials found, testing assignment fetch...")

                # Import and test scraper
                from managebac_checker.scraper import ManageBacScraper
                scraper = ManageBacScraper(config)

                print("🌐 Testing authentication...")
                # Note: This is just a test, we won't actually scrape without user permission
                print("⚠️ Skipping actual scrape test to avoid hitting ManageBac servers repeatedly")
                print("💡 To test assignment detection, run: python3 main_new.py")

            else:
                print("⚠️ Example credentials detected, skipping live test")
                self.log_solution("Configure real ManageBac credentials to test assignment detection")

        except Exception as e:
            self.log_issue("Assignment Fetch", f"Assignment fetch test failed: {e}", "WARNING")

    def generate_report(self):
        """Generate diagnostic report"""
        print("\n" + "="*60)
        print("📊 COMPREHENSIVE DIAGNOSTIC REPORT")
        print("📊 综合诊断报告")
        print("="*60)

        print(f"\n🖥️ System Information:")
        print(f"   Platform: {self.system}")
        print(f"   Python: {self.python_version.major}.{self.python_version.minor}")
        print(f"   Working Directory: {self.working_dir}")

        if self.issues_found:
            print(f"\n❌ Issues Found ({len(self.issues_found)}):")
            critical_count = len([i for i in self.issues_found if i['severity'] == 'CRITICAL'])
            warning_count = len([i for i in self.issues_found if i['severity'] == 'WARNING'])

            print(f"   🔴 Critical: {critical_count}")
            print(f"   🟡 Warnings: {warning_count}")

            for issue in self.issues_found:
                severity_icon = "🔴" if issue['severity'] == 'CRITICAL' else "🟡"
                print(f"   {severity_icon} [{issue['category']}] {issue['description']}")

        if self.solutions:
            print(f"\n💡 Suggested Solutions ({len(self.solutions)}):")
            for i, solution in enumerate(self.solutions, 1):
                print(f"   {i}. {solution}")

        # Specific recommendations
        print(f"\n🎯 Specific Recommendations:")

        gui_issues = [i for i in self.issues_found if i['category'] in ['GUI', 'GUI Import', 'GUI Startup']]
        if gui_issues:
            print(f"   📱 GUI Issues: Run 'python3 fixed_gui.py' to test basic GUI")

        config_issues = [i for i in self.issues_found if i['category'] == 'Config']
        if config_issues:
            print(f"   🔐 Config Issues: Update .env file with real ManageBac credentials")

        if not self.issues_found:
            print("\n✅ No major issues detected!")
            print("✅ 未发现重大问题！")
        else:
            print(f"\n🔧 Priority: Fix critical issues first, then warnings")
            print(f"🔧 优先级：先修复关键问题，然后处理警告")

    def run_full_diagnostic(self):
        """Run complete diagnostic suite"""
        print("🚀 Starting Comprehensive Diagnostic...")
        print("🚀 开始综合诊断...")
        print("="*60)

        self.check_basic_environment()
        self.check_gui_specific_issues()
        self.test_professional_gui_import()
        self.test_gui_startup_sequence()
        self.check_assignment_detection()
        self.test_assignment_fetch()
        self.generate_report()

        return len([i for i in self.issues_found if i['severity'] == 'CRITICAL']) == 0


def main():
    """Main diagnostic function"""
    diagnostic = ComprehensiveDiagnostic()
    success = diagnostic.run_full_diagnostic()

    if success:
        print("\n🎉 Diagnostic completed - system appears healthy!")
        return True
    else:
        print("\n⚠️ Diagnostic completed - issues found that need attention")
        return False


if __name__ == "__main__":
    main()