#!/usr/bin/env python3
"""
ManageBac Assignment Checker - 主入口文件

自动化工具，用于登录ManageBac并检查未提交的作业。
"""

import asyncio
import sys
from managebac_checker import ManageBacChecker


async def main():
    """主入口函数"""
    try:
        checker = ManageBacChecker()
        await checker.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了程序")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
