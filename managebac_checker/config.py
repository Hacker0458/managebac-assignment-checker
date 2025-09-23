"""
🎓 ManageBac Assignment Checker Configuration | ManageBac作业检查器配置管理
=============================================================================

Configuration management for ManageBac Assignment Checker.
ManageBac作业检查器的配置管理模块。
"""

import os
import sys
import getpass
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv


class ConfigMessages:
    """Bilingual configuration messages | 双语配置消息."""

    ERROR_MISSING_CREDENTIALS = {
        "en": "❌ Error: ManageBac credentials are required!",
        "zh": "❌ 错误：需要ManageBac登录凭据！",
    }

    SETUP_INSTRUCTIONS = {
        "en": """
🔧 Setup Instructions:
1. Copy config.example.env to .env: cp config.example.env .env
2. Edit .env file with your ManageBac credentials
3. Run the program again

Or you can enter credentials now (they will be saved to .env):""",
        "zh": """
🔧 配置说明：
1. 复制配置模板：cp config.example.env .env
2. 编辑.env文件，填入您的ManageBac凭据
3. 重新运行程序

或者您可以现在输入凭据（将保存到.env文件）：""",
    }

    INPUT_EMAIL = {
        "en": "📧 Enter your ManageBac email: ",
        "zh": "📧 请输入您的ManageBac邮箱: ",
    }

    INPUT_PASSWORD = {
        "en": "🔒 Enter your ManageBac password: ",
        "zh": "🔒 请输入您的ManageBac密码: ",
    }

    INPUT_URL = {
        "en": "🌐 Enter your ManageBac URL (press Enter for default): ",
        "zh": "🌐 请输入您的ManageBac网址（回车使用默认值）: ",
    }

    SAVE_SUCCESS = {
        "en": "✅ Configuration saved successfully to .env file!",
        "zh": "✅ 配置已成功保存到.env文件！",
    }

    CONFIG_LOADED = {
        "en": "✅ Configuration loaded successfully",
        "zh": "✅ 配置加载成功",
    }


