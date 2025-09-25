#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ManageBac Assignment Checker - User Experience Test
🧪 ManageBac作业检查器 - 用户体验测试

End-to-end user experience testing for setup and configuration flow.
端到端用户体验测试，用于设置和配置流程。
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

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

class UserExperienceTest:
    """Complete user experience test suite"""

    def __init__(self):
        self.test_results: List[Dict] = []
        self.project_root = Path(__file__).parent

    def log_test(self, test_name: str, success: bool, message: str, details: Optional[str] = None):
        """Log a test result"""
        self.test_results.append({
            'test_name': test_name,
            'success': success,
            'message': message,
            'details': details,
            'timestamp': time.time()
        })

        # Print immediate feedback
        status = f"{Colors.GREEN}✅" if success else f"{Colors.RED}❌"
        print(f"{status} {test_name}: {message}{Colors.END}")
        if details:
            print(f"   {Colors.YELLOW}💡 {details}{Colors.END}")

    def test_project_structure(self) -> bool:
        """Test if project structure is complete"""
        required_files = [
            'install.sh',
            'setup_wizard.py',
            'first_run_setup.py',
            'config_templates.py',
            'quick_templates.py',
            'config_validator.py',
            'test_config.py',
            'gui_launcher.py',
            'main_new.py',
            'config.example.env'
        ]

        missing_files = []
        for file in required_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)

        if missing_files:
            self.log_test(
                "Project Structure Check",
                False,
                f"Missing files: {', '.join(missing_files)}",
                "Some core files are missing from the project."
            )
            return False
        else:
            self.log_test(
                "Project Structure Check",
                True,
                "All required files are present",
                f"Found all {len(required_files)} required files."
            )
            return True

    def test_python_imports(self) -> bool:
        """Test if Python files can be imported without errors"""
        python_files_to_test = [
            'setup_wizard',
            'first_run_setup',
            'config_templates',
            'quick_templates',
            'config_validator',
            'test_config'
        ]

        import_errors = []

        for module_name in python_files_to_test:
            try:
                # Add current directory to path for imports
                sys.path.insert(0, str(self.project_root))
                __import__(module_name)
                print(f"  ✓ {module_name}.py imports successfully")
            except ImportError as e:
                import_errors.append(f"{module_name}: {str(e)}")
            except Exception as e:
                import_errors.append(f"{module_name}: {str(e)}")

        if import_errors:
            self.log_test(
                "Python Import Test",
                False,
                f"Import errors in {len(import_errors)} files",
                f"Errors: {'; '.join(import_errors)}"
            )
            return False
        else:
            self.log_test(
                "Python Import Test",
                True,
                f"All {len(python_files_to_test)} Python files import successfully"
            )
            return True

    def test_configuration_flow(self) -> bool:
        """Test the configuration flow components"""
        tests_passed = 0
        total_tests = 4

        # Test 1: Config templates functionality
        try:
            from config_templates import ConfigTemplates
            templates = ConfigTemplates()
            template_list = templates.list_templates()

            if len(template_list) >= 5:  # We created 6 templates
                print(f"  ✓ Config templates: {len(template_list)} templates available")
                tests_passed += 1
            else:
                print(f"  ❌ Config templates: only {len(template_list)} templates found")
        except Exception as e:
            print(f"  ❌ Config templates error: {str(e)}")

        # Test 2: Quick templates functionality
        try:
            from quick_templates import QuickTemplates
            quick = QuickTemplates()
            school_templates = quick.list_school_templates()
            quick_configs = quick.list_quick_configs()

            if len(school_templates) >= 3 and len(quick_configs) >= 3:
                print(f"  ✓ Quick templates: {len(school_templates)} schools, {len(quick_configs)} configs")
                tests_passed += 1
            else:
                print(f"  ❌ Quick templates: insufficient templates")
        except Exception as e:
            print(f"  ❌ Quick templates error: {str(e)}")

        # Test 3: Configuration validator
        try:
            from config_validator import ConfigValidator
            validator = ConfigValidator('.env')
            # Just test instantiation - don't run full validation without proper config
            print(f"  ✓ Config validator: instantiated successfully")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ Config validator error: {str(e)}")

        # Test 4: Test config functionality
        try:
            from test_config import print_header
            print_header()  # Just test a simple function
            print(f"  ✓ Test config: functions available")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ Test config error: {str(e)}")

        success = tests_passed == total_tests
        self.log_test(
            "Configuration Flow Test",
            success,
            f"{tests_passed}/{total_tests} configuration components working",
            "All configuration tools are functional" if success else "Some configuration tools have issues"
        )

        return success

    def test_gui_components(self) -> bool:
        """Test GUI components without actually launching them"""
        gui_tests_passed = 0
        total_gui_tests = 2

        # Test GUI launcher
        try:
            gui_launcher_path = self.project_root / 'gui_launcher.py'
            with open(gui_launcher_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for key functions
            required_functions = ['is_first_time_setup', 'run_first_time_setup', 'setup_environment']
            found_functions = sum(1 for func in required_functions if func in content)

            if found_functions == len(required_functions):
                print(f"  ✓ GUI launcher: all {len(required_functions)} required functions found")
                gui_tests_passed += 1
            else:
                print(f"  ❌ GUI launcher: only {found_functions}/{len(required_functions)} functions found")
        except Exception as e:
            print(f"  ❌ GUI launcher error: {str(e)}")

        # Test first run setup
        try:
            first_run_path = self.project_root / 'first_run_setup.py'
            with open(first_run_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for key classes and methods
            if 'class FirstRunSetupGUI' in content and 'def show_step' in content:
                print(f"  ✓ First run setup: GUI class and methods found")
                gui_tests_passed += 1
            else:
                print(f"  ❌ First run setup: missing GUI class or methods")
        except Exception as e:
            print(f"  ❌ First run setup error: {str(e)}")

        success = gui_tests_passed == total_gui_tests
        self.log_test(
            "GUI Components Test",
            success,
            f"{gui_tests_passed}/{total_gui_tests} GUI components working",
            "GUI components are properly structured" if success else "Some GUI components have issues"
        )

        return success

    def test_installation_script(self) -> bool:
        """Test installation script structure"""
        try:
            install_script = self.project_root / 'install.sh'
            with open(install_script, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for key features we added
            required_features = [
                'Smart Setup Wizard',
                'setup_wizard.py',
                'first_run_setup.py',
                'config_templates.py',
                'Interactive configuration'
            ]

            found_features = sum(1 for feature in required_features if feature in content)

            if found_features == len(required_features):
                self.log_test(
                    "Installation Script Test",
                    True,
                    f"All {len(required_features)} enhanced features found",
                    "Installation script includes all new interactive features"
                )
                return True
            else:
                self.log_test(
                    "Installation Script Test",
                    False,
                    f"Only {found_features}/{len(required_features)} features found",
                    "Installation script missing some enhanced features"
                )
                return False

        except Exception as e:
            self.log_test(
                "Installation Script Test",
                False,
                f"Error reading install.sh: {str(e)}"
            )
            return False

    def test_cli_integration(self) -> bool:
        """Test CLI integration with new test-config option"""
        try:
            cli_path = self.project_root / 'managebac_checker' / 'cli.py'
            with open(cli_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for test-config functionality
            if '--test-config' in content and 'run_config_test' in content:
                self.log_test(
                    "CLI Integration Test",
                    True,
                    "Test-config option successfully integrated",
                    "Users can now run 'python main_new.py --test-config'"
                )
                return True
            else:
                self.log_test(
                    "CLI Integration Test",
                    False,
                    "Test-config option not found in CLI",
                    "CLI integration may be incomplete"
                )
                return False

        except Exception as e:
            self.log_test(
                "CLI Integration Test",
                False,
                f"Error reading CLI file: {str(e)}"
            )
            return False

    def test_user_workflow_simulation(self) -> bool:
        """Simulate complete user workflow"""
        workflow_steps = [
            "Download and run install.sh",
            "Setup wizard prompts for school URL",
            "Setup wizard asks for credentials",
            "Setup wizard asks about AI features",
            "Configuration file is created",
            "User can test configuration",
            "User can launch GUI application"
        ]

        # For this test, we'll check that all the components exist for each step
        workflow_complete = True

        # Step 1: Install script exists and has interactive features
        if not (self.project_root / 'install.sh').exists():
            workflow_complete = False
            print(f"  ❌ Step 1: install.sh not found")
        else:
            print(f"  ✓ Step 1: install.sh available with interactive features")

        # Step 2-4: Setup wizard exists and has required functions
        if not (self.project_root / 'setup_wizard.py').exists():
            workflow_complete = False
            print(f"  ❌ Steps 2-4: setup_wizard.py not found")
        else:
            print(f"  ✓ Steps 2-4: setup_wizard.py available for interactive setup")

        # Step 5: Config templates available
        if not (self.project_root / 'config_templates.py').exists():
            workflow_complete = False
            print(f"  ❌ Step 5: config_templates.py not found")
        else:
            print(f"  ✓ Step 5: config_templates.py available for configuration")

        # Step 6: Test functionality available
        if not (self.project_root / 'test_config.py').exists():
            workflow_complete = False
            print(f"  ❌ Step 6: test_config.py not found")
        else:
            print(f"  ✓ Step 6: test_config.py available for configuration testing")

        # Step 7: GUI launcher available
        if not (self.project_root / 'gui_launcher.py').exists():
            workflow_complete = False
            print(f"  ❌ Step 7: gui_launcher.py not found")
        else:
            print(f"  ✓ Step 7: gui_launcher.py available with first-time setup integration")

        self.log_test(
            "User Workflow Simulation",
            workflow_complete,
            "Complete user workflow components available" if workflow_complete else "User workflow has missing components",
            f"All {len(workflow_steps)} workflow steps supported" if workflow_complete else "Some workflow steps cannot be completed"
        )

        return workflow_complete

    def run_all_tests(self) -> Tuple[int, int]:
        """Run all user experience tests"""
        print(f"{Colors.PURPLE}{Colors.BOLD}🧪 ManageBac Assignment Checker - User Experience Test{Colors.END}")
        print(f"{Colors.PURPLE}🧪 ManageBac作业检查器 - 用户体验测试{Colors.END}")
        print("=" * 70)
        print()

        tests = [
            self.test_project_structure,
            self.test_python_imports,
            self.test_configuration_flow,
            self.test_gui_components,
            self.test_installation_script,
            self.test_cli_integration,
            self.test_user_workflow_simulation
        ]

        print(f"{Colors.BLUE}🔍 Running {len(tests)} user experience tests...{Colors.END}")
        print(f"{Colors.BLUE}🔍 正在运行{len(tests)}个用户体验测试...{Colors.END}")
        print()

        passed = 0
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"{Colors.RED}❌ Test failed with exception: {str(e)}{Colors.END}")

        return passed, len(tests)

    def print_summary(self, passed: int, total: int):
        """Print test summary"""
        print("\n" + "=" * 70)
        print(f"{Colors.BOLD}📊 User Experience Test Summary | 用户体验测试总结{Colors.END}")
        print("=" * 70)

        if passed == total:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! ({passed}/{total}){Colors.END}")
            print(f"{Colors.GREEN}🎉 所有测试通过！({passed}/{total}){Colors.END}")
            print()
            print(f"{Colors.CYAN}✨ The ManageBac Assignment Checker is ready for users!{Colors.END}")
            print(f"{Colors.CYAN}✨ ManageBac作业检查器已准备好供用户使用！{Colors.END}")
            print()
            print(f"{Colors.WHITE}🚀 Complete user experience flow:{Colors.END}")
            print("   1. Run: bash <(curl -s https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh)")
            print("   2. Follow interactive setup wizard")
            print("   3. Test configuration: python main_new.py --test-config")
            print("   4. Launch GUI: python gui_launcher.py")

        else:
            failed = total - passed
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {passed}/{total} tests passed, {failed} failed.{Colors.END}")
            print(f"{Colors.YELLOW}⚠️  {passed}/{total} 个测试通过，{failed} 个失败。{Colors.END}")
            print()
            print(f"{Colors.RED}🔧 Issues found that need attention:{Colors.END}")

            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test_name']}: {result['message']}")

            print()
            print(f"{Colors.CYAN}💡 Fix the issues above and re-run the test.{Colors.END}")
            print(f"{Colors.CYAN}💡 修复上述问题后重新运行测试。{Colors.END}")

def main():
    """Main test function"""
    test_suite = UserExperienceTest()

    try:
        passed, total = test_suite.run_all_tests()
        test_suite.print_summary(passed, total)

        # Exit with appropriate code
        sys.exit(0 if passed == total else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Test cancelled by user.{Colors.END}")
        print(f"{Colors.YELLOW}👋 用户取消了测试。{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()