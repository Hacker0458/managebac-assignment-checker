#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 Improved System Tray Integration | 改进的系统托盘集成
Cross-platform system tray with fallback notifications
跨平台系统托盘，支持备用通知方案
"""

import os
import sys
import threading
import webbrowser
import subprocess
import platform
from typing import Optional, Callable
from pathlib import Path

# Try to import system tray libraries with fallbacks
try:
    import pystray
    from pystray import MenuItem, Icon, Menu
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False

# Cross-platform notification fallbacks
def show_notification_fallback(title: str, message: str, timeout: int = 5):
    """Cross-platform notification fallback | 跨平台通知备用方案"""
    system = platform.system().lower()
    
    try:
        if system == 'darwin':  # macOS
            # Use osascript for macOS notifications
            script = f'''
            display notification "{message}" with title "{title}" sound name "default"
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            
        elif system == 'linux':
            # Use notify-send for Linux
            subprocess.run(['notify-send', title, message], check=True)
            
        elif system == 'windows':
            # Use Windows toast notifications
            try:
                import win10toast
                toaster = win10toast.ToastNotifier()
                toaster.show_toast(title, message, duration=timeout)
            except ImportError:
                # Fallback to print
                print(f"🔔 {title}: {message}")
                
        else:
            # Fallback to console output
            print(f"🔔 {title}: {message}")
            
    except Exception as e:
        # Ultimate fallback
        print(f"🔔 {title}: {message}")
        print(f"   (Notification error: {e})")


class ImprovedSystemTrayManager:
    """Improved system tray manager with better compatibility | 改进的系统托盘管理器，更好的兼容性"""
    
    def __init__(self, app_callback: Optional[Callable] = None, language: str = 'zh'):
        self.app_callback = app_callback
        self.language = language
        self.icon = None
        self.running = False
        
        # Bilingual messages
        self.messages = {
            'en': {
                'app_name': 'ManageBac Checker',
                'show_app': 'Show Application',
                'check_assignments': 'Check Assignments',
                'open_reports': 'Open Reports',
                'settings': 'Settings',
                'about': 'About',
                'exit': 'Exit',
                'assignment_notification': 'Assignment Reminder',
                'new_assignments': 'New assignments found!',
                'overdue_assignments': 'You have overdue assignments!',
                'app_started': 'ManageBac Checker is running in the background',
            },
            'zh': {
                'app_name': 'ManageBac检查器',
                'show_app': '显示应用程序',
                'check_assignments': '检查作业',
                'open_reports': '打开报告',
                'settings': '设置',
                'about': '关于',
                'exit': '退出',
                'assignment_notification': '作业提醒',
                'new_assignments': '发现新作业！',
                'overdue_assignments': '您有逾期作业！',
                'app_started': 'ManageBac检查器正在后台运行',
            }
        }
    
    def get_message(self, key: str) -> str:
        """Get localized message | 获取本地化消息"""
        return self.messages[self.language].get(key, key)
    
    def create_icon_image(self) -> Optional[Image.Image]:
        """Create system tray icon | 创建系统托盘图标"""
        try:
            # Create a modern, high-quality icon (128x128 for better quality)
            width = 128
            height = 128
            image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # Modern gradient background
            for y in range(height):
                alpha = int(255 * (1 - y / height * 0.3))
                color = (52, 152, 219, alpha)
                draw.line([(0, y), (width, y)], fill=color)
            
            # Draw modern book icon with better proportions
            book_width = int(width * 0.5)
            book_height = int(height * 0.6)
            book_x = (width - book_width) // 2
            book_y = (height - book_height) // 2
            
            # Book shadow
            shadow_offset = 3
            draw.rectangle([book_x + shadow_offset, book_y + shadow_offset, 
                           book_x + book_width + shadow_offset, book_y + book_height + shadow_offset],
                          fill=(0, 0, 0, 60))
            
            # Book cover with gradient
            draw.rectangle([book_x, book_y, book_x + book_width, book_y + book_height],
                          fill=(255, 255, 255, 240), outline=(44, 62, 80, 255), width=3)
            
            # Book spine
            spine_width = book_width // 8
            draw.rectangle([book_x, book_y, book_x + spine_width, book_y + book_height],
                          fill=(231, 76, 60, 200))
            
            # Pages with subtle lines
            page_margin = 12
            page_area = [book_x + spine_width + page_margin, book_y + page_margin, 
                        book_x + book_width - page_margin, book_y + book_height - page_margin]
            
            # Page lines
            line_count = 6
            for i in range(line_count):
                line_y = page_area[1] + (page_area[3] - page_area[1]) * (i + 1) / (line_count + 1)
                draw.line([page_area[0] + 8, line_y, page_area[2] - 8, line_y],
                         fill=(149, 165, 166, 180), width=2)
            
            # Add a small "M" for ManageBac
            try:
                from PIL import ImageFont
                # Try to use a system font
                font_size = width // 8
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                text_bbox = draw.textbbox((0, 0), "M", font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = book_x + book_width - text_width - 8
                text_y = book_y + 8
                draw.text((text_x, text_y), "M", fill=(52, 152, 219, 255), font=font)
            except:
                # Fallback without custom font
                pass
            
            return image
            
        except Exception as e:
            print(f"⚠️ Error creating icon: {e}")
            return None
    
    def create_menu(self) -> Optional[Menu]:
        """Create system tray menu | 创建系统托盘菜单"""
        if not TRAY_AVAILABLE:
            return None
        
        return Menu(
            MenuItem(self.get_message('show_app'), self.show_app),
            MenuItem(self.get_message('check_assignments'), self.check_assignments),
            MenuItem(self.get_message('open_reports'), self.open_reports),
            Menu.SEPARATOR,
            MenuItem(self.get_message('settings'), self.show_settings),
            MenuItem(self.get_message('about'), self.show_about),
            Menu.SEPARATOR,
            MenuItem(self.get_message('exit'), self.quit_app)
        )
    
    def start_tray(self):
        """Start system tray | 启动系统托盘"""
        if not TRAY_AVAILABLE:
            print("⚠️ System tray not available, using fallback notifications")
            self.show_notification(
                self.get_message('app_name'),
                self.get_message('app_started')
            )
            return
        
        try:
            icon_image = self.create_icon_image()
            if not icon_image:
                print("⚠️ Could not create tray icon")
                return
            
            menu = self.create_menu()
            
            self.icon = Icon(
                self.get_message('app_name'),
                icon_image,
                menu=menu
            )
            
            self.running = True
            
            # Show startup notification
            self.show_notification(
                self.get_message('app_name'),
                self.get_message('app_started')
            )
            
            # Start tray in separate thread
            tray_thread = threading.Thread(target=self.icon.run, daemon=True)
            tray_thread.start()
            
            print("✅ System tray started successfully")
            
        except Exception as e:
            print(f"❌ Failed to start system tray: {e}")
            print("   Using fallback notification system")
    
    def stop_tray(self):
        """Stop system tray | 停止系统托盘"""
        if self.icon and self.running:
            try:
                self.icon.stop()
                self.running = False
                print("✅ System tray stopped")
            except:
                pass
    
    def show_notification(self, title: str, message: str, timeout: int = 5):
        """Show desktop notification with fallbacks | 显示桌面通知（带备用方案）"""
        # Try advanced notification first
        try:
            # Try plyer first (if available and working)
            try:
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    timeout=timeout,
                    app_name=self.get_message('app_name')
                )
                return
            except:
                pass
            
            # Use fallback notification
            show_notification_fallback(title, message, timeout)
            
        except Exception as e:
            # Ultimate fallback
            print(f"🔔 {title}: {message}")
    
    def notify_assignments(self, assignment_count: int, overdue_count: int = 0):
        """Notify about assignments | 通知作业情况"""
        if overdue_count > 0:
            title = self.get_message('assignment_notification')
            message = f"{self.get_message('overdue_assignments')} ({overdue_count})"
        elif assignment_count > 0:
            title = self.get_message('assignment_notification')
            message = f"{self.get_message('new_assignments')} ({assignment_count})"
        else:
            return
        
        self.show_notification(title, message)
    
    def show_app(self, icon=None, item=None):
        """Show main application | 显示主应用程序"""
        if self.app_callback:
            self.app_callback('show')
        print("📱 Show application requested")
    
    def check_assignments(self, icon=None, item=None):
        """Check assignments | 检查作业"""
        if self.app_callback:
            self.app_callback('check')
        print("🔍 Check assignments requested")
    
    def open_reports(self, icon=None, item=None):
        """Open reports folder | 打开报告文件夹"""
        reports_dir = Path("reports")
        if reports_dir.exists():
            system = platform.system().lower()
            try:
                if system == "darwin":
                    subprocess.run(['open', str(reports_dir)])
                elif system == "windows":
                    subprocess.run(['explorer', str(reports_dir)])
                else:
                    subprocess.run(['xdg-open', str(reports_dir)])
            except Exception as e:
                print(f"❌ Could not open reports folder: {e}")
        else:
            self.show_notification(
                self.get_message('app_name'),
                "Reports folder not found" if self.language == 'en' else "未找到报告文件夹"
            )
    
    def show_settings(self, icon=None, item=None):
        """Show settings | 显示设置"""
        if self.app_callback:
            self.app_callback('settings')
        print("⚙️ Settings requested")
    
    def show_about(self, icon=None, item=None):
        """Show about dialog | 显示关于对话框"""
        webbrowser.open("https://github.com/Hacker0458/managebac-assignment-checker")
    
    def quit_app(self, icon=None, item=None):
        """Quit application | 退出应用程序"""
        if self.app_callback:
            self.app_callback('quit')
        self.stop_tray()
        print("👋 Application quit requested")


class ImprovedNotificationManager:
    """Improved desktop notification manager | 改进的桌面通知管理器"""
    
    def __init__(self, language: str = 'zh'):
        self.language = language
        self.enabled = True
    
    def is_available(self) -> bool:
        """Check if notifications are available | 检查通知是否可用"""
        return self.enabled
    
    def send_notification(self, title: str, message: str, timeout: int = 5):
        """Send desktop notification with fallbacks | 发送桌面通知（带备用方案）"""
        show_notification_fallback(title, message, timeout)
    
    def notify_assignment_reminder(self, assignments: list):
        """Send assignment reminder notification | 发送作业提醒通知"""
        if not assignments:
            return
        
        overdue = [a for a in assignments if a.get('status') == 'overdue']
        high_priority = [a for a in assignments if a.get('priority') == 'high']
        
        if overdue:
            title = "⚠️ Overdue Assignments" if self.language == 'en' else "⚠️ 逾期作业"
            message = f"You have {len(overdue)} overdue assignments!" if self.language == 'en' else f"您有{len(overdue)}个逾期作业！"
            self.send_notification(title, message, timeout=10)
        
        elif high_priority:
            title = "🔥 High Priority Assignments" if self.language == 'en' else "🔥 高优先级作业"
            message = f"You have {len(high_priority)} high priority assignments" if self.language == 'en' else f"您有{len(high_priority)}个高优先级作业"
            self.send_notification(title, message, timeout=8)
        
        else:
            title = "📚 Assignment Update" if self.language == 'en' else "📚 作业更新"
            message = f"Found {len(assignments)} assignments" if self.language == 'en' else f"找到{len(assignments)}个作业"
            self.send_notification(title, message)
    
    def notify_ai_analysis_complete(self):
        """Notify when AI analysis is complete | AI分析完成时通知"""
        title = "🤖 AI Analysis Complete" if self.language == 'en' else "🤖 AI分析完成"
        message = "AI analysis has been completed with new suggestions" if self.language == 'en' else "AI分析已完成，包含新建议"
        self.send_notification(title, message)
    
    def notify_report_generated(self, report_path: str):
        """Notify when report is generated | 报告生成时通知"""
        title = "📊 Report Generated" if self.language == 'en' else "📊 报告已生成"
        message = f"Report saved successfully" if self.language == 'en' else f"报告已成功保存"
        self.send_notification(title, message)


if __name__ == "__main__":
    # Test improved system tray functionality
    def test_callback(action):
        print(f"Callback received: {action}")
        if action == 'quit':
            import time
            time.sleep(1)
            exit(0)
    
    print("🧪 Testing improved system tray functionality...")
    
    tray_manager = ImprovedSystemTrayManager(test_callback, 'zh')
    tray_manager.start_tray()
    
    # Test notifications
    notification_manager = ImprovedNotificationManager('zh')
    notification_manager.send_notification("测试通知", "这是一个测试通知消息")
    
    # Keep the script running
    try:
        import time
        while tray_manager.running or not TRAY_AVAILABLE:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping improved system tray...")
        tray_manager.stop_tray()
