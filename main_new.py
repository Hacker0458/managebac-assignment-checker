#!/usr/bin/env python3
"""
🎓 ManageBac Assignment Checker | ManageBac作业检查器
=====================================================

An intelligent automation tool for ManageBac assignment tracking.
一个用于ManageBac作业追踪的智能自动化工具。

Author: Hacker0458
GitHub: https://github.com/Hacker0458/managebac-assignment-checker
License: MIT

Usage:
  python main_new.py
  python -m managebac_checker
  managebac-checker  # if installed via pip
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from managebac_checker.cli import main


def welcome_message():
    """Display welcome message in bilingual format."""
    # Detect language from environment
    lang = "zh" if os.getenv("LANG", "").startswith("zh") else "zh"  # Default to Chinese
    
    if lang == "zh":
        print("🎓 欢迎使用 ManageBac作业检查器 v2.0.0")
        print("=" * 50)
        print("📚 智能作业追踪自动化工具")
        print("👨‍💻 作者: Hacker0458")
        print("🔗 GitHub: https://github.com/Hacker0458/managebac-assignment-checker")
        print("📄 许可证: MIT")
        print()
        print("🚀 正在启动...")
        print()
    else:
        print("🎓 Welcome to ManageBac Assignment Checker v2.0.0")
        print("=" * 50)
        print("📚 Intelligent automation tool for assignment tracking")
        print("👨‍💻 Author: Hacker0458")
        print("🔗 GitHub: https://github.com/Hacker0458/managebac-assignment-checker")
        print("📄 License: MIT")
        print()
        print("🚀 Starting up...")
        print()


if __name__ == "__main__":
    try:
        welcome_message()
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断 | Program interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序出错 | Program error: {e}")
        sys.exit(1)