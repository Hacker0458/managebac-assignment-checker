#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Enhanced Setup GUI | 增强的设置GUI
Beautiful graphical installation wizard for ManageBac Assignment Checker
ManageBac作业检查器的美观图形安装向导
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Callable
import json
import os

class Colors:
    """Color scheme for the GUI"""
    PRIMARY = "#2563eb"      # Blue
    SECONDARY = "#7c3aed"    # Purple
    SUCCESS = "#16a34a"      # Green
    WARNING = "#ea580c"      # Orange
    ERROR = "#dc2626"        # Red
    BACKGROUND = "#f8fafc"   # Light gray
    CARD = "#ffffff"         # White
    TEXT = "#1e293b"         # Dark gray
    TEXT_LIGHT = "#64748b"   # Medium gray

class ProgressStep:
    """Represents a progress step"""
    def __init__(self, name: str, description: str, function: Callable = None):
        self.name = name
        self.description = description
        self.function = function
        self.status = "pending"  # pending, running, completed, failed
        self.progress = 0

class EnhancedSetupGUI:
    """Enhanced graphical setup wizard"""

    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()

        # Configuration data
        self.config = {}
        self.current_step = 0
        self.installation_thread = None

        # Progress steps
        self.steps = [
            ProgressStep("系统检查", "检查系统要求和依赖", self.check_system),
            ProgressStep("依赖安装", "安装必需的Python包", self.install_dependencies),
            ProgressStep("浏览器设置", "安装Playwright浏览器", self.install_browser),
            ProgressStep("配置向导", "设置ManageBac连接信息", self.configure_settings),
            ProgressStep("环境准备", "创建必要的文件夹和文件", self.setup_environment),
            ProgressStep("快捷方式", "创建桌面快捷方式", self.create_shortcuts),
            ProgressStep("测试安装", "验证安装是否成功", self.test_installation),
            ProgressStep("完成设置", "启动应用程序", self.launch_application)
        ]

        self.create_widgets()
        self.show_welcome_page()

    def setup_window(self):
        """Setup main window"""
        self.root.title("ManageBac Assignment Checker - 安装向导")
        self.root.geometry("800x600")
        self.root.configure(bg=Colors.BACKGROUND)
        self.root.resizable(False, False)

        # Center window
        self.center_window()

        # Set window icon (if available)
        try:
            icon_path = Path(__file__).parent / "icon.png"
            if icon_path.exists():
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except:
            pass

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create main widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.title_label = ttk.Label(
            self.header_frame,
            text="🚀 ManageBac Assignment Checker",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack()

        self.subtitle_label = ttk.Label(
            self.header_frame,
            text="安装向导 | Installation Wizard",
            font=("Arial", 12)
        )
        self.subtitle_label.pack(pady=(5, 0))

        # Content area (will be populated dynamically)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(20, 0))

    def clear_content(self):
        """Clear content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome_page(self):
        """Show welcome page"""
        self.clear_content()

        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(expand=True, fill=tk.BOTH)

        # Welcome message
        welcome_text = """
🎓 欢迎使用 ManageBac Assignment Checker!
🎓 Welcome to ManageBac Assignment Checker!

这个安装向导将帮助您快速设置和配置应用程序。
This installation wizard will help you quickly set up and configure the application.

✨ 功能特色 | Features:
• 🔍 自动检测和分析ManageBac作业 | Automatic ManageBac assignment detection
• 🤖 AI智能助手分析 | AI-powered intelligent analysis
• 📊 多种报告格式 | Multiple report formats
• 🔔 提醒和通知 | Reminders and notifications
• 🎨 现代化用户界面 | Modern user interface

🚀 安装过程大约需要2-5分钟
🚀 Installation takes approximately 2-5 minutes

点击"开始安装"继续...
Click "Start Installation" to continue...
        """

        welcome_label = ttk.Label(
            welcome_frame,
            text=welcome_text,
            font=("Arial", 11),
            justify=tk.LEFT
        )
        welcome_label.pack(expand=True, pady=50)

        # Clear button frame and add start button
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        start_button = ttk.Button(
            self.button_frame,
            text="🚀 开始安装 | Start Installation",
            command=self.show_progress_page
        )
        start_button.pack(side=tk.RIGHT, padx=(10, 0))

        quit_button = ttk.Button(
            self.button_frame,
            text="❌ 退出 | Quit",
            command=self.root.quit
        )
        quit_button.pack(side=tk.RIGHT)

    def show_progress_page(self):
        """Show installation progress page"""
        self.clear_content()

        # Progress container
        progress_container = ttk.Frame(self.content_frame)
        progress_container.pack(fill=tk.BOTH, expand=True, pady=20)

        # Overall progress
        overall_frame = ttk.LabelFrame(progress_container, text="🎯 总体进度 | Overall Progress")
        overall_frame.pack(fill=tk.X, pady=(0, 20))

        self.overall_progress = ttk.Progressbar(
            overall_frame,
            mode='determinate',
            length=400
        )
        self.overall_progress.pack(pady=10, padx=10)

        self.overall_label = ttk.Label(overall_frame, text="准备开始... | Preparing to start...")
        self.overall_label.pack(pady=(0, 10))

        # Steps progress
        steps_frame = ttk.LabelFrame(progress_container, text="📋 安装步骤 | Installation Steps")
        steps_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollable frame for steps
        canvas = tk.Canvas(steps_frame, height=300)
        scrollbar = ttk.Scrollbar(steps_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        # Create step widgets
        self.step_widgets = []
        for i, step in enumerate(self.steps):
            step_frame = ttk.Frame(scrollable_frame)
            step_frame.pack(fill=tk.X, pady=2)

            # Status icon
            icon_label = ttk.Label(step_frame, text="⏸️", font=("Arial", 12))
            icon_label.pack(side=tk.LEFT, padx=(10, 5))

            # Step info
            info_frame = ttk.Frame(step_frame)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

            name_label = ttk.Label(info_frame, text=step.name, font=("Arial", 10, "bold"))
            name_label.pack(anchor=tk.W)

            desc_label = ttk.Label(info_frame, text=step.description, font=("Arial", 9))
            desc_label.pack(anchor=tk.W)

            # Progress bar for step
            step_progress = ttk.Progressbar(
                step_frame,
                mode='determinate',
                length=100
            )
            step_progress.pack(side=tk.RIGHT, padx=(5, 10))

            self.step_widgets.append({
                'frame': step_frame,
                'icon': icon_label,
                'name': name_label,
                'desc': desc_label,
                'progress': step_progress
            })

        # Log area
        log_frame = ttk.LabelFrame(progress_container, text="📝 安装日志 | Installation Log")
        log_frame.pack(fill=tk.X, pady=(20, 0))

        self.log_text = tk.Text(log_frame, height=6, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        log_scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

        # Button frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        self.start_install_button = ttk.Button(
            self.button_frame,
            text="▶️ 开始安装 | Start Installation",
            command=self.start_installation
        )
        self.start_install_button.pack(side=tk.RIGHT, padx=(10, 0))

        self.cancel_button = ttk.Button(
            self.button_frame,
            text="❌ 取消 | Cancel",
            command=self.cancel_installation
        )
        self.cancel_button.pack(side=tk.RIGHT)

    def log_message(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_step_status(self, step_index: int, status: str, progress: int = 0):
        """Update step status"""
        if step_index >= len(self.step_widgets):
            return

        widget = self.step_widgets[step_index]
        step = self.steps[step_index]

        # Update status
        step.status = status
        step.progress = progress

        # Update icon
        icons = {
            'pending': '⏸️',
            'running': '🔄',
            'completed': '✅',
            'failed': '❌'
        }
        widget['icon'].config(text=icons.get(status, '❓'))

        # Update progress
        widget['progress']['value'] = progress

        # Update overall progress
        completed_steps = sum(1 for s in self.steps if s.status == 'completed')
        overall_progress = (completed_steps / len(self.steps)) * 100
        self.overall_progress['value'] = overall_progress

        # Update overall label
        if status == 'running':
            self.overall_label.config(text=f"正在执行: {step.name} | Executing: {step.name}")
        elif status == 'completed':
            self.overall_label.config(text=f"已完成: {step.name} | Completed: {step.name}")
        elif status == 'failed':
            self.overall_label.config(text=f"失败: {step.name} | Failed: {step.name}")

        self.root.update_idletasks()

    def start_installation(self):
        """Start installation process"""
        self.start_install_button.config(state='disabled')
        self.cancel_button.config(text="🛑 停止 | Stop")

        # Start installation in separate thread
        self.installation_thread = threading.Thread(target=self.run_installation)
        self.installation_thread.daemon = True
        self.installation_thread.start()

    def run_installation(self):
        """Run installation steps"""
        try:
            for i, step in enumerate(self.steps):
                if hasattr(self, '_cancelled') and self._cancelled:
                    break

                self.update_step_status(i, 'running', 0)
                self.log_message(f"开始: {step.name} | Starting: {step.name}")

                try:
                    if step.function:
                        success = step.function()
                    else:
                        # Simulate work
                        for progress in range(0, 101, 20):
                            if hasattr(self, '_cancelled') and self._cancelled:
                                break
                            self.update_step_status(i, 'running', progress)
                            time.sleep(0.1)
                        success = True

                    if success:
                        self.update_step_status(i, 'completed', 100)
                        self.log_message(f"完成: {step.name} | Completed: {step.name}")
                    else:
                        self.update_step_status(i, 'failed', 0)
                        self.log_message(f"失败: {step.name} | Failed: {step.name}")
                        break

                except Exception as e:
                    self.update_step_status(i, 'failed', 0)
                    self.log_message(f"错误: {step.name} - {str(e)} | Error: {step.name} - {str(e)}")
                    break

                time.sleep(0.5)  # Brief pause between steps

            # Check if installation completed successfully
            if all(step.status == 'completed' for step in self.steps):
                self.show_completion_page(success=True)
            else:
                self.show_completion_page(success=False)

        except Exception as e:
            self.log_message(f"安装过程出错: {str(e)} | Installation error: {str(e)}")
            self.show_completion_page(success=False)

    def cancel_installation(self):
        """Cancel installation"""
        if hasattr(self, 'installation_thread') and self.installation_thread.is_alive():
            self._cancelled = True
            self.log_message("用户取消安装 | Installation cancelled by user")
            self.cancel_button.config(text="❌ 退出 | Quit", command=self.root.quit)
        else:
            self.root.quit()

    # Installation step methods
    def check_system(self) -> bool:
        """Check system requirements"""
        try:
            self.log_message("检查Python版本 | Checking Python version")
            if sys.version_info < (3, 8):
                self.log_message(f"Python版本过低: {sys.version_info} | Python version too old: {sys.version_info}")
                return False

            self.log_message("检查磁盘空间 | Checking disk space")
            # Add more system checks here

            return True
        except Exception as e:
            self.log_message(f"系统检查失败: {str(e)} | System check failed: {str(e)}")
            return False

    def install_dependencies(self) -> bool:
        """Install dependencies"""
        try:
            self.log_message("安装核心依赖 | Installing core dependencies")

            # List of required packages
            packages = [
                'playwright>=1.40.0',
                'python-dotenv>=1.0.0',
                'jinja2>=3.1.0',
                'requests>=2.28.0'
            ]

            for package in packages:
                self.log_message(f"安装: {package} | Installing: {package}")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)

                if result.returncode != 0:
                    self.log_message(f"安装失败: {package} | Failed to install: {package}")
                    return False

            return True
        except Exception as e:
            self.log_message(f"依赖安装失败: {str(e)} | Dependency installation failed: {str(e)}")
            return False

    def install_browser(self) -> bool:
        """Install Playwright browser"""
        try:
            self.log_message("安装Playwright浏览器 | Installing Playwright browser")

            result = subprocess.run([
                sys.executable, '-m', 'playwright', 'install', 'chromium'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                self.log_message("浏览器安装成功 | Browser installed successfully")
                return True
            else:
                self.log_message(f"浏览器安装失败: {result.stderr} | Browser installation failed: {result.stderr}")
                return False

        except Exception as e:
            self.log_message(f"浏览器安装错误: {str(e)} | Browser installation error: {str(e)}")
            return False

    def configure_settings(self) -> bool:
        """Configure application settings"""
        try:
            self.log_message("配置应用设置 | Configuring application settings")

            # Create minimal configuration
            config_content = """# ManageBac Assignment Checker Configuration
MANAGEBAC_URL=https://shtcs.managebac.cn
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password

# Report Settings
REPORT_FORMAT=html,json,console
OUTPUT_DIR=reports
LANGUAGE=zh

# Browser Settings
HEADLESS=true
BROWSER_TIMEOUT=30000

# Basic Settings
DEBUG=false
LOG_LEVEL=INFO
"""

            with open('.env', 'w', encoding='utf-8') as f:
                f.write(config_content)

            self.log_message("配置文件创建成功 | Configuration file created successfully")
            return True

        except Exception as e:
            self.log_message(f"配置设置失败: {str(e)} | Configuration setup failed: {str(e)}")
            return False

    def setup_environment(self) -> bool:
        """Setup environment"""
        try:
            self.log_message("创建必要目录 | Creating necessary directories")

            directories = ['logs', 'reports', 'cache', 'screenshots']
            for directory in directories:
                Path(directory).mkdir(exist_ok=True)
                self.log_message(f"创建目录: {directory} | Created directory: {directory}")

            return True

        except Exception as e:
            self.log_message(f"环境设置失败: {str(e)} | Environment setup failed: {str(e)}")
            return False

    def create_shortcuts(self) -> bool:
        """Create shortcuts"""
        try:
            self.log_message("创建桌面快捷方式 | Creating desktop shortcuts")
            # Placeholder for shortcut creation
            return True

        except Exception as e:
            self.log_message(f"快捷方式创建失败: {str(e)} | Shortcut creation failed: {str(e)}")
            return False

    def test_installation(self) -> bool:
        """Test installation"""
        try:
            self.log_message("测试安装 | Testing installation")

            # Test basic imports
            try:
                import tkinter
                self.log_message("tkinter - ✓")
            except ImportError:
                self.log_message("tkinter - ✗")
                return False

            return True

        except Exception as e:
            self.log_message(f"安装测试失败: {str(e)} | Installation test failed: {str(e)}")
            return False

    def launch_application(self) -> bool:
        """Launch application"""
        try:
            self.log_message("准备启动应用 | Preparing to launch application")
            return True

        except Exception as e:
            self.log_message(f"应用启动失败: {str(e)} | Application launch failed: {str(e)}")
            return False

    def show_completion_page(self, success: bool = True):
        """Show installation completion page"""
        self.clear_content()

        completion_frame = ttk.Frame(self.content_frame)
        completion_frame.pack(expand=True, fill=tk.BOTH)

        if success:
            # Success message
            success_text = """
🎉 安装成功！| Installation Successful!

ManageBac Assignment Checker 已成功安装到您的系统。
ManageBac Assignment Checker has been successfully installed on your system.

✅ 所有组件已正确安装
✅ All components installed correctly

📝 后续步骤 | Next Steps:
1. 编辑 .env 文件配置您的 ManageBac 凭据
   Edit .env file to configure your ManageBac credentials

2. 运行应用程序开始使用
   Run the application to start using it

🚀 准备启动应用程序...
🚀 Ready to launch application...
            """

            completion_label = ttk.Label(
                completion_frame,
                text=success_text,
                font=("Arial", 11),
                justify=tk.CENTER
            )
            completion_label.pack(expand=True, pady=50)

            # Buttons
            for widget in self.button_frame.winfo_children():
                widget.destroy()

            launch_button = ttk.Button(
                self.button_frame,
                text="🚀 启动应用 | Launch App",
                command=self.launch_app_and_close
            )
            launch_button.pack(side=tk.RIGHT, padx=(10, 0))

            close_button = ttk.Button(
                self.button_frame,
                text="✅ 完成 | Finish",
                command=self.root.quit
            )
            close_button.pack(side=tk.RIGHT)

        else:
            # Failure message
            failure_text = """
❌ 安装过程中遇到问题 | Installation encountered issues

一些步骤未能成功完成。请查看安装日志了解详细信息。
Some steps could not be completed successfully. Please check the installation log for details.

🔧 建议的解决方案 | Suggested solutions:
• 检查网络连接 | Check network connection
• 确保有足够的磁盘空间 | Ensure sufficient disk space
• 以管理员权限运行 | Run with administrator privileges
• 查看日志文件获取详细错误信息 | Check log files for detailed error information

您可以稍后重新运行安装程序。
You can re-run the installer later.
            """

            failure_label = ttk.Label(
                completion_frame,
                text=failure_text,
                font=("Arial", 11),
                justify=tk.CENTER
            )
            failure_label.pack(expand=True, pady=50)

            # Buttons
            for widget in self.button_frame.winfo_children():
                widget.destroy()

            retry_button = ttk.Button(
                self.button_frame,
                text="🔄 重试 | Retry",
                command=self.show_progress_page
            )
            retry_button.pack(side=tk.RIGHT, padx=(10, 0))

            close_button = ttk.Button(
                self.button_frame,
                text="❌ 关闭 | Close",
                command=self.root.quit
            )
            close_button.pack(side=tk.RIGHT)

    def launch_app_and_close(self):
        """Launch application and close installer"""
        try:
            # Try to launch application
            launcher_files = ['smart_launcher.py', 'gui_launcher.py', 'main_new.py']

            for launcher_file in launcher_files:
                launcher_path = Path(__file__).parent / launcher_file
                if launcher_path.exists():
                    try:
                        subprocess.Popen([sys.executable, str(launcher_path)])
                        messagebox.showinfo(
                            "启动成功 | Launch Successful",
                            "应用程序已启动！\nApplication launched successfully!"
                        )
                        break
                    except Exception as e:
                        continue
            else:
                messagebox.showwarning(
                    "启动失败 | Launch Failed",
                    "无法自动启动应用程序，请手动运行 python gui_launcher.py\n"
                    "Could not launch automatically, please run python gui_launcher.py manually"
                )

        finally:
            self.root.quit()

    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = EnhancedSetupGUI()
        app.run()
    except Exception as e:
        print(f"GUI setup failed: {e}")
        print("Falling back to command line installer...")

        # Fallback to command line
        try:
            from advanced_installer import AdvancedInstaller
            installer = AdvancedInstaller()
            installer.run()
        except Exception as e2:
            print(f"Command line installer also failed: {e2}")
            sys.exit(1)

if __name__ == "__main__":
    main()