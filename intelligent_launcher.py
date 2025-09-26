#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Intelligent Launcher | 智能启动器
智能检测运行环境和应用状态，提供最佳的启动体验
Intelligently detects runtime environment and app status for optimal launch experience
"""

import os
import sys
import subprocess
import platform
import time
import json
import psutil
import signal
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class Colors:
    """Terminal colors"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class IntelligentLauncher:
    """智能启动器 - 提供完美的用户体验"""

    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.platform_name = platform.system().lower()
        self.state_file = self.project_root / '.app_state.json'
        self.config_file = self.project_root / '.env'

        # 启动选项
        self.launch_options = {
            'timeout': 15,  # 启动超时时间
            'retry_attempts': 3,  # 重试次数
            'wait_for_ready': True,  # 等待应用就绪
            'kill_existing': False,  # 是否杀死现有进程
            'show_progress': True  # 显示启动进度
        }

    def print_header(self):
        """打印启动器头部信息"""
        print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       🧠 ManageBac Assignment Checker - Intelligent Launcher       ║
║            🧠 ManageBac作业检查器 - 智能启动器                       ║
║                                                                      ║
║    🎯 Smart environment detection | 智能环境检测                     ║
║    🚀 Optimal launch experience | 最佳启动体验                       ║
║    🔄 Auto-recovery on failure | 失败时自动恢复                      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}
""")

    def load_app_state(self) -> Dict:
        """加载应用状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        return {
            'last_launch': None,
            'successful_launches': 0,
            'failed_launches': 0,
            'preferred_launcher': None,
            'running_processes': []
        }

    def save_app_state(self, state: Dict):
        """保存应用状态"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ 无法保存应用状态: {e}{Colors.END}")

    def check_environment(self) -> Dict:
        """检查运行环境"""
        env_info = {
            'python_version': sys.version_info,
            'platform': self.platform_name,
            'has_display': self._check_display(),
            'has_tkinter': self._check_tkinter(),
            'config_exists': self.config_file.exists(),
            'dependencies_ok': self._check_dependencies()
        }

        return env_info

    def _check_display(self) -> bool:
        """检查显示环境"""
        try:
            if self.platform_name == "darwin":  # macOS
                result = subprocess.run(['launchctl', 'managername'],
                                      capture_output=True, text=True, timeout=5)
                return 'Aqua' in result.stdout
            elif self.platform_name == "linux":
                return 'DISPLAY' in os.environ and os.environ.get('DISPLAY') != ''
            elif self.platform_name == "windows":
                return True  # Windows 几乎总是有显示
            return False
        except:
            return False

    def _check_tkinter(self) -> bool:
        """检查tkinter可用性"""
        try:
            import tkinter
            return True
        except ImportError:
            return False

    def _check_dependencies(self) -> bool:
        """检查核心依赖"""
        required_modules = ['playwright', 'requests', 'dotenv']
        for module in required_modules:
            try:
                __import__(module.replace('-', '_'))
            except ImportError:
                return False
        return True

    def find_running_instances(self) -> List[Dict]:
        """查找正在运行的应用实例"""
        running_instances = []

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline'] or []
                cmdline_str = ' '.join(cmdline)

                # 检查是否是我们的应用
                if any(launcher in cmdline_str for launcher in [
                    'smart_launcher.py', 'gui_launcher.py', 'run_app.py',
                    'main_new.py', 'professional_gui.py'
                ]):
                    running_instances.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline_str,
                        'create_time': proc.create_time()
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return running_instances

    def get_available_launchers(self) -> List[Dict]:
        """获取可用的启动器"""
        launchers = [
            {
                'file': 'professional_gui.py',
                'name': 'Professional GUI',
                'description': '专业GUI界面',
                'priority': 1,
                'requires_display': True,
                'requires_tkinter': True
            },
            {
                'file': 'smart_launcher.py',
                'name': 'Smart Launcher',
                'description': '智能启动器',
                'priority': 2,
                'requires_display': True,
                'requires_tkinter': True
            },
            {
                'file': 'gui_launcher.py',
                'name': 'GUI Launcher',
                'description': 'GUI启动器',
                'priority': 3,
                'requires_display': True,
                'requires_tkinter': True
            },
            {
                'file': 'run_app.py',
                'name': 'App Runner',
                'description': '应用运行器',
                'priority': 4,
                'requires_display': False,
                'requires_tkinter': False
            },
            {
                'file': 'main_new.py',
                'name': 'Main Application',
                'description': '主应用程序',
                'priority': 5,
                'requires_display': False,
                'requires_tkinter': False
            }
        ]

        # 过滤出存在的启动器
        available = []
        env_info = self.check_environment()

        for launcher in launchers:
            launcher_path = self.project_root / launcher['file']
            if launcher_path.exists():
                # 检查环境要求
                if launcher.get('requires_display', False) and not env_info['has_display']:
                    continue
                if launcher.get('requires_tkinter', False) and not env_info['has_tkinter']:
                    continue

                launcher['path'] = launcher_path
                launcher['available'] = True
                available.append(launcher)

        return sorted(available, key=lambda x: x['priority'])

    def select_best_launcher(self, available_launchers: List[Dict], app_state: Dict) -> Optional[Dict]:
        """选择最佳启动器"""
        if not available_launchers:
            return None

        # 如果有首选启动器且可用，使用它
        preferred = app_state.get('preferred_launcher')
        if preferred:
            for launcher in available_launchers:
                if launcher['file'] == preferred:
                    return launcher

        # 否则使用优先级最高的
        return available_launchers[0]

    def launch_with_progress(self, launcher: Dict) -> bool:
        """带进度显示的启动"""
        print(f"{Colors.CYAN}🚀 Starting {launcher['name']} | 启动 {launcher['description']}{Colors.END}")

        if self.launch_options['show_progress']:
            print(f"{Colors.BLUE}⏳ Initializing", end="")

        try:
            # 启动应用程序
            if self.platform_name == "windows":
                process = subprocess.Popen([
                    sys.executable, str(launcher['path'])
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                process = subprocess.Popen([
                    sys.executable, str(launcher['path'])
                ])

            # 显示启动进度
            if self.launch_options['show_progress']:
                for i in range(self.launch_options['timeout']):
                    print(".", end="", flush=True)
                    time.sleep(1)

                    # 检查进程是否还在运行
                    if process.poll() is not None:
                        print(f" {Colors.RED}✗{Colors.END}")
                        return False

                print(f" {Colors.GREEN}✓{Colors.END}")

            print(f"{Colors.GREEN}✅ {launcher['name']} started successfully!{Colors.END}")
            print(f"{Colors.GREEN}✅ {launcher['description']} 启动成功！{Colors.END}")

            return True

        except Exception as e:
            if self.launch_options['show_progress']:
                print(f" {Colors.RED}✗{Colors.END}")
            print(f"{Colors.RED}❌ Failed to start {launcher['name']}: {e}{Colors.END}")
            return False

    def handle_existing_instances(self, running_instances: List[Dict]) -> bool:
        """处理现有实例"""
        if not running_instances:
            return True

        print(f"{Colors.YELLOW}📋 Found {len(running_instances)} running instance(s):"){Colors.END}
        for i, instance in enumerate(running_instances, 1):
            uptime = time.time() - instance['create_time']
            print(f"   {i}. PID {instance['pid']} (running for {uptime/60:.1f}m)")

        if self.launch_options['kill_existing']:
            print(f"{Colors.YELLOW}🔄 Terminating existing instances...{Colors.END}")
            for instance in running_instances:
                try:
                    os.kill(instance['pid'], signal.SIGTERM)
                    time.sleep(1)
                    print(f"✅ Terminated PID {instance['pid']}")
                except:
                    print(f"❌ Failed to terminate PID {instance['pid']}")
            return True
        else:
            print(f"{Colors.CYAN}💡 Applications are already running. Use --kill-existing to restart.{Colors.END}")
            print(f"{Colors.CYAN}💡 应用程序已在运行。使用 --kill-existing 重新启动。{Colors.END}")
            return False

    def show_launch_summary(self, success: bool, launcher: Optional[Dict], app_state: Dict):
        """显示启动总结"""
        if success and launcher:
            app_state['successful_launches'] += 1
            app_state['last_launch'] = time.time()
            app_state['preferred_launcher'] = launcher['file']

            print(f"""
{Colors.GREEN}🎉 Launch Successful | 启动成功{Colors.END}

