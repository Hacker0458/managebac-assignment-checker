#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 System Tray Integration | 系统托盘集成
Provides system tray functionality and notifications
提供系统托盘功能和通知
"""

import os
import sys
import threading
import webbrowser
from typing import Optional, Callable
from pathlib import Path

def _is_graphical_environment_available() -> bool:
    """Return True when a graphical environment is accessible.

    ``pystray`` triggers the selection of a backend on import time. The X11
    backend attempts to connect to ``$DISPLAY`` immediately which raises
    ``DisplayNameError`` inside headless CI environments.  Importing
    ``pystray`` only when we can talk to a windowing system therefore keeps
    the module importable under automated tests.
    """

    platform = sys.platform.lower()

    if platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY"))
    if platform == "darwin":  # macOS always has a window server for GUI apps
        return True
    if platform.startswith("win"):
        return True
    return False


MenuItem = Icon = Menu = None
Image = ImageDraw = None

if _is_graphical_environment_available():
    try:
        import pystray
        from pystray import MenuItem, Icon, Menu
        from PIL import Image, ImageDraw

        TRAY_AVAILABLE = True
    except ImportError:
        TRAY_AVAILABLE = False
        print("⚠️ pystray not available. System tray features disabled.")
else:
    TRAY_AVAILABLE = False
    print("⚠️ No graphical environment detected. System tray features disabled.")

try:
    from plyer import notification

    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    # Try macOS native notifications instead
    import platform
    if platform.system() == "Darwin":
        try:
            import subprocess
            # Test osascript availability
            subprocess.run(['osascript', '-e', 'display notification "Test" with title "Test"'],
                         check=True, capture_output=True)
            NOTIFICATIONS_AVAILABLE = True
            print("✅ Using macOS native notifications (osascript)")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ plyer and osascript not available. Desktop notifications disabled.")
    else:
        print("⚠️ plyer not available. Desktop notifications disabled.")


class SystemTrayManager:
    """System tray manager | 系统托盘管理器"""

    def __init__(self, app_callback: Optional[Callable] = None, language: str = "zh"):
        self.app_callback = app_callback
        self.language = language
        self.icon = None
        self.running = False

        # Bilingual messages
        self.messages = {
            "en": {
                "app_name": "ManageBac Checker",
                "show_app": "Show Application",
                "check_assignments": "Check Assignments",
                "open_reports": "Open Reports",
                "settings": "Settings",
                "about": "About",
                "exit": "Exit",
                "assignment_notification": "Assignment Reminder",
                "new_assignments": "New assignments found!",
                "overdue_assignments": "You have overdue assignments!",
                "app_started": "ManageBac Checker is running in the background",
            },
            "zh": {
                "app_name": "ManageBac检查器",
                "show_app": "显示应用程序",
                "check_assignments": "检查作业",
                "open_reports": "打开报告",
                "settings": "设置",
                "about": "关于",
                "exit": "退出",
                "assignment_notification": "作业提醒",
                "new_assignments": "发现新作业！",
                "overdue_assignments": "您有逾期作业！",
                "app_started": "ManageBac检查器正在后台运行",
            },
        }

    def get_message(self, key: str) -> str:
        """Get localized message | 获取本地化消息"""
        return self.messages[self.language].get(key, key)

    def create_icon_image(self) -> Optional["Image.Image"]:
        """Create system tray icon | 创建系统托盘图标"""
        if not TRAY_AVAILABLE or Image is None:
            return None

        # Create a simple icon (64x64)
        width = 64
        height = 64
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw a simple book icon
        # Background circle
        draw.ellipse([4, 4, width - 4, height - 4], fill=(52, 152, 219, 255))

        # Book shape
        book_left = width // 4
        book_right = 3 * width // 4
        book_top = height // 4
        book_bottom = 3 * height // 4

        # Book cover
        draw.rectangle(
            [book_left, book_top, book_right, book_bottom],
            fill=(255, 255, 255, 255),
            outline=(44, 62, 80, 255),
            width=2,
        )

        # Book pages
        draw.rectangle(
            [book_left + 4, book_top + 4, book_right - 4, book_bottom - 4],
            fill=(236, 240, 241, 255),
        )

        # Lines on the book
        for i in range(3):
            y = book_top + 12 + i * 8
            draw.line(
                [book_left + 8, y, book_right - 8, y],
                fill=(149, 165, 166, 255),
                width=1,
            )

        return image

    def create_menu(self) -> Menu:
        """Create system tray menu | 创建系统托盘菜单"""
        if not TRAY_AVAILABLE:
            return None

        return Menu(
            MenuItem(self.get_message("show_app"), self.show_app),
            MenuItem(self.get_message("check_assignments"), self.check_assignments),
            MenuItem(self.get_message("open_reports"), self.open_reports),
            Menu.SEPARATOR,
            MenuItem(self.get_message("settings"), self.show_settings),
            MenuItem(self.get_message("about"), self.show_about),
            Menu.SEPARATOR,
            MenuItem(self.get_message("exit"), self.quit_app),
        )

    def start_tray(self):
        """Start system tray | 启动系统托盘"""
        if not TRAY_AVAILABLE:
            print("⚠️ System tray not available")
            return

        try:
            icon_image = self.create_icon_image()
            menu = self.create_menu()

            self.icon = Icon(self.get_message("app_name"), icon_image, menu=menu)

            self.running = True

            # Show startup notification
            self.show_notification(
                self.get_message("app_name"), self.get_message("app_started")
            )

            # Start tray in separate thread
            tray_thread = threading.Thread(target=self.icon.run, daemon=True)
            tray_thread.start()

            print("✅ System tray started")

        except Exception as e:
            print(f"❌ Failed to start system tray: {e}")

    def stop_tray(self):
        """Stop system tray | 停止系统托盘"""
        if self.icon and self.running:
            self.icon.stop()
            self.running = False
            print("✅ System tray stopped")

    def show_notification(self, title: str, message: str, timeout: int = 5):
        """Show desktop notification | 显示桌面通知"""
        if not NOTIFICATIONS_AVAILABLE:
            print(f"Notification: {title} - {message}")
            return

        try:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout,
                app_name=self.get_message("app_name"),
                app_icon=None,  # Use default icon
            )
        except Exception as e:
            print(f"❌ Failed to show notification: {e}")

    def notify_assignments(self, assignment_count: int, overdue_count: int = 0):
        """Notify about assignments | 通知作业情况"""
        if overdue_count > 0:
            title = self.get_message("assignment_notification")
            message = f"{self.get_message('overdue_assignments')} ({overdue_count})"
        elif assignment_count > 0:
            title = self.get_message("assignment_notification")
            message = f"{self.get_message('new_assignments')} ({assignment_count})"
        else:
            return

        self.show_notification(title, message)

    def show_app(self, icon=None, item=None):
        """Show main application | 显示主应用程序"""
        if self.app_callback:
            self.app_callback("show")
        print("📱 Show application requested")

    def check_assignments(self, icon=None, item=None):
        """Check assignments | 检查作业"""
        if self.app_callback:
            self.app_callback("check")
        print("🔍 Check assignments requested")

    def open_reports(self, icon=None, item=None):
        """Open reports folder | 打开报告文件夹"""
        reports_dir = Path("reports")
        if reports_dir.exists():
            if sys.platform == "win32":
                os.startfile(reports_dir)
            elif sys.platform == "darwin":
                os.system(f"open {reports_dir}")
            else:
                os.system(f"xdg-open {reports_dir}")
        else:
            self.show_notification(
                self.get_message("app_name"),
                (
                    "Reports folder not found"
                    if self.language == "en"
                    else "未找到报告文件夹"
                ),
            )

    def show_settings(self, icon=None, item=None):
        """Show settings | 显示设置"""
        if self.app_callback:
            self.app_callback("settings")
        print("⚙️ Settings requested")

    def show_about(self, icon=None, item=None):
        """Show about dialog | 显示关于对话框"""
        webbrowser.open("https://github.com/Hacker0458/managebac-assignment-checker")

    def quit_app(self, icon=None, item=None):
        """Quit application | 退出应用程序"""
        if self.app_callback:
            self.app_callback("quit")
        self.stop_tray()
        print("👋 Application quit requested")


class NotificationManager:
    """Desktop notification manager | 桌面通知管理器"""

    def __init__(self, language: str = "zh"):
        self.language = language
        self.enabled = NOTIFICATIONS_AVAILABLE

    def is_available(self) -> bool:
        """Check if notifications are available | 检查通知是否可用"""
        return self.enabled

    def send_notification(self, title: str, message: str, timeout: int = 5):
        """Send desktop notification | 发送桌面通知"""
        if not self.enabled:
            print(f"Notification: {title} - {message}")
            return

        try:
            # Try plyer first
            try:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=timeout,
                    app_name="ManageBac Checker",
                )
            except NameError:
                # plyer not available, try macOS native
                import platform
                import subprocess
                if platform.system() == "Darwin":
                    script = f'display notification "{message}" with title "{title}"'
                    subprocess.run(['osascript', '-e', script], check=True, capture_output=True)
                else:
                    # Fallback to console
                    print(f"Notification: {title} - {message}")
        except Exception as e:
            print(f"❌ Failed to send notification: {e}")

    def notify_assignment_reminder(self, assignments: list):
        """Send assignment reminder notification | 发送作业提醒通知"""
        if not assignments:
            return

        overdue = [a for a in assignments if a.get("status") == "overdue"]
        high_priority = [a for a in assignments if a.get("priority") == "high"]

        if overdue:
            title = "⚠️ Overdue Assignments" if self.language == "en" else "⚠️ 逾期作业"
            message = (
                f"You have {len(overdue)} overdue assignments!"
                if self.language == "en"
                else f"您有{len(overdue)}个逾期作业！"
            )
            self.send_notification(title, message, timeout=10)

        elif high_priority:
            title = (
                "🔥 High Priority Assignments"
                if self.language == "en"
                else "🔥 高优先级作业"
            )
            message = (
                f"You have {len(high_priority)} high priority assignments"
                if self.language == "en"
                else f"您有{len(high_priority)}个高优先级作业"
            )
            self.send_notification(title, message, timeout=8)

        else:
            title = "📚 Assignment Update" if self.language == "en" else "📚 作业更新"
            message = (
                f"Found {len(assignments)} assignments"
                if self.language == "en"
                else f"找到{len(assignments)}个作业"
            )
            self.send_notification(title, message)

    def notify_ai_analysis_complete(self):
        """Notify when AI analysis is complete | AI分析完成时通知"""
        title = "🤖 AI Analysis Complete" if self.language == "en" else "🤖 AI分析完成"
        message = (
            "AI analysis has been completed with new suggestions"
            if self.language == "en"
            else "AI分析已完成，包含新建议"
        )
        self.send_notification(title, message)

    def notify_report_generated(self, report_path: str):
        """Notify when report is generated | 报告生成时通知"""
        title = "📊 Report Generated" if self.language == "en" else "📊 报告已生成"
        message = (
            f"Report saved to {report_path}"
            if self.language == "en"
            else f"报告已保存到{report_path}"
        )
        self.send_notification(title, message)


def install_tray_dependencies():
    """Install system tray dependencies | 安装系统托盘依赖"""
    dependencies = ["pystray", "pillow", "plyer"]

    print("📦 Installing system tray dependencies...")
    print("📦 安装系统托盘依赖...")

    import subprocess
    import sys

    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False

    print("✅ All system tray dependencies installed!")
    print("✅ 所有系统托盘依赖已安装！")
    return True


if __name__ == "__main__":
    # Test system tray functionality
    def test_callback(action):
        print(f"Callback received: {action}")
        if action == "quit":
            import time

            time.sleep(1)
            exit(0)

    print("🧪 Testing system tray functionality...")

    if not TRAY_AVAILABLE:
        print("Installing dependencies...")
        if install_tray_dependencies():
            print("Please restart the script to test system tray.")
        exit(0)

    tray_manager = SystemTrayManager(test_callback, "zh")
    tray_manager.start_tray()

    # Keep the script running
    try:
        import time

        while tray_manager.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system tray...")
        tray_manager.stop_tray()
