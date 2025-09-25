#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧙‍♂️ ManageBac Assignment Checker - Interactive Setup Wizard
🧙‍♂️ ManageBac作业检查器 - 交互式配置向导

A user-friendly configuration wizard that guides users through the setup process.
一个用户友好的配置向导，引导用户完成设置过程。
"""

import os
import sys
import re
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import getpass

class Colors:
    """Console colors for beautiful output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class SetupWizard:
    """Interactive setup wizard for ManageBac Assignment Checker"""

    def __init__(self):
        self.config = {}
        self.env_file = '.env'
        self.supported_schools = {
            'shtcs': 'https://shtcs.managebac.cn',
            'example': 'https://example.managebac.com',
            # Add more known schools here
        }

    def print_header(self):
        """Print welcome header"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🧙‍♂️ ManageBac Assignment Checker Setup Wizard        ║
║              🧙‍♂️ ManageBac作业检查器配置向导                 ║
║                                                              ║
║   🎯 Let's get your assignment tracker configured quickly!   ║
║        🎯 让我们快速配置您的作业跟踪器！                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}Welcome! This wizard will help you configure ManageBac Assignment Checker
in just a few minutes. We'll guide you through the essential settings.

欢迎！此向导将帮助您在几分钟内配置ManageBac作业检查器。
我们将引导您完成基本设置。{Colors.END}

""")

    def get_input(self, prompt: str, default: str = "", required: bool = True,
                  secret: bool = False, validator=None) -> str:
        """Get user input with validation"""
        while True:
            if secret:
                if default:
                    value = getpass.getpass(f"{prompt} [{Colors.YELLOW}current: ***{Colors.END}]: ")
                else:
                    value = getpass.getpass(f"{prompt}: ")
            else:
                if default:
                    value = input(f"{prompt} [{Colors.YELLOW}{default}{Colors.END}]: ").strip()
                else:
                    value = input(f"{prompt}: ").strip()

            if not value and default:
                value = default

            if required and not value:
                print(f"{Colors.RED}❌ This field is required!{Colors.END}")
                continue

            if validator:
                is_valid, error_msg = validator(value)
                if not is_valid:
                    print(f"{Colors.RED}❌ {error_msg}{Colors.END}")
                    continue

            return value

    def validate_url(self, url: str) -> Tuple[bool, str]:
        """Validate ManageBac URL"""
        if not url:
            return True, ""  # Empty is OK for optional fields

        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                url = f"https://{url}"
                parsed = urlparse(url)

            if not parsed.netloc:
                return False, "Invalid URL format"

            if not ('managebac' in parsed.netloc.lower()):
                return False, "URL must be a ManageBac domain (e.g., yourschool.managebac.com)"

            return True, ""
        except:
            return False, "Invalid URL format"

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email address"""
        if not email:
            return True, ""  # Empty is OK for optional fields

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"

    def step_1_basic_config(self):
        """Step 1: Basic ManageBac Configuration"""
        print(f"""
{Colors.HEADER}📚 Step 1: Basic ManageBac Configuration
🔗 第一步：基本ManageBac配置{Colors.END}

Let's start with your ManageBac school information.
首先设置您的ManageBac学校信息。

""")

        # School URL with smart suggestions
        print(f"{Colors.CYAN}💡 Common school examples:{Colors.END}")
        print("   • https://shtcs.managebac.cn (Shanghai)")
        print("   • https://yourschool.managebac.com")
        print("   • https://yourschool.managebac.cn")
        print("")

        url = self.get_input(
            f"{Colors.BLUE}🏫 Enter your school's ManageBac URL{Colors.END}",
            default="https://shtcs.managebac.cn",
            validator=self.validate_url
        )

        # Ensure URL has proper format
        if not url.startswith('http'):
            url = f"https://{url}"

        self.config['MANAGEBAC_URL'] = url

        # Login credentials
        print(f"\n{Colors.CYAN}🔐 Login Credentials | 登录凭据{Colors.END}")
        print("Enter your ManageBac login information:")
        print("输入您的ManageBac登录信息：")

        email = self.get_input(
            f"{Colors.BLUE}📧 Your ManageBac email{Colors.END}",
            validator=self.validate_email
        )
        self.config['MANAGEBAC_EMAIL'] = email

        password = self.get_input(
            f"{Colors.BLUE}🔑 Your ManageBac password{Colors.END}",
            secret=True
        )
        self.config['MANAGEBAC_PASSWORD'] = password

        print(f"{Colors.GREEN}✅ Basic configuration completed!{Colors.END}")

    def step_2_ai_configuration(self):
        """Step 2: AI Assistant Configuration"""
        print(f"""
{Colors.HEADER}🤖 Step 2: AI Assistant Configuration (Optional)
🤖 第二步：AI助手配置（可选）{Colors.END}

