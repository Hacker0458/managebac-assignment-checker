"""增强的日志系统，支持结构化日志和更详细的跟踪。"""

from __future__ import annotations

import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """JSON格式的日志格式化器，用于结构化日志。"""

    def format(self, record: logging.LogRecord) -> str:
        """
        将日志记录格式化为JSON。

        Args:
            record: 日志记录

        Returns:
            JSON格式的日志字符串
        """
        log_obj = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # 添加异常信息
        if record.exc_info:
            log_obj["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": "".join(
                    traceback.format_exception(*record.exc_info)
                ).strip(),
            }

        # 添加额外字段
        if hasattr(record, "extra_data"):
            log_obj["extra"] = record.extra_data

        return json.dumps(log_obj, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器，在终端中显示彩色日志。"""

    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[35m",  # 紫色
    }
    RESET = "\033[0m"

    EMOJIS = {
        "DEBUG": "🔍",
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        将日志记录格式化为彩色输出。

        Args:
            record: 日志记录

        Returns:
            彩色格式化的日志字符串
        """
        # 添加颜色
        color = self.COLORS.get(record.levelname, "")
        emoji = self.EMOJIS.get(record.levelname, "")
        record.levelname = f"{color}{emoji} {record.levelname}{self.RESET}"

        return super().format(record)


class StructuredLogger(logging.LoggerAdapter):
    """结构化日志记录器，支持添加上下文信息。"""

    def __init__(
        self,
        logger: logging.Logger,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        初始化结构化日志记录器。

        Args:
            logger: 基础日志记录器
            extra: 额外的上下文信息
        """
        super().__init__(logger, extra or {})

    def process(
        self, msg: str, kwargs: Dict[str, Any]
    ) -> tuple[str, Dict[str, Any]]:
        """
        处理日志消息，添加上下文信息。

        Args:
            msg: 日志消息
            kwargs: 日志参数

        Returns:
            处理后的消息和参数
        """
        # 将extra信息合并到kwargs中
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        # 添加适配器的extra信息
        kwargs["extra"].update(self.extra)

        # 添加额外的上下文字段
        if "extra_data" in kwargs:
            record_extra = kwargs.get("extra", {})
            record_extra["extra_data"] = kwargs.pop("extra_data")
            kwargs["extra"] = record_extra

        return msg, kwargs

    def with_context(self, **context: Any) -> StructuredLogger:
        """
        创建带有额外上下文的新日志记录器。

        Args:
            **context: 上下文信息

        Returns:
            新的结构化日志记录器

        Example:
            user_logger = logger.with_context(user_id="12345", session="abc")
            user_logger.info("User logged in")
        """
        new_extra = dict(self.extra)
        new_extra.update(context)
        return StructuredLogger(self.logger, new_extra)


def setup_enhanced_logging(
    level: str | int = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False,
    colored: bool = True,
) -> StructuredLogger:
    """
    设置增强的日志系统。

    Args:
        level: 日志级别
        log_file: 日志文件路径
        json_format: 是否使用JSON格式
        colored: 是否使用彩色输出

    Returns:
        结构化日志记录器
    """
    # 转换日志级别
    if isinstance(level, bool):
        numeric_level = logging.DEBUG if level else logging.INFO
    elif isinstance(level, str):
        numeric_level = getattr(logging, level.upper(), logging.INFO)
    else:
        numeric_level = int(level)

    # 创建日志目录
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # 清除现有的处理器
    root_logger.handlers.clear()

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)

    if colored and sys.stdout.isatty():
        console_formatter = ColoredFormatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        console_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器
    if log_file:
        file_path = log_dir / log_file

        # 普通日志文件
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

        # JSON日志文件（如果启用）
        if json_format:
            json_file = log_dir / f"{Path(log_file).stem}_json.log"
            json_handler = logging.FileHandler(json_file, encoding="utf-8")
            json_handler.setLevel(numeric_level)
            json_handler.setFormatter(JSONFormatter())
            root_logger.addHandler(json_handler)

    # 创建应用程序日志记录器
    app_logger = logging.getLogger("managebac_checker")
    app_logger.setLevel(numeric_level)

    return StructuredLogger(app_logger)


class LogContext:
    """日志上下文管理器，用于临时添加上下文信息。"""

    def __init__(self, logger: StructuredLogger, **context: Any) -> None:
        """
        初始化日志上下文。

        Args:
            logger: 结构化日志记录器
            **context: 上下文信息
        """
        self.logger = logger
        self.context = context
        self.old_logger: Optional[StructuredLogger] = None

    def __enter__(self) -> StructuredLogger:
        """进入上下文。"""
        self.old_logger = self.logger
        return self.logger.with_context(**self.context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文。"""
        # 上下文自动恢复
        pass
