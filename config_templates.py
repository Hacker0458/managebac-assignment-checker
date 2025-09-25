#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 ManageBac Assignment Checker - Configuration Templates
📋 ManageBac作业检查器 - 配置模板

Pre-configured templates for different use cases.
为不同使用场景预配置的模板。
"""

import os
import json
from typing import Dict, List

class ConfigTemplates:
    """Configuration templates for different user scenarios"""

    def __init__(self):
        self.templates = {
            "student_basic": {
                "name": "🎓 Student - Basic Setup",
                "description": "Perfect for students who want simple assignment tracking",
                "description_zh": "适合想要简单作业跟踪的学生",
                "config": {
                    "REPORT_FORMAT": "html,console",
                    "OUTPUT_DIR": "reports",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "LANGUAGE": "zh",
                    "AI_ENABLED": "false",
                    "ENABLE_EMAIL_NOTIFICATIONS": "false",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "25",
                    "SHOW_OVERDUE_ONLY": "false",
                    "SHOW_HIGH_PRIORITY_ONLY": "false",
                    "HTML_THEME": "auto",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "colorful",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_CACHING": "true",
                    "CACHE_EXPIRATION": "12"
                }
            },

            "student_ai_powered": {
                "name": "🤖 Student - AI-Powered",
                "description": "For students who want AI assistance and smart insights",
                "description_zh": "适合需要AI辅助和智能洞察的学生",
                "config": {
                    "REPORT_FORMAT": "html,json,console",
                    "OUTPUT_DIR": "reports",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "LANGUAGE": "zh",
                    "AI_ENABLED": "true",
                    "AI_MODEL": "gpt-3.5-turbo",
                    "AI_TEMPERATURE": "0.7",
                    "AI_MAX_TOKENS": "500",
                    "ENABLE_EMAIL_NOTIFICATIONS": "false",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "50",
                    "SHOW_OVERDUE_ONLY": "false",
                    "SHOW_HIGH_PRIORITY_ONLY": "false",
                    "HTML_THEME": "auto",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "colorful",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_CACHING": "true",
                    "CACHE_EXPIRATION": "6",
                    "PRIORITY_KEYWORDS": "exam,test,project,essay,final,midterm,quiz,presentation,homework"
                }
            },

            "parent_monitoring": {
                "name": "👨‍👩‍👧‍👦 Parent - Child Monitoring",
                "description": "For parents who want to monitor their child's assignments",
                "description_zh": "适合希望监控孩子作业的家长",
                "config": {
                    "REPORT_FORMAT": "html,email",
                    "OUTPUT_DIR": "reports",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "LANGUAGE": "zh",
                    "AI_ENABLED": "false",
                    "ENABLE_EMAIL_NOTIFICATIONS": "true",
                    "SMTP_SERVER": "smtp.gmail.com",
                    "SMTP_PORT": "587",
                    "SMTP_USE_TLS": "true",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "100",
                    "SHOW_OVERDUE_ONLY": "true",
                    "SHOW_HIGH_PRIORITY_ONLY": "true",
                    "MIN_DAYS_BEFORE_DUE": "3",
                    "HTML_THEME": "light",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "minimal",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_SCHEDULING": "true",
                    "SCHEDULE_CRON": "0 8,20 * * *",  # 8 AM and 8 PM daily
                    "SCHEDULE_TIMEZONE": "Asia/Shanghai",
                    "ENABLE_CACHING": "true",
                    "CACHE_EXPIRATION": "4",
                    "PRIORITY_KEYWORDS": "exam,test,project,essay,final,midterm,assignment,homework,due"
                }
            },

            "teacher_class_management": {
                "name": "👩‍🏫 Teacher - Class Management",
                "description": "For teachers managing multiple students",
                "description_zh": "适合管理多个学生的老师",
                "config": {
                    "REPORT_FORMAT": "html,json,csv,xlsx",
                    "OUTPUT_DIR": "class_reports",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "LANGUAGE": "zh",
                    "AI_ENABLED": "true",
                    "AI_MODEL": "gpt-4",
                    "AI_TEMPERATURE": "0.3",
                    "AI_MAX_TOKENS": "1000",
                    "ENABLE_EMAIL_NOTIFICATIONS": "true",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "200",
                    "SHOW_OVERDUE_ONLY": "false",
                    "SHOW_HIGH_PRIORITY_ONLY": "false",
                    "HTML_THEME": "light",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "default",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_SCHEDULING": "true",
                    "SCHEDULE_CRON": "0 9 * * 1-5",  # 9 AM weekdays
                    "SCHEDULE_TIMEZONE": "Asia/Shanghai",
                    "ENABLE_CACHING": "false",  # Always fresh data for teachers
                    "ENABLE_BACKUPS": "true",
                    "BACKUP_DIR": "class_backups",
                    "BACKUP_RETENTION_DAYS": "90",
                    "EXPORT_FORMATS": "csv,xlsx,pdf",
                    "MAX_BROWSER_INSTANCES": "3",
                    "MEMORY_LIMIT": "2048"
                }
            },

            "power_user_advanced": {
                "name": "🔧 Power User - Advanced Features",
                "description": "For advanced users who want all features enabled",
                "description_zh": "适合需要所有高级功能的高级用户",
                "config": {
                    "REPORT_FORMAT": "html,json,markdown,csv,xlsx,pdf",
                    "OUTPUT_DIR": "advanced_reports",
                    "HEADLESS": "false",  # Can see browser for debugging
                    "DEBUG": "true",
                    "LOG_LEVEL": "DEBUG",
                    "LANGUAGE": "zh",
                    "AI_ENABLED": "true",
                    "AI_MODEL": "gpt-4",
                    "AI_TEMPERATURE": "0.5",
                    "AI_MAX_TOKENS": "1500",
                    "ENABLE_EMAIL_NOTIFICATIONS": "true",
                    "FETCH_DETAILS": "true",
                    "DETAILS_LIMIT": "500",
                    "SHOW_OVERDUE_ONLY": "false",
                    "SHOW_HIGH_PRIORITY_ONLY": "false",
                    "HTML_THEME": "dark",
                    "INCLUDE_CHARTS": "true",
                    "CHART_COLOR_SCHEME": "dark",
                    "MOBILE_FRIENDLY": "true",
                    "ENABLE_PWA": "true",
                    "ENABLE_SCHEDULING": "true",
                    "SCHEDULE_CRON": "0 */6 * * *",  # Every 6 hours
                    "SCHEDULE_TIMEZONE": "Asia/Shanghai",
                    "ENABLE_CACHING": "true",
                    "CACHE_EXPIRATION": "2",
                    "ENABLE_BACKUPS": "true",
                    "BACKUP_DIR": "power_backups",
                    "BACKUP_RETENTION_DAYS": "180",
                    "BACKUP_COMPRESSION": "tar.gz",
                    "EXPORT_FORMATS": "csv,xlsx,pdf,json",
                    "CAPTURE_SCREENSHOTS": "true",
                    "SCREENSHOT_DIR": "debug_screenshots",
                    "MAX_BROWSER_INSTANCES": "5",
                    "MEMORY_LIMIT": "4096",
                    "MAX_RETRIES": "5",
                    "REQUEST_DELAY": "0.5",
                    "PRIORITY_KEYWORDS": "urgent,important,exam,test,project,essay,final,midterm,quiz,presentation,assignment,homework,due,deadline"
                }
            },

            "minimal_lightweight": {
                "name": "⚡ Minimal - Lightweight Setup",
                "description": "Minimal setup for basic functionality and fast performance",
                "description_zh": "最小化设置，基本功能和快速性能",
                "config": {
                    "REPORT_FORMAT": "console",
                    "OUTPUT_DIR": "simple_reports",
                    "HEADLESS": "true",
                    "DEBUG": "false",
                    "LANGUAGE": "en",
                    "AI_ENABLED": "false",
                    "ENABLE_EMAIL_NOTIFICATIONS": "false",
                    "FETCH_DETAILS": "false",
                    "DETAILS_LIMIT": "10",
                    "SHOW_OVERDUE_ONLY": "true",
                    "SHOW_HIGH_PRIORITY_ONLY": "false",
                    "HTML_THEME": "minimal",
                    "INCLUDE_CHARTS": "false",
                    "MOBILE_FRIENDLY": "false",
                    "ENABLE_CACHING": "false",
                    "ENABLE_BACKUPS": "false",
                    "MAX_BROWSER_INSTANCES": "1",
                    "MEMORY_LIMIT": "512",
                    "PAGE_LOAD_TIMEOUT": "15",
                    "ELEMENT_WAIT_TIMEOUT": "5"
                }
            }
        }

    def list_templates(self) -> Dict:
        """List all available templates"""
        template_list = {}
        for key, template in self.templates.items():
            template_list[key] = {
                "name": template["name"],
                "description": template["description"],
                "description_zh": template["description_zh"]
            }
        return template_list

    def get_template(self, template_key: str) -> Dict:
        """Get a specific template"""
        return self.templates.get(template_key, {})

    def apply_template(self, template_key: str, user_config: Dict) -> Dict:
        """Apply a template to user configuration"""
        template = self.get_template(template_key)
        if not template:
            return user_config

        # Start with template config
        final_config = template["config"].copy()

        # Override with user-specific settings (these always take precedence)
        user_overrides = {
            "MANAGEBAC_URL",
            "MANAGEBAC_EMAIL",
            "MANAGEBAC_PASSWORD",
            "OPENAI_API_KEY",
            "SMTP_USERNAME",
            "SMTP_PASSWORD",
            "NOTIFICATION_RECIPIENTS"
        }

        for key, value in user_config.items():
            if key in user_overrides or key not in final_config:
                final_config[key] = value

        return final_config

    def create_env_from_template(self, template_key: str, user_config: Dict,
                                output_file: str = ".env") -> bool:
        """Create .env file from template"""
        try:
            final_config = self.apply_template(template_key, user_config)

            # Read the example config file as base
            example_file = "config.example.env"
            if not os.path.exists(example_file):
                return False

            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Replace values in the content
            import re
            for key, value in final_config.items():
                pattern = rf'^{key}=.*$'
                replacement = f'{key}={value}'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        except Exception:
            return False

    def save_template_info(self, template_key: str, output_file: str = "template_info.json"):
        """Save template information to file"""
        template = self.get_template(template_key)
        if template:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)

def interactive_template_selector():
    """Interactive template selection"""
    templates = ConfigTemplates()

    print("\n🎯 Choose a Configuration Template | 选择配置模板\n")

    template_list = templates.list_templates()
    options = list(template_list.keys())

    for i, (key, info) in enumerate(template_list.items(), 1):
        print(f"{i}. {info['name']}")
        print(f"   {info['description']}")
        print(f"   {info['description_zh']}\n")

    while True:
        try:
            choice = input(f"Select template (1-{len(options)}) [1]: ").strip()
            if not choice:
                choice = "1"

            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None

def main():
    """Main entry point for template management"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "list":
            templates = ConfigTemplates()
            for key, info in templates.list_templates().items():
                print(f"{key}: {info['name']}")
        elif command == "interactive":
            selected = interactive_template_selector()
            if selected:
                print(f"Selected template: {selected}")
    else:
        print("Usage: python config_templates.py [list|interactive]")

if __name__ == "__main__":
    main()