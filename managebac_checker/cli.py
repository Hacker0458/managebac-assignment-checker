"""ManageBac Assignment Checker 的命令行入口。"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Dict, List, Optional
import sys

from . import __version__
from .runner import Runner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ManageBac 作业检查器",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--email", help="ManageBac 登录邮箱")
    parser.add_argument("--password", help="ManageBac 登录密码")
    parser.add_argument("--url", help="ManageBac 门户地址")
    parser.add_argument(
        "--headless", choices=["true", "false"], help="是否使用无头模式运行浏览器"
    )
    parser.add_argument("--debug", action="store_true", help="启用调试日志")
    parser.add_argument(
        "--format", help="报告格式，逗号分隔：console,html,json,markdown"
    )
    parser.add_argument("--output-dir", type=Path, help="报告输出目录")
    parser.add_argument(
        "--fetch-details", choices=["true", "false"], help="是否抓取作业详情页"
    )
    parser.add_argument("--details-limit", type=int, help="抓取作业详情的最大数量")
    parser.add_argument(
        "--notifications", choices=["true", "false"], help="是否启用邮件通知"
    )
    parser.add_argument("--timeout", type=int, help="Playwright 超时时间 (毫秒)")
    parser.add_argument(
        "--test-config", action="store_true", help="测试配置设置并退出"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def parse_args(argv: Optional[List[str]] = None) -> Dict:
    parser = build_parser()
    args = parser.parse_args(argv)

    overrides: Dict = {}
    if args.email:
        overrides["email"] = args.email
    if args.password:
        overrides["password"] = args.password
    if args.url:
        overrides["url"] = args.url
    if args.headless is not None:
        overrides["headless"] = args.headless.lower() == "true"
    if args.debug:
        overrides["debug"] = True
    if args.format:
        overrides["report_format"] = args.format
    if args.output_dir:
        overrides["output_dir"] = str(args.output_dir)
    if args.fetch_details is not None:
        overrides["fetch_details"] = args.fetch_details.lower() == "true"
    if args.details_limit is not None:
        overrides["details_limit"] = args.details_limit
    if args.notifications is not None:
        overrides["enable_notifications"] = args.notifications.lower() == "true"
    if args.timeout is not None:
        overrides["timeout"] = args.timeout

    # Special handling for test-config
    overrides["test_config"] = getattr(args, 'test_config', False)

    return overrides


async def run_config_test() -> None:
    """Run configuration test"""
    try:
        # Import here to avoid dependency issues
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from test_config import run_quick_test

        print("🧪 Running configuration test...")
        print("🧪 正在运行配置测试...")
        print()

        success = await run_quick_test()
        if success:
            print("\n✅ Configuration test passed!")
            print("✅ 配置测试通过！")
        else:
            print("\n❌ Configuration test failed!")
            print("❌ 配置测试失败！")
            raise SystemExit(1)

    except ImportError:
        print("❌ Configuration test unavailable - test_config.py not found")
        print("❌ 配置测试不可用 - 找不到test_config.py")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        print(f"❌ 配置测试错误：{e}")
        raise SystemExit(1)


def main(argv: Optional[List[str]] = None) -> None:
    overrides = parse_args(argv)

    # Handle test-config option
    if overrides.get("test_config", False):
        try:
            asyncio.run(run_config_test())
            return
        except SystemExit:
            raise

    try:
        runner = Runner(overrides)
    except ValueError as exc:
        print(f"配置错误：{exc}", file=sys.stderr)
        raise SystemExit(2)

    try:
        asyncio.run(runner.execute())
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        raise SystemExit(130)


if __name__ == "__main__":  # pragma: no cover
    main()
