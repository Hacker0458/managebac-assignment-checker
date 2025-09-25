#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ ManageBac Assignment Checker - 桌面快捷方式创建器
🖥️ ManageBac作业检查器 - 桌面快捷方式创建器

为小白用户创建桌面快捷方式，让他们能够轻松启动应用程序。
Create desktop shortcuts for novice users to easily launch the application.
"""

import os
import sys
import platform
from pathlib import Path
import subprocess

class DesktopShortcutCreator:
    def __init__(self):
        self.system = platform.system()
        self.project_path = Path(__file__).parent.absolute()

    def create_shortcut(self):
        """Create desktop shortcut based on operating system"""
        try:
            if self.system == "Windows":
                return self.create_windows_shortcut()
            elif self.system == "Darwin":  # macOS
                return self.create_macos_shortcut()
            elif self.system == "Linux":
                return self.create_linux_shortcut()
            else:
                print(f"❌ 不支持的操作系统: {self.system}")
                return False
        except Exception as e:
            print(f"❌ 创建桌面快捷方式失败: {e}")
            return False

    def create_windows_shortcut(self):
        """Create Windows desktop shortcut"""
        try:
            import win32com.client

            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "ManageBac作业检查器.lnk"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))

            # Set shortcut properties
            if (self.project_path / "run_app.py").exists():
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "run_app.py")
            elif (self.project_path / "gui_launcher.py").exists():
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "gui_launcher.py")
            else:
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "main_new.py")

            shortcut.WorkingDirectory = str(self.project_path)
            shortcut.Description = "ManageBac Assignment Checker - 作业跟踪器"

            # Try to set icon if available
            icon_path = self.project_path / "icon.ico"
            if icon_path.exists():
                shortcut.IconLocation = str(icon_path)

            shortcut.save()
            print(f"✅ Windows桌面快捷方式已创建: {shortcut_path}")
            return True

        except ImportError:
            print("⚠️ 需要安装pywin32: pip install pywin32")
            return False
        except Exception as e:
            print(f"❌ Windows快捷方式创建失败: {e}")
            return False

    def create_macos_shortcut(self):
        """Create macOS desktop shortcut (app bundle)"""
        try:
            desktop = Path.home() / "Desktop"
            app_name = "ManageBac作业检查器.app"
            app_path = desktop / app_name

            # Create app bundle structure
            contents_path = app_path / "Contents"
            macos_path = contents_path / "MacOS"
            resources_path = contents_path / "Resources"

            # Create directories
            macos_path.mkdir(parents=True, exist_ok=True)
            resources_path.mkdir(parents=True, exist_ok=True)

            # Create Info.plist
            info_plist = contents_path / "Info.plist"
            plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ManageBac作业检查器</string>
    <key>CFBundleIdentifier</key>
    <string>com.managebac.assignment-checker</string>
    <key>CFBundleName</key>
    <string>ManageBac作业检查器</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>'''

            with open(info_plist, 'w', encoding='utf-8') as f:
                f.write(plist_content)

            # Create executable script
            executable_path = macos_path / "ManageBac作业检查器"

            # Determine which script to run
            if (self.project_path / "run_app.py").exists():
                script_to_run = "run_app.py"
            elif (self.project_path / "gui_launcher.py").exists():
                script_to_run = "gui_launcher.py"
            else:
                script_to_run = "main_new.py"

            script_content = f'''#!/bin/bash
cd "{self.project_path}"
{sys.executable} {script_to_run}
'''

            with open(executable_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # Make executable
            os.chmod(executable_path, 0o755)

            print(f"✅ macOS桌面应用已创建: {app_path}")
            print("💡 双击桌面上的应用图标即可启动")
            return True

        except Exception as e:
            print(f"❌ macOS快捷方式创建失败: {e}")
            return False

    def create_linux_shortcut(self):
        """Create Linux desktop shortcut (.desktop file)"""
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "ManageBac作业检查器.desktop"

            # Determine which script to run
            if (self.project_path / "run_app.py").exists():
                script_to_run = str(self.project_path / "run_app.py")
            elif (self.project_path / "gui_launcher.py").exists():
                script_to_run = str(self.project_path / "gui_launcher.py")
            else:
                script_to_run = str(self.project_path / "main_new.py")

            desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=ManageBac作业检查器
Comment=ManageBac Assignment Checker - 智能作业跟踪器
Exec={sys.executable} "{script_to_run}"
Path={self.project_path}
Icon=application-default
Terminal=false
Categories=Education;Office;
'''

            with open(shortcut_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)

            # Make executable
            os.chmod(shortcut_path, 0o755)

            print(f"✅ Linux桌面快捷方式已创建: {shortcut_path}")
            print("💡 双击桌面上的快捷方式即可启动")
            return True

        except Exception as e:
            print(f"❌ Linux快捷方式创建失败: {e}")
            return False

    def create_start_menu_entry(self):
        """Create start menu entry for Windows or Applications folder entry for macOS/Linux"""
        try:
            if self.system == "Windows":
                return self.create_windows_start_menu()
            elif self.system == "Darwin":
                return self.create_macos_applications()
            elif self.system == "Linux":
                return self.create_linux_applications()
            return False
        except Exception as e:
            print(f"⚠️ 创建开始菜单项失败: {e}")
            return False

    def create_windows_start_menu(self):
        """Create Windows Start Menu entry"""
        try:
            import win32com.client

            start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
            shortcut_path = start_menu / "ManageBac作业检查器.lnk"

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))

            if (self.project_path / "run_app.py").exists():
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "run_app.py")
            elif (self.project_path / "gui_launcher.py").exists():
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "gui_launcher.py")
            else:
                shortcut.Targetpath = sys.executable
                shortcut.Arguments = str(self.project_path / "main_new.py")

            shortcut.WorkingDirectory = str(self.project_path)
            shortcut.Description = "ManageBac Assignment Checker - 作业跟踪器"
            shortcut.save()

            print(f"✅ Windows开始菜单项已创建")
            return True

        except Exception as e:
            print(f"⚠️ Windows开始菜单项创建失败: {e}")
            return False

    def create_macos_applications(self):
        """Create macOS Applications folder entry"""
        # This would typically involve copying the app bundle to /Applications
        # For now, we'll just inform the user
        print("💡 macOS: 您可以将桌面上的应用拖拽到应用程序文件夹中")
        return True

    def create_linux_applications(self):
        """Create Linux applications menu entry"""
        try:
            applications_dir = Path.home() / ".local/share/applications"
            applications_dir.mkdir(parents=True, exist_ok=True)

            shortcut_path = applications_dir / "managebac-assignment-checker.desktop"

            if (self.project_path / "run_app.py").exists():
                script_to_run = str(self.project_path / "run_app.py")
            elif (self.project_path / "gui_launcher.py").exists():
                script_to_run = str(self.project_path / "gui_launcher.py")
            else:
                script_to_run = str(self.project_path / "main_new.py")

            desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=ManageBac作业检查器
Comment=ManageBac Assignment Checker - 智能作业跟踪器
Exec={sys.executable} "{script_to_run}"
Path={self.project_path}
Icon=application-default
Terminal=false
Categories=Education;Office;
'''

            with open(shortcut_path, 'w', encoding='utf-8') as f:
                f.write(desktop_content)

            os.chmod(shortcut_path, 0o755)

            print(f"✅ Linux应用程序菜单项已创建")
            return True

        except Exception as e:
            print(f"⚠️ Linux应用程序菜单项创建失败: {e}")
            return False

def main():
    """Main function"""
    print("🖥️ ManageBac Assignment Checker - 桌面快捷方式创建器")
    print("=" * 60)

    creator = DesktopShortcutCreator()

    print(f"🔍 检测到操作系统: {creator.system}")
    print(f"📁 项目路径: {creator.project_path}")
    print()

    # Create desktop shortcut
    print("📋 创建桌面快捷方式...")
    desktop_success = creator.create_shortcut()

    # Create start menu/applications entry
    print("\n📋 创建开始菜单/应用程序项...")
    menu_success = creator.create_start_menu_entry()

    print("\n" + "=" * 60)
    if desktop_success:
        print("✅ 桌面快捷方式创建成功！")
        print("💡 您现在可以从桌面直接启动ManageBac作业检查器")
    else:
        print("❌ 桌面快捷方式创建失败")

    if menu_success:
        print("✅ 开始菜单/应用程序项创建成功！")

    print("\n🚀 启动方法:")
    print("1. 双击桌面快捷方式")
    print("2. 从开始菜单/应用程序启动")
    print("3. 运行命令: python run_app.py")
    print("4. 运行快捷脚本: ./quick_start.sh")

if __name__ == "__main__":
    main()