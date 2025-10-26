#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 ManageBac Assignment Checker - Configuration Validator
🔍 ManageBac作业检查器 - 配置验证器

Validates configuration settings and tests functionality.
验证配置设置并测试功能。
"""

import os
import sys
import re
import asyncio
import urllib.parse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

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

@dataclass
class ValidationResult:
    """Result of a configuration validation test"""
    test_name: str
    success: bool
    message: str
    details: Optional[str] = None

class ConfigValidator:
    """Configuration validator for ManageBac Assignment Checker"""

    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self.config: Dict[str, str] = {}
        self.results: List[ValidationResult] = []

    def load_config(self) -> bool:
        """Load configuration from .env file"""
        if not self.env_file.exists():
            self.results.append(ValidationResult(
                "Config File Check",
                False,
                f".env file not found at {self.env_file}",
                "Please run the setup wizard or create .env file manually."
            ))
            return False

        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    self.config[key.strip()] = value.strip().strip('"\'')

            self.results.append(ValidationResult(
                "Config File Check",
                True,
                f"Configuration loaded from {self.env_file}",
                f"Found {len(self.config)} configuration variables."
            ))
            return True

        except Exception as e:
            self.results.append(ValidationResult(
                "Config File Check",
                False,
                f"Error reading {self.env_file}: {str(e)}"
            ))
            return False

    def validate_required_fields(self) -> None:
        """Validate required configuration fields"""
        required_fields = {
            'MANAGEBAC_URL': 'ManageBac school URL',
            'MANAGEBAC_EMAIL': 'ManageBac login email',
            'MANAGEBAC_PASSWORD': 'ManageBac login password'
        }

        missing_fields = []
        placeholder_fields = []

        # Common placeholder values that indicate unconfigured setup
        placeholder_values = [
            'your_email@school.edu',
            'your_password',
            'your-school.managebac.com',
            'your.email@example.com',
            'your_managebac_password',
            'https://your-school.managebac.cn',
            'your_openai_api_key'
        ]

        for field, description in required_fields.items():
            value = self.config.get(field, '').strip()

            if not value:
                missing_fields.append(f"{field} ({description})")
            elif any(placeholder in value.lower() for placeholder in placeholder_values):
                placeholder_fields.append(f"{field} ({description})")

        if missing_fields:
            self.results.append(ValidationResult(
                "Required Fields Check",
                False,
                f"Missing required fields: {', '.join(missing_fields)}",
                "Please provide values for all required fields."
            ))
        elif placeholder_fields:
            self.results.append(ValidationResult(
                "Required Fields Check",
                False,
                f"Placeholder values detected: {', '.join(placeholder_fields)}",
                "Please replace placeholder values with your actual credentials."
            ))
        else:
            self.results.append(ValidationResult(
                "Required Fields Check",
                True,
                "All required fields are present and configured."
            ))

    def validate_managebac_url(self) -> None:
        """Validate ManageBac URL format"""
        url = self.config.get('MANAGEBAC_URL', '').strip()

        if not url:
            self.results.append(ValidationResult(
                "ManageBac URL Validation",
                False,
                "ManageBac URL is not set."
            ))
            return

        # URL validation regex
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(url):
            self.results.append(ValidationResult(
                "ManageBac URL Validation",
                False,
                f"Invalid URL format: {url}",
                "URL should start with http:// or https:// and be properly formatted."
            ))
            return

        # Check if it's a ManageBac domain
        if 'managebac' not in url.lower():
            self.results.append(ValidationResult(
                "ManageBac URL Validation",
                False,
                f"URL doesn't appear to be a ManageBac domain: {url}",
                "ManageBac URLs typically contain 'managebac' in the domain name."
            ))
        else:
            self.results.append(ValidationResult(
                "ManageBac URL Validation",
                True,
                f"ManageBac URL format is valid: {url}"
            ))

    def validate_email_format(self) -> None:
        """Validate email format"""
        email = self.config.get('MANAGEBAC_EMAIL', '').strip()

        if not email:
            self.results.append(ValidationResult(
                "Email Format Validation",
                False,
                "Email is not set."
            ))
            return

        # Email validation regex
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        if not email_pattern.match(email):
            self.results.append(ValidationResult(
                "Email Format Validation",
                False,
                f"Invalid email format: {email}",
                "Please provide a valid email address."
            ))
        else:
            self.results.append(ValidationResult(
                "Email Format Validation",
                True,
                f"Email format is valid: {email}"
            ))

    def validate_ai_configuration(self) -> None:
        """Validate AI configuration if enabled"""
        ai_enabled = self.config.get('AI_ENABLED', 'false').lower() in ['true', '1', 'yes']

        if not ai_enabled:
            self.results.append(ValidationResult(
                "AI Configuration Check",
                True,
                "AI features are disabled - no configuration needed.",
                "Set AI_ENABLED=true to enable AI features."
            ))
            return

        # Check for OpenAI API key
        api_key = self.config.get('OPENAI_API_KEY', '').strip()

        if not api_key:
            self.results.append(ValidationResult(
                "AI Configuration Check",
                False,
                "AI is enabled but OPENAI_API_KEY is not set.",
                "Please provide your OpenAI API key or disable AI features."
            ))
            return

        # Check API key format (should start with sk-)
        if not api_key.startswith('sk-'):
            self.results.append(ValidationResult(
                "AI Configuration Check",
                False,
                "OpenAI API key format appears incorrect.",
                "OpenAI API keys typically start with 'sk-'."
            ))
        else:
            self.results.append(ValidationResult(
                "AI Configuration Check",
                True,
                "AI configuration appears valid.",
                f"API key format is correct (key: {api_key[:10]}...)"
            ))

    def validate_email_notifications(self) -> None:
        """Validate email notification configuration"""
        email_enabled = self.config.get('ENABLE_EMAIL_NOTIFICATIONS', 'false').lower() in ['true', '1', 'yes']

        if not email_enabled:
            self.results.append(ValidationResult(
                "Email Notifications Check",
                True,
                "Email notifications are disabled - no configuration needed.",
                "Set ENABLE_EMAIL_NOTIFICATIONS=true to enable email notifications."
            ))
            return

        required_email_fields = {
            'SMTP_SERVER': 'SMTP server address',
            'SMTP_USERNAME': 'SMTP username',
            'SMTP_PASSWORD': 'SMTP password'
        }

        missing_fields = []

        for field, description in required_email_fields.items():
            value = self.config.get(field, '').strip()
            if not value:
                missing_fields.append(f"{field} ({description})")

        if missing_fields:
            self.results.append(ValidationResult(
                "Email Notifications Check",
                False,
                f"Email notifications enabled but missing: {', '.join(missing_fields)}",
                "Please provide all required SMTP configuration."
            ))
        else:
            self.results.append(ValidationResult(
                "Email Notifications Check",
                True,
                "Email notification configuration appears complete."
            ))

    def validate_directories(self) -> None:
        """Validate required directories exist"""
        directories = {
            'OUTPUT_DIR': self.config.get('OUTPUT_DIR', 'reports'),
            'logs': 'logs',
            'cache': 'cache'
        }

        missing_dirs = []
        created_dirs = []

        for name, path in directories.items():
            dir_path = Path(path)
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(path)
                except Exception as e:
                    missing_dirs.append(f"{path} ({str(e)})")

        if missing_dirs:
            self.results.append(ValidationResult(
                "Directory Structure Check",
                False,
                f"Could not create directories: {', '.join(missing_dirs)}"
            ))
        else:
            message = "All required directories exist."
            if created_dirs:
                message += f" Created: {', '.join(created_dirs)}"

            self.results.append(ValidationResult(
                "Directory Structure Check",
                True,
                message
            ))

    async def test_managebac_connection(self) -> None:
        """Test connection to ManageBac (basic connectivity)"""
        url = self.config.get('MANAGEBAC_URL', '').strip()

        if not url:
            self.results.append(ValidationResult(
                "ManageBac Connectivity Test",
                False,
                "Cannot test connection - ManageBac URL not configured."
            ))
            return

        try:
            import aiohttp
            import ssl

            # Create SSL context that's more permissive for testing
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            timeout = aiohttp.ClientTimeout(total=10)

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, ssl=ssl_context) as response:
                    if response.status == 200:
                        self.results.append(ValidationResult(
                            "ManageBac Connectivity Test",
                            True,
                            f"Successfully connected to {url}",
                            f"HTTP Status: {response.status}"
                        ))
                    else:
                        self.results.append(ValidationResult(
                            "ManageBac Connectivity Test",
                            False,
                            f"Connection failed with status {response.status}",
                            f"URL: {url}"
                        ))

        except ImportError:
            self.results.append(ValidationResult(
                "ManageBac Connectivity Test",
                False,
                "Cannot test connection - aiohttp not available.",
                "Install aiohttp to enable connectivity testing."
            ))
        except Exception as e:
            self.results.append(ValidationResult(
                "ManageBac Connectivity Test",
                False,
                f"Connection test failed: {str(e)}",
                f"URL: {url}"
            ))

    async def test_ai_functionality(self) -> None:
        """Test AI functionality if enabled"""
        ai_enabled = self.config.get('AI_ENABLED', 'false').lower() in ['true', '1', 'yes']

        if not ai_enabled:
            self.results.append(ValidationResult(
                "AI Functionality Test",
                True,
                "AI features are disabled - test skipped."
            ))
            return

        api_key = self.config.get('OPENAI_API_KEY', '').strip()

        if not api_key:
            self.results.append(ValidationResult(
                "AI Functionality Test",
                False,
                "Cannot test AI - API key not configured."
            ))
            return

        try:
            import openai

            # Test with a simple API call
            client = openai.OpenAI(api_key=api_key)

            # Use a minimal test request
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model=self.config.get('AI_MODEL', 'gpt-3.5-turbo'),
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )

            self.results.append(ValidationResult(
                "AI Functionality Test",
                True,
                "AI functionality test successful.",
                f"Model: {self.config.get('AI_MODEL', 'gpt-3.5-turbo')}"
            ))

        except ImportError:
            self.results.append(ValidationResult(
                "AI Functionality Test",
                False,
                "Cannot test AI - openai library not available.",
                "Install openai library to enable AI testing."
            ))
        except Exception as e:
            self.results.append(ValidationResult(
                "AI Functionality Test",
                False,
                f"AI test failed: {str(e)}",
                "Check your API key and network connection."
            ))

    def validate_dependencies(self) -> None:
        """Validate required dependencies are installed"""
        required_packages = {
            'playwright': 'Web scraping functionality',
            'dotenv': 'Environment variable loading',
            'jinja2': 'Template rendering',
        }

        optional_packages = {
            'openai': 'AI features',
            'aiohttp': 'Async HTTP requests',
            'smtplib': 'Email notifications'  # Built-in module
        }

        missing_required = []
        missing_optional = []

        # Check required packages
        for package, description in required_packages.items():
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_required.append(f"{package} ({description})")

        # Check optional packages
        for package, description in optional_packages.items():
            try:
                if package == 'smtplib':
                    import smtplib
                elif package == 'dotenv':
                    from dotenv import load_dotenv
                else:
                    __import__(package.replace('-', '_'))
            except ImportError:
                missing_optional.append(f"{package} ({description})")

        if missing_required:
            self.results.append(ValidationResult(
                "Dependencies Check",
                False,
                f"Missing required packages: {', '.join(missing_required)}",
                "Install missing packages using: pip install -r requirements.txt"
            ))
        else:
            message = "All required dependencies are installed."
            if missing_optional:
                message += f" Optional packages missing: {', '.join(missing_optional)}"

            self.results.append(ValidationResult(
                "Dependencies Check",
                True,
                message
            ))

    async def run_all_validations(self) -> None:
        """Run all validation tests"""
        print(f"{Colors.CYAN}{Colors.BOLD}🔍 ManageBac Assignment Checker - Configuration Validator{Colors.END}")
        print(f"{Colors.CYAN}🔍 ManageBac作业检查器 - 配置验证器{Colors.END}")
        print("=" * 60)

        # Load configuration
        if not self.load_config():
            return

        print(f"\n{Colors.BLUE}📋 Running validation tests...{Colors.END}")
        print(f"{Colors.BLUE}📋 正在运行验证测试...{Colors.END}\n")

        # Run all validation tests
        self.validate_dependencies()
        self.validate_required_fields()
        self.validate_managebac_url()
        self.validate_email_format()
        self.validate_ai_configuration()
        self.validate_email_notifications()
        self.validate_directories()

        # Run async tests
        await self.test_managebac_connection()
        await self.test_ai_functionality()

    def print_results(self) -> None:
        """Print validation results"""
        success_count = sum(1 for result in self.results if result.success)
        total_count = len(self.results)

        print(f"\n{Colors.BOLD}📊 Validation Results | 验证结果{Colors.END}")
        print("=" * 60)

        for result in self.results:
            status_icon = f"{Colors.GREEN}✅" if result.success else f"{Colors.RED}❌"
            test_name = f"{Colors.BOLD}{result.test_name}{Colors.END}"
            message = result.message

            print(f"\n{status_icon} {test_name}{Colors.END}")
            print(f"   {message}")

            if result.details:
                print(f"   {Colors.YELLOW}💡 {result.details}{Colors.END}")

        # Summary
        print("\n" + "=" * 60)
        if success_count == total_count:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! ({success_count}/{total_count}){Colors.END}")
            print(f"{Colors.GREEN}🎉 所有测试通过！({success_count}/{total_count}){Colors.END}")
        else:
            failed_count = total_count - success_count
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  {success_count}/{total_count} tests passed, {failed_count} failed.{Colors.END}")
            print(f"{Colors.YELLOW}⚠️  {success_count}/{total_count} 个测试通过，{failed_count} 个失败。{Colors.END}")

            print(f"\n{Colors.CYAN}💡 Next steps | 下一步操作:{Colors.END}")
            print("   • Fix the failed tests above")
            print("   • Run the setup wizard: python setup_wizard.py")
            print("   • Edit .env file manually")
            print("   • Re-run validation: python config_validator.py")

async def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate ManageBac Assignment Checker configuration'
    )
    parser.add_argument(
        '--env-file',
        default='.env',
        help='Path to environment file (default: .env)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Show only failed tests'
    )

    args = parser.parse_args()

    validator = ConfigValidator(args.env_file)
    await validator.run_all_validations()

    # Filter results if quiet mode
    if args.quiet:
        validator.results = [r for r in validator.results if not r.success]

    validator.print_results()

    # Exit with error code if any tests failed
    failed_tests = [r for r in validator.results if not r.success]
    sys.exit(len(failed_tests))

if __name__ == "__main__":
    asyncio.run(main())