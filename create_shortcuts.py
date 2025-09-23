#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 Desktop Shortcut Creator | 桌面快捷方式创建器
Creates desktop shortcuts for easy access to the GUI application
创建桌面快捷方式以便于访问GUI应用程序
"""

import os
import sys
import platform
from pathlib import Path


def create_windows_shortcut():
    """Create Windows desktop shortcut | 创建Windows桌面快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "ManageBac Assignment Checker.lnk")
        
        # Get current directory and Python executable
        current_dir = Path.cwd()
        python_exe = sys.executable
        script_path = current_dir / "gui_launcher.py"
        
        # Create shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = str(current_dir)
        shortcut.Description = "ManageBac Assignment Checker - GUI Application"
        
        # Set icon if available
        icon_path = current_dir / "icon.ico"
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        
        shortcut.save()
        
        print("✅ Windows desktop shortcut created successfully!")
        print("✅ Windows桌面快捷方式创建成功！")
        return True
        
    except ImportError:
        print("❌ winshell and pywin32 are required for Windows shortcuts")
        print("❌ Windows快捷方式需要winshell和pywin32")
        print("Install with: pip install winshell pywin32")
        return False
    except Exception as e:
        print(f"❌ Failed to create Windows shortcut: {e}")
        return False


def create_linux_shortcut():
    """Create Linux desktop shortcut | 创建Linux桌面快捷方式"""
    try:
        desktop_dir = Path.home() / "Desktop"
        if not desktop_dir.exists():
            desktop_dir = Path.home() / ".local" / "share" / "applications"
            desktop_dir.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = desktop_dir / "managebac-assignment-checker.desktop"
        
        # Get current directory and Python executable
        current_dir = Path.cwd()
        python_exe = sys.executable
        script_path = current_dir / "gui_launcher.py"
        
        # Create .desktop file content
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=ManageBac Assignment Checker
Name[zh]=ManageBac作业检查器
Comment=Intelligent automation tool for ManageBac assignment tracking
Comment[zh]=ManageBac作业追踪的智能自动化工具
Exec={python_exe} "{script_path}"
Path={current_dir}
Icon={current_dir / "icon.png" if (current_dir / "icon.png").exists() else "application-x-executable"}
Terminal=false
Categories=Education;Utility;
Keywords=managebac;assignment;homework;education;
StartupWMClass=ManageBac Assignment Checker
"""
        
        # Write desktop file
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # Make executable
        os.chmod(shortcut_path, 0o755)
        
        print("✅ Linux desktop shortcut created successfully!")
        print("✅ Linux桌面快捷方式创建成功！")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Linux shortcut: {e}")
        return False


def create_macos_shortcut():
    """Create macOS application bundle | 创建macOS应用程序包"""
    try:
        # Create .app bundle structure
        app_name = "ManageBac Assignment Checker.app"
        app_dir = Path.home() / "Desktop" / app_name
        
        # Create directory structure
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        for directory in [contents_dir, macos_dir, resources_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Get current directory and Python executable
        current_dir = Path.cwd()
        python_exe = sys.executable
        script_path = current_dir / "gui_launcher.py"
        
        # Create Info.plist
        info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>ManageBac Assignment Checker</string>
    <key>CFBundleExecutable</key>
    <string>managebac-checker</string>
    <key>CFBundleIdentifier</key>
    <string>com.managebac.assignment-checker</string>
    <key>CFBundleName</key>
    <string>ManageBac Assignment Checker</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.9</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>CFBundleDocumentTypes</key>
    <array>
    </array>
</dict>
</plist>"""
        
        with open(contents_dir / "Info.plist", 'w') as f:
            f.write(info_plist)
        
        # Create launcher script
        launcher_script = f"""#!/bin/bash
cd "{current_dir}"
"{python_exe}" "{script_path}"
"""
        
        launcher_path = macos_dir / "managebac-checker"
        with open(launcher_path, 'w') as f:
            f.write(launcher_script)
        
        # Make launcher executable
        os.chmod(launcher_path, 0o755)
        
        print("✅ macOS application bundle created successfully!")
        print("✅ macOS应用程序包创建成功！")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create macOS shortcut: {e}")
        return False