The AI assistant can help you with:
AI助手可以帮助您：

📊 • Analyze assignment patterns and workload
    分析作业模式和工作量
📈 • Generate insights about your academic performance
    生成关于学习表现的洞察
💡 • Provide study suggestions and time management tips
    提供学习建议和时间管理技巧
🎯 • Prioritize assignments based on difficulty and importance
    根据难度和重要性优先排序作业

""")

        enable_ai = self.get_input(
            f"{Colors.BLUE}🤖 Do you want to enable AI assistant? (y/n){Colors.END}",
            default="n",
            required=False
        ).lower() in ['y', 'yes', '1', 'true']

        self.config['AI_ENABLED'] = str(enable_ai).lower()

        if enable_ai:
            print(f"\n{Colors.CYAN}🔑 AI Configuration | AI配置{Colors.END}")
            print("You'll need an OpenAI API key. Get one at: https://platform.openai.com/api-keys")
            print("您需要OpenAI API密钥。获取地址：https://platform.openai.com/api-keys")

            api_key = self.get_input(
                f"{Colors.BLUE}🗝️  Enter your OpenAI API Key{Colors.END}",
                secret=True,
                required=False
            )

            if api_key:
                self.config['OPENAI_API_KEY'] = api_key

                # AI Model selection
                print(f"\n{Colors.CYAN}🧠 AI Model Selection | AI模型选择{Colors.END}")
                print("Available models:")
                print("  • gpt-3.5-turbo (Faster, cheaper)")
                print("  • gpt-4 (More accurate, more expensive)")

                model = self.get_input(
                    f"{Colors.BLUE}🧠 Choose AI model (gpt-3.5-turbo/gpt-4){Colors.END}",
                    default="gpt-3.5-turbo"
                )
                self.config['AI_MODEL'] = model

                print(f"{Colors.GREEN}✅ AI assistant configured!{Colors.END}")
            else:
                self.config['AI_ENABLED'] = 'false'
                print(f"{Colors.YELLOW}⚠️  AI assistant disabled (no API key provided){Colors.END}")
        else:
            print(f"{Colors.YELLOW}ℹ️  AI assistant disabled{Colors.END}")

    def step_3_notification_preferences(self):
        """Step 3: Notification Preferences"""
        print(f"""
{Colors.HEADER}📧 Step 3: Notification Preferences (Optional)
📧 第三步：通知偏好设置（可选）{Colors.END}

Get notified about:
获得以下通知：

🔔 • Overdue assignments | 逾期作业
📅 • Upcoming deadlines | 即将到期的截止日期
📊 • Daily/weekly summaries | 每日/每周总结

""")

        enable_notifications = self.get_input(
            f"{Colors.BLUE}📧 Enable email notifications? (y/n){Colors.END}",
            default="n",
            required=False
        ).lower() in ['y', 'yes', '1', 'true']

        self.config['ENABLE_EMAIL_NOTIFICATIONS'] = str(enable_notifications).lower()

        if enable_notifications:
            print(f"\n{Colors.CYAN}📧 Email Configuration | 邮箱配置{Colors.END}")

            smtp_server = self.get_input(
                f"{Colors.BLUE}📮 SMTP Server{Colors.END}",
                default="smtp.gmail.com"
            )
            self.config['SMTP_SERVER'] = smtp_server

            smtp_username = self.get_input(
                f"{Colors.BLUE}👤 SMTP Username (email){Colors.END}",
                validator=self.validate_email
            )
            self.config['SMTP_USERNAME'] = smtp_username

            smtp_password = self.get_input(
                f"{Colors.BLUE}🔐 SMTP Password (for Gmail, use App Password){Colors.END}",
                secret=True
            )
            self.config['SMTP_PASSWORD'] = smtp_password

            recipients = self.get_input(
                f"{Colors.BLUE}📬 Notification recipients (comma-separated){Colors.END}",
                default=smtp_username
            )
            self.config['NOTIFICATION_RECIPIENTS'] = recipients

            print(f"{Colors.GREEN}✅ Email notifications configured!{Colors.END}")
        else:
            print(f"{Colors.YELLOW}ℹ️  Email notifications disabled{Colors.END}")

    def step_4_report_preferences(self):
        """Step 4: Report Preferences"""
        print(f"""
{Colors.HEADER}📊 Step 4: Report Preferences
📊 第四步：报告偏好设置{Colors.END}

Choose your preferred report formats:
选择您喜欢的报告格式：