class Config:
    """
    Configuration class for ManageBac Assignment Checker.
    ManageBac作业检查器配置类。
    """

    def __init__(self, language: str = "zh", interactive: bool = True):
        """
        Initialize configuration from environment variables.
        从环境变量初始化配置。

        Args:
            language: Interface language ('en' or 'zh')
            interactive: Allow interactive credential input
        """
        self.language = language
        self.interactive = interactive
        self.messages = ConfigMessages()

        # Load environment variables
        load_dotenv()

        # Try to load from .env first, then from config.example.env
        if not os.path.exists(".env") and os.path.exists("config.example.env"):
            load_dotenv("config.example.env")

        # Required credentials
        self.email = os.getenv("MANAGEBAC_EMAIL")
        self.password = os.getenv("MANAGEBAC_PASSWORD")
        self.url = os.getenv("MANAGEBAC_URL", "https://shtcs.managebac.cn")

        # Browser settings | 浏览器设置
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.timeout = int(os.getenv("BROWSER_TIMEOUT", "30000"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

        # Report settings | 报告设置
        self.report_format = os.getenv("REPORT_FORMAT", "html,json,console").split(",")
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "./reports"))

        # UI Settings | 界面设置
        self.html_theme = os.getenv("HTML_THEME", "auto")
        self.include_charts = os.getenv("INCLUDE_CHARTS", "true").lower() == "true"
        self.chart_color_scheme = os.getenv("CHART_COLOR_SCHEME", "default")

        # Email notification settings | 邮件通知设置
        self.enable_notifications = (
            os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
        )
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.notification_recipients = os.getenv("NOTIFICATION_RECIPIENTS", "").split(
            ","
        )

        # Analysis settings | 分析设置
        self.fetch_details = os.getenv("FETCH_DETAILS", "true").lower() == "true"
        self.details_limit = int(os.getenv("DETAILS_LIMIT", "50"))
        self.show_overdue_only = (
            os.getenv("SHOW_OVERDUE_ONLY", "false").lower() == "true"
        )
        self.show_high_priority_only = (
            os.getenv("SHOW_HIGH_PRIORITY_ONLY", "false").lower() == "true"
        )
        self.min_days_before_due = int(os.getenv("MIN_DAYS_BEFORE_DUE", "0"))

        # Logging settings | 日志设置
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/managebac_checker.log")

        # Create necessary directories | 创建必要目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)

        # Validate and setup credentials | 验证并设置凭据
        self._validate_and_setup()

    def _validate_and_setup(self) -> None:
        """
        Validate required configuration and setup if needed.
        验证必需配置并在需要时进行设置。
        """
        if not self.email or not self.password:
            if self.interactive:
                self._interactive_setup()
            else:
                self._print_error_and_exit()
        else:
            self._print_message("CONFIG_LOADED")

    def _interactive_setup(self) -> None:
        """
        Interactive setup for missing credentials.
        交互式设置缺失的凭据。
        """
        self._print_message("ERROR_MISSING_CREDENTIALS")
        self._print_message("SETUP_INSTRUCTIONS")

        print()

        # Get email
        if not self.email:
            self.email = input(self.messages.INPUT_EMAIL[self.language]).strip()

        # Get password
        if not self.password:
            self.password = getpass.getpass(
                self.messages.INPUT_PASSWORD[self.language]
            ).strip()

        # Get URL (optional)
        url_input = input(
            f"{self.messages.INPUT_URL[self.language]}[{self.url}]: "
        ).strip()
        if url_input:
            self.url = url_input

        # Save to .env file
        self._save_to_env()
        self._print_message("SAVE_SUCCESS")

    def _save_to_env(self) -> None:
        """
        Save configuration to .env file.
        保存配置到.env文件。
        """
        env_content = f"""# ========================================
# ManageBac Assignment Checker Configuration
# ManageBac作业检查器配置文件
# ========================================

# 🔐 ManageBac Credentials | ManageBac凭据
MANAGEBAC_EMAIL={self.email}
MANAGEBAC_PASSWORD={self.password}
MANAGEBAC_URL={self.url}

# 📊 Report Settings | 报告设置
REPORT_FORMAT=html,json,console
OUTPUT_DIR=reports
FETCH_DETAILS=true
DETAILS_LIMIT=50

# 📧 Email Notification Settings | 邮件通知设置
ENABLE_EMAIL_NOTIFICATIONS=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=true
NOTIFICATION_RECIPIENTS=

# 🔧 Browser Settings | 浏览器设置
HEADLESS=true
BROWSER_TIMEOUT=30000

# 🐛 Debug Settings | 调试设置
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/managebac_checker.log

# 🎨 UI Settings | 界面设置
HTML_THEME=auto
INCLUDE_CHARTS=true
CHART_COLOR_SCHEME=default
"""

        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)

    def _print_error_and_exit(self) -> None:
        """
        Print error message and exit.
        打印错误消息并退出。
        """
        self._print_message("ERROR_MISSING_CREDENTIALS")
        self._print_message("SETUP_INSTRUCTIONS")
        sys.exit(1)

    def _print_message(self, key: str) -> None:
        """
        Print bilingual message.
        打印双语消息。
        """
        message = getattr(self.messages, key, {})
        if isinstance(message, dict):
            print(message.get(self.language, message.get("en", key)))

    def get_report_formats(self) -> List[str]:
        """
        Get list of report formats to generate.
        获取要生成的报告格式列表。
        """
        return [fmt.strip().lower() for fmt in self.report_format if fmt.strip()]

    def is_notification_enabled(self) -> bool:
        """
        Check if email notifications are properly configured.
        检查邮件通知是否正确配置。
        """
        return (
            self.enable_notifications
            and self.smtp_server
            and self.smtp_username
            and self.smtp_password
            and self.notification_recipients
            and any(email.strip() for email in self.notification_recipients)
        )

    def get_notification_recipients(self) -> List[str]:
        """
        Get list of notification email recipients.
        获取通知邮件收件人列表。
        """
        return [
            email.strip() for email in self.notification_recipients if email.strip()
        ]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary (without sensitive data).
        将配置转换为字典（不包含敏感数据）。
        """
        return {
            "email": self.email,
            "url": self.url,
            "language": self.language,
            "headless": self.headless,
            "debug": self.debug,
            "report_formats": self.get_report_formats(),
            "output_dir": str(self.output_dir),
            "fetch_details": self.fetch_details,
            "details_limit": self.details_limit,
            "notifications_enabled": self.is_notification_enabled(),
            "log_level": self.log_level,
        }

    def __repr__(self) -> str:
        """
        String representation of config (without sensitive data).
        配置的字符串表示（不包含敏感数据）。
        """
        return (
            f"Config(email={self.email}, url={self.url}, "
            f"language={self.language}, headless={self.headless}, "
            f"debug={self.debug})"
        )
