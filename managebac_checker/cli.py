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
    return overrides


def main(argv: Optional[List[str]] = None) -> None:
    overrides = parse_args(argv)
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
