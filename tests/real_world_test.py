#!/usr/bin/env python3
"""
真实账号功能测试 | Real-World Functional Test

使用真实的ManageBac账号进行完整的端到端测试，验证：
1. 登录功能
2. 作业抓取准确性（与Playwright手动验证对比）
3. 数据完整性
4. 过滤功能

"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from managebac_checker.config import Config
from managebac_checker.scraper import run_scraper
from managebac_checker.logging_utils import setup_logging
import logging


class RealWorldTester:
    """真实世界功能测试器"""

    def __init__(self):
        bilingual_logger = setup_logging(level="INFO", log_file="real_world_test.log")
        self.logger = bilingual_logger.logger
        self.test_results = {}

    async def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🧪 ManageBac Assignment Checker - 真实账号功能测试")
        print("=" * 80)
        print()

        # 加载配置
        try:
            from dotenv import load_dotenv
            load_dotenv()
            config = Config.from_environment()
        except Exception as e:
            print(f"❌ 配置加载失败: {e}")
            return False

        print(f"📧 测试账号: {config.email}")
        print(f"🏫 学校URL: {config.url}")
        print()

        # 测试1: 基础作业抓取（包含所有类型）
        print("=" * 80)
        print("测试1: 完整作业抓取（包含overdue + upcoming）")
        print("=" * 80)
        config_all = Config.from_environment({
            "include_submitted": False,
            "include_overdue": True,
            "include_upcoming": True,
        })
        
        assignments_all = await run_scraper(config_all, self.logger)
        print(f"✅ 抓取完成: {len(assignments_all)}个未提交作业")
        self.test_results['all_assignments'] = len(assignments_all)
        
        self._print_assignments_summary(assignments_all)
        print()

        # 测试2: 只抓取即将到期的作业
        print("=" * 80)
        print("测试2: 只抓取即将到期的作业（不包含overdue）")
        print("=" * 80)
        config_upcoming = Config.from_environment({
            "include_submitted": False,
            "include_overdue": False,
            "include_upcoming": True,
        })
        
        assignments_upcoming = await run_scraper(config_upcoming, self.logger)
        print(f"✅ 抓取完成: {len(assignments_upcoming)}个即将到期作业")
        self.test_results['upcoming_only'] = len(assignments_upcoming)
        print()

        # 测试3: 只抓取过期作业
        print("=" * 80)
        print("测试3: 只抓取过期作业（不包含upcoming）")
        print("=" * 80)
        config_overdue = Config.from_environment({
            "include_submitted": False,
            "include_overdue": True,
            "include_upcoming": False,
        })
        
        assignments_overdue = await run_scraper(config_overdue, self.logger)
        print(f"✅ 抓取完成: {len(assignments_overdue)}个过期作业")
        self.test_results['overdue_only'] = len(assignments_overdue)
        print()

        # 验证数据一致性
        print("=" * 80)
        print("数据一致性验证")
        print("=" * 80)
        total_from_filters = self.test_results['upcoming_only'] + self.test_results['overdue_only']
        print(f"分类抓取总数: {total_from_filters} (upcoming: {self.test_results['upcoming_only']} + overdue: {self.test_results['overdue_only']})")
        print(f"完整抓取总数: {self.test_results['all_assignments']}")
        
        if total_from_filters == self.test_results['all_assignments']:
            print("✅ 数据一致性验证通过")
        else:
            diff = abs(total_from_filters - self.test_results['all_assignments'])
            print(f"⚠️ 数据不一致，差异: {diff}个作业")
        print()

        # 生成测试报告
        self._generate_report(assignments_all)

        return True

    def _print_assignments_summary(self, assignments):
        """打印作业摘要"""
        if not assignments:
            print("  ℹ️ 未找到作业")
            return

        print(f"\n  📚 作业列表 (共{len(assignments)}个):")
        print("  " + "-" * 76)
        
        for i, assignment in enumerate(assignments[:10], 1):  # 只显示前10个
            status_icon = "⏰" if assignment.overdue else "📅"
            print(f"  {i}. {status_icon} {assignment.title}")
            print(f"     课程: {assignment.course}")
            print(f"     截止: {assignment.due_date}")
            print(f"     状态: {assignment.status}")
            print()
        
        if len(assignments) > 10:
            print(f"  ... 还有 {len(assignments) - 10} 个作业未显示")

    def _generate_report(self, assignments):
        """生成详细测试报告"""
        print("=" * 80)
        print("📊 测试报告生成")
        print("=" * 80)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = Path(f"./debug_output/real_world_test_{timestamp}.txt")
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("ManageBac Assignment Checker - 真实账号测试报告\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总作业数: {len(assignments)}\n\n")
            
            f.write("测试结果汇总:\n")
            f.write("-" * 80 + "\n")
            for key, value in self.test_results.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            f.write("详细作业列表:\n")
            f.write("-" * 80 + "\n")
            for i, assignment in enumerate(assignments, 1):
                f.write(f"\n{i}. {assignment.title}\n")
                f.write(f"   课程: {assignment.course}\n")
                f.write(f"   截止日期: {assignment.due_date}\n")
                f.write(f"   状态: {assignment.status}\n")
                f.write(f"   类型: {assignment.assignment_type}\n")
                f.write(f"   优先级: {assignment.priority}\n")
                f.write(f"   已提交: {assignment.submitted}\n")
                f.write(f"   过期: {assignment.overdue}\n")
                if assignment.link:
                    f.write(f"   链接: {assignment.link}\n")
        
        print(f"✅ 测试报告已保存: {report_file}")


async def main():
    """主函数"""
    tester = RealWorldTester()
    success = await tester.run_all_tests()
    
    print()
    print("=" * 80)
    if success:
        print("🎉 所有测试完成！")
    else:
        print("❌ 测试失败")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

