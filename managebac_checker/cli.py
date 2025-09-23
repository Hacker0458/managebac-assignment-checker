"""
🎓 ManageBac Assignment Checker CLI | ManageBac作业检查器命令行界面
====================================================================

Bilingual command line interface for ManageBac Assignment Checker.
ManageBac作业检查器的双语命令行接口。
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

from .checker import ManageBacChecker
from .config import Config
from .logging_utils import setup_logging


class BilingualCLI:
    """
    Bilingual Command Line Interface.
    双语命令行界面。
    """

    def __init__(self, language: str = "zh"):
        self.language = language
        self.messages = self._get_messages()

    def _get_messages(self) -> Dict[str, Dict[str, str]]:
        """Get bilingual CLI messages."""
        return {
            "description": {
                "en": "🎓 ManageBac Assignment Checker - Intelligent automation tool for assignment tracking",
                "zh": "🎓 ManageBac作业检查器 - 智能作业追踪自动化工具",
            },
            "epilog": {
                "en": """
🌟 Example Usage | 使用示例:
  managebac-checker                           # Run with default settings | 使用默认设置运行
  managebac-checker --language en            # Use English interface | 使用英文界面
  managebac-checker --debug                   # Enable debug mode | 开启调试模式
  managebac-checker --headless=false          # Show browser window | 显示浏览器窗口
  managebac-checker --format html,json       # Generate only HTML and JSON reports | 只生成HTML和JSON报告
  managebac-checker --interactive             # Interactive setup | 交互式设置
  managebac-checker --check-config            # Check configuration | 检查配置

🔗 More Information | 更多信息:
  GitHub: https://github.com/Hacker0458/managebac-assignment-checker
  Documentation: https://github.com/Hacker0458/managebac-assignment-checker#readme
                """,
                "zh": """
🌟 使用示例 | Example Usage:
  managebac-checker                           # 使用默认设置运行 | Run with default settings
  managebac-checker --language en            # 使用英文界面 | Use English interface
  managebac-checker --debug                   # 开启调试模式 | Enable debug mode
  managebac-checker --headless=false          # 显示浏览器窗口 | Show browser window
  managebac-checker --format html,json       # 只生成HTML和JSON报告 | Generate only HTML and JSON reports
  managebac-checker --interactive             # 交互式设置 | Interactive setup
  managebac-checker --check-config            # 检查配置 | Check configuration

