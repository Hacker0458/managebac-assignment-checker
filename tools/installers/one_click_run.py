#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ManageBac Assignment Checker - 终极一键运行脚本
🎯 ManageBac作业检查器 - 终极一键运行脚本

专为小白用户设计的零配置启动脚本，完全自动化处理所有步骤。
Zero-configuration startup script designed for novice users, fully automated handling of all steps.
"""

import os
import sys
import time
import platform
import subprocess
from pathlib import Path

# 确保正确的编码
if sys.stdout.encoding != 'utf-8':
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

class Colors:
    """终端颜色常量"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class OneClickRunner:
    """一键运行器 - 完全自动化的应用程序启动"""

    def __init__(self):
        self.project_path = Path(__file__).parent.absolute()
        self.system = platform.system()
        self.python_cmd = self.find_python()

    def find_python(self):
        """查找Python命令"""
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run([cmd, '--version'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and 'Python 3' in result.stdout:
                    return cmd
            except:
                continue
        return 'python3'  # 默认使用python3

    def print_banner(self):
        """显示欢迎横幅"""
        print(f"{Colors.PURPLE}{'=' * 80}{Colors.END}")
        print(f"{Colors.PURPLE}{Colors.BOLD}🎯 ManageBac Assignment Checker - 一键启动{Colors.END}")
        print(f"{Colors.PURPLE}🎯 ManageBac作业检查器 - 一键启动{Colors.END}")
        print(f"{Colors.PURPLE}{'=' * 80}{Colors.END}")
        print(f"{Colors.CYAN}专为小白用户设计的零配置启动脚本{Colors.END}")
        print(f"{Colors.CYAN}Zero-configuration startup script for novice users{Colors.END}")
        print(f"{Colors.PURPLE}{'=' * 80}{Colors.END}")
        print()

    def animate_loading(self, text, duration=3):
        """显示加载动画"""
        animation = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            print(f"\r{Colors.CYAN}{text} {animation[i % len(animation)]}{Colors.END}",
                  end="", flush=True)
            time.sleep(0.1)
            i += 1
        print(f"\r{Colors.GREEN}{text} ✅{Colors.END}", flush=True)

    def check_python_version(self):
        """检查Python版本"""
        try:
            result = subprocess.run([self.python_cmd, '--version'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.strip()
                print(f"{Colors.GREEN}✅ {version_line} 检测完成{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}❌ Python版本检测失败{Colors.END}")
                return False
        except Exception as e:
            print(f"{Colors.RED}❌ Python检测错误: {e}{Colors.END}")
            return False

    def check_dependencies(self):
        """检查必要依赖"""
        print(f"{Colors.BLUE}🔍 检查项目依赖...{Colors.END}")

        required_files = [
            'smart_launcher.py',
            'run_app.py',
            'gui_launcher.py',
            'main_new.py',
            'setup_wizard.py'
        ]

        found_files = []
        for file in required_files:
            if (self.project_path / file).exists():
                found_files.append(file)
                print(f"{Colors.GREEN}   ✅ {file}{Colors.END}")

        if not found_files:
            print(f"{Colors.RED}❌ 未找到任何启动文件{Colors.END}")
            return False

        print(f"{Colors.GREEN}✅ 找到 {len(found_files)} 个启动文件{Colors.END}")
        return True

    def check_configuration(self):
        """检查配置状态"""
        print(f"{Colors.BLUE}🔧 检查配置状态...{Colors.END}")

        env_file = self.project_path / '.env'

        if not env_file.exists():
            print(f"{Colors.YELLOW}⚠️ 配置文件不存在，需要首次配置{Colors.END}")
            return False

        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查关键配置
            required_configs = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
            missing = []

            for config in required_configs:
                if config not in content:
                    missing.append(config)

            if missing:
                print(f"{Colors.YELLOW}⚠️ 配置不完整，缺少: {', '.join(missing)}{Colors.END}")
                return False

            # 检查占位符
            placeholders = ['your.email@example.com', 'your_password', 'your-school.managebac.cn']
            for placeholder in placeholders:
                if placeholder in content:
                    print(f"{Colors.YELLOW}⚠️ 配置包含占位符，需要填写真实信息{Colors.END}")
                    return False

            print(f"{Colors.GREEN}✅ 配置文件检查通过{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}❌ 配置文件读取错误: {e}{Colors.END}")
            return False

    def run_automated_setup(self):
        """运行自动化设置"""
        print(f"\n{Colors.CYAN}🧙‍♂️ 启动自动配置向导...{Colors.END}")
        print(f"{Colors.WHITE}我们将引导您完成快速配置{Colors.END}")
        print()

        # 尝试运行设置向导
        setup_files = ['setup_wizard.py', 'first_run_setup.py']

        for setup_file in setup_files:
            setup_path = self.project_path / setup_file
            if setup_path.exists():
                try:
                    print(f"{Colors.BLUE}📋 使用 {setup_file} 进行配置...{Colors.END}")

                    # 运行设置向导
                    result = subprocess.run([self.python_cmd, str(setup_path)],
                                          cwd=self.project_path)

                    if result.returncode == 0:
                        print(f"\n{Colors.GREEN}✅ 配置完成！{Colors.END}")
                        return True
                    else:
                        print(f"\n{Colors.YELLOW}⚠️ {setup_file} 配置未完成{Colors.END}")
                        continue

                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️ {setup_file} 配置失败: {e}{Colors.END}")
                    continue

        # 如果所有设置向导都失败，提供简单的交互式配置
        print(f"\n{Colors.CYAN}📝 简易配置模式{Colors.END}")
        return self.simple_interactive_setup()

    def simple_interactive_setup(self):
        """简单交互式配置"""
        try:
            print(f"\n{Colors.GREEN}请输入以下信息来完成配置：{Colors.END}")
            print(f"{Colors.WHITE}(所有信息都会保存到本地，不会上传){Colors.END}")
            print()

            # 获取学校URL
            print(f"{Colors.BLUE}🏫 学校ManageBac网址:{Colors.END}")
            print(f"{Colors.WHITE}   例如: https://shtcs.managebac.cn{Colors.END}")
            url = input(f"{Colors.CYAN}请输入 [直接按回车使用示例]: {Colors.END}").strip()
            if not url:
                url = "https://shtcs.managebac.cn"

            # 获取邮箱
            print(f"\n{Colors.BLUE}📧 您的邮箱地址:{Colors.END}")
            email = input(f"{Colors.CYAN}请输入: {Colors.END}").strip()
            if not email:
                print(f"{Colors.RED}❌ 邮箱不能为空{Colors.END}")
                return False

            # 获取密码
            print(f"\n{Colors.BLUE}🔐 您的密码:{Colors.END}")
            password = input(f"{Colors.CYAN}请输入: {Colors.END}").strip()
            if not password:
                print(f"{Colors.RED}❌ 密码不能为空{Colors.END}")
                return False

            # 创建配置文件
            config_content = f"""# ManageBac Assignment Checker Configuration
MANAGEBAC_EMAIL={email}
MANAGEBAC_PASSWORD={password}
MANAGEBAC_URL={url}

# Report Settings
REPORT_FORMAT=console,html
OUTPUT_DIR=./reports
FETCH_DETAILS=true
DETAILS_LIMIT=50

# Browser Settings
HEADLESS=true
BROWSER_TIMEOUT=30000

# Debug Settings
DEBUG=false
LOG_LEVEL=INFO
LOG_FILE=logs/managebac_checker.log

# UI Settings
HTML_THEME=auto
INCLUDE_CHARTS=true

# AI Settings (disabled by default)
AI_ENABLED=false
OPENAI_API_KEY=
AI_MODEL=gpt-4

# Language Settings
LANGUAGE=zh
"""

            with open(self.project_path / '.env', 'w', encoding='utf-8') as f:
                f.write(config_content)

            print(f"\n{Colors.GREEN}✅ 配置文件创建成功！{Colors.END}")
            return True

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠️ 用户取消配置{Colors.END}")
            return False
        except Exception as e:
            print(f"\n{Colors.RED}❌ 配置失败: {e}{Colors.END}")
            return False

    def launch_application(self):
        """启动应用程序"""
        print(f"\n{Colors.GREEN}🚀 启动应用程序...{Colors.END}")

        # 按优先级尝试不同的启动器
        launchers = [
            ('smart_launcher.py', '智能启动器'),
            ('run_app.py', '应用启动器'),
            ('gui_launcher.py', 'GUI启动器'),
            ('main_new.py', '主程序')
        ]

        for launcher, description in launchers:
            launcher_path = self.project_path / launcher
            if launcher_path.exists():
                try:
                    print(f"{Colors.BLUE}📱 使用{description}启动...{Colors.END}")

                    # 启动应用程序
                    result = subprocess.run([self.python_cmd, str(launcher_path)],
                                          cwd=self.project_path)

                    print(f"\n{Colors.GREEN}✅ 应用程序运行完成{Colors.END}")
                    return True

                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}⚠️ 用户退出应用程序{Colors.END}")
                    return True
                except Exception as e:
                    print(f"{Colors.YELLOW}⚠️ {description}启动失败: {e}{Colors.END}")
                    continue

        print(f"{Colors.RED}❌ 所有启动器都失败了{Colors.END}")
        return False

    def show_success_message(self):
        """显示成功信息"""
        print(f"\n{Colors.GREEN}{'=' * 80}{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ManageBac作业检查器运行成功！{Colors.END}")
        print(f"{Colors.GREEN}🎉 ManageBac Assignment Checker ran successfully!{Colors.END}")
        print(f"{Colors.GREEN}{'=' * 80}{Colors.END}")
        print()
        print(f"{Colors.CYAN}📋 下次启动方法：{Colors.END}")
        print(f"{Colors.WHITE}   1. 双击运行: one_click_run.py{Colors.END}")
        print(f"{Colors.WHITE}   2. 命令行运行: python one_click_run.py{Colors.END}")
        print(f"{Colors.WHITE}   3. 快捷脚本: ./quick_start.sh{Colors.END}")
        print()
        print(f"{Colors.PURPLE}感谢使用ManageBac作业检查器！{Colors.END}")

    def run(self):
        """主运行方法"""
        try:
            self.print_banner()

            # 第1步：检查Python
            self.animate_loading("检查Python环境", 2)
            if not self.check_python_version():
                print(f"{Colors.RED}❌ Python环境检查失败，请确保Python 3.8+已安装{Colors.END}")
                return False

            # 第2步：检查依赖
            self.animate_loading("检查项目文件", 2)
            if not self.check_dependencies():
                print(f"{Colors.RED}❌ 项目文件不完整，请重新下载{Colors.END}")
                return False

            # 第3步：检查配置
            self.animate_loading("检查配置状态", 2)
            config_ok = self.check_configuration()

            if not config_ok:
                print(f"\n{Colors.YELLOW}🔧 需要进行配置设置{Colors.END}")
                print(f"{Colors.WHITE}首次使用需要配置您的ManageBac账户信息{Colors.END}")

                if not self.run_automated_setup():
                    print(f"{Colors.RED}❌ 配置失败，无法启动应用程序{Colors.END}")
                    return False

            # 第4步：启动应用程序
            self.animate_loading("准备启动应用程序", 1)
            success = self.launch_application()

            if success:
                self.show_success_message()
            else:
                print(f"{Colors.RED}❌ 应用程序启动失败{Colors.END}")

            return success

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 用户退出{Colors.END}")
            return True
        except Exception as e:
            print(f"\n{Colors.RED}❌ 运行出错: {e}{Colors.END}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主函数"""
    runner = OneClickRunner()
    success = runner.run()

    # 等待用户按键退出
    try:
        input(f"\n{Colors.CYAN}按回车键退出...{Colors.END}")
    except KeyboardInterrupt:
        pass

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())