📄 • HTML - Interactive web reports | 交互式网页报告
📋 • JSON - Machine-readable data | 机器可读数据
📝 • Markdown - Text-based reports | 基于文本的报告
💻 • Console - Terminal output | 终端输出

""")

        formats = []

        if self.get_input(f"{Colors.BLUE}📄 Include HTML reports? (y/n){Colors.END}", "y").lower() in ['y', 'yes']:
            formats.append('html')

        if self.get_input(f"{Colors.BLUE}📋 Include JSON reports? (y/n){Colors.END}", "y").lower() in ['y', 'yes']:
            formats.append('json')

        if self.get_input(f"{Colors.BLUE}📝 Include Markdown reports? (y/n){Colors.END}", "n").lower() in ['y', 'yes']:
            formats.append('markdown')

        formats.append('console')  # Always include console output

        self.config['REPORT_FORMAT'] = ','.join(formats)

        # Output directory
        output_dir = self.get_input(
            f"{Colors.BLUE}📁 Report output directory{Colors.END}",
            default="reports"
        )
        self.config['OUTPUT_DIR'] = output_dir

        print(f"{Colors.GREEN}✅ Report preferences configured!{Colors.END}")

    def step_5_language_and_preferences(self):
        """Step 5: Language and Other Preferences"""
        print(f"""
{Colors.HEADER}🌐 Step 5: Language and Preferences
🌐 第五步：语言和偏好设置{Colors.END}

""")

        # Language preference
        language = self.get_input(
            f"{Colors.BLUE}🗣️  Preferred language (en/zh){Colors.END}",
            default="zh"
        )
        self.config['LANGUAGE'] = language

        # Browser headless mode
        headless = self.get_input(
            f"{Colors.BLUE}🤖 Run browser in background? (recommended: y){Colors.END}",
            default="y"
        ).lower() in ['y', 'yes']
        self.config['HEADLESS'] = str(headless).lower()

        # Debug mode
        debug = self.get_input(
            f"{Colors.BLUE}🐛 Enable debug mode? (y/n){Colors.END}",
            default="n"
        ).lower() in ['y', 'yes']
        self.config['DEBUG'] = str(debug).lower()

        print(f"{Colors.GREEN}✅ Preferences configured!{Colors.END}")

    def test_configuration(self):
        """Test the configuration"""
        print(f"""
{Colors.HEADER}🔬 Step 6: Testing Configuration
🔬 第六步：测试配置{Colors.END}

""")

        test_config = self.get_input(
            f"{Colors.BLUE}🧪 Would you like to test the configuration now? (y/n){Colors.END}",
            default="y"
        ).lower() in ['y', 'yes']

        if test_config:
            print(f"{Colors.CYAN}🔄 Testing ManageBac connection...{Colors.END}")
            # Here you would add actual connection testing logic
            print(f"{Colors.GREEN}✅ Configuration test would run here (not implemented in wizard){Colors.END}")
            print(f"{Colors.YELLOW}💡 You can test by running: python main_new.py --test-config{Colors.END}")

    def generate_env_file(self):
        """Generate .env file from collected configuration"""
        print(f"""
{Colors.HEADER}💾 Generating Configuration File
💾 生成配置文件{Colors.END}