🔗 更多信息 | More Information:
  GitHub: https://github.com/Hacker0458/managebac-assignment-checker
  文档 | Documentation: https://github.com/Hacker0458/managebac-assignment-checker#readme
                """,
            },
            "args": {
                "language": {
                    "en": "Interface language (en/zh)",
                    "zh": "界面语言 (en/zh)",
                },
                "debug": {
                    "en": "Enable debug mode with detailed logging",
                    "zh": "开启调试模式，显示详细日志",
                },
                "headless": {
                    "en": "Run browser in headless mode (default: true)",
                    "zh": "使用无头浏览器模式 (默认: true)",
                },
                "format": {
                    "en": "Report formats, comma-separated (e.g., html,json,console)",
                    "zh": "报告格式，用逗号分隔 (例如: html,json,console)",
                },
                "output_dir": {
                    "en": "Output directory for reports (default: ./reports)",
                    "zh": "报告输出目录 (默认: ./reports)",
                },
                "fetch_details": {
                    "en": "Fetch detailed assignment information",
                    "zh": "抓取详细的作业信息",
                },
                "details_limit": {
                    "en": "Maximum number of assignments to fetch details for (default: 50)",
                    "zh": "抓取详情的最大作业数量 (默认: 50)",
                },
                "interactive": {
                    "en": "Run in interactive mode for configuration setup",
                    "zh": "运行交互模式进行配置设置",
                },
                "check_config": {
                    "en": "Check and validate configuration without running",
                    "zh": "检查并验证配置而不运行程序",
                },
                "no_notifications": {
                    "en": "Disable email notifications",
                    "zh": "禁用邮件通知",
                },
                "ai_enabled": {
                    "en": "Enable AI Assistant for intelligent analysis",
                    "zh": "启用AI助手进行智能分析",
                },
                "ai_key": {
                    "en": "OpenAI API Key for AI Assistant",
                    "zh": "AI助手的OpenAI API密钥",
                },
                "ai_model": {
                    "en": "AI model to use (gpt-3.5-turbo or gpt-4)",
                    "zh": "使用的AI模型 (gpt-3.5-turbo 或 gpt-4)",
                },
                "version": {"en": "Show version information", "zh": "显示版本信息"},
            },
            "messages": {
                "starting": {
                    "en": "🚀 Starting ManageBac Assignment Checker...",
                    "zh": "🚀 启动ManageBac作业检查器...",
                },
                "interrupted": {
                    "en": "\n\n⚠️  Program interrupted by user",
                    "zh": "\n\n⚠️  用户中断了程序",
                },
                "error_occurred": {
                    "en": "\n❌ Program error: {error}",
                    "zh": "\n❌ 程序运行出错: {error}",
                },
                "config_check": {
                    "en": "🔧 Configuration Check Results:",
                    "zh": "🔧 配置检查结果:",
                },
                "config_valid": {
                    "en": "✅ Configuration is valid",
                    "zh": "✅ 配置有效",
                },
                "config_invalid": {
                    "en": "❌ Configuration has issues",
                    "zh": "❌ 配置存在问题",
                },
                "completion": {
                    "en": "🎉 ManageBac Assignment Checker completed successfully!",
                    "zh": "🎉 ManageBac作业检查器运行完成！",
                },
            },
        }

    def get_message(self, category: str, key: str, **kwargs) -> str:
        """Get localized message."""
        message = self.messages.get(category, {}).get(key, {})
        text = message.get(self.language, message.get("en", f"{category}.{key}"))
        return text.format(**kwargs) if kwargs else text

    def create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        parser = argparse.ArgumentParser(
            prog="managebac-checker",
            description=self.get_message("description", ""),
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self.get_message("epilog", ""),
        )

        # Language selection
        parser.add_argument(
            "--language",
            "--lang",
            type=str,
            choices=["en", "zh"],
            default=self.language,
            help=self.get_message("args", "language"),
        )

        # Debug mode
        parser.add_argument(
            "--debug", "-d", action="store_true", help=self.get_message("args", "debug")
        )

        # Browser settings
        parser.add_argument(
            "--headless",
            type=str,
            choices=["true", "false"],
            help=self.get_message("args", "headless"),
        )

        # Report settings
        parser.add_argument(
            "--format", "-f", type=str, help=self.get_message("args", "format")
        )

        parser.add_argument(
            "--output-dir", "-o", type=str, help=self.get_message("args", "output_dir")
        )

        # Scraping settings
        parser.add_argument(
            "--fetch-details",
            action="store_true",
            help=self.get_message("args", "fetch_details"),
        )

        parser.add_argument(
            "--details-limit", type=int, help=self.get_message("args", "details_limit")
        )

        # Interactive mode
        parser.add_argument(
            "--interactive",
            "-i",
            action="store_true",
            help=self.get_message("args", "interactive"),
        )

        # Configuration check
        parser.add_argument(
            "--check-config",
            action="store_true",
            help=self.get_message("args", "check_config"),
        )

        # Notification settings
        parser.add_argument(
            "--no-notifications",
            action="store_true",
            help=self.get_message("args", "no_notifications"),
        )

        # AI Assistant arguments | AI助手参数
        parser.add_argument(
            "--ai-enabled",
            action="store_true",
            help=self.get_message("args", "ai_enabled"),
        )
        parser.add_argument(
            "--ai-key",
            type=str,
            help=self.get_message("args", "ai_key"),
        )
        parser.add_argument(
            "--ai-model",
            type=str,
            choices=["gpt-3.5-turbo", "gpt-4"],
            default="gpt-3.5-turbo",
            help=self.get_message("args", "ai_model"),
        )

        # Version
        parser.add_argument(
            "--version",
            "-v",
            action="version",
            version="%(prog)s 2.0.0",
            help=self.get_message("args", "version"),
        )

        return parser

    def apply_cli_overrides(self, config: Config, args: argparse.Namespace) -> None:
        """Apply command line argument overrides to configuration."""
        if args.debug:
            config.debug = True

        if args.headless is not None:
            config.headless = args.headless.lower() == "true"

        if args.format:
            config.report_format = args.format.split(",")

        if args.output_dir:
            config.output_dir = Path(args.output_dir)
            config.output_dir.mkdir(parents=True, exist_ok=True)

        if args.fetch_details:
            config.fetch_details = True

        if args.details_limit:
            config.details_limit = args.details_limit

        if args.no_notifications:
            config.enable_notifications = False

        # Update language
        if args.language:
            config.language = args.language

    def check_configuration(self, config: Config) -> bool:
        """Check and validate configuration."""
        print(self.get_message("messages", "config_check"))
        print()

        issues = []

        # Check credentials
        if not config.email:
            issues.append("❌ ManageBac email not configured")
        else:
            print(f"✅ Email: {config.email}")

        if not config.password:
            issues.append("❌ ManageBac password not configured")
        else:
            print("✅ Password: [CONFIGURED]")

        print(f"✅ URL: {config.url}")
        print(f"✅ Report formats: {', '.join(config.get_report_formats())}")
        print(f"✅ Output directory: {config.output_dir}")
        print(f"✅ Headless mode: {config.headless}")
        print(f"✅ Debug mode: {config.debug}")
        print(f"✅ Language: {config.language}")

        if config.is_notification_enabled():
            print("✅ Email notifications: Enabled")
            print(f"  📧 Recipients: {', '.join(config.get_notification_recipients())}")
        else:
            print("ℹ️ Email notifications: Disabled")

        print()

        if issues:
            print(self.get_message("messages", "config_invalid"))
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print(self.get_message("messages", "config_valid"))
            return True

    async def run(self) -> int:
        """Main CLI execution."""
        parser = self.create_parser()
        args = parser.parse_args()

        # Update language if specified
        if args.language and args.language != self.language:
            self.language = args.language
            self.messages = self._get_messages()

        try:
            print(self.get_message("messages", "starting"))

            # Create configuration
            config = Config(
                language=args.language or self.language, interactive=args.interactive
            )

            # Setup logging
            log_level = "DEBUG" if args.debug else config.log_level
            logger = setup_logging(
                level=log_level, log_file=config.log_file, language=config.language
            )

            # Apply CLI overrides
            self.apply_cli_overrides(config, args)

            # Check configuration only
            if args.check_config:
                is_valid = self.check_configuration(config)
                return 0 if is_valid else 1

            # Create and run checker
            checker = ManageBacChecker(config=config, logger=logger)
            await checker.run()

            print(self.get_message("messages", "completion"))
            return 0

        except KeyboardInterrupt:
            print(self.get_message("messages", "interrupted"))
            return 1
        except Exception as e:
            print(self.get_message("messages", "error_occurred", error=str(e)))
            if args.debug:
                import traceback

                traceback.print_exc()
            return 1


def main() -> int:
    """Main CLI entry point."""
    # Detect system language
    default_language = "zh" if os.getenv("LANG", "").startswith("zh") else "zh"

    # Check for language override in args
    if "--language" in sys.argv:
        try:
            lang_index = sys.argv.index("--language")
            if lang_index + 1 < len(sys.argv):
                default_language = sys.argv[lang_index + 1]
        except (ValueError, IndexError):
            pass
    elif "--lang" in sys.argv:
        try:
            lang_index = sys.argv.index("--lang")
            if lang_index + 1 < len(sys.argv):
                default_language = sys.argv[lang_index + 1]
        except (ValueError, IndexError):
            pass

    cli = BilingualCLI(language=default_language)
    return asyncio.run(cli.run())


def cli_main() -> None:
    """CLI entry point for console scripts."""
    sys.exit(main())


if __name__ == "__main__":
    cli_main()
