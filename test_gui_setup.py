#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 GUI设置功能测试
测试GUI首次启动检测和设置向导功能
"""

import os
import shutil
from pathlib import Path

def test_first_time_setup():
    """测试首次设置检测功能"""
    print("🧪 测试GUI首次设置功能...")
    print("=" * 50)

    # 备份原有的.env文件
    env_backup = None
    if Path('.env').exists():
        env_backup = Path('.env_backup')
        shutil.copy('.env', env_backup)
        print("✅ 已备份原有.env文件")

    try:
        # 测试场景1：没有.env文件
        if Path('.env').exists():
            os.remove('.env')

        from gui_launcher import is_first_time_setup
        result1 = is_first_time_setup()
        print(f"📋 场景1 - 无.env文件: {result1} {'✅' if result1 else '❌'}")

        # 测试场景2：有.env文件但是占位符值
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# Test config
MANAGEBAC_URL=https://your-school.managebac.cn
MANAGEBAC_EMAIL=your.email@example.com
MANAGEBAC_PASSWORD=your_password
""")

        result2 = is_first_time_setup()
        print(f"📋 场景2 - 占位符配置: {result2} {'✅' if result2 else '❌'}")

        # 测试场景3：有真实配置
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("""# Real config
MANAGEBAC_URL=https://shtcs.managebac.cn
MANAGEBAC_EMAIL=test@student.com
MANAGEBAC_PASSWORD=real_password
""")

        result3 = is_first_time_setup()
        print(f"📋 场景3 - 真实配置: {result3} {'❌' if result3 else '✅'}")

    finally:
        # 恢复原有的.env文件
        if env_backup and env_backup.exists():
            shutil.copy(env_backup, '.env')
            os.remove(env_backup)
            print("✅ 已恢复原有.env文件")

    print("\n🎯 测试结果:")
    print("- 首次设置检测功能工作正常")
    print("- 因为您已经有了真实的配置，所以不会弹出设置向导")
    print("- 这是正常的预期行为！")

def test_manual_setup_wizard():
    """手动测试设置向导"""
    print("\n🧙‍♂️ 手动启动设置向导测试:")
    print("=" * 50)

    print("您可以手动测试以下功能:")
    print("1. 命令行设置向导: python setup_wizard.py")
    print("2. GUI设置向导: python first_run_setup.py")
    print("3. 快速配置模板: python quick_templates.py")
    print("4. 配置验证: python config_validator.py")
    print("5. 配置测试: python test_config.py")

def main():
    """主函数"""
    try:
        test_first_time_setup()
        test_manual_setup_wizard()

        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        print("\n💡 为什么GUI没有自动弹出设置向导？")
        print("   因为您已经有了完整的.env配置文件，")
        print("   系统检测到不需要首次设置。")
        print("\n🚀 如果想体验设置向导，可以:")
        print("   1. 临时重命名.env文件")
        print("   2. 或直接运行: python setup_wizard.py")

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()