""")

        # Read the example config file
        example_file = 'config.example.env'
        if not os.path.exists(example_file):
            print(f"{Colors.RED}❌ Error: config.example.env not found!{Colors.END}")
            return False

        # Set default values for unconfigured options
        defaults = {
            'REPORT_FORMAT': 'html,json,console',
            'OUTPUT_DIR': 'reports',
            'FETCH_DETAILS': 'true',
            'DETAILS_LIMIT': '50',
            'SHOW_OVERDUE_ONLY': 'false',
            'SHOW_HIGH_PRIORITY_ONLY': 'false',
            'MIN_DAYS_BEFORE_DUE': '0',
            'SMTP_PORT': '587',
            'SMTP_USE_TLS': 'true',
            'BROWSER_TIMEOUT': '30000',
            'LOG_LEVEL': 'INFO',
            'LOG_FILE': 'logs/managebac_checker.log',
            'HTML_THEME': 'auto',
            'INCLUDE_CHARTS': 'true',
            'CHART_COLOR_SCHEME': 'default',
            'AI_TEMPERATURE': '0.7',
            'AI_MAX_TOKENS': '500',
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'MAX_RETRIES': '3',
            'REQUEST_DELAY': '1',
            'CAPTURE_SCREENSHOTS': 'false',
            'SCREENSHOT_DIR': 'screenshots',
            'ENCRYPT_CREDENTIALS': 'false',
            'ENCRYPTION_KEY': '',
            'ENABLE_SCHEDULING': 'false',
            'SCHEDULE_CRON': '0 8 * * *',
            'SCHEDULE_TIMEZONE': 'Asia/Shanghai',
            'STATUS_FILTER': '',
            'COURSE_FILTER': '',
            'TYPE_FILTER': '',
            'PRIORITY_KEYWORDS': 'exam,test,project,essay,final,midterm,quiz,presentation',
            'ENABLE_CACHING': 'true',
            'CACHE_DIR': 'cache',
            'CACHE_EXPIRATION': '24',
            'EXPORT_FORMATS': '',
            'WEBHOOK_URL': '',
            'SLACK_TOKEN': '',
            'DISCORD_WEBHOOK': '',
            'TEAMS_WEBHOOK': '',
            'MOBILE_FRIENDLY': 'true',
            'ENABLE_PWA': 'false',
            'MAX_BROWSER_INSTANCES': '1',
            'PAGE_LOAD_TIMEOUT': '30',
            'ELEMENT_WAIT_TIMEOUT': '10',
            'MEMORY_LIMIT': '1024',
            'ENABLE_BACKUPS': 'false',
            'BACKUP_DIR': 'backups',
            'BACKUP_RETENTION_DAYS': '30',
            'BACKUP_COMPRESSION': 'zip',
            'CUSTOM_CSS_FILE': '',
            'CUSTOM_JS_FILE': '',
            'CUSTOM_LOGO_URL': '',
            'CUSTOM_FOOTER_TEXT': ''
        }

        # Merge user config with defaults
        final_config = defaults.copy()
        final_config.update(self.config)

        try:
            # Read example file and replace values
            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace values in the content
            for key, value in final_config.items():
                pattern = rf'^{key}=.*$'
                replacement = f'{key}={value}'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            # Write to .env file
            with open(self.env_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"{Colors.GREEN}✅ Configuration saved to {self.env_file}{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}❌ Error saving configuration: {e}{Colors.END}")
            return False

    def show_next_steps(self):
        """Show next steps to user"""
        print(f"""
{Colors.HEADER}🎉 Setup Complete! Next Steps
🎉 设置完成！后续步骤{Colors.END}

{Colors.GREEN}Congratulations! Your ManageBac Assignment Checker is now configured.
恭喜！您的ManageBac作业检查器现已配置完成。{Colors.END}

{Colors.CYAN}📋 What you can do now:{Colors.END}

{Colors.BLUE}1. 🚀 Run the application:{Colors.END}
   • GUI Mode: python gui_launcher.py
   • CLI Mode: python main_new.py
   • Interactive: python main_new.py --interactive

{Colors.BLUE}2. 🧪 Test your configuration:{Colors.END}
   • python main_new.py --test-config

{Colors.BLUE}3. 📊 Generate your first report:{Colors.END}
   • python main_new.py --format html
   • Open reports/assignment_report.html in your browser

{Colors.BLUE}4. ⚙️  Customize settings:{Colors.END}
   • Edit .env file for advanced options
   • Run this wizard again: python setup_wizard.py

{Colors.YELLOW}💡 Tips:{Colors.END}
   • Check the logs/ directory for debugging information
   • Reports are saved in the '{self.config.get('OUTPUT_DIR', 'reports')}' directory
   • Visit the project documentation for more features

{Colors.GREEN}Happy assignment tracking! 🎯
愉快地跟踪作业！🎯{Colors.END}

""")

    def run(self):
        """Run the complete setup wizard"""
        try:
            self.print_header()

            # Check if .env already exists
            if os.path.exists(self.env_file):
                overwrite = self.get_input(
                    f"{Colors.YELLOW}⚠️  Configuration file already exists. Overwrite? (y/n){Colors.END}",
                    default="n"
                ).lower() in ['y', 'yes']

                if not overwrite:
                    print(f"{Colors.CYAN}ℹ️  Setup cancelled. Your existing configuration is preserved.{Colors.END}")
                    return

            # Run setup steps
            self.step_1_basic_config()
            self.step_2_ai_configuration()
            self.step_3_notification_preferences()
            self.step_4_report_preferences()
            self.step_5_language_and_preferences()

            # Generate configuration file
            if self.generate_env_file():
                self.test_configuration()
                self.show_next_steps()
            else:
                print(f"{Colors.RED}❌ Setup failed. Please try again.{Colors.END}")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}⚠️  Setup cancelled by user.{Colors.END}")
        except Exception as e:
            print(f"\n\n{Colors.RED}❌ Setup failed with error: {e}{Colors.END}")

def main():
    """Main entry point"""
    wizard = SetupWizard()
    wizard.run()

if __name__ == "__main__":
    main()