{Colors.CYAN}📊 Session Info:
   🚀 Launcher: {launcher['name']}
   📅 Total successful launches: {app_state['successful_launches']}
   ⏱️  Launch time: {time.strftime('%H:%M:%S')}

{Colors.YELLOW}💡 Tips:
   • Application is starting in the background
   • Check your taskbar/dock for the application window
   • If needed, you can run this launcher again

   • 应用程序正在后台启动
   • 检查任务栏/程序坞中的应用程序窗口
   • 如需要，您可以再次运行此启动器{Colors.END}""")
        else:
            app_state['failed_launches'] += 1
            print(f"""
{Colors.RED}❌ Launch Failed | 启动失败{Colors.END}

{Colors.YELLOW}🔧 Troubleshooting | 故障排除:
   1. Check if dependencies are installed: pip install -r requirements.txt
   1. 检查是否安装了依赖: pip install -r requirements.txt

   2. Run the installation wizard: python ultimate_installer.py
   2. 运行安装向导: python ultimate_installer.py

   3. Manual start: python main_new.py --interactive
   3. 手动启动: python main_new.py --interactive{Colors.END}""")

    def run(self) -> bool:
        """主运行方法"""
        self.print_header()

        # 加载应用状态
        app_state = self.load_app_state()

        # 检查环境
        env_info = self.check_environment()
        print(f"{Colors.BLUE}🔍 Environment Check | 环境检查{Colors.END}")
        print(f"   ✅ Python {env_info['python_version'].major}.{env_info['python_version'].minor}")
        print(f"   {'✅' if env_info['has_display'] else '❌'} Display available")
        print(f"   {'✅' if env_info['has_tkinter'] else '❌'} Tkinter available")
        print(f"   {'✅' if env_info['config_exists'] else '❌'} Configuration file")
        print(f"   {'✅' if env_info['dependencies_ok'] else '❌'} Dependencies")

        if not env_info['dependencies_ok']:
            print(f"{Colors.YELLOW}⚠️ Missing dependencies. Run: python ultimate_installer.py{Colors.END}")

        # 查找运行实例
        running_instances = self.find_running_instances()
        if not self.handle_existing_instances(running_instances):
            return False

        # 获取可用启动器
        available_launchers = self.get_available_launchers()
        if not available_launchers:
            print(f"{Colors.RED}❌ No suitable launchers found{Colors.END}")
            print(f"{Colors.RED}❌ 找不到合适的启动器{Colors.END}")
            return False

        print(f"\n{Colors.BLUE}📋 Available launchers | 可用启动器:{Colors.END}")
        for launcher in available_launchers:
            print(f"   • {launcher['name']} - {launcher['description']}")

        # 选择最佳启动器
        best_launcher = self.select_best_launcher(available_launchers, app_state)
        if not best_launcher:
            return False

        print(f"\n{Colors.CYAN}🎯 Selected: {best_launcher['name']}{Colors.END}")

        # 启动应用
        success = False
        for attempt in range(self.launch_options['retry_attempts']):
            if attempt > 0:
                print(f"{Colors.YELLOW}🔄 Retry attempt {attempt + 1}/{self.launch_options['retry_attempts']}{Colors.END}")

            success = self.launch_with_progress(best_launcher)
            if success:
                break

            time.sleep(2)  # 等待重试

        # 保存状态并显示总结
        self.save_app_state(app_state)
        self.show_launch_summary(success, best_launcher if success else None, app_state)

        return success

def main():
    """主入口"""
    try:
        # 解析命令行参数
        if '--kill-existing' in sys.argv:
            launcher = IntelligentLauncher()
            launcher.launch_options['kill_existing'] = True
        else:
            launcher = IntelligentLauncher()

        success = launcher.run()
        return success

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🛑 Cancelled by user | 用户取消{Colors.END}")
        return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)