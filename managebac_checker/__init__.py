"""ManageBac Assignment Checker 包装模块。"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:  # pragma: no cover - 打包后可读取真实版本
    __version__ = version("managebac-assignment-checker")
except PackageNotFoundError:  # pragma: no cover - 开发环境回退
    __version__ = "0.0.0"

from .config import Config
from .runner import Runner, run_sync
from .analysis import analyse_assignments
from .reporting import ReportBuilder
from .scraper import ManageBacScraper
from .checker import ManageBacChecker
from .reporter import ReportGenerator
from .notifications import NotificationManager
from .analyzer import AssignmentAnalyzer

__all__ = [
    "__version__",
    "Config",
    "Runner",
    "run_sync",
    "analyse_assignments",
    "ReportBuilder",
    "ManageBacScraper",
    "ManageBacChecker",
    "ReportGenerator",
    "NotificationManager",
    "AssignmentAnalyzer",
]
