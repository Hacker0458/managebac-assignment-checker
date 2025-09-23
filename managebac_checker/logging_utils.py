"""
🎓 ManageBac Assignment Checker Logging | ManageBac作业检查器日志系统
========================================================================

Bilingual logging utilities for ManageBac Assignment Checker.
ManageBac作业检查器的双语日志工具。
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class BilingualFormatter(logging.Formatter):
    """
    Custom formatter for bilingual logging.
    双语日志的自定义格式化器。
    """

    def __init__(self, language: str = "zh", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language = language

        # Bilingual level names | 双语级别名称
        self.level_names = {
            "en": {
                logging.DEBUG: "DEBUG",
                logging.INFO: "INFO",
                logging.WARNING: "WARNING",
                logging.ERROR: "ERROR",
                logging.CRITICAL: "CRITICAL",
            },
            "zh": {
                logging.DEBUG: "调试",
                logging.INFO: "信息",
                logging.WARNING: "警告",
                logging.ERROR: "错误",
                logging.CRITICAL: "严重",
            },
        }

    def format(self, record):
        """Format log record with bilingual support."""
        # Get localized level name
        level_name = self.level_names.get(self.language, self.level_names["en"]).get(
            record.levelno, record.levelname
        )

        # Create formatted message
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        if self.language == "zh":
            formatted_msg = (
                f"[{timestamp}] [{level_name}] {record.name}: {record.getMessage()}"
            )
        else:
            formatted_msg = (
                f"[{timestamp}] [{level_name}] {record.name}: {record.getMessage()}"
            )

        return formatted_msg


class BilingualLogger:
    """
    Bilingual logger wrapper.
    双语日志包装器。
    """

    def __init__(self, name: str, language: str = "zh"):
        self.name = name
        self.language = language
        self.logger = logging.getLogger(name)

        # Message templates | 消息模板
        self.templates = {
            "startup": {
                "en": "🚀 ManageBac Assignment Checker started",
                "zh": "🚀 ManageBac作业检查器已启动",
            },
            "config_loaded": {
                "en": "⚙️ Configuration loaded successfully",
                "zh": "⚙️ 配置加载成功",
            },
            "login_start": {
                "en": "🔐 Starting ManageBac login...",
                "zh": "🔐 开始登录ManageBac...",
            },
            "login_success": {
                "en": "✅ Successfully logged into ManageBac",
                "zh": "✅ 成功登录ManageBac",
            },
            "scraping_start": {
                "en": "🔍 Starting assignment scraping...",
                "zh": "🔍 开始抓取作业信息...",
            },
            "assignments_found": {
                "en": "📚 Found {count} assignments",
                "zh": "📚 发现 {count} 个作业",
            },
            "analysis_start": {
                "en": "📊 Starting assignment analysis...",
                "zh": "📊 开始分析作业...",
            },
            "report_generation": {
                "en": "📝 Generating {format} report...",
                "zh": "📝 生成 {format} 报告...",
            },
            "report_saved": {
                "en": "💾 Report saved to: {path}",
                "zh": "💾 报告已保存至: {path}",
            },
            "notification_sent": {
                "en": "📧 Email notification sent to {recipients}",
                "zh": "📧 邮件通知已发送至 {recipients}",
            },
            "error_occurred": {
                "en": "❌ Error occurred: {error}",
                "zh": "❌ 发生错误: {error}",
            },
            "completion": {
                "en": "🎉 Assignment check completed successfully!",
                "zh": "🎉 作业检查完成！",
            },
        }

    def _format_message(self, template_key: str, **kwargs) -> str:
        """Format message using template and language."""
        template = self.templates.get(template_key, {})
        message = template.get(self.language, template.get("en", template_key))
        return message.format(**kwargs) if kwargs else message

    def startup(self):
        """Log startup message."""
        self.logger.info(self._format_message("startup"))

    def config_loaded(self):
        """Log configuration loaded message."""
        self.logger.info(self._format_message("config_loaded"))

    def login_start(self):
        """Log login start message."""
        self.logger.info(self._format_message("login_start"))

    def login_success(self):
        """Log successful login message."""
        self.logger.info(self._format_message("login_success"))

    def scraping_start(self):
        """Log scraping start message."""
        self.logger.info(self._format_message("scraping_start"))

    def assignments_found(self, count: int):
        """Log assignments found message."""
        self.logger.info(self._format_message("assignments_found", count=count))

    def analysis_start(self):
        """Log analysis start message."""
        self.logger.info(self._format_message("analysis_start"))

    def report_generation(self, format_type: str):
        """Log report generation message."""
        self.logger.info(self._format_message("report_generation", format=format_type))

    def report_saved(self, path: str):
        """Log report saved message."""
        self.logger.info(self._format_message("report_saved", path=path))

    def notification_sent(self, recipients: str):
        """Log notification sent message."""
        self.logger.info(
            self._format_message("notification_sent", recipients=recipients)
        )

    def error_occurred(self, error: str):
        """Log error message."""
        self.logger.error(self._format_message("error_occurred", error=error))

    def completion(self):
        """Log completion message."""
        self.logger.info(self._format_message("completion"))

    # Standard logging methods
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)

    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    language: str = "zh",
    format_string: Optional[str] = None,
) -> BilingualLogger:
    """
    Set up bilingual logging configuration.
    设置双语日志配置。

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        language: Interface language ('en' or 'zh')
        format_string: Optional custom format string

    Returns:
        Configured bilingual logger instance
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Create bilingual formatter
    formatter = BilingualFormatter(language=language)

    # Get root logger
    root_logger = logging.getLogger("managebac_checker")
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Return bilingual logger wrapper
    return BilingualLogger("managebac_checker", language=language)


def get_logger(
    name: str = "managebac_checker", language: str = "zh"
) -> BilingualLogger:
    """
    Get a bilingual logger instance.
    获取双语日志实例。

    Args:
        name: Logger name
        language: Interface language ('en' or 'zh')

    Returns:
        Bilingual logger instance
    """
    return BilingualLogger(name, language=language)
