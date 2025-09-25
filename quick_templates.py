#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ManageBac Assignment Checker - Quick Configuration Templates
⚡ ManageBac作业检查器 - 快速配置模板

Quick setup templates for common school configurations.
常见学校配置的快速设置模板。
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional

class QuickTemplates:
    """Quick configuration templates for specific schools and use cases"""

    def __init__(self):
        self.school_templates = {
            # Shanghai High School International Division
            "shtcs": {
                "name": "📚 上海中学国际部 (SHTCS)",
                "name_en": "Shanghai High School International Division",
                "url": "https://shtcs.managebac.cn",
                "description": "上海中学国际部专用配置",
                "description_en": "Configuration for Shanghai High School International Division",
                "timezone": "Asia/Shanghai",
                "language": "zh",
                "config": {
                    "MANAGEBAC_URL": "https://shtcs.managebac.cn",
                    "LANGUAGE": "zh",
                    "HTML_THEME": "auto",
                    "TIMEZONE": "Asia/Shanghai",
                    "REPORT_FORMAT": "html,json,console",
                    "MOBILE_FRIENDLY": "true",
                    "CHART_COLOR_SCHEME": "colorful",
                    "SCHEDULE_TIMEZONE": "Asia/Shanghai",
                    "INCLUDE_CHARTS": "true"
                }
            },

            # Common international schools in China
            "dulwich_shanghai": {
                "name": "📚 德威国际学校 (Dulwich Shanghai)",
                "url": "https://dulwich-shanghai.managebac.cn",
                "description": "德威国际学校上海配置",
                "config": {
                    "MANAGEBAC_URL": "https://dulwich-shanghai.managebac.cn",
                    "LANGUAGE": "zh",
                    "TIMEZONE": "Asia/Shanghai"
                }
            },

            "ycis_shanghai": {
                "name": "📚 耀中国际学校 (YCIS Shanghai)",
                "url": "https://ycis-shanghai.managebac.cn",
                "description": "耀中国际学校上海配置",
                "config": {
                    "MANAGEBAC_URL": "https://ycis-shanghai.managebac.cn",
                    "LANGUAGE": "zh",
                    "TIMEZONE": "Asia/Shanghai"
                }
            },

            "wellington_shanghai": {
                "name": "📚 惠灵顿国际学校 (Wellington Shanghai)",
                "url": "https://wellington-shanghai.managebac.cn",
                "description": "惠灵顿国际学校上海配置",
                "config": {
                    "MANAGEBAC_URL": "https://wellington-shanghai.managebac.cn",
                    "LANGUAGE": "zh",
                    "TIMEZONE": "Asia/Shanghai"
                }
            }
        }

        self.quick_configs = {
            "student_basic_cn": {
                "name": "🎓 学生基础版 (中文)",
                "description": "适合中国学生的基础配置",
                "config": {
                    "LANGUAGE": "zh",
                    "HTML_THEME": "auto",
                    "REPORT_FORMAT": "html,console",
                    "AI_ENABLED": "false",
                    "ENABLE_EMAIL_NOTIFICATIONS": "false",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "25",
                    "SHOW_OVERDUE_ONLY": "false",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "colorful",
                    "MOBILE_FRIENDLY": "true",
                    "TIMEZONE": "Asia/Shanghai"
                }
            },

            "student_ai_cn": {
                "name": "🤖 学生AI版 (中文)",
                "description": "带AI辅助的中国学生配置",
                "config": {
                    "LANGUAGE": "zh",
                    "HTML_THEME": "auto",
                    "REPORT_FORMAT": "html,json,console",
                    "AI_ENABLED": "true",
                    "AI_MODEL": "gpt-3.5-turbo",
                    "AI_TEMPERATURE": "0.7",
                    "ENABLE_EMAIL_NOTIFICATIONS": "false",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "50",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "colorful",
                    "MOBILE_FRIENDLY": "true",
                    "TIMEZONE": "Asia/Shanghai",
                    "PRIORITY_KEYWORDS": "考试,测试,项目,论文,期末,期中,作业,演示"
                }
            },

            "parent_monitor_cn": {
                "name": "👨‍👩‍👧‍👦 家长监控版 (中文)",
                "description": "中国家长监控孩子作业配置",
                "config": {
                    "LANGUAGE": "zh",
                    "HTML_THEME": "light",
                    "REPORT_FORMAT": "html,email",
                    "AI_ENABLED": "false",
                    "ENABLE_EMAIL_NOTIFICATIONS": "true",
                    "SMTP_SERVER": "smtp.qq.com",
                    "SMTP_PORT": "587",
                    "SMTP_USE_TLS": "true",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "100",
                    "SHOW_OVERDUE_ONLY": "true",
                    "SHOW_HIGH_PRIORITY_ONLY": "true",
                    "MIN_DAYS_BEFORE_DUE": "3",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "minimal",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_SCHEDULING": "true",
                    "SCHEDULE_CRON": "0 8,20 * * *",  # 8 AM and 8 PM daily
                    "SCHEDULE_TIMEZONE": "Asia/Shanghai",
                    "TIMEZONE": "Asia/Shanghai",
                    "PRIORITY_KEYWORDS": "考试,测试,项目,论文,期末,期中,作业,到期"
                }
            }
        }

    def get_school_template(self, school_key: str) -> Optional[Dict]:
        """Get a school-specific template"""
        return self.school_templates.get(school_key)

    def list_school_templates(self) -> Dict[str, Dict]:
        """List all available school templates"""
        return {key: {
            "name": template["name"],
            "url": template["url"],
            "description": template["description"]
        } for key, template in self.school_templates.items()}

    def get_quick_config(self, config_key: str) -> Optional[Dict]:
        """Get a quick configuration template"""
        return self.quick_configs.get(config_key)

    def list_quick_configs(self) -> Dict[str, Dict]:
        """List all available quick configurations"""
        return {key: {
            "name": config["name"],
            "description": config["description"]
        } for key, config in self.quick_configs.items()}

    def create_env_from_school_template(self, school_key: str, email: str, password: str,
                                      additional_config: Optional[Dict] = None) -> bool:
        """Create .env file from school template"""
        school_template = self.get_school_template(school_key)
        if not school_template:
            return False

        try:
            # Start with school template config
            config = school_template["config"].copy()

            # Add user credentials
            config["MANAGEBAC_EMAIL"] = email
            config["MANAGEBAC_PASSWORD"] = password

            # Add any additional configuration
            if additional_config:
                config.update(additional_config)

            # Create .env file
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(f"# ManageBac Configuration for {school_template['name']}\n")
                f.write(f"# {school_template['description']}\n")
                f.write(f"# Generated on: {self._get_current_time()}\n\n")

                # Write all configuration variables
                for key, value in config.items():
                    f.write(f"{key}={value}\n")

                # Add common optional settings
                f.write("\n# Optional AI settings (uncomment to enable)\n")
                f.write("# OPENAI_API_KEY=your_openai_api_key\n")
                f.write("# AI_MODEL=gpt-3.5-turbo\n\n")

                f.write("# Optional email notification settings\n")
                f.write("# SMTP_USERNAME=your.email@example.com\n")
                f.write("# SMTP_PASSWORD=your_email_password\n")
                f.write("# NOTIFICATION_RECIPIENTS=parent@example.com,student@example.com\n")

            return True

        except Exception as e:
            print(f"Error creating .env file: {e}")
            return False

    def create_env_from_quick_config(self, config_key: str, managebac_url: str,
                                   email: str, password: str) -> bool:
        """Create .env file from quick configuration"""
        quick_config = self.get_quick_config(config_key)
        if not quick_config:
            return False

        try:
            # Start with quick config
            config = quick_config["config"].copy()

            # Add user credentials
            config["MANAGEBAC_URL"] = managebac_url
            config["MANAGEBAC_EMAIL"] = email
            config["MANAGEBAC_PASSWORD"] = password

            # Create .env file
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(f"# ManageBac Configuration - {quick_config['name']}\n")
                f.write(f"# {quick_config['description']}\n")
                f.write(f"# Generated on: {self._get_current_time()}\n\n")

                # Write all configuration variables
                for key, value in config.items():
                    f.write(f"{key}={value}\n")

                # Add optional settings based on config type
                if "ai" in config_key:
                    f.write("\n# AI settings (required for AI features)\n")
                    f.write("# OPENAI_API_KEY=your_openai_api_key\n\n")

                if "parent" in config_key or "monitor" in config_key:
                    f.write("\n# Email notification settings (required for email alerts)\n")
                    f.write("# SMTP_USERNAME=your.email@example.com\n")
                    f.write("# SMTP_PASSWORD=your_email_password\n")
                    f.write("# NOTIFICATION_RECIPIENTS=parent@example.com\n\n")

            return True

        except Exception as e:
            print(f"Error creating .env file: {e}")
            return False

    def _get_current_time(self) -> str:
        """Get current time string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def auto_detect_school(self, url: str) -> Optional[str]:
        """Auto-detect school from URL"""
        url_lower = url.lower()

        for key, template in self.school_templates.items():
            if template["url"].lower() in url_lower or key in url_lower:
                return key

        # Check for common school identifiers
        school_patterns = {
            "shtcs": ["shtcs", "shanghai-high", "上海中学"],
            "dulwich": ["dulwich", "德威"],
            "ycis": ["ycis", "耀中"],
            "wellington": ["wellington", "惠灵顿"]
        }

        for key, patterns in school_patterns.items():
            if any(pattern in url_lower for pattern in patterns):
                return key

        return None

def interactive_quick_setup():
    """Interactive quick setup"""
    templates = QuickTemplates()

    print("\n⚡ Quick Configuration Setup | 快速配置设置")
    print("=" * 50)

    # Step 1: Get ManageBac URL
    managebac_url = input("\n🏫 Enter your school's ManageBac URL | 输入学校ManageBac网址: ").strip()

    # Try to auto-detect school
    detected_school = templates.auto_detect_school(managebac_url) if managebac_url else None

    if detected_school:
        school_template = templates.get_school_template(detected_school)
        print(f"\n🎯 Detected school | 检测到学校: {school_template['name']}")

        use_school_template = input("Use school-specific template? (y/n) | 使用学校专用模板？(y/n) [y]: ").strip().lower()
        if use_school_template in ['', 'y', 'yes', '是']:
            email = input("\n📧 Enter your ManageBac email | 输入ManageBac邮箱: ").strip()
            password = input("🔑 Enter your ManageBac password | 输入ManageBac密码: ").strip()

            if templates.create_env_from_school_template(detected_school, email, password):
                print(f"\n✅ Configuration created using {school_template['name']} template!")
                print(f"✅ 使用{school_template['name']}模板创建配置成功！")
                return True
            else:
                print("\n❌ Failed to create configuration!")
                return False

    # Step 2: Choose quick config
    print("\n📋 Choose configuration type | 选择配置类型:")
    quick_configs = templates.list_quick_configs()

    for i, (key, config) in enumerate(quick_configs.items(), 1):
        print(f"{i}. {config['name']}")
        print(f"   {config['description']}")

    while True:
        try:
            choice = input(f"\nSelect configuration (1-{len(quick_configs)}) | 选择配置 (1-{len(quick_configs)}) [1]: ").strip()
            if not choice:
                choice = "1"

            index = int(choice) - 1
            if 0 <= index < len(quick_configs):
                selected_key = list(quick_configs.keys())[index]
                break
            else:
                print(f"Please enter a number between 1 and {len(quick_configs)}")
        except ValueError:
            print("Please enter a valid number")

    # Get credentials
    if not managebac_url:
        managebac_url = input("\n🏫 Enter your school's ManageBac URL | 输入学校ManageBac网址: ").strip()

    email = input("📧 Enter your ManageBac email | 输入ManageBac邮箱: ").strip()
    password = input("🔑 Enter your ManageBac password | 输入ManageBac密码: ").strip()

    # Create configuration
    if templates.create_env_from_quick_config(selected_key, managebac_url, email, password):
        selected_config = templates.get_quick_config(selected_key)
        print(f"\n✅ Configuration created using {selected_config['name']}!")
        print(f"✅ 使用{selected_config['name']}创建配置成功！")

        # Show next steps
        print(f"\n🚀 Next steps | 下一步:")
        print("   • Test configuration: python main_new.py --test-config")
        print("   • Run application: python gui_launcher.py")
        print("   • 测试配置: python main_new.py --test-config")
        print("   • 运行应用: python gui_launcher.py")

        return True
    else:
        print("\n❌ Failed to create configuration!")
        print("❌ 创建配置失败！")
        return False

def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        templates = QuickTemplates()

        if command == "list-schools":
            print("Available school templates:")
            for key, info in templates.list_school_templates().items():
                print(f"  {key}: {info['name']} - {info['url']}")

        elif command == "list-configs":
            print("Available quick configurations:")
            for key, info in templates.list_quick_configs().items():
                print(f"  {key}: {info['name']} - {info['description']}")

        elif command == "interactive":
            interactive_quick_setup()

        else:
            print("Usage: python quick_templates.py [list-schools|list-configs|interactive]")
    else:
        interactive_quick_setup()

if __name__ == "__main__":
    main()