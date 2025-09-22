"""
ManageBac Assignment Checker

A Python tool to automatically check ManageBac assignments and generate reports.
"""

__version__ = "1.0.0"
__author__ = "ManageBac Assignment Checker Team"
__email__ = ""

from .checker import ManageBacChecker
from .config import Config
from .scraper import ManageBacScraper
from .analyzer import AssignmentAnalyzer
from .reporter import ReportGenerator

__all__ = [
    "ManageBacChecker",
    "Config", 
    "ManageBacScraper",
    "AssignmentAnalyzer",
    "ReportGenerator"
]