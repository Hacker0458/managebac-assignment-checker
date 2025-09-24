#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ManageBac Assignment Checker GUI Launcher
GUI启动器 - 现代化桌面应用程序
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check and install required dependencies | 检查并安装必需的依赖"""
    required_packages = [
        'tkinter',  # Usually comes with Python
        'playwright',
        'python-dotenv',
        'jinja2',
        'openai',
        'pystray',  # For system tray
        'pillow'    # For system tray icons
    ]
    
    missing_packages = []
    
    # Check tkinter
    try:
        import tkinter
        print("✅ tkinter is available")
    except ImportError:
        print("❌ tkinter is not available")
        missing_packages.append('tkinter')
    
    # Check other packages
    for package in required_packages[1:]:  # Skip tkinter as we checked it separately
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
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
