#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Complete Installation Script | 完整安装脚本
One-click installation of ManageBac Assignment Checker with GUI
ManageBac作业检查器GUI版本一键安装
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Print installation banner | 打印安装横幅"""
    print("=" * 80)
    print("🎓 ManageBac Assignment Checker - Complete Installation")
    print("🎓 ManageBac作业检查器 - 完整安装")
    print("=" * 80)
    print()
    print("🚀 This script will install all components including:")
    print("🚀 此脚本将安装所有组件，包括：")
    print("   • 📱 Modern GUI Application | 现代化GUI应用程序")
    print("   • 🤖 AI Assistant Integration | AI助手集成")
    print("   • 🔔 System Tray & Notifications | 系统托盘和通知")
    print("   • 🎨 Multiple Themes | 多种主题")
    print("   • 🌐 Bilingual Interface | 双语界面")
    print("   • 📊 Advanced Reporting | 高级报告")
    print()


def check_python_version():
    """Check Python version | 检查Python版本"""
    print("🐍 Checking Python version...")
    print("🐍 检查Python版本...")
    
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8+ is required, but you have {sys.version}")
        print(f"❌ 需要Python 3.8+，但您当前版本是 {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - OK")
    return True


def install_dependencies():
    """Install all dependencies | 安装所有依赖"""
    print("\n📦 Installing dependencies...")
    print("📦 安装依赖...")
    
    # Core dependencies
    core_deps = [
        'playwright>=1.40.0',
        'python-dotenv>=1.0.0',
        'jinja2>=3.1.0',
        'openai>=1.0.0'
    ]
    
    # GUI dependencies
    gui_deps = [
        'pystray>=0.19.0',
        'pillow>=10.0.0',
        'plyer>=2.1.0'
    ]
    
    # Optional dependencies for shortcuts
    shortcut_deps = []
    if platform.system().lower() == 'windows':
        shortcut_deps = ['winshell', 'pywin32']
    
    all_deps = core_deps + gui_deps + shortcut_deps
    
    print(f"📋 Installing {len(all_deps)} packages...")
    print(f"📋 安装{len(all_deps)}个包...")
    
    failed_packages = []
    
    for package in all_deps:
        try:
            print(f"   📦 Installing {package}...")
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Some packages failed to install: {', '.join(failed_packages)}")
        print(f"⚠️ 某些包安装失败: {', '.join(failed_packages)}")
        print("The application may still work with reduced functionality.")
        print("应用程序可能仍可运行，但功能会有所减少。")
    else:
        print("\n✅ All dependencies installed successfully!")
        print("✅ 所有依赖安装成功！")
    
    return len(failed_packages) == 0


def install_playwright():
    """Install Playwright browsers | 安装Playwright浏览器"""
    print("\n🌐 Installing Playwright browsers...")
    print("🌐 安装Playwright浏览器...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium'])
        print("✅ Playwright browsers installed successfully!")
        print("✅ Playwright浏览器安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Playwright browsers")
        print("❌ Playwright浏览器安装失败")
        print("You may need to run: python -m playwright install")
        print("您可能需要运行: python -m playwright install")
        return False


def setup_environment():
    """Setup application environment | 设置应用程序环境"""
    print("\n🔧 Setting up environment...")
    print("🔧 设置环境...")
    
    # Create directories
    directories = ['logs', 'reports', 'cache']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   📁 Created directory: {directory}")
    
    # Copy config template
    if Path('config.example.env').exists() and not Path('.env').exists():
        import shutil
        shutil.copy('config.example.env', '.env')
        print("   📄 Created .env from template")
    
    # Set file permissions
    scripts = ['start_gui.sh', 'install.sh']
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            try:
                os.chmod(script_path, 0o755)
                print(f"   🔑 Set executable permissions for {script}")
            except:
                pass
    
    print("✅ Environment setup completed!")
    print("✅ 环境设置完成！")


def create_desktop_shortcuts():
    """Create desktop shortcuts | 创建桌面快捷方式"""
    print("\n🔗 Creating desktop shortcuts...")
    print("🔗 创建桌面快捷方式...")
    
    try:
        # Run the shortcut creation script
        result = subprocess.run([sys.executable, 'create_shortcuts.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Desktop shortcuts created successfully!")
            print("✅ 桌面快捷方式创建成功！")
            return True
        else:
            print("⚠️ Desktop shortcut creation had some issues")
            print("⚠️ 桌面快捷方式创建存在一些问题")
            print("You can still run the application manually.")
            print("您仍可以手动运行应用程序。")
            return False
    except Exception as e:
        print(f"⚠️ Could not create desktop shortcuts: {e}")
        print("⚠️ 无法创建桌面快捷方式")
        return False


def test_installation():
    """Test the installation | 测试安装"""
    print("\n🧪 Testing installation...")
    print("🧪 测试安装...")
    
    try:
        # Test basic imports
        print("   📦 Testing imports...")
        
        import tkinter
        print("   ✅ tkinter - OK")
        
        from managebac_checker.config import Config
        print("   ✅ config module - OK")
        
        from managebac_checker.gui import ManageBacGUI
        print("   ✅ GUI module - OK")
        
        try:
            from managebac_checker.enhanced_gui import EnhancedManageBacGUI
            print("   ✅ Enhanced GUI module - OK")
        except ImportError:
            print("   ⚠️ Enhanced GUI module - Some features may not be available")
        
        try:
            from managebac_checker.ai_assistant import AIAssistant
            print("   ✅ AI Assistant module - OK")
        except ImportError:
            print("   ⚠️ AI Assistant module - AI features may not be available")
        
        print("\n✅ Installation test completed successfully!")
        print("✅ 安装测试成功完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ Installation test failed: {e}")
        print(f"❌ 安装测试失败: {e}")
        return False


def show_usage_instructions():
    """Show usage instructions | 显示使用说明"""
    print("\n" + "=" * 80)
    print("🎉 Installation Complete! | 安装完成！")
    print("=" * 80)
    
    print("\n🚀 How to start the application | 如何启动应用程序:")
    print()
    
    # Desktop shortcut
    if Path.home().joinpath("Desktop", "ManageBac Assignment Checker.lnk").exists() or \
       Path.home().joinpath("Desktop", "managebac-assignment-checker.desktop").exists() or \
       Path.home().joinpath("Desktop", "ManageBac Assignment Checker.app").exists():
        print("   🖱️  Double-click the desktop shortcut")
        print("   🖱️  双击桌面快捷方式")
        print()
    
    # Command line options
    print("   💻 Command line options | 命令行选项:")
    print("      python gui_launcher.py")
    print("      ./start_gui.sh          (Linux/macOS)")
    print("      start_gui.bat           (Windows)")
    print()
    
    print("🔧 First time setup | 首次设置:")
    print("   1. 📧 Enter your ManageBac credentials | 输入您的ManageBac凭据")
    print("   2. 🤖 Optionally configure AI Assistant | 可选配置AI助手")
    print("   3. 🎨 Choose your preferred theme | 选择您喜欢的主题")
    print("   4. 🔍 Start checking assignments! | 开始检查作业！")
    print()
    
    print("📚 Documentation | 文档:")
    print("   GitHub: https://github.com/Hacker0458/managebac-assignment-checker")
    print()
    
    print("🆘 Need help? | 需要帮助？")
    print("   Issues: https://github.com/Hacker0458/managebac-assignment-checker/issues")
    print()


def main():
    """Main installation function | 主安装函数"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    deps_success = install_dependencies()
    
    # Install Playwright
    playwright_success = install_playwright()
    
    # Setup environment
    setup_environment()
    
    # Create desktop shortcuts
    shortcuts_success = create_desktop_shortcuts()
    
    # Test installation
    test_success = test_installation()
    
    # Show results
    print("\n" + "=" * 80)
    print("📋 Installation Summary | 安装摘要")
    print("=" * 80)
    
    print(f"   📦 Dependencies: {'✅ Success' if deps_success else '⚠️ Partial'}")
    print(f"   🌐 Playwright: {'✅ Success' if playwright_success else '⚠️ Manual setup needed'}")
    print(f"   🔗 Shortcuts: {'✅ Success' if shortcuts_success else '⚠️ Manual creation'}")
    print(f"   🧪 Testing: {'✅ Success' if test_success else '❌ Failed'}")
    
    if test_success:
        show_usage_instructions()
        
        # Ask if user wants to start the application
        print("🚀 Would you like to start the application now? | 您想现在启动应用程序吗？")
        response = input("   (y/n): ").lower().strip()
        
        if response in ['y', 'yes', '是', '好']:
            print("\n🎯 Starting ManageBac Assignment Checker...")
            print("🎯 启动ManageBac作业检查器...")
            try:
                subprocess.run([sys.executable, 'gui_launcher.py'])
            except KeyboardInterrupt:
                print("\n👋 Application closed by user")
                print("👋 用户关闭了应用程序")
    else:
        print("\n❌ Installation had issues. Please check the error messages above.")
        print("❌ 安装存在问题。请检查上面的错误消息。")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Installation cancelled by user")
        print("🛑 用户取消了安装")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed with error: {e}")
        print(f"❌ 安装失败，错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
