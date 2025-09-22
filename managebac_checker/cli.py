"""
命令行接口模块
"""

import asyncio
import argparse
import sys
from typing import Optional

from .checker import ManageBacChecker


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="ManageBac Assignment Checker - 自动化作业检查工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  managebac-checker                    # 使用默认配置运行
  managebac-checker --debug            # 开启调试模式
  managebac-checker --headless=false   # 显示浏览器窗口
  managebac-checker --format html,json # 只生成HTML和JSON报告
        """
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="开启调试模式，显示详细的调试信息"
    )
    
    parser.add_argument(
        "--headless",
        type=str,
        choices=["true", "false"],
        help="是否使用无头浏览器模式 (默认: true)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        help="报告格式，用逗号分隔 (例如: html,json,markdown)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="报告输出目录 (默认: ./reports)"
    )
    
    parser.add_argument(
        "--fetch-details",
        action="store_true",
        help="抓取作业详情页面"
    )
    
    parser.add_argument(
        "--details-limit",
        type=int,
        help="抓取详情页面的最大数量 (默认: 10)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def apply_cli_overrides(config, args) -> None:
    """应用命令行参数覆盖配置"""
    if args.debug:
        config.debug = True
    
    if args.headless is not None:
        config.headless = args.headless.lower() == "true"
    
    if args.format:
        config.report_format = args.format.split(",")
    
    if args.output_dir:
        from pathlib import Path
        config.output_dir = Path(args.output_dir)
        config.output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.fetch_details:
        config.fetch_details = True
    
    if args.details_limit:
        config.details_limit = args.details_limit


async def main() -> int:
    """主CLI函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # 创建检查器
        checker = ManageBacChecker()
        
        # 应用命令行参数覆盖
        apply_cli_overrides(checker.config, args)
        
        # 运行检查
        await checker.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了程序")
        return 1
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def cli_main() -> None:
    """CLI入口点"""
    sys.exit(asyncio.run(main()))


if __name__ == "__main__":
    cli_main()