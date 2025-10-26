#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ManageBac Assignment Checker - 一键启动
🎯 ManageBac作业检查器 - 一键启动

专为小白用户设计的傻瓜式启动脚本。
Fool-proof startup script designed specifically for novice users.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def clear_screen():
    """清屏"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """显示欢迎横幅"""
    clear_screen()
    print("=" * 70)
    print("🎓 ManageBac Assignment Checker | ManageBac作业检查器")
    print("=" * 70)
    print("📚 智能作业追踪自动化工具")
    print("📚 Intelligent Assignment Tracking Tool")
    print("=" * 70)
    print()

def animate_loading(text, duration=2):
    """显示加载动画"""
    animation = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r{text} {animation[i % len(animation)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r{text} ✅", flush=True)

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8或更高版本")
        return False

def check_files():
    """检查必要文件"""
    required_files = ['run_app.py', 'gui_launcher.py', 'main_new.py']

    for file in required_files:
        if Path(file).exists():
            print(f"✅ 找到启动文件: {file}")
            return file

    print("❌ 未找到任何启动文件")
    return None

def check_config():
    """检查配置文件"""
    config_file = Path('.env')

    if not config_file.exists():
        print("⚠️ 配置文件不存在，需要首次设置")
        return False

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查关键配置
        required_configs = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
        missing = []

        for config in required_configs:
            if config not in content:
                missing.append(config)

        if missing:
            print(f"⚠️ 配置文件缺少必要设置: {', '.join(missing)}")
            return False

        # 检查是否为占位符
        placeholders = ['your.email@example.com', 'your_password', 'your-school.managebac.cn']
        for placeholder in placeholders:
            if placeholder in content:
                print("⚠️ 配置文件包含占位符，需要填写真实信息")
                return False

        print("✅ 配置文件检查通过")
        return True

    except Exception as e:
        print(f"❌ 配置文件读取错误: {e}")
        return False

def run_setup():
    """运行设置向导"""
    print("\n🔧 正在启动设置向导...")

    # 尝试运行智能启动器进行设置
    if Path('run_app.py').exists():
        try:
            subprocess.run([sys.executable, 'run_app.py'], timeout=600)
            return True
        except subprocess.TimeoutExpired:
            print("⚠️ 设置向导超时")
        except Exception as e:
            print(f"⚠️ 设置向导启动失败: {e}")

    return False

def run_application(launch_file):
    """运行应用程序"""
    try:
        print(f"\n🚀 正在启动应用程序...")
        animate_loading("启动中", 2)

        # 运行应用程序
        subprocess.run([sys.executable, launch_file])

        print("\n✅ 应用程序已关闭")
        return True

    except KeyboardInterrupt:
        print("\n⚠️ 用户中断操作")
        return False
    except Exception as e:
        print(f"\n❌ 应用程序启动失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("\n" + "=" * 70)
    print("💡 帮助信息 | Help Information")
    print("=" * 70)
    print()
    print("如果遇到问题，请尝试以下解决方案:")
    print("If you encounter issues, try these solutions:")
    print()
    print("1. 🔧 重新配置 | Reconfigure:")
    print("   python setup_wizard.py")
    print()
    print("2. 🧪 测试配置 | Test Configuration:")
    print("   python test_config.py")
    print()
    print("3. ✅ 验证配置 | Validate Configuration:")
    print("   python config_validator.py")
    print()
    print("4. 📋 查看详细说明 | View Documentation:")
    print("   查看SETUP_SUMMARY.md文件")
    print()
    print("5. 🆘 获取更多帮助 | Get More Help:")
    print("   GitHub: https://github.com/Hacker0458/managebac-assignment-checker")
    print()

def wait_for_key():
    """等待用户按键"""
    try:
        input("\n按Enter键继续... | Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n👋 再见！")
        sys.exit(0)

def main():
    """主函数"""
    while True:
        try:
            print_banner()

            print("🔍 正在检查系统环境...")
            time.sleep(1)

            # 1. 检查Python版本
            if not check_python_version():
                print("\n❌ Python版本检查失败，请升级Python版本")
                wait_for_key()
                continue

            # 2. 检查文件
            launch_file = check_files()
            if not launch_file:
                print("\n❌ 系统文件检查失败，请重新安装")
                show_help()
                wait_for_key()
                continue

            # 3. 检查配置
            config_ok = check_config()

            if not config_ok:
                print("\n🎯 需要进行首次设置")
                print("   This is your first time running the application.")
                print("   Let's set it up!")

                setup_success = run_setup()
                if setup_success:
                    print("\n✅ 设置完成！正在重新检查...")
                    time.sleep(2)
                    continue
                else:
                    print("\n❌ 设置失败")
                    show_help()
                    wait_for_key()
                    continue

            # 4. 启动应用程序
            print("\n🎉 一切准备就绪！")
            print("   Everything is ready!")
            time.sleep(1)

            success = run_application(launch_file)

            if success:
                print("\n🎯 感谢使用ManageBac作业检查器！")
                print("   Thank you for using ManageBac Assignment Checker!")
            else:
                print("\n⚠️ 应用程序遇到问题")
                show_help()

            # 询问是否再次运行
            print("\n" + "=" * 70)
            try:
                again = input("是否再次运行？(y/n) | Run again? (y/n): ").strip().lower()
                if again not in ['y', 'yes', '是', '1']:
                    break
            except KeyboardInterrupt:
                break

        except KeyboardInterrupt:
            print("\n👋 用户退出")
            break
        except Exception as e:
            print(f"\n❌ 意外错误: {e}")
            show_help()
            wait_for_key()

    print("\n👋 再见！| Goodbye!")

if __name__ == "__main__":
    main()