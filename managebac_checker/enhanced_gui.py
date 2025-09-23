#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 Enhanced ManageBac Assignment Checker GUI | 增强版ManageBac作业检查器GUI
Complete desktop application with all features integrated
集成所有功能的完整桌面应用程序
"""

import os
import sys
import json
import asyncio
import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import tkinter.font as tkfont

# Import our modules
from .gui import ManageBacGUI, ModernTheme, ConfigDialog, AssignmentCard, StatusBar, AnimatedButton
from .system_tray import SystemTrayManager, NotificationManager
from .config import Config
from .checker import ManageBacChecker


class EnhancedManageBacGUI(ManageBacGUI):
    """Enhanced GUI with system tray and advanced features | 增强版GUI，包含系统托盘和高级功能"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize additional components
        self.tray_manager = None
        self.notification_manager = NotificationManager('zh')
        self.auto_check_enabled = False
        self.auto_check_interval = 30  # minutes
        self.minimize_to_tray = True
        
        # Add system tray support
        self._setup_system_tray()
        
        # Add minimize to tray behavior
        self._setup_window_behavior()
        
        # Add auto-refresh timer
        self._setup_auto_refresh()
        
        # Load user preferences
        self._load_user_preferences()
    
    def _setup_system_tray(self):
        """Setup system tray integration | 设置系统托盘集成"""
        try:
            self.tray_manager = SystemTrayManager(
                app_callback=self._handle_tray_callback,
                language='zh'
            )
            self.tray_manager.start_tray()
        except Exception as e:
            print(f"⚠️ System tray not available: {e}")
            self.tray_manager = None
    
    def _setup_window_behavior(self):
        """Setup window behavior for minimize to tray | 设置窗口行为以支持最小化到托盘"""
        # Override window close behavior
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Bind window state change
        self.root.bind("<Unmap>", self._on_window_minimize)
        self.root.bind("<Map>", self._on_window_restore)
    
    def _setup_auto_refresh(self):
        """Setup automatic assignment checking | 设置自动作业检查"""
        self.auto_check_timer = None
        self._schedule_auto_check()
    
    def _load_user_preferences(self):
        """Load user preferences | 加载用户偏好"""
        prefs_file = Path("user_preferences.json")
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                
                self.auto_check_enabled = prefs.get('auto_check_enabled', False)
                self.auto_check_interval = prefs.get('auto_check_interval', 30)
                self.minimize_to_tray = prefs.get('minimize_to_tray', True)
                
                # Apply theme
                theme_name = prefs.get('theme', 'light')
                self.theme = ModernTheme(theme_name)
                
                # Apply window settings
                window_settings = prefs.get('window', {})
                if 'geometry' in window_settings:
                    self.root.geometry(window_settings['geometry'])
                
            except Exception as e:
                print(f"⚠️ Error loading preferences: {e}")
    
    def _save_user_preferences(self):
        """Save user preferences | 保存用户偏好"""
        prefs = {
            'auto_check_enabled': self.auto_check_enabled,
            'auto_check_interval': self.auto_check_interval,
            'minimize_to_tray': self.minimize_to_tray,
            'theme': self.theme.current_theme,
            'window': {
                'geometry': self.root.geometry()
            }
        }
        
        try:
            with open("user_preferences.json", 'w', encoding='utf-8') as f:
                json.dump(prefs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving preferences: {e}")
    
    def _handle_tray_callback(self, action: str):
        """Handle system tray callbacks | 处理系统托盘回调"""
        if action == 'show':
            self._show_window()
        elif action == 'check':
            self._check_assignments()
        elif action == 'settings':
            self._open_settings()
        elif action == 'quit':
            self._quit_application()
    
    def _on_window_close(self):
        """Handle window close event | 处理窗口关闭事件"""
        if self.minimize_to_tray and self.tray_manager:
            self._hide_window()
            self.notification_manager.send_notification(
                "ManageBac检查器",
                "应用程序已最小化到系统托盘"
            )
        else:
            self._quit_application()
    
    def _on_window_minimize(self, event):
        """Handle window minimize | 处理窗口最小化"""
        if self.minimize_to_tray and self.tray_manager and event.widget == self.root:
            self.root.after(100, self._hide_window)
    
    def _on_window_restore(self, event):
        """Handle window restore | 处理窗口恢复"""
        if event.widget == self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
    
    def _hide_window(self):
        """Hide window to system tray | 隐藏窗口到系统托盘"""
        self.root.withdraw()
    
    def _show_window(self):
        """Show window from system tray | 从系统托盘显示窗口"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def _schedule_auto_check(self):
        """Schedule automatic assignment checking | 安排自动作业检查"""
        if self.auto_check_timer:
            self.root.after_cancel(self.auto_check_timer)
        
        if self.auto_check_enabled:
            # Schedule next check
            interval_ms = self.auto_check_interval * 60 * 1000  # Convert minutes to milliseconds
            self.auto_check_timer = self.root.after(interval_ms, self._auto_check_assignments)
    
    def _auto_check_assignments(self):
        """Automatically check assignments | 自动检查作业"""
        print("🔄 Auto-checking assignments...")
        
        # Run check in background
        def auto_check_thread():
            try:
                # Simulate checking (replace with actual implementation)
                import time
                time.sleep(2)
                
                # Notify if new assignments found
                if self.assignments:
                    self.notification_manager.notify_assignment_reminder(self.assignments)
                
            except Exception as e:
                print(f"❌ Auto-check failed: {e}")
            finally:
                # Schedule next check
                self.root.after(0, self._schedule_auto_check)
        
        threading.Thread(target=auto_check_thread, daemon=True).start()
    
    def _create_menu_bar(self):
        """Override to add more menu items | 重写以添加更多菜单项"""
        super()._create_menu_bar()
        
        # Add preferences menu
        menubar = self.root.nametowidget(self.root['menu'])
        
        # Preferences menu
        prefs_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎛️ Preferences | 偏好设置", menu=prefs_menu)
        prefs_menu.add_command(label="⚙️ General Settings | 常规设置", command=self._show_preferences)
        prefs_menu.add_command(label="🔔 Notifications | 通知设置", command=self._show_notification_settings)
        prefs_menu.add_command(label="🎨 Appearance | 外观设置", command=self._show_appearance_settings)
        prefs_menu.add_separator()
        prefs_menu.add_command(label="📱 System Tray | 系统托盘", command=self._toggle_system_tray)
        prefs_menu.add_command(label="🔄 Auto Check | 自动检查", command=self._toggle_auto_check)
    
    def _show_preferences(self):
        """Show general preferences dialog | 显示常规偏好设置对话框"""
        prefs_window = tk.Toplevel(self.root)
        prefs_window.title("⚙️ General Preferences | 常规偏好设置")
        prefs_window.geometry("500x400")
        prefs_window.configure(bg=self.theme.get_color('bg'))
        prefs_window.transient(self.root)
        prefs_window.grab_set()
        
        # Center window
        prefs_window.update_idletasks()
        x = (prefs_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (prefs_window.winfo_screenheight() // 2) - (400 // 2)
        prefs_window.geometry(f"500x400+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(prefs_window, bg=self.theme.get_color('bg'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="⚙️ General Preferences | 常规偏好设置",
            font=('Segoe UI', 16, 'bold'),
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg')
        ).pack(pady=(0, 20))
        
        # Auto-check settings
        auto_frame = tk.LabelFrame(
            main_frame,
            text="🔄 Automatic Checking | 自动检查",
            font=('Segoe UI', 12, 'bold'),
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg')
        )
        auto_frame.pack(fill='x', pady=(0, 15))
        
        auto_check_var = tk.BooleanVar(value=self.auto_check_enabled)
        tk.Checkbutton(
            auto_frame,
            text="Enable automatic assignment checking | 启用自动作业检查",
            variable=auto_check_var,
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg'),
            font=('Segoe UI', 10)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Interval setting
        interval_frame = tk.Frame(auto_frame, bg=self.theme.get_color('bg'))
        interval_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            interval_frame,
            text="Check interval (minutes) | 检查间隔（分钟）:",
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg'),
            font=('Segoe UI', 10)
        ).pack(side='left')
        
        interval_var = tk.IntVar(value=self.auto_check_interval)
        interval_spin = tk.Spinbox(
            interval_frame,
            from_=5,
            to=120,
            textvariable=interval_var,
            width=10,
            font=('Segoe UI', 10)
        )
        interval_spin.pack(side='right')
        
        # Window behavior settings
        window_frame = tk.LabelFrame(
            main_frame,
            text="🪟 Window Behavior | 窗口行为",
            font=('Segoe UI', 12, 'bold'),
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg')
        )
        window_frame.pack(fill='x', pady=(0, 15))
        
        minimize_var = tk.BooleanVar(value=self.minimize_to_tray)
        tk.Checkbutton(
            window_frame,
            text="Minimize to system tray | 最小化到系统托盘",
            variable=minimize_var,
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg'),
            font=('Segoe UI', 10)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.get_color('bg'))
        button_frame.pack(fill='x', pady=(20, 0))
        
        def save_preferences():
            self.auto_check_enabled = auto_check_var.get()
            self.auto_check_interval = interval_var.get()
            self.minimize_to_tray = minimize_var.get()
            
            self._save_user_preferences()
            self._schedule_auto_check()
            
            messagebox.showinfo(
                "Success | 成功",
                "✅ Preferences saved successfully!\n✅ 偏好设置保存成功！"
            )
            prefs_window.destroy()
        
        AnimatedButton(
            button_frame,
            self.theme,
            text="💾 Save | 保存",
            command=save_preferences
        ).pack(side='right', padx=(10, 0))
        
        AnimatedButton(
            button_frame,
            self.theme,
            text="❌ Cancel | 取消",
            command=prefs_window.destroy
        ).pack(side='right')
    
    def _show_notification_settings(self):
        """Show notification settings | 显示通知设置"""
        messagebox.showinfo(
            "Notifications | 通知",
            "🔔 Notification settings\n🔔 通知设置\n\nDesktop notifications are enabled by default.\n桌面通知默认启用。"
        )
    
    def _show_appearance_settings(self):
        """Show appearance settings | 显示外观设置"""
        appearance_window = tk.Toplevel(self.root)
        appearance_window.title("🎨 Appearance Settings | 外观设置")
        appearance_window.geometry("400x300")
        appearance_window.configure(bg=self.theme.get_color('bg'))
        appearance_window.transient(self.root)
        appearance_window.grab_set()
        
        # Center window
        appearance_window.update_idletasks()
        x = (appearance_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (appearance_window.winfo_screenheight() // 2) - (300 // 2)
        appearance_window.geometry(f"400x300+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(appearance_window, bg=self.theme.get_color('bg'))
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="🎨 Appearance Settings | 外观设置",
            font=('Segoe UI', 16, 'bold'),
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg')
        ).pack(pady=(0, 20))
        
        # Theme selection
        theme_frame = tk.LabelFrame(
            main_frame,
            text="🌈 Theme | 主题",
            font=('Segoe UI', 12, 'bold'),
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg')
        )
        theme_frame.pack(fill='x', pady=(0, 15))
        
        theme_var = tk.StringVar(value=self.theme.current_theme)
        
        tk.Radiobutton(
            theme_frame,
            text="🌞 Light Theme | 浅色主题",
            variable=theme_var,
            value='light',
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg'),
            font=('Segoe UI', 10)
        ).pack(anchor='w', padx=10, pady=5)
        
        tk.Radiobutton(
            theme_frame,
            text="🌙 Dark Theme | 深色主题",
            variable=theme_var,
            value='dark',
            bg=self.theme.get_color('bg'),
            fg=self.theme.get_color('fg'),
            font=('Segoe UI', 10)
        ).pack(anchor='w', padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.get_color('bg'))
        button_frame.pack(fill='x', pady=(20, 0))
        
        def apply_theme():
            new_theme = theme_var.get()
            if new_theme != self.theme.current_theme:
                self.theme = ModernTheme(new_theme)
                self._save_user_preferences()
                
                messagebox.showinfo(
                    "Theme Applied | 主题已应用",
                    "✅ Theme will be applied on next restart.\n✅ 主题将在下次重启时应用。"
                )
            
            appearance_window.destroy()
        
        AnimatedButton(
            button_frame,
            self.theme,
            text="🎨 Apply | 应用",
            command=apply_theme
        ).pack(side='right', padx=(10, 0))
        
        AnimatedButton(
            button_frame,
            self.theme,
            text="❌ Cancel | 取消",
            command=appearance_window.destroy
        ).pack(side='right')
    
    def _toggle_system_tray(self):
        """Toggle system tray | 切换系统托盘"""
        if self.tray_manager and self.tray_manager.running:
            self.tray_manager.stop_tray()
            messagebox.showinfo(
                "System Tray | 系统托盘",
                "❌ System tray disabled\n❌ 系统托盘已禁用"
            )
        else:
            self._setup_system_tray()
            messagebox.showinfo(
                "System Tray | 系统托盘",
                "✅ System tray enabled\n✅ 系统托盘已启用"
            )
    
    def _toggle_auto_check(self):
        """Toggle auto check | 切换自动检查"""
        self.auto_check_enabled = not self.auto_check_enabled
        self._schedule_auto_check()
        
        status = "enabled" if self.auto_check_enabled else "disabled"
        status_zh = "已启用" if self.auto_check_enabled else "已禁用"
        
        messagebox.showinfo(
            "Auto Check | 自动检查",
            f"🔄 Auto check {status}\n🔄 自动检查{status_zh}"
        )
    
    def _quit_application(self):
        """Quit the application completely | 完全退出应用程序"""
        # Save preferences
        self._save_user_preferences()
        
        # Stop system tray
        if self.tray_manager:
            self.tray_manager.stop_tray()
        
        # Cancel auto check timer
        if self.auto_check_timer:
            self.root.after_cancel(self.auto_check_timer)
        
        # Quit
        self.root.quit()
        self.root.destroy()
    
    def _on_assignments_loaded(self):
        """Override to add notification | 重写以添加通知"""
        super()._on_assignments_loaded()
        
        # Send notification about loaded assignments
        if self.assignments:
            self.notification_manager.notify_assignment_reminder(self.assignments)
            
            # Update tray with assignment count
            if self.tray_manager:
                overdue_count = len([a for a in self.assignments if a.get('status') == 'overdue'])
                self.tray_manager.notify_assignments(len(self.assignments), overdue_count)
    
    def _on_report_generated(self, html_file: Path):
        """Override to add notification | 重写以添加通知"""
        super()._on_report_generated(html_file)
        
        # Notify about report generation
        self.notification_manager.notify_report_generated(str(html_file))
    
    def run(self):
        """Start the enhanced GUI application | 启动增强版GUI应用程序"""
        try:
            # Show startup notification
            if self.tray_manager:
                self.notification_manager.send_notification(
                    "ManageBac检查器",
                    "应用程序已启动 - 点击系统托盘图标访问功能"
                )
            
            self.root.mainloop()
        except KeyboardInterrupt:
            self._quit_application()
        finally:
            # Cleanup
            if self.tray_manager:
                self.tray_manager.stop_tray()


def main():
    """Main function to run the enhanced GUI | 运行增强版GUI的主函数"""
    try:
        app = EnhancedManageBacGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start enhanced GUI application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
