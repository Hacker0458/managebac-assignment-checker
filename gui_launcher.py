#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ManageBac Assignment Checker GUI Launcher
GUI启动器 - 现代化桌面应用程序
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies | 检查并安装必需的依赖"""
    required_packages = [
        'tkinter',  # Usually comes with Python
        'playwright',
        'python-dotenv',
        'jinja2'
    ]

    optional_packages = [
        'openai',
        'pillow'
    ]

    missing_packages = []

    # Check tkinter
    try:
        import tkinter
        print("✅ tkinter is available")
    except ImportError:
        print("❌ tkinter is not available")
        missing_packages.append('tkinter')

    # Check required packages
    for package in required_packages[1:]:  # Skip tkinter as we checked it separately
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)

    # Check optional packages (don't add to missing if not found)
    for package in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is available")
        except ImportError:
            print(f"⚠️ {package} is optional and not installed")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        
        # Install missing packages
        for package in missing_packages:
            if package == 'tkinter':
                print("⚠️ tkinter needs to be installed system-wide.")
                print("   On Ubuntu/Debian: sudo apt-get install python3-tk")
                print("   On CentOS/RHEL: sudo yum install tkinter")
                print("   On macOS: tkinter should come with Python")
                print("   On Windows: tkinter should come with Python")
                continue
            
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def is_first_time_setup():
    """Check if this is the first time setup | 检查是否为首次设置"""
    env_file = Path('.env')

    # No .env file exists
    if not env_file.exists():
        return True

    # Check if .env file has required credentials
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for placeholder values that indicate unconfigured setup
        placeholder_indicators = [
            'your_email@school.edu',
            'your_password',
            'your-school.managebac.com',
            'your.email@example.com',
            'your_managebac_password',
            'https://your-school.managebac.cn'
        ]

        # If any placeholder is found, it's likely not configured
        for placeholder in placeholder_indicators:
            if placeholder in content:
                return True

        # Check if required variables are missing or empty
        required_vars = ['MANAGEBAC_URL', 'MANAGEBAC_EMAIL', 'MANAGEBAC_PASSWORD']
        for var in required_vars:
            if f'{var}=' not in content or f'{var}=\n' in content:
                return True

    except Exception as e:
        print(f"⚠️ Error reading .env file: {e}")
        return True

    return False

def run_first_time_setup():
    """Run the first-time setup wizard | 运行首次设置向导"""
    print("\n🧙‍♂️ First-time setup detected, launching configuration wizard...")
    print("🧙‍♂️ 检测到首次设置，启动配置向导...")

    # Check if first_run_setup.py exists
    setup_script = Path('first_run_setup.py')
    if not setup_script.exists():
        print("⚠️ first_run_setup.py not found, using fallback configuration...")
        print("⚠️ 未找到首次设置向导，使用后备配置...")

        # Show a simple dialog asking user to configure manually
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            result = messagebox.askyesno(
                "First Time Setup | 首次设置",
                "Welcome to ManageBac Assignment Checker!\n"
                "欢迎使用ManageBac作业检查器！\n\n"
                "This appears to be your first time running the application.\n"
                "这似乎是您首次运行该应用程序。\n\n"
                "Would you like to run the setup wizard now?\n"
                "您想现在运行设置向导吗？\n\n"
                "Click 'Yes' to configure, or 'No' to setup manually later.\n"
                "点击'是'进行配置，或'否'稍后手动设置。"
            )

            root.destroy()

            if result:
                # Try to run setup wizard
                if Path('setup_wizard.py').exists():
                    print("🧙‍♂️ Running command-line setup wizard...")
                    subprocess.call([sys.executable, 'setup_wizard.py'])
                    return True
                else:
                    messagebox.showinfo(
                        "Manual Setup Required | 需要手动设置",
                        "Please edit the .env file with your ManageBac credentials.\n"
                        "请编辑.env文件并填入您的ManageBac凭据。\n\n"
                        "Required settings | 必需设置:\n"
                        "• MANAGEBAC_URL - Your school's ManageBac URL\n"
                        "• MANAGEBAC_EMAIL - Your login email\n"
                        "• MANAGEBAC_PASSWORD - Your password"
                    )
                    return False
            else:
                return False

        except Exception as e:
            print(f"⚠️ Error showing setup dialog: {e}")
            return False

    else:
        # Run the GUI setup wizard
        print("🎯 Launching GUI setup wizard...")
        print("🎯 启动GUI设置向导...")
        try:
            result = subprocess.call([sys.executable, 'first_run_setup.py'])
            return result == 0
        except Exception as e:
            print(f"❌ Error running first_run_setup.py: {e}")
            return False

def setup_environment():
    """Setup the environment | 设置环境"""
    # Create necessary directories
    directories = ['logs', 'reports']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Check if .env exists, if not copy from config.example.env
    if not Path('.env').exists() and Path('config.example.env').exists():
        import shutil
        shutil.copy('config.example.env', '.env')
        print("📄 Created .env file from config.example.env")

def launch_gui():
    """Launch the GUI application | 启动GUI应用程序"""
    try:
        print("🚀 Launching ManageBac Assignment Checker GUI...")
        print("🚀 正在启动ManageBac作业检查器GUI...")
        
        # Try professional GUI first, then enhanced, then basic
        try:
            from managebac_checker.professional_gui import main
            print("🎯 Starting Professional GUI...")
            print("🎯 启动专业版GUI...")
            main()
        except ImportError:
            try:
                from managebac_checker.enhanced_gui import main
                print("⚠️ Professional GUI not available, using enhanced GUI...")
                print("⚠️ 专业版GUI不可用，使用增强版GUI...")
                main()
            except ImportError:
                print("⚠️ Enhanced GUI not available, using basic GUI...")
                print("⚠️ 增强版GUI不可用，使用基础GUI...")
                from managebac_checker.gui import main
                main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def main():
    """Main launcher function | 主启动函数"""
    print("=" * 60)
    print("🎓 ManageBac Assignment Checker GUI Launcher")
    print("🎓 ManageBac作业检查器GUI启动器")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print("❌ 需要Python 3.8或更高版本！")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    print("📦 检查依赖...")
    
    if not check_dependencies():
        print("\n❌ Dependency check failed!")
        print("❌ 依赖检查失败！")
        sys.exit(1)
    
    # Setup environment
    print("\n🔧 Setting up environment...")
    print("🔧 设置环境...")
    setup_environment()

    # Check if first-time setup is needed
    if is_first_time_setup():
        print("\n🎯 First-time setup required!")
        print("🎯 需要首次设置！")

        if not run_first_time_setup():
            print("\n⚠️ Setup was cancelled or failed.")
            print("⚠️ 设置被取消或失败。")
            print("You can run setup later using: python setup_wizard.py")
            print("您可以稍后使用以下命令运行设置：python setup_wizard.py")

            # Ask user if they want to continue anyway
            try:
                root = tk.Tk()
                root.withdraw()

                continue_anyway = messagebox.askyesno(
                    "Continue without setup? | 是否不设置就继续？",
                    "The application may not work properly without proper configuration.\n"
                    "应用程序在没有正确配置的情况下可能无法正常工作。\n\n"
                    "Do you want to continue anyway?\n"
                    "您是否要继续？"
                )

                root.destroy()

                if not continue_anyway:
                    print("✋ User chose to exit for configuration.")
                    print("✋ 用户选择退出进行配置。")
                    sys.exit(0)

            except Exception as e:
                print(f"⚠️ Error showing continue dialog: {e}")
                # Continue anyway if dialog fails

        else:
            print("\n✅ Setup completed successfully!")
            print("✅ 设置完成！")

    # Launch GUI
    print("\n🚀 Starting GUI application...")
    print("🚀 启动GUI应用程序...")

    if launch_gui():
        print("\n✅ GUI application closed successfully!")
        print("✅ GUI应用程序成功关闭！")
    else:
        print("\n❌ GUI application failed to start!")
        print("❌ GUI应用程序启动失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