def create_icon():
    """Create application icon | 创建应用程序图标"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        size = (256, 256)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw background circle
        margin = 20
        draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], 
                    fill=(52, 152, 219, 255))
        
        # Draw book icon
        book_width = size[0] // 3
        book_height = size[1] // 2
        book_x = (size[0] - book_width) // 2
        book_y = (size[1] - book_height) // 2
        
        # Book cover
        draw.rectangle([book_x, book_y, book_x + book_width, book_y + book_height],
                      fill=(255, 255, 255, 255), outline=(44, 62, 80, 255), width=4)
        
        # Book pages
        page_margin = 8
        draw.rectangle([book_x + page_margin, book_y + page_margin, 
                       book_x + book_width - page_margin, book_y + book_height - page_margin],
                      fill=(236, 240, 241, 255))
        
        # Lines on book
        for i in range(4):
            line_y = book_y + 40 + i * 20
            draw.line([book_x + 20, line_y, book_x + book_width - 20, line_y],
                     fill=(149, 165, 166, 255), width=3)
        
        # Save icons
        image.save("icon.png", "PNG")
        
        # Create ICO for Windows
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_images = []
        for ico_size in ico_sizes:
            ico_img = image.resize(ico_size, Image.Resampling.LANCZOS)
            ico_images.append(ico_img)
        
        ico_images[0].save("icon.ico", format="ICO", sizes=[(img.width, img.height) for img in ico_images])
        
        print("✅ Application icons created successfully!")
        print("✅ 应用程序图标创建成功！")
        return True
        
    except ImportError:
        print("❌ PIL (Pillow) is required for icon creation")
        print("❌ 图标创建需要PIL (Pillow)")
        print("Install with: pip install pillow")
        return False
    except Exception as e:
        print(f"❌ Failed to create icons: {e}")
        return False


def main():
    """Main function to create shortcuts | 创建快捷方式的主函数"""
    print("=" * 60)
    print("🔗 Desktop Shortcut Creator | 桌面快捷方式创建器")
    print("=" * 60)
    
    # Create application icon first
    print("\n🎨 Creating application icon...")
    print("🎨 创建应用程序图标...")
    create_icon()
    
    # Detect operating system and create appropriate shortcut
    system = platform.system().lower()
    
    print(f"\n🖥️ Detected OS: {system}")
    print(f"🖥️ 检测到操作系统: {system}")
    
    success = False
    
    if system == "windows":
        print("\n🪟 Creating Windows desktop shortcut...")
        print("🪟 创建Windows桌面快捷方式...")
        success = create_windows_shortcut()
        
    elif system == "linux":
        print("\n🐧 Creating Linux desktop shortcut...")
        print("🐧 创建Linux桌面快捷方式...")
        success = create_linux_shortcut()
        
    elif system == "darwin":  # macOS
        print("\n🍎 Creating macOS application bundle...")
        print("🍎 创建macOS应用程序包...")
        success = create_macos_shortcut()
        
    else:
        print(f"❌ Unsupported operating system: {system}")
        print(f"❌ 不支持的操作系统: {system}")
        return
    
    if success:
        print("\n✅ Desktop shortcut created successfully!")
        print("✅ 桌面快捷方式创建成功！")
        print("\nYou can now launch the application from your desktop.")
        print("现在您可以从桌面启动应用程序。")
    else:
        print("\n❌ Failed to create desktop shortcut.")
        print("❌ 创建桌面快捷方式失败。")
        print("\nYou can still run the application using:")
        print("您仍可以使用以下方式运行应用程序:")
        print(f"  python gui_launcher.py")
        print(f"  ./start_gui.sh  (Linux/macOS)")
        print(f"  start_gui.bat   (Windows)")


if __name__ == "__main__":
    main()
