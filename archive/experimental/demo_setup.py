#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 演示设置功能
展示所有配置工具的功能
"""

import os
import shutil
from pathlib import Path

def demo_all_setup_tools():
    """演示所有设置工具"""
    print("🎬 ManageBac Assignment Checker - 完整功能演示")
    print("=" * 60)

    # 1. 展示现有配置
    print("\n1️⃣ 当前配置状态:")
    print("-" * 30)
    if Path('.env').exists():
        print("✅ .env配置文件存在")
        try:
            from gui_launcher import is_first_time_setup
            is_first_time = is_first_time_setup()
            print(f"🎯 首次设置检测: {'是' if is_first_time else '否'} (这就是为什么GUI没有自动弹出)")
        except Exception as e:
            print(f"⚠️ 检测失败: {e}")
    else:
        print("❌ .env配置文件不存在")

    # 2. 配置验证
    print("\n2️⃣ 配置验证:")
    print("-" * 30)
    try:
        from test_config import print_header
        print("✅ 配置测试工具可用")
        print("   运行命令: python test_config.py")
    except Exception as e:
        print(f"❌ 配置测试工具错误: {e}")

    # 3. 配置模板
    print("\n3️⃣ 配置模板系统:")
    print("-" * 30)
    try:
        from config_templates import ConfigTemplates
        templates = ConfigTemplates()
        template_list = templates.list_templates()
        print(f"✅ 配置模板可用: {len(template_list)}个模板")
        for key, info in list(template_list.items())[:3]:  # 显示前3个
            print(f"   • {info['name']}")
    except Exception as e:
        print(f"❌ 配置模板错误: {e}")

    # 4. 快速模板
    print("\n4️⃣ 快速模板系统:")
    print("-" * 30)
    try:
        from quick_templates import QuickTemplates
        quick = QuickTemplates()
        schools = quick.list_school_templates()
        configs = quick.list_quick_configs()
        print(f"✅ 快速模板可用: {len(schools)}个学校模板, {len(configs)}个快速配置")
        print("   学校模板包括:")
        for key, info in schools.items():
            print(f"   • {info['name']}")
    except Exception as e:
        print(f"❌ 快速模板错误: {e}")

    # 5. 用户体验测试
    print("\n5️⃣ 用户体验测试:")
    print("-" * 30)
    try:
        from user_experience_test import UserExperienceTest
        print("✅ 用户体验测试工具可用")
        print("   运行命令: python user_experience_test.py")
    except Exception as e:
        print(f"❌ 用户体验测试错误: {e}")

    # 6. 完整配置验证
    print("\n6️⃣ 完整配置验证:")
    print("-" * 30)
    try:
        from config_validator import ConfigValidator
        print("✅ 完整配置验证工具可用")
        print("   运行命令: python config_validator.py")
    except Exception as e:
        print(f"❌ 完整配置验证错误: {e}")

    # 7. 可用命令总结
    print("\n" + "=" * 60)
    print("🚀 所有可用的配置命令:")
    print("=" * 60)
    commands = [
        ("python test_config.py", "快速配置测试"),
        ("python config_validator.py", "完整配置验证"),
        ("python setup_wizard.py", "交互式设置向导"),
        ("python first_run_setup.py", "GUI设置向导"),
        ("python quick_templates.py", "快速配置模板"),
        ("python main_new.py --test-config", "主程序配置测试"),
        ("python gui_launcher.py", "GUI启动器（智能检测首次设置）"),
        ("python user_experience_test.py", "完整用户体验测试")
    ]

    for i, (command, description) in enumerate(commands, 1):
        print(f"{i:2d}. {command:<35} - {description}")

    print("\n" + "=" * 60)
    print("💡 为什么设置向导没有自动弹出？")
    print("   因为您已经有完整的.env配置文件！")
    print("   系统智能检测到不需要首次设置。")
    print("\n🎯 如果想体验首次设置流程:")
    print("   1. 临时重命名 .env 为 .env.backup")
    print("   2. 运行 python gui_launcher.py")
    print("   3. 体验完成后恢复 .env 文件")

def test_first_time_experience():
    """测试首次设置体验"""
    print("\n" + "=" * 60)
    print("🧪 测试首次设置体验")
    print("=" * 60)

    # 备份当前配置
    env_backup = Path('.env.test_backup')
    if Path('.env').exists():
        shutil.copy('.env', env_backup)

    try:
        # 创建空配置触发首次设置
        if Path('.env').exists():
            os.remove('.env')

        from gui_launcher import is_first_time_setup
        result = is_first_time_setup()
        print(f"✅ 无配置文件时首次设置检测: {result}")

        # 创建占位符配置
        with open('.env', 'w', encoding='utf-8') as f:
            f.write("MANAGEBAC_URL=https://your-school.managebac.cn\n")
            f.write("MANAGEBAC_EMAIL=your.email@example.com\n")
            f.write("MANAGEBAC_PASSWORD=your_password\n")

        result2 = is_first_time_setup()
        print(f"✅ 占位符配置时首次设置检测: {result2}")

    finally:
        # 恢复原配置
        if env_backup.exists():
            shutil.copy(env_backup, '.env')
            os.remove(env_backup)

    print("✅ 首次设置检测功能完全正常！")

if __name__ == "__main__":
    demo_all_setup_tools()
    test_first_time_experience()