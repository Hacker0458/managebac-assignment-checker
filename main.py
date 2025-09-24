#!/usr/bin/env python3
"""ManageBac Assignment Checker 命令行入口。"""

from __future__ import annotations

import asyncio
import sys

from managebac_checker.cli import parse_args
from managebac_checker.runner import Runner


def main() -> None:
    overrides = parse_args()
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


if __name__ == "__main__":
    main()
