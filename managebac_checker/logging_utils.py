"""日志工具，为旧有接口提供兼容支持。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


class BilingualLogger:
    """轻量级双语记录器包装，兼容旧接口。"""

    def __init__(self, logger: logging.Logger, language: str = "zh") -> None:
        self.logger = logger
        self.language = language

    # 旧接口使用的语义化方法
    def startup(self) -> None:
        self.logger.info("🚀 ManageBac 作业检查器启动")

    def config_loaded(self) -> None:
        self.logger.info("⚙️ 配置加载完成")

    def login_start(self) -> None:
        self.logger.info("🔐 正在登录 ManageBac")

    def login_success(self) -> None:
        self.logger.info("✅ 登录成功")

    def scraping_start(self) -> None:
        self.logger.info("🔍 开始抓取作业数据")

    def assignments_found(self, count: int) -> None:
        self.logger.info("📚 共发现 %s 个作业", count)

    def analysis_start(self) -> None:
        self.logger.info("📊 开始分析作业数据")

    def report_generation(self, format_type: str) -> None:
        self.logger.info("📝 正在生成 %s 报告", format_type)

    def report_saved(self, path: str) -> None:
        self.logger.info("💾 报告已保存至 %s", path)

    def notification_sent(self, recipients: str) -> None:
        self.logger.info("📧 通知邮件已发送至 %s", recipients)

    def error_occurred(self, error: str) -> None:
        self.logger.error("❌ 发生错误: %s", error)

    def completion(self) -> None:
        self.logger.info("🎉 作业检查完成")

    # 透传常用方法
    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self.logger.critical(message, *args, **kwargs)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance | 获取日志记录器实例"""
    return logging.getLogger(name)


def setup_logging(
    level: str | int = "INFO",
    log_file: Optional[str] = None,
    language: str = "zh",
) -> BilingualLogger:
    """配置日志并返回兼容旧接口的记录器。"""
    if isinstance(level, bool):
        numeric_level = logging.DEBUG if level else logging.INFO
    elif isinstance(level, str):
        numeric_level = getattr(logging, level.upper(), logging.INFO)
    else:
        numeric_level = int(level)

    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)

    handlers = [logging.StreamHandler()]
    file_target = log_dir / (log_file or "managebac_checker.log")
    handlers.append(logging.FileHandler(file_target))

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )

    base_logger = logging.getLogger("managebac_checker")
    base_logger.debug("Logging configured (level=%s)", numeric_level)
    return BilingualLogger(base_logger, language=language)
