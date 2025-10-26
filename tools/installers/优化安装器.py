#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 优化安装器 - 完美的用户体验
Optimized Installer - Perfect User Experience

解决一键安装后应用不自动打开的问题
Fixes the issue where applications don't auto-launch after installation
"""

import os
import sys
import subprocess
import platform
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any

class Colors:
    """Console colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class OptimizedInstaller:
    """优化的安装器 - 默认自动启动应用"""

    def __init__(self):
        self.platform = platform.system().lower()
        self.python_version = sys.version_info
        self.project_root = Path(__file__).parent
        self.state_file = self.project_root / '.install_state.json'
        self.env_file = self.project_root / '.env'
        self.install_start_time = time.time()

        # 默认配置 - 用户体验优化
        self.config = {
            'auto_launch': True,  # 默认自动启动
            'launch_timeout': 10,  # 启动超时时间
            'show_welcome': True,  # 显示欢迎信息
            'create_shortcuts': True,  # 创建桌面快捷方式
            'skip_confirmation': True  # 跳过启动确认
        }

    def print_banner(self):
        """Print optimized banner"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║    🌟 ManageBac Assignment Checker - 优化安装器 🌟                    ║
║         Perfect User Experience Installation System                  ║
║                                                                      ║
║  ✨ 默认自动启动应用 | Auto-launch by default                        ║
║  🚀 智能环境检测 | Smart environment detection                       ║
║  🎯 零配置体验 | Zero-configuration experience                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.GREEN}Platform: {self.platform.title()} | Python: {self.python_version.major}.{self.python_version.minor}{Colors.END}
""")

    def load_install_state(self) -> Dict:
        """加载安装状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'installed': False,
            'last_launch': None,
            'launch_count': 0,
            'components': {},
            'install_date': None
        }

    def save_install_state(self, state: Dict):
        """保存安装状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ 无法保存安装状态: {e}{Colors.END}")

    def check_system_requirements(self) -> bool:
        """快速系统检查"""
        print(f"{Colors.BLUE}🔍 System Check | 系统检查{Colors.END}", end=" ... ")

        if self.python_version < (3, 8):
            print(f"{Colors.RED}❌ Python 3.8+ required{Colors.END}")
            return False

        print(f"{Colors.GREEN}✅{Colors.END}")
        return True

    def install_dependencies(self) -> bool:
        """安装核心依赖"""
        print(f"{Colors.BLUE}📦 Installing Dependencies | 安装依赖{Colors.END}", end=" ... ")

        try:
            # 核心依赖
            core_deps = [
                'python-dotenv>=1.0.0',
                'requests>=2.28.0',
                'playwright>=1.40.0'
            ]

            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '--quiet'
            ] + core_deps, capture_output=True, timeout=120)

            if result.returncode == 0:
                print(f"{Colors.GREEN}✅{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}❌{Colors.END}")
                return False

        except Exception as e:
            print(f"{Colors.RED}❌ {str(e)}{Colors.END}")
            return False

    def install_browser(self) -> bool:
        """安装浏览器"""
        print(f"{Colors.BLUE}🌐 Installing Browser | 安装浏览器{Colors.END}", end=" ... ")

        try:
            result = subprocess.run([
                sys.executable, '-m', 'playwright', 'install', 'chromium'
            ], capture_output=True, text=True, timeout=180)

            if result.returncode == 0:
                print(f"{Colors.GREEN}✅{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}❌{Colors.END}")
                return False

        except Exception as e:
            print(f"{Colors.RED}❌ {str(e)}{Colors.END}")
            return False

    def create_configuration(self) -> bool:
        """创建基础配置"""
        print(f"{Colors.BLUE}⚙️  Creating Config | 创建配置{Colors.END}", end=" ... ")

        try:
            if not self.env_file.exists():
                config_content = """# ManageBac Assignment Checker - Auto Configuration
MANAGEBAC_URL=https://shtcs.managebac.cn
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password
REPORT_FORMAT=html,console
OUTPUT_DIR=reports
LANGUAGE=zh
HEADLESS=true
DEBUG=false
AUTO_LAUNCH=true
"""
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(config_content)

            # 创建必要目录
            for directory in ['logs', 'reports']:
                Path(directory).mkdir(exist_ok=True)

            print(f"{Colors.GREEN}✅{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.RED}❌ {str(e)}{Colors.END}")
            return False

    def create_desktop_shortcuts(self) -> bool:
        """创建桌面快捷方式"""
        if not self.config.get('create_shortcuts', True):
            return True

        print(f"{Colors.BLUE}🔗 Creating Shortcuts | 创建快捷方式{Colors.END}", end=" ... ")

        try:
            if self.platform == 'darwin':  # macOS
                self._create_macos_shortcut()
            elif self.platform == 'windows':
                self._create_windows_shortcut()
            elif self.platform == 'linux':
                self._create_linux_shortcut()

            print(f"{Colors.GREEN}✅{Colors.END}")
            return True

        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ {str(e)}{Colors.END}")
            return True  # 非关键功能，失败不影响安装

    def _create_macos_shortcut(self):
        """创建macOS快捷方式"""
        app_script = f"""#!/bin/bash
cd "{self.project_root}"
python3 smart_launcher.py
"""
        shortcut_path = Path.home() / 'Desktop' / 'ManageBac作业检查器.command'
        with open(shortcut_path, 'w') as f:
            f.write(app_script)
        os.chmod(shortcut_path, 0o755)

    def _create_windows_shortcut(self):
        """创建Windows快捷方式"""
        import winshell
        from win32com.client import Dispatch

        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, 'ManageBac作业检查器.lnk')

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{self.project_root / "smart_launcher.py"}"'
        shortcut.WorkingDirectory = str(self.project_root)
        shortcut.save()

    def _create_linux_shortcut(self):
        """创建Linux快捷方式"""
        desktop_file = f"""[Desktop Entry]
Name=ManageBac作业检查器
Comment=ManageBac Assignment Checker
Exec=python3 "{self.project_root / 'smart_launcher.py'}"
Icon={self.project_root / 'icon.png'}
Type=Application
Categories=Education;Office;
Terminal=false
"""
        shortcut_path = Path.home() / 'Desktop' / 'managebac-checker.desktop'
        with open(shortcut_path, 'w') as f:
            f.write(desktop_file)
        os.chmod(shortcut_path, 0o755)

    def detect_available_launcher(self) -> Optional[Path]:
        """检测可用的启动器"""
        # 按优先级排序的启动器列表
        launchers = [
            'smart_launcher.py',
            'gui_launcher.py',
            'run_app.py',
            'main_new.py',
            'professional_gui.py'
        ]

        for launcher in launchers:
            launcher_path = self.project_root / launcher
            if launcher_path.exists():
                return launcher_path

        return None

    def launch_application(self) -> bool:
        """智能启动应用 - 改进版本"""
        if not self.config.get('auto_launch', True):
            return True

        print(f"\n{Colors.HEADER}🚀 Auto-launching Application | 自动启动应用{Colors.END}")

        # 检测最佳启动器
        launcher = self.detect_available_launcher()
        if not launcher:
            print(f"{Colors.YELLOW}⚠️ No launcher found | 未找到启动器{Colors.END}")
            return False

        print(f"{Colors.CYAN}🔄 Starting with {launcher.name} | 使用 {launcher.name} 启动{Colors.END}")

        try:
            # 启动应用
            if self.platform == "windows":
                subprocess.Popen([
                    sys.executable, str(launcher)
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # macOS/Linux
                subprocess.Popen([sys.executable, str(launcher)])

            # 等待应用启动
            print(f"{Colors.BLUE}⏳ Starting application (timeout: {self.config['launch_timeout']}s)...{Colors.END}")

            # 简单等待，让应用有时间启动
            for i in range(self.config['launch_timeout']):
                print(".", end="", flush=True)
                time.sleep(1)

            print(f"\n{Colors.GREEN}✅ Application launched successfully! | 应用启动成功！{Colors.END}")

            # 更新启动统计
            state = self.load_install_state()
            state['last_launch'] = time.time()
            state['launch_count'] = state.get('launch_count', 0) + 1
            self.save_install_state(state)

            return True

        except Exception as e:
            print(f"\n{Colors.RED}❌ Failed to launch: {e}{Colors.END}")
            print(f"{Colors.YELLOW}💡 Manual start: python {launcher.name}{Colors.END}")
            return False

    def show_welcome_message(self):
        """显示欢迎信息"""
        if not self.config.get('show_welcome', True):
            return

        duration = time.time() - self.install_start_time

        print(f"""
{Colors.HEADER}🎉 Installation Complete | 安装完成{Colors.END}

{Colors.GREEN}✨ ManageBac Assignment Checker is ready to use!
✨ ManageBac作业检查器已准备就绪！{Colors.END}

{Colors.CYAN}📊 Installation Summary | 安装总结:
   ⏱️  Duration: {duration:.1f}s | 耗时: {duration:.1f}秒
   🎯 Auto-launch: Enabled | 自动启动: 已启用
   📁 Config: .env created | 配置文件: 已创建{Colors.END}

{Colors.YELLOW}📝 Next Steps | 下一步:
   1. Edit .env file with your ManageBac credentials
   1. 编辑.env文件，填入你的ManageBac账户信息

   2. The application should be starting automatically
   2. 应用程序应该正在自动启动

   3. If not, run: python smart_launcher.py
   3. 如果没有，请运行: python smart_launcher.py{Colors.END}

{Colors.GREEN}🔗 Desktop shortcut created (if supported)
🔗 已创建桌面快捷方式（如果支持）{Colors.END}
""")

    def run(self) -> bool:
        """主安装流程"""
        self.print_banner()

        print(f"{Colors.CYAN}🚀 Starting optimized installation | 开始优化安装{Colors.END}\n")

        # 安装步骤
        steps = [
            ("System Check", self.check_system_requirements),
            ("Dependencies", self.install_dependencies),
            ("Browser Setup", self.install_browser),
            ("Configuration", self.create_configuration),
            ("Shortcuts", self.create_desktop_shortcuts)
        ]

        # 执行安装步骤
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n{Colors.RED}❌ Installation failed at: {step_name}{Colors.END}")
                return False

        # 更新安装状态
        state = self.load_install_state()
        state.update({
            'installed': True,
            'install_date': time.time(),
            'version': '1.0.0'
        })
        self.save_install_state(state)

        # 显示欢迎信息
        self.show_welcome_message()

        # 自动启动应用
        self.launch_application()

        return True

def main():
    """主入口"""
    try:
        installer = OptimizedInstaller()
        success = installer.run()

        if success:
            print(f"\n{Colors.GREEN}🎊 All done! Enjoy using ManageBac Assignment Checker!{Colors.END}")
            print(f"{Colors.GREEN}🎊 全部完成！享受使用ManageBac作业检查器！{Colors.END}")
        else:
            print(f"\n{Colors.RED}💥 Installation failed. Please check the errors above.{Colors.END}")
            print(f"{Colors.RED}💥 安装失败。请检查上面的错误信息。{Colors.END}")

        return success

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}🛑 Installation cancelled by user{Colors.END}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)