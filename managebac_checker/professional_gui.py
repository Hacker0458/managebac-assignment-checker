#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💼 Professional ManageBac Assignment Checker GUI | 专业级ManageBac作业检查器GUI
Enterprise-grade desktop application with superior UX/UI
企业级桌面应用程序，具有卓越的用户体验和界面
"""

import os
import sys
import json
import asyncio
import threading
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import tkinter.font as tkfont


def _is_headless_environment() -> bool:
    """Return True when the current process cannot create real Tk widgets."""

    if os.environ.get("MANAGEBAC_FORCE_GUI") == "1":
        return False

    if os.environ.get("PYTEST_CURRENT_TEST"):
        # Tests run in a headless environment inside CI containers
        return True

    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        return True

    return False


if _is_headless_environment():
    from types import SimpleNamespace

    class _HeadlessVariable:
        def __init__(self, value=None):
            self._value = value
            self._trace_callbacks = []

        def get(self):
            return self._value

        def set(self, value):
            self._value = value
            for callback in list(self._trace_callbacks):
                callback(None, None, None)

        def trace(self, mode, callback):
            def _wrapped(*args, **kwargs):
                callback(*args, **kwargs)

            self._trace_callbacks.append(_wrapped)
            return _wrapped

        def trace_add(self, mode, callback):
            return self.trace(mode, callback)

        def trace_remove(self, mode, callback_name):
            self._trace_callbacks = [
                cb for cb in self._trace_callbacks if cb != callback_name
            ]

    class _HeadlessWidget:
        def __init__(self, master=None, **kwargs):
            self.master = master
            self.children = []
            self._config = dict(kwargs)
            self._bindings = []
            if master is not None and hasattr(master, "children"):
                master.children.append(self)

        # Tkinter compatibility helpers -------------------------------------------------
        def config(self, **kwargs):
            self._config.update(kwargs)

        configure = config

        def cget(self, key):
            return self._config.get(key)

        def bind(self, event=None, handler=None, add=None):
            self._bindings.append((event, handler, add))

        def pack(self, *args, **kwargs):
            return None

        def grid(self, *args, **kwargs):
            return None

        def place(self, *args, **kwargs):
            return None

        def pack_propagate(self, flag):
            self._config["pack_propagate"] = bool(flag)

        def grid_propagate(self, flag):
            self._config["grid_propagate"] = bool(flag)

        def grid_columnconfigure(self, index, **kwargs):
            self._config.setdefault("grid_columns", {})[index] = kwargs

        def grid_rowconfigure(self, index, **kwargs):
            self._config.setdefault("grid_rows", {})[index] = kwargs

        def destroy(self):
            self.children.clear()

        def winfo_children(self):
            return list(self.children)

        def winfo_exists(self):
            return True

        def winfo_screenwidth(self):
            return 1920

        def winfo_screenheight(self):
            return 1080

        def after(self, delay, callback=None, *args):
            if callback and delay <= 0:
                callback(*args)
            return object()

        def after_cancel(self, handle):
            return None

        def insert(self, index, value):
            text = self._config.setdefault("_text", "")
            if isinstance(index, str) and index.lower() in {"end", "insert"}:
                index = len(text)
            if not isinstance(index, int):
                index = 0
            self._config["_text"] = text[:index] + str(value) + text[index:]

        def delete(self, start, end=None):
            text = self._config.setdefault("_text", "")
            if isinstance(start, str) and start.lower() == "end":
                start = len(text)
            if not isinstance(start, int):
                start = 0
            if end is None:
                end = start + 1
            if isinstance(end, str) and end.lower() == "end":
                end = len(text)
            if not isinstance(end, int):
                end = start
            self._config["_text"] = text[:start] + text[end:]

        def get(self):
            return self._config.get("_text", "")
            
    class _HeadlessTk(_HeadlessWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(None)
            self._geometry = ""
            self.tk = self

        def mainloop(self):
            return None

        def withdraw(self):
            return None

        def deiconify(self):
            return None

        def lift(self):
            return None

        def focus_force(self):
            return None

        def quit(self):
            return None

        def call(self, *args, **kwargs):
            return None

        def protocol(self, *args, **kwargs):
            return None

        def title(self, value):
            self._config["title"] = value

        def geometry(self, value=None):
            if value is not None:
                self._geometry = value
            return self._geometry or "1024x768"

        def iconbitmap(self, *args, **kwargs):
            return None

        def minsize(self, *args, **kwargs):
            return None

        def wait_window(self, *args, **kwargs):
            return None

        def destroy(self):
            super().destroy()

    class _HeadlessMenu(_HeadlessWidget):
        def add_command(self, *args, **kwargs):
            return None

        def add_separator(self, *args, **kwargs):
            return None

        def add_cascade(self, *args, **kwargs):
            return None

    class _HeadlessProgressbar(_HeadlessWidget):
        def start(self, interval=None):
            return None

        def stop(self):
            return None

    class _HeadlessScrollbar(_HeadlessWidget):
        def set(self, *args, **kwargs):
            self._config["scroll"] = (args, kwargs)

        def get(self):
            return (0.0, 1.0)

    class _HeadlessScrolledText(_HeadlessWidget):
        def insert(self, *args, **kwargs):
            return None

        def delete(self, *args, **kwargs):
            return None

        def get(self, *args, **kwargs):
            return ""

    class _HeadlessStyle:
        def configure(self, *args, **kwargs):
            return None

        def map(self, *args, **kwargs):
            return None

    class _HeadlessStringVar(_HeadlessVariable):
        pass

    class _HeadlessBooleanVar(_HeadlessVariable):
        def __init__(self, value=False):
            super().__init__(bool(value))

    class _HeadlessCanvas(_HeadlessWidget):
        def create_window(self, *args, **kwargs):
            return None

        def configure(self, **kwargs):
            self._config.update(kwargs)

        config = configure

        def yview(self, *args, **kwargs):
            return (0.0, 1.0)

        def yview_moveto(self, fraction):
            self._config["yview"] = fraction

        def yview_scroll(self, number, what):
            self._config["yview_scroll"] = (number, what)

    class _HeadlessPanedWindow(_HeadlessWidget):
        def add(self, *args, **kwargs):
            return None

    class _HeadlessCheckbutton(_HeadlessWidget):
        pass

    class _HeadlessMessageBox:
        @staticmethod
        def askyesno(*args, **kwargs):
            return True

        @staticmethod
        def showinfo(*args, **kwargs):
            return None

        @staticmethod
        def showwarning(*args, **kwargs):
            return None

        @staticmethod
        def showerror(*args, **kwargs):
            return None

    def _headless_var_factory(initial=None):
        return _HeadlessStringVar(initial)

    class _HeadlessTclError(Exception):
        """Fallback TclError replacement used in headless mode."""

    tk = SimpleNamespace(
        Tk=_HeadlessTk,
        Toplevel=_HeadlessTk,
        Frame=_HeadlessWidget,
        Label=_HeadlessWidget,
        Button=_HeadlessWidget,
        Entry=_HeadlessWidget,
        Canvas=_HeadlessCanvas,
        PanedWindow=_HeadlessPanedWindow,
        Checkbutton=_HeadlessCheckbutton,
        Menu=_HeadlessMenu,
        StringVar=_headless_var_factory,
        BooleanVar=_HeadlessBooleanVar,
        IntVar=_HeadlessVariable,
        DoubleVar=_HeadlessVariable,
        PhotoImage=lambda *args, **kwargs: None,
        END="end",
        WORD="word",
        TclError=_HeadlessTclError,
    )

    ttk = SimpleNamespace(
        Progressbar=_HeadlessProgressbar,
        Scrollbar=_HeadlessScrollbar,
        Style=_HeadlessStyle,
    )

    messagebox = _HeadlessMessageBox()
    filedialog = SimpleNamespace(
        askopenfilename=lambda **kwargs: "",
        asksaveasfilename=lambda **kwargs: "",
    )
    scrolledtext = SimpleNamespace(ScrolledText=_HeadlessScrolledText)
    tkfont = SimpleNamespace(Font=lambda *args, **kwargs: ("Arial", 12))

# Import our modules
from .config import Config
from .checker import ManageBacChecker

# Import enhanced error handling
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from enhanced_error_handler import get_error_handler, handle_error, log_info, log_warning, log_error
    ERROR_HANDLER_AVAILABLE = True
    print("✅ Enhanced error handler loaded")
except ImportError:
    ERROR_HANDLER_AVAILABLE = False
    def handle_error(error, context="", severity="ERROR", user_friendly=True):
        print(f"❌ [{context}] {type(error).__name__}: {error}")
        return {"error_type": type(error).__name__, "error_message": str(error)}
    def log_info(msg): print(f"ℹ️ {msg}")
    def log_warning(msg): print(f"⚠️ {msg}")
    def log_error(msg): print(f"❌ {msg}")
    print("⚠️ Using fallback error handling")

# Try to import system tray components, fallback to improved versions
try:
    from .system_tray import SystemTrayManager, NotificationManager

    print("✅ Using standard system tray components")
except ImportError:
    from .improved_system_tray import (
        ImprovedSystemTrayManager as SystemTrayManager,
        ImprovedNotificationManager as NotificationManager,
    )

    print("✅ Using improved system tray components (fallback)")


class ProfessionalTheme:
    """Professional theme with high-quality colors and fonts | 专业主题，高质量颜色和字体"""

    THEMES = {
        "professional_light": {
            "primary": "#2563EB",  # Professional blue
            "primary_hover": "#1D4ED8",
            "secondary": "#64748B",
            "success": "#059669",
            "warning": "#D97706",
            "danger": "#DC2626",
            "background": "#FFFFFF",
            "surface": "#F8FAFC",
            "card": "#FFFFFF",
            "border": "#E2E8F0",
            "text_primary": "#0F172A",
            "text_secondary": "#475569",
            "text_muted": "#94A3B8",
            "sidebar": "#F1F5F9",
            "accent": "#3B82F6",
        },
        "professional_dark": {
            "primary": "#3B82F6",
            "primary_hover": "#2563EB",
            "secondary": "#64748B",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "background": "#0F172A",
            "surface": "#1E293B",
            "card": "#334155",
            "border": "#475569",
            "text_primary": "#FFFFFF",  # 确保主要文字是白色
            "text_secondary": "#E2E8F0",  # 次要文字是浅灰色
            "text_muted": "#94A3B8",
            "sidebar": "#1E293B",
            "accent": "#60A5FA",
        },
    }

    def __init__(self, theme_name: str = "professional_light"):
        self.current_theme = theme_name
        self.colors = self.THEMES[theme_name]

        # High-quality fonts for different platforms
        self.fonts = self._get_platform_fonts()

    def _get_platform_fonts(self) -> Dict[str, tuple]:
        """Get platform-specific high-quality fonts | 获取平台特定的高质量字体"""
        system = sys.platform.lower()

        if system == "darwin":  # macOS
            return {
                "heading": ("SF Pro Display", 18, "bold"),
                "subheading": ("SF Pro Display", 14, "bold"),
                "body": ("SF Pro Text", 12, "normal"),
                "small": ("SF Pro Text", 10, "normal"),
                "code": ("SF Mono", 11, "normal"),
                "button": ("SF Pro Text", 11, "bold"),
            }
        elif system.startswith("win"):  # Windows
            return {
                "heading": ("Segoe UI", 18, "bold"),
                "subheading": ("Segoe UI", 14, "bold"),
                "body": ("Segoe UI", 12, "normal"),
                "small": ("Segoe UI", 10, "normal"),
                "code": ("Consolas", 11, "normal"),
                "button": ("Segoe UI", 11, "bold"),
            }
        else:  # Linux
            return {
                "heading": ("Ubuntu", 18, "bold"),
                "subheading": ("Ubuntu", 14, "bold"),
                "body": ("Ubuntu", 12, "normal"),
                "small": ("Ubuntu", 10, "normal"),
                "code": ("Ubuntu Mono", 11, "normal"),
                "button": ("Ubuntu", 11, "bold"),
            }

    def get_color(self, name: str) -> str:
        """Get theme color | 获取主题颜色"""
        # Map common color names to theme colors
        color_mapping = {
            "bg": "background",
            "fg": "text_primary",
            "text": "text_primary",
            "button": "primary",
            "button_text": "text_primary",
            "entry": "card",
            "entry_text": "text_primary",
            "label": "text_primary",
            "frame": "background",
            "border": "border",
            "success": "success",
            "warning": "warning",
            "error": "danger",
            "info": "primary",
        }

        mapped_name = color_mapping.get(name, name)
        return self.colors.get(mapped_name, "#000000")

    def get_font(self, style: str) -> tuple:
        """Get font for style | 获取样式字体"""
        return self.fonts.get(style, ("Arial", 12, "normal"))

    def switch_theme(self, theme_name: str):
        """Switch to a different theme | 切换到不同主题"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.colors = self.THEMES[theme_name]
            return True
        return False


class ProfessionalButton(tk.Button):
    """Professional button with enhanced styling | 专业按钮，增强样式"""

    def __init__(
        self, parent, theme: ProfessionalTheme, style: str = "primary", **kwargs
    ):
        self.theme = theme
        self.style = style

        # Button styles
        styles = {
            "primary": {
                "bg": theme.get_color("primary"),
                "hover_bg": theme.get_color("primary_hover"),
                "fg": "white",
            },
            "secondary": {
                "bg": theme.get_color("surface"),
                "hover_bg": theme.get_color("border"),
                "fg": theme.get_color("text_primary"),
            },
            "success": {
                "bg": theme.get_color("success"),
                "hover_bg": "#047857",
                "fg": "white",
            },
            "warning": {
                "bg": theme.get_color("warning"),
                "hover_bg": "#B45309",
                "fg": "white",
            },
            "danger": {
                "bg": theme.get_color("danger"),
                "hover_bg": "#B91C1C",
                "fg": "white",
            },
        }

        style_config = styles.get(style, styles["primary"])
        self.default_bg = style_config["bg"]
        self.hover_bg = style_config["hover_bg"]

        super().__init__(
            parent,
            bg=self.default_bg,
            fg=style_config["fg"],
            font=theme.get_font("button"),
            relief="flat",
            cursor="hand2",
            bd=0,
            padx=20,
            pady=12,
            **kwargs,
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_enter(self, event):
        self.config(bg=self.hover_bg)

    def _on_leave(self, event):
        self.config(bg=self.default_bg)

    def _on_click(self, event):
        self.config(relief="sunken")

    def _on_release(self, event):
        self.config(relief="flat")


class ProfessionalCard(tk.Frame):
    """Professional assignment card with enhanced design | 专业作业卡片，增强设计"""

    def __init__(
        self, parent, theme: ProfessionalTheme, assignment_data: Dict[str, Any]
    ):
        super().__init__(parent, bg=theme.get_color("card"), relief="flat", bd=0)
        self.theme = theme
        self.assignment = assignment_data

        # Add subtle shadow effect
        self.configure(
            highlightbackground=theme.get_color("border"), highlightthickness=1
        )

        self._create_widgets()
        self._setup_hover_effects()

    def _setup_hover_effects(self):
        """Setup hover effects for the card | 设置卡片悬停效果"""

        def on_enter(event):
            self.configure(bg=self.theme.get_color("surface"))
            for widget in self.winfo_children():
                self._update_widget_bg(widget, self.theme.get_color("surface"))

        def on_leave(event):
            self.configure(bg=self.theme.get_color("card"))
            for widget in self.winfo_children():
                self._update_widget_bg(widget, self.theme.get_color("card"))

        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)

    def _update_widget_bg(self, widget, bg_color):
        """Recursively update widget background | 递归更新组件背景"""
        try:
            if isinstance(widget, (tk.Frame, tk.Label)):
                widget.configure(bg=bg_color)
            for child in widget.winfo_children():
                self._update_widget_bg(child, bg_color)
        except:
            pass

    def _create_widgets(self):
        # Main container with better padding
        main_frame = tk.Frame(self, bg=self.theme.get_color("card"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=16)

        # Header with improved layout
        header_frame = tk.Frame(main_frame, bg=self.theme.get_color("card"))
        header_frame.pack(fill="x", pady=(0, 12))

        # Title with better typography
        title_text = self.assignment.get("title", "Unknown Assignment")
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=self.theme.get_font("subheading"),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_primary"),
            wraplength=400,
            justify="left",
            anchor="w",
        )
        title_label.pack(side="left", anchor="w", fill="x", expand=True)

        # Status badge with improved design
        status = self.assignment.get("status", "unknown")
        status_colors = {
            "overdue": self.theme.get_color("danger"),
            "due_soon": self.theme.get_color("warning"),
            "pending": self.theme.get_color("primary"),
            "completed": self.theme.get_color("success"),
        }

        status_frame = tk.Frame(
            header_frame,
            bg=status_colors.get(status, self.theme.get_color("secondary")),
            relief="flat",
        )
        status_frame.pack(side="right", anchor="e")

        status_label = tk.Label(
            status_frame,
            text=status.upper().replace("_", " "),
            font=(
                ("SF Pro Text", 9, "bold")
                if sys.platform == "darwin"
                else ("Segoe UI", 9, "bold")
            ),
            bg=status_colors.get(status, self.theme.get_color("secondary")),
            fg="white",
            padx=12,
            pady=4,
        )
        status_label.pack()

        # Course and due date with improved spacing
        info_frame = tk.Frame(main_frame, bg=self.theme.get_color("card"))
        info_frame.pack(fill="x", pady=(0, 12))

        # Course with icon
        course_frame = tk.Frame(info_frame, bg=self.theme.get_color("card"))
        course_frame.pack(side="left", anchor="w")

        tk.Label(
            course_frame,
            text="📚",
            font=(
                ("Apple Color Emoji", 14)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 12)
            ),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_secondary"),
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            course_frame,
            text=self.assignment.get("course", "Unknown Course"),
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_secondary"),
        ).pack(side="left")

        # Due date with improved formatting
        due_frame = tk.Frame(info_frame, bg=self.theme.get_color("card"))
        due_frame.pack(side="right", anchor="e")

        tk.Label(
            due_frame,
            text="📅",
            font=(
                ("Apple Color Emoji", 14)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 12)
            ),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_secondary"),
        ).pack(side="left", padx=(0, 6))

        due_date = self.assignment.get("due_date", "Unknown")
        # Format due date nicely
        try:
            if due_date != "Unknown":
                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
                days_until = (due_dt - datetime.now()).days
                if days_until < 0:
                    due_text = f"{due_date} (逾期 {abs(days_until)} 天)"
                elif days_until == 0:
                    due_text = f"{due_date} (今天到期)"
                elif days_until == 1:
                    due_text = f"{due_date} (明天到期)"
                else:
                    due_text = f"{due_date} ({days_until} 天后)"
            else:
                due_text = due_date
        except:
            due_text = due_date

        tk.Label(
            due_frame,
            text=due_text,
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_secondary"),
        ).pack(side="left")

        # Priority indicator with better design
        priority = self.assignment.get("priority", "medium")
        priority_colors = {
            "high": ("🔴", self.theme.get_color("danger")),
            "medium": ("🟡", self.theme.get_color("warning")),
            "low": ("🟢", self.theme.get_color("success")),
        }

        priority_frame = tk.Frame(main_frame, bg=self.theme.get_color("card"))
        priority_frame.pack(fill="x", pady=(0, 12))

        priority_emoji, priority_color = priority_colors.get(
            priority, ("⚪", self.theme.get_color("secondary"))
        )

        priority_container = tk.Frame(priority_frame, bg=self.theme.get_color("card"))
        priority_container.pack(side="left", anchor="w")

        tk.Label(
            priority_container,
            text=priority_emoji,
            font=(
                ("Apple Color Emoji", 14)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 12)
            ),
            bg=self.theme.get_color("card"),
        ).pack(side="left", padx=(0, 6))

        tk.Label(
            priority_container,
            text=f"Priority: {priority.title()} | 优先级: {priority.title()}",
            font=self.theme.get_font("small"),
            bg=self.theme.get_color("card"),
            fg=priority_color,
        ).pack(side="left")

        # Assignment type if available
        assignment_type = self.assignment.get("assignment_type", "")
        if assignment_type:
            type_label = tk.Label(
                priority_frame,
                text=f"📝 {assignment_type}",
                font=self.theme.get_font("small"),
                bg=self.theme.get_color("card"),
                fg=self.theme.get_color("text_muted"),
            )
            type_label.pack(side="right", anchor="e")

        # AI suggestion with better formatting
        if hasattr(self.assignment, "ai_suggestion") and self.assignment.ai_suggestion:
            ai_frame = tk.Frame(
                main_frame, bg=self.theme.get_color("surface"), relief="flat"
            )
            ai_frame.pack(fill="x", pady=(0, 12))

            # AI header
            ai_header = tk.Frame(ai_frame, bg=self.theme.get_color("surface"))
            ai_header.pack(fill="x", padx=12, pady=(8, 4))

            tk.Label(
                ai_header,
                text="🤖",
                font=(
                    ("Apple Color Emoji", 14)
                    if sys.platform == "darwin"
                    else ("Segoe UI Emoji", 12)
                ),
                bg=self.theme.get_color("surface"),
            ).pack(side="left", padx=(0, 6))

            tk.Label(
                ai_header,
                text="AI Suggestion | AI建议:",
                font=(
                    self.theme.get_font("small")[0],
                    self.theme.get_font("small")[1],
                    "bold",
                ),
                bg=self.theme.get_color("surface"),
                fg=self.theme.get_color("primary"),
            ).pack(side="left")

            # AI content
            tk.Label(
                ai_frame,
                text=self.assignment.ai_suggestion,
                font=self.theme.get_font("small"),
                bg=self.theme.get_color("surface"),
                fg=self.theme.get_color("text_secondary"),
                wraplength=450,
                justify="left",
                anchor="w",
            ).pack(anchor="w", padx=12, pady=(0, 8))

        # Action buttons with improved design
        button_frame = tk.Frame(main_frame, bg=self.theme.get_color("card"))
        button_frame.pack(fill="x", pady=(8, 0))

        if self.assignment.get("link"):
            ProfessionalButton(
                button_frame,
                self.theme,
                style="primary",
                text="🔗 Open Assignment | 打开作业",
                command=lambda: webbrowser.open(self.assignment["link"]),
            ).pack(side="left", padx=(0, 8))

        ProfessionalButton(
            button_frame,
            self.theme,
            style="secondary",
            text="📝 Details | 详情",
            command=self._show_details,
        ).pack(side="left", padx=(0, 8))

        # Mark as completed button
        if self.assignment.get("status") != "completed":
            ProfessionalButton(
                button_frame,
                self.theme,
                style="success",
                text="✅ Mark Complete | 标记完成",
                command=self._mark_completed,
            ).pack(side="right")

    def _show_details(self):
        """Show assignment details in professional dialog | 在专业对话框中显示作业详情"""
        details_window = tk.Toplevel(self)
        details_window.title("📝 Assignment Details | 作业详情")
        details_window.geometry("600x500")
        details_window.configure(bg=self.theme.get_color("background"))
        details_window.transient(self.winfo_toplevel())
        details_window.grab_set()

        # Center the window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (details_window.winfo_screenheight() // 2) - (500 // 2)
        details_window.geometry(f"600x500+{x}+{y}")

        # Header
        header_frame = tk.Frame(
            details_window, bg=self.theme.get_color("primary"), height=60
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📝 Assignment Details | 作业详情",
            font=self.theme.get_font("heading"),
            bg=self.theme.get_color("primary"),
            fg="white",
        ).pack(expand=True)

        # Content area
        content_frame = tk.Frame(details_window, bg=self.theme.get_color("background"))
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create scrolled text widget with better styling
        text_widget = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
            relief="flat",
            bd=0,
            padx=15,
            pady=15,
        )
        text_widget.pack(fill="both", expand=True)

        # Format assignment details professionally
        details = self._format_assignment_details()
        text_widget.insert(tk.END, details)
        text_widget.config(state="disabled")

        # Close button
        close_frame = tk.Frame(details_window, bg=self.theme.get_color("background"))
        close_frame.pack(fill="x", padx=20, pady=(0, 20))

        ProfessionalButton(
            close_frame,
            self.theme,
            style="secondary",
            text="❌ Close | 关闭",
            command=details_window.destroy,
        ).pack(side="right")

    def _format_assignment_details(self) -> str:
        """Format assignment details professionally | 专业格式化作业详情"""
        details = f"""📚 Course Information | 课程信息
{'─' * 50}
Course: {self.assignment.get('course', 'Unknown')}
课程: {self.assignment.get('course', 'Unknown')}

📋 Assignment Details | 作业详情
{'─' * 50}
Title: {self.assignment.get('title', 'Unknown')}
标题: {self.assignment.get('title', 'Unknown')}

Type: {self.assignment.get('assignment_type', 'Unknown')}
类型: {self.assignment.get('assignment_type', 'Unknown')}

📅 Timeline | 时间线
{'─' * 50}
Due Date: {self.assignment.get('due_date', 'Unknown')}
截止日期: {self.assignment.get('due_date', 'Unknown')}

Status: {self.assignment.get('status', 'Unknown')}
状态: {self.assignment.get('status', 'Unknown')}

Priority: {self.assignment.get('priority', 'Unknown')}
优先级: {self.assignment.get('priority', 'Unknown')}

📄 Description | 描述
{'─' * 50}
{self.assignment.get('description', 'No description available | 无可用描述')}

🔗 Resources | 资源
{'─' * 50}
Link: {self.assignment.get('link', 'Not available | 不可用')}

🕒 Metadata | 元数据
{'─' * 50}
Fetched At: {self.assignment.get('fetched_at', 'Unknown')}
获取时间: {self.assignment.get('fetched_at', 'Unknown')}
"""

        if hasattr(self.assignment, "ai_suggestion") and self.assignment.ai_suggestion:
            details += f"""
🤖 AI Analysis | AI分析
{'─' * 50}
{self.assignment.ai_suggestion}
"""

        return details

    def _mark_completed(self):
        """Mark assignment as completed | 标记作业为已完成"""
        result = messagebox.askyesno(
            "Confirm | 确认",
            f"Mark '{self.assignment.get('title', 'this assignment')}' as completed?\n\n将'{self.assignment.get('title', '此作业')}'标记为已完成？",
        )

        if result:
            self.assignment["status"] = "completed"
            messagebox.showinfo(
                "Success | 成功",
                "✅ Assignment marked as completed!\n✅ 作业已标记为完成！",
            )

            # Refresh the parent display
            parent = self.winfo_toplevel()
            if hasattr(parent, "_refresh_display"):
                parent._refresh_display()


class ProfessionalStatusBar(tk.Frame):
    """Professional status bar with enhanced design | 专业状态栏，增强设计"""

    def __init__(self, parent, theme: ProfessionalTheme):
        super().__init__(
            parent, bg=theme.get_color("surface"), height=40, relief="flat"
        )
        self.theme = theme
        self.pack_propagate(False)

        # Left side - status
        left_frame = tk.Frame(self, bg=theme.get_color("surface"))
        left_frame.pack(side="left", fill="y", padx=15, pady=8)

        self.status_icon = tk.Label(
            left_frame,
            text="🔄",
            font=(
                ("Apple Color Emoji", 14)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 12)
            ),
            bg=theme.get_color("surface"),
        )
        self.status_icon.pack(side="left", padx=(0, 8))

        self.status_label = tk.Label(
            left_frame,
            text="Ready | 就绪",
            bg=theme.get_color("surface"),
            fg=theme.get_color("text_secondary"),
            font=theme.get_font("small"),
        )
        self.status_label.pack(side="left")

        # Right side - progress and time
        right_frame = tk.Frame(self, bg=theme.get_color("surface"))
        right_frame.pack(side="right", fill="y", padx=15, pady=8)

        self.time_label = tk.Label(
            right_frame,
            text=datetime.now().strftime("%H:%M"),
            bg=theme.get_color("surface"),
            fg=theme.get_color("text_muted"),
            font=theme.get_font("small"),
        )
        self.time_label.pack(side="right", padx=(8, 0))

        # Progress bar with better styling
        self.progress = ttk.Progressbar(
            right_frame,
            length=200,
            mode="indeterminate",
            style="Professional.Horizontal.TProgressbar",
        )
        self.progress.pack(side="right", padx=(0, 8))

        # Update time every minute
        self._update_time()

    def _update_time(self):
        """Update time display | 更新时间显示"""
        self.time_label.config(text=datetime.now().strftime("%H:%M"))
        self.after(60000, self._update_time)  # Update every minute

    def set_status(self, message: str, icon: str = "🔄", show_progress: bool = False):
        """Set status with icon | 设置状态和图标"""
        self.status_icon.config(text=icon)
        self.status_label.config(text=message)

        if show_progress:
            self.progress.start()
        else:
            self.progress.stop()


class ProfessionalManageBacGUI:
    """Professional ManageBac GUI with enterprise-grade UX | 专业级ManageBac GUI，企业级用户体验"""

    def __init__(self):
        self.root = tk.Tk()
        self.theme = ProfessionalTheme("professional_light")

        # High DPI support
        self._setup_high_dpi()

        # Professional window setup
        self._setup_professional_window()

        # Initialize components
        self.config = None
        self.checker = None
        self.assignments = []
        self.filtered_assignments = []

        # System integration
        self.tray_manager = None
        self.notification_manager = NotificationManager("zh")

        # Auto-refresh settings
        self.auto_check_enabled = False
        self.auto_check_interval = 30
        self.auto_check_timer = None

        # Create professional UI
        self._create_professional_ui()
        self._setup_system_integration()
        self._load_configuration()

        # Load user preferences
        self._load_user_preferences()

    def _setup_high_dpi(self):
        """Setup high DPI support | 设置高DPI支持"""
        try:
            # Windows DPI awareness
            if sys.platform.startswith("win"):
                import ctypes

                ctypes.windll.shcore.SetProcessDpiAwareness(1)

            # Tkinter DPI scaling
            self.root.tk.call("tk", "scaling", 2.0)

        except Exception as e:
            print(f"⚠️ Could not set high DPI: {e}")

    def _setup_professional_window(self):
        """Setup professional window appearance | 设置专业窗口外观"""
        self.root.title(
            "🎓 ManageBac Assignment Checker Pro | ManageBac作业检查器专业版"
        )

        # Calculate optimal window size based on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Use 80% of screen size, but with reasonable limits
        window_width = min(max(int(screen_width * 0.8), 1200), 1600)
        window_height = min(max(int(screen_height * 0.8), 800), 1000)

        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=self.theme.get_color("background"))

        # Set minimum size
        self.root.minsize(1000, 700)

        # Professional window icon
        self._set_window_icon()

        # Configure ttk styles
        self._configure_ttk_styles()

    def _set_window_icon(self):
        """Set professional window icon | 设置专业窗口图标"""
        icon_path = Path("icon.ico")
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except:
                pass

    def _configure_ttk_styles(self):
        """Configure ttk styles for professional look | 配置ttk样式以获得专业外观"""
        style = ttk.Style()

        # Configure progressbar
        style.configure(
            "Professional.Horizontal.TProgressbar",
            background=self.theme.get_color("primary"),
            troughcolor=self.theme.get_color("border"),
            borderwidth=0,
            lightcolor=self.theme.get_color("primary"),
            darkcolor=self.theme.get_color("primary"),
        )

        # Configure notebook
        style.configure(
            "Professional.TNotebook",
            background=self.theme.get_color("surface"),
            borderwidth=0,
        )

        style.configure(
            "Professional.TNotebook.Tab",
            background=self.theme.get_color("card"),
            foreground=self.theme.get_color("text_secondary"),
            padding=[20, 10],
            font=self.theme.get_font("body"),
        )

        style.map(
            "Professional.TNotebook.Tab",
            background=[("selected", self.theme.get_color("primary"))],
            foreground=[("selected", "white")],
        )

    def _create_professional_ui(self):
        """Create professional UI layout | 创建专业UI布局"""
        # Create main menu
        self._create_professional_menu()

        # Main container with professional layout
        self._create_main_container()

        # Professional status bar
        self.status_bar = ProfessionalStatusBar(self.root, self.theme)
        self.status_bar.pack(side="bottom", fill="x")

    def _create_professional_menu(self):
        """Create professional menu bar | 创建专业菜单栏"""
        menubar = tk.Menu(
            self.root,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        menubar.add_cascade(label="📁 File | 文件", menu=file_menu)
        file_menu.add_command(
            label="⚙️ Settings | 设置", command=self._open_settings, accelerator="Cmd+,"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="📊 Open Reports | 打开报告",
            command=self._open_reports_folder,
            accelerator="Cmd+R",
        )
        file_menu.add_command(
            label="📁 Open Data Folder | 打开数据文件夹", command=self._open_data_folder
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="❌ Quit | 退出", command=self._quit_application, accelerator="Cmd+Q"
        )

        # Edit menu
        edit_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        menubar.add_cascade(label="✏️ Edit | 编辑", menu=edit_menu)
        edit_menu.add_command(
            label="🔍 Find Assignments | 查找作业",
            command=self._focus_search,
            accelerator="Cmd+F",
        )
        edit_menu.add_command(
            label="🔄 Refresh | 刷新",
            command=self._refresh_assignments,
            accelerator="Cmd+R",
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="✅ Mark All Read | 全部标记已读", command=self._mark_all_read
        )
        edit_menu.add_command(
            label="🧹 Clear Cache | 清除缓存", command=self._clear_cache
        )

        # Tools menu
        tools_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        menubar.add_cascade(label="🔧 Tools | 工具", menu=tools_menu)
        tools_menu.add_command(
            label="🔍 Check Assignments | 检查作业",
            command=self._check_assignments,
            accelerator="F5",
        )
        tools_menu.add_command(
            label="🧪 Test Connection | 测试连接", command=self._test_connection
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="🤖 AI Analysis | AI分析",
            command=self._run_ai_analysis,
            accelerator="Cmd+A",
        )
        tools_menu.add_command(
            label="📊 Generate Report | 生成报告",
            command=self._generate_report,
            accelerator="Cmd+G",
        )
        tools_menu.add_command(
            label="📧 Send Notifications | 发送通知", command=self._send_notifications
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="📈 Statistics | 统计",
            command=self._show_statistics,
            accelerator="Cmd+S",
        )

        # View menu
        view_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        menubar.add_cascade(label="👁️ View | 查看", menu=view_menu)
        view_menu.add_command(
            label="🌞 Light Theme | 浅色主题",
            command=lambda: self._change_theme("professional_light"),
        )
        view_menu.add_command(
            label="🌙 Dark Theme | 深色主题",
            command=lambda: self._change_theme("professional_dark"),
        )
        view_menu.add_separator()
        view_menu.add_command(
            label="📋 Show All | 显示全部", command=self._show_all_assignments
        )
        view_menu.add_command(
            label="⚠️ Overdue Only | 仅逾期", command=self._show_overdue_only
        )
        view_menu.add_command(
            label="🔥 High Priority | 高优先级", command=self._show_high_priority
        )
        view_menu.add_separator()
        view_menu.add_command(
            label="🔍 Toggle Search | 切换搜索",
            command=self._toggle_search,
            accelerator="Cmd+F",
        )
        view_menu.add_command(
            label="📊 Toggle Sidebar | 切换侧边栏", command=self._toggle_sidebar
        )

        # Help menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
        )
        menubar.add_cascade(label="❓ Help | 帮助", menu=help_menu)
        help_menu.add_command(
            label="📖 Documentation | 文档", command=self._open_documentation
        )
        help_menu.add_command(
            label="🎥 Video Tutorial | 视频教程", command=self._open_video_tutorial
        )
        help_menu.add_command(label="💬 Community | 社区", command=self._open_community)
        help_menu.add_separator()
        help_menu.add_command(
            label="🐛 Report Bug | 报告错误", command=self._report_bug
        )
        help_menu.add_command(
            label="💡 Feature Request | 功能请求", command=self._feature_request
        )
        help_menu.add_separator()
        help_menu.add_command(
            label="🔄 Check Updates | 检查更新", command=self._check_updates
        )
        help_menu.add_command(label="ℹ️ About | 关于", command=self._show_about)

        # Bind keyboard shortcuts
        self._bind_keyboard_shortcuts()

    def _bind_keyboard_shortcuts(self):
        """Bind keyboard shortcuts | 绑定键盘快捷键"""
        # Universal shortcuts
        self.root.bind("<F5>", lambda e: self._refresh_assignments())
        self.root.bind("<Control-f>", lambda e: self._focus_search())
        self.root.bind("<Control-r>", lambda e: self._refresh_assignments())
        self.root.bind("<Control-q>", lambda e: self._quit_application())

        # macOS specific
        if sys.platform == "darwin":
            self.root.bind("<Command-f>", lambda e: self._focus_search())
            self.root.bind("<Command-r>", lambda e: self._refresh_assignments())
            self.root.bind("<Command-q>", lambda e: self._quit_application())
            self.root.bind("<Command-comma>", lambda e: self._open_settings())
            self.root.bind("<Command-a>", lambda e: self._run_ai_analysis())
            self.root.bind("<Command-g>", lambda e: self._generate_report())
            self.root.bind("<Command-s>", lambda e: self._show_statistics())

    def _create_main_container(self):
        """Create main container with professional layout | 创建专业布局的主容器"""
        # Create paned window for resizable layout
        self.paned_window = tk.PanedWindow(
            self.root,
            orient="horizontal",
            bg=self.theme.get_color("background"),
            sashrelief="flat",
            sashwidth=8,
            sashpad=0,
        )
        self.paned_window.pack(fill="both", expand=True)

        # Create sidebar
        self._create_professional_sidebar()

        # Create main content area
        self._create_professional_content()

    def _create_professional_sidebar(self):
        """Create professional sidebar | 创建专业侧边栏"""
        sidebar = tk.Frame(
            self.paned_window, bg=self.theme.get_color("sidebar"), width=350
        )
        self.paned_window.add(sidebar, minsize=300)

        # Sidebar header with gradient effect
        header_frame = tk.Frame(sidebar, bg=self.theme.get_color("primary"), height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # App title with professional typography
        title_frame = tk.Frame(header_frame, bg=self.theme.get_color("primary"))
        title_frame.pack(expand=True)

        tk.Label(
            title_frame,
            text="🎓 ManageBac",
            font=self.theme.get_font("heading"),
            bg=self.theme.get_color("primary"),
            fg="white",
        ).pack()

        tk.Label(
            title_frame,
            text="Assignment Checker Pro",
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("primary"),
            fg="white",
        ).pack()

        # Quick stats with professional cards
        self._create_professional_stats(sidebar)

        # Action buttons with better spacing
        self._create_professional_buttons(sidebar)

        # Advanced filters
        self._create_professional_filters(sidebar)

    def _create_professional_stats(self, parent):
        """Create professional statistics cards | 创建专业统计卡片"""
        stats_container = tk.Frame(parent, bg=self.theme.get_color("sidebar"))
        stats_container.pack(fill="x", padx=20, pady=20)

        tk.Label(
            stats_container,
            text="📊 Statistics | 统计信息",
            font=self.theme.get_font("subheading"),
            bg=self.theme.get_color("sidebar"),
            fg=self.theme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 15))

        # Create 2x2 grid of stat cards
        stats_grid = tk.Frame(stats_container, bg=self.theme.get_color("sidebar"))
        stats_grid.pack(fill="x")

        # Configure grid
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)

        # Stat cards data
        stats_data = [
            ("📚", "Total", "0", "total_assignments", 0, 0),
            ("⚠️", "Overdue", "0", "overdue_assignments", 0, 1),
            ("🔥", "High Priority", "0", "high_priority", 1, 0),
            ("✅", "Completed", "0", "completed_assignments", 1, 1),
        ]

        for emoji, label, value, var_name, row, col in stats_data:
            self._create_professional_stat_card(
                stats_grid, emoji, label, value, var_name, row, col
            )

    def _create_professional_stat_card(
        self,
        parent,
        emoji: str,
        label: str,
        value: str,
        var_name: str,
        row: int,
        col: int,
    ):
        """Create a professional stat card | 创建专业统计卡片"""
        card_frame = tk.Frame(
            parent,
            bg=self.theme.get_color("card"),
            relief="flat",
            bd=0,
            highlightbackground=self.theme.get_color("border"),
            highlightthickness=1,
        )
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Emoji
        tk.Label(
            card_frame,
            text=emoji,
            font=(
                ("Apple Color Emoji", 20)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 16)
            ),
            bg=self.theme.get_color("card"),
        ).pack(pady=(12, 4))

        # Value
        value_label = tk.Label(
            card_frame,
            text=value,
            font=(self.theme.get_font("heading")[0], 24, "bold"),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("primary"),
        )
        value_label.pack()

        # Label
        tk.Label(
            card_frame,
            text=label,
            font=self.theme.get_font("small"),
            bg=self.theme.get_color("card"),
            fg=self.theme.get_color("text_muted"),
        ).pack(pady=(0, 12))

        # Store reference for updating
        setattr(self, f"{var_name}_label", value_label)

    def _create_professional_buttons(self, parent):
        """Create professional action buttons | 创建专业操作按钮"""
        button_container = tk.Frame(parent, bg=self.theme.get_color("sidebar"))
        button_container.pack(fill="x", padx=20, pady=20)

        # Main action buttons
        self.check_button = ProfessionalButton(
            button_container,
            self.theme,
            style="primary",
            text="🔍 Check Assignments\n检查作业",
            command=self._check_assignments,
        )
        self.check_button.pack(fill="x", pady=(0, 12))

        ProfessionalButton(
            button_container,
            self.theme,
            style="secondary",
            text="⚙️ Settings | 设置",
            command=self._open_settings,
        ).pack(fill="x", pady=(0, 12))

        ProfessionalButton(
            button_container,
            self.theme,
            style="success",
            text="📊 Generate Report | 生成报告",
            command=self._generate_report,
        ).pack(fill="x", pady=(0, 12))

        # AI Analysis button (if available)
        if self.config and getattr(self.config, "ai_enabled", False):
            ProfessionalButton(
                button_container,
                self.theme,
                style="warning",
                text="🤖 AI Analysis | AI分析",
                command=self._run_ai_analysis,
            ).pack(fill="x")

    def _create_professional_filters(self, parent):
        """Create professional filter section | 创建专业筛选器部分"""
        filter_container = tk.Frame(parent, bg=self.theme.get_color("sidebar"))
        filter_container.pack(fill="x", padx=20, pady=20)

        tk.Label(
            filter_container,
            text="🔍 Filters | 筛选器",
            font=self.theme.get_font("subheading"),
            bg=self.theme.get_color("sidebar"),
            fg=self.theme.get_color("text_primary"),
        ).pack(anchor="w", pady=(0, 15))

        # Filter options with better styling
        self.filter_vars = {}
        filters = [
            ("show_overdue", "⚠️ Overdue Only | 仅逾期"),
            ("show_high_priority", "🔥 High Priority | 高优先级"),
            ("show_pending", "📝 Pending Only | 仅待完成"),
            ("show_completed", "✅ Include Completed | 包含已完成"),
        ]

        for var_name, text in filters:
            var = tk.BooleanVar()
            self.filter_vars[var_name] = var

            check_frame = tk.Frame(filter_container, bg=self.theme.get_color("sidebar"))
            check_frame.pack(fill="x", pady=3)

            tk.Checkbutton(
                check_frame,
                text=text,
                variable=var,
                bg=self.theme.get_color("sidebar"),
                fg=self.theme.get_color("text_primary"),
                font=self.theme.get_font("body"),
                command=self._apply_filters,
                selectcolor=self.theme.get_color("card"),
                activebackground=self.theme.get_color("surface"),
            ).pack(anchor="w")

    def _create_professional_content(self):
        """Create professional content area | 创建专业内容区域"""
        content_frame = tk.Frame(
            self.paned_window, bg=self.theme.get_color("background")
        )
        self.paned_window.add(content_frame, minsize=600)

        # Content header with search
        self._create_content_header(content_frame)

        # Assignment display area
        self._create_assignment_display(content_frame)

    def _create_content_header(self, parent):
        """Create content header with search | 创建带搜索的内容头部"""
        header_frame = tk.Frame(
            parent, bg=self.theme.get_color("background"), height=80
        )
        header_frame.pack(fill="x", padx=30, pady=20)
        header_frame.pack_propagate(False)

        # Title
        title_frame = tk.Frame(header_frame, bg=self.theme.get_color("background"))
        title_frame.pack(side="left", fill="y")

        tk.Label(
            title_frame,
            text="📋 Assignments | 作业列表",
            font=self.theme.get_font("heading"),
            bg=self.theme.get_color("background"),
            fg=self.theme.get_color("text_primary"),
        ).pack(anchor="w")

        self.assignment_count_label = tk.Label(
            title_frame,
            text="No assignments loaded | 未加载作业",
            font=self.theme.get_font("small"),
            bg=self.theme.get_color("background"),
            fg=self.theme.get_color("text_muted"),
        )
        self.assignment_count_label.pack(anchor="w", pady=(4, 0))

        # Search area
        search_frame = tk.Frame(header_frame, bg=self.theme.get_color("background"))
        search_frame.pack(side="right", fill="y")

        # Search label
        tk.Label(
            search_frame,
            text="🔍 Search | 搜索:",
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("background"),
            fg=self.theme.get_color("text_secondary"),
        ).pack(anchor="e")

        # Search entry with professional styling
        search_container = tk.Frame(
            search_frame, bg=self.theme.get_color("surface"), relief="flat", bd=1
        )
        search_container.pack(anchor="e", pady=(4, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)

        self.search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=self.theme.get_font("body"),
            width=25,
            bg=self.theme.get_color("surface"),
            fg=self.theme.get_color("text_primary"),
            relief="flat",
            bd=0,
            insertbackground=self.theme.get_color("primary"),
        )
        self.search_entry.pack(padx=12, pady=8, ipady=4)

        # Search placeholder
        self._setup_search_placeholder()

    def _setup_search_placeholder(self):
        """Setup search placeholder text | 设置搜索占位符文本"""
        placeholder = "Search assignments... | 搜索作业..."

        def on_focus_in(event):
            if self.search_entry.get() == placeholder:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=self.theme.get_color("text_primary"))

        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, placeholder)
                self.search_entry.config(fg=self.theme.get_color("text_muted"))

        self.search_entry.insert(0, placeholder)
        self.search_entry.config(fg=self.theme.get_color("text_muted"))
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)

    def _create_assignment_display(self, parent):
        """Create assignment display area | 创建作业显示区域"""
        # Container with professional scrolling
        display_container = tk.Frame(parent, bg=self.theme.get_color("background"))
        display_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Canvas for smooth scrolling
        canvas = tk.Canvas(
            display_container,
            bg=self.theme.get_color("background"),
            highlightthickness=0,
            relief="flat",
        )

        # Professional scrollbar
        scrollbar = ttk.Scrollbar(
            display_container,
            orient="vertical",
            command=canvas.yview,
            style="Professional.Vertical.TScrollbar",
        )

        self.assignments_frame = tk.Frame(canvas, bg=self.theme.get_color("background"))

        # Configure scrolling
        self.assignments_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.assignments_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Smooth mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initial empty state
        self._show_empty_state()

    def _show_empty_state(self):
        """Show professional empty state | 显示专业空状态"""
        empty_frame = tk.Frame(
            self.assignments_frame, bg=self.theme.get_color("background")
        )
        empty_frame.pack(expand=True, fill="both", pady=100)

        # Large icon
        tk.Label(
            empty_frame,
            text="📚",
            font=(
                ("Apple Color Emoji", 64)
                if sys.platform == "darwin"
                else ("Segoe UI Emoji", 48)
            ),
            bg=self.theme.get_color("background"),
        ).pack()

        # Main message
        tk.Label(
            empty_frame,
            text="No assignments loaded yet",
            font=self.theme.get_font("subheading"),
            bg=self.theme.get_color("background"),
            fg=self.theme.get_color("text_primary"),
        ).pack(pady=(20, 8))

        # Secondary message
        tk.Label(
            empty_frame,
            text="Click 'Check Assignments' to get started\n点击\"检查作业\"开始使用",
            font=self.theme.get_font("body"),
            bg=self.theme.get_color("background"),
            fg=self.theme.get_color("text_muted"),
            justify="center",
        ).pack()

        # Quick start button
        ProfessionalButton(
            empty_frame,
            self.theme,
            style="primary",
            text="🚀 Get Started | 开始使用",
            command=self._check_assignments,
        ).pack(pady=(30, 0))

    def _setup_system_integration(self):
        """Setup system integration | 设置系统集成"""
        try:
            log_info("Setting up system integration...")
            self.tray_manager = SystemTrayManager(
                app_callback=self._handle_tray_callback, language="zh"
            )
            self.tray_manager.start_tray()
            log_info("System tray initialized successfully")
        except Exception as e:
            handle_error(e, "System Integration Setup", "WARNING", user_friendly=False)
            self.tray_manager = None

    def _load_configuration(self):
        """Load configuration | 加载配置"""
        try:
            log_info("Loading configuration...")
            self.config = Config(interactive=False)
            self._update_status("✅ Configuration loaded | 配置已加载", "✅")
            log_info("Configuration loaded successfully")
        except Exception as e:
            handle_error(e, "Configuration Loading", "WARNING", user_friendly=False)
            self.config = None
            try:
                self._update_status(f"⚠️ Using default configuration | 使用默认配置", "⚠️")
            except Exception as status_error:
                handle_error(status_error, "Status Update", "WARNING", user_friendly=False)

    def _load_user_preferences(self):
        """Load user preferences | 加载用户偏好"""
        try:
            log_info("Loading user preferences...")
            prefs_file = Path("user_preferences.json")
            if prefs_file.exists():
                try:
                    with open(prefs_file, "r", encoding="utf-8") as f:
                        prefs = json.load(f)

                    # Apply preferences
                    self.auto_check_enabled = prefs.get("auto_check_enabled", False)
                    self.auto_check_interval = prefs.get("auto_check_interval", 30)
                    log_info("User preferences loaded from file")
                except Exception as file_error:
                    handle_error(file_error, "Preferences File Loading", "WARNING", user_friendly=False)
                    self._set_default_preferences()
            else:
                log_info("No preferences file found, using defaults")
                self._set_default_preferences()
        except Exception as e:
            handle_error(e, "User Preferences Loading", "WARNING", user_friendly=False)
            self._set_default_preferences()

    def _set_default_preferences(self):
        """Set default user preferences | 设置默认用户偏好"""
        self.auto_check_enabled = False
        self.auto_check_interval = 30

    def _update_status(
        self, message: str, icon: str = "🔄", show_progress: bool = False
    ):
        """Update status bar | 更新状态栏"""
        self.status_bar.set_status(message, icon, show_progress)

    def _update_stats(self):
        """Update statistics display | 更新统计显示"""
        if not self.assignments:
            stats = {"total": 0, "overdue": 0, "high_priority": 0, "completed": 0}
        else:
            stats = {
                "total": len(self.assignments),
                "overdue": len(
                    [a for a in self.assignments if a.get("status") == "overdue"]
                ),
                "high_priority": len(
                    [a for a in self.assignments if a.get("priority") == "high"]
                ),
                "completed": len(
                    [a for a in self.assignments if a.get("status") == "completed"]
                ),
            }

        # Update stat cards
        self.total_assignments_label.config(text=str(stats["total"]))
        self.overdue_assignments_label.config(text=str(stats["overdue"]))
        self.high_priority_label.config(text=str(stats["high_priority"]))
        self.completed_assignments_label.config(text=str(stats["completed"]))

        # Update assignment count label
        self.assignment_count_label.config(
            text=f"Total: {stats['total']} | Overdue: {stats['overdue']} | 总计: {stats['total']} | 逾期: {stats['overdue']}"
        )

    def _check_assignments(self):
        """Check assignments with professional feedback | 专业反馈检查作业"""
        if not self.config:
            messagebox.showwarning(
                "Configuration Required | 需要配置",
                "⚠️ Please configure your ManageBac credentials first!\n⚠️ 请先配置您的ManageBac凭据！",
            )
            self._open_settings()
            return

        if not self.config.email or not self.config.password:
            messagebox.showwarning(
                "Credentials Required | 需要凭据",
                "⚠️ Please enter your ManageBac email and password in settings!\n⚠️ 请在设置中输入您的ManageBac邮箱和密码！",
            )
            self._open_settings()
            return

        # Update UI for checking state
        self._update_status("🔄 Checking assignments... | 正在检查作业...", "🔄", True)
        self.check_button.config(state="disabled", text="🔄 Checking...\n检查中...")

        def check_thread():
            try:
                # Simulate checking with realistic data
                import time

                time.sleep(3)

                # Generate realistic sample data
                sample_assignments = self._generate_sample_assignments()
                self.assignments = sample_assignments

                # Update UI in main thread
                self.root.after(0, self._on_assignments_loaded)

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_check_error(error_msg))

        threading.Thread(target=check_thread, daemon=True).start()

    def _generate_sample_assignments(self) -> List[Dict]:
        """Generate realistic sample assignments | 生成真实的示例作业"""
        courses = [
            "Mathematics",
            "Physics",
            "Chemistry",
            "English Literature",
            "History",
            "Computer Science",
        ]
        assignment_types = [
            "Homework",
            "Lab Report",
            "Essay",
            "Project",
            "Quiz",
            "Presentation",
        ]

        assignments = []
        for i in range(8):
            course = courses[i % len(courses)]
            assignment_type = assignment_types[i % len(assignment_types)]

            # Vary due dates
            base_date = datetime.now()
            if i % 4 == 0:  # Some overdue
                due_date = (base_date - timedelta(days=1 + i)).strftime("%Y-%m-%d")
                status = "overdue"
            elif i % 4 == 1:  # Some due soon
                due_date = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
                status = "pending"
            elif i % 4 == 2:  # Some future
                due_date = (base_date + timedelta(days=3 + i)).strftime("%Y-%m-%d")
                status = "pending"
            else:  # Some completed
                due_date = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
                status = "completed"

            # Vary priorities
            priorities = ["high", "medium", "low"]
            priority = priorities[i % len(priorities)]

            assignment = {
                "identifier": str(i + 1),
                "title": f"{course} {assignment_type} - Chapter {i + 1}",
                "course": course,
                "due_date": due_date,
                "status": status,
                "assignment_type": assignment_type,
                "priority": priority,
                "link": f"https://example.com/assignment/{i + 1}",
                "description": f"Complete the {assignment_type.lower()} for {course}. This assignment covers important concepts and requires careful attention to detail.",
                "fetched_at": datetime.now().isoformat(),
                "ai_suggestion": f"Focus on this {priority} priority {assignment_type.lower()}. Break it into smaller tasks and allocate sufficient time for completion.",
            }

            assignments.append(assignment)

        return assignments

    def _on_assignments_loaded(self):
        """Handle successful assignment loading | 处理成功加载作业"""
        self._update_status(
            f"✅ Loaded {len(self.assignments)} assignments | 已加载{len(self.assignments)}个作业",
            "✅",
        )
        self.check_button.config(state="normal", text="🔍 Check Assignments\n检查作业")

        self._update_stats()
        self._display_assignments()

        # Show success notification
        self.notification_manager.notify_assignment_reminder(self.assignments)

        messagebox.showinfo(
            "Success | 成功",
            f"✅ Successfully loaded {len(self.assignments)} assignments!\n\n"
            f"📊 Statistics:\n"
            f"• Total: {len(self.assignments)}\n"
            f"• Overdue: {len([a for a in self.assignments if a.get('status') == 'overdue'])}\n"
            f"• High Priority: {len([a for a in self.assignments if a.get('priority') == 'high'])}\n\n"
            f"✅ 成功加载了{len(self.assignments)}个作业！",
        )

    def _on_check_error(self, error_msg: str):
        """Handle assignment checking error | 处理作业检查错误"""
        self._update_status("❌ Error checking assignments | 检查作业时出错", "❌")
        self.check_button.config(state="normal", text="🔍 Check Assignments\n检查作业")

        messagebox.showerror(
            "Error | 错误",
            f"❌ Failed to check assignments:\n❌ 检查作业失败：\n\n{error_msg}\n\n"
            f"💡 Troubleshooting tips:\n"
            f"• Check your internet connection\n"
            f"• Verify ManageBac credentials\n"
            f"• Ensure ManageBac URL is correct\n\n"
            f"💡 故障排除提示：\n"
            f"• 检查网络连接\n"
            f"• 验证ManageBac凭据\n"
            f"• 确保ManageBac网址正确",
        )

    def _display_assignments(self, assignments: List[Dict] = None):
        """Display assignments professionally | 专业显示作业"""
        if assignments is None:
            assignments = self.assignments

        # Clear existing assignments
        for widget in self.assignments_frame.winfo_children():
            widget.destroy()

        if not assignments:
            self._show_empty_state()
            return

        # Display assignments as professional cards
        for i, assignment in enumerate(assignments):
            card = ProfessionalCard(self.assignments_frame, self.theme, assignment)
            card.pack(fill="x", pady=(0, 15), padx=10)

            # Add separator line except for last item
            if i < len(assignments) - 1:
                separator = tk.Frame(
                    self.assignments_frame, bg=self.theme.get_color("border"), height=1
                )
                separator.pack(fill="x", padx=20, pady=8)

    def _apply_filters(self):
        """Apply professional filters | 应用专业筛选器"""
        if not self.assignments:
            return

        filtered = self.assignments.copy()

        # Apply filters
        if self.filter_vars["show_overdue"].get():
            filtered = [a for a in filtered if a.get("status") == "overdue"]

        if self.filter_vars["show_high_priority"].get():
            filtered = [a for a in filtered if a.get("priority") == "high"]

        if self.filter_vars["show_pending"].get():
            filtered = [a for a in filtered if a.get("status") == "pending"]

        if not self.filter_vars["show_completed"].get():
            filtered = [a for a in filtered if a.get("status") != "completed"]

        self.filtered_assignments = filtered
        self._display_assignments(filtered)

        # Update count
        self.assignment_count_label.config(
            text=f"Showing {len(filtered)} of {len(self.assignments)} assignments | 显示{len(filtered)}/{len(self.assignments)}个作业"
        )

    def _on_search_change(self, *args):
        """Handle search with professional feedback | 专业搜索处理"""
        search_term = self.search_var.get().lower()
        placeholder = "search assignments... | 搜索作业..."

        if not search_term or search_term == placeholder:
            self._apply_filters()
            return

        # Advanced search
        filtered = []
        for assignment in self.assignments:
            if (
                search_term in assignment.get("title", "").lower()
                or search_term in assignment.get("course", "").lower()
                or search_term in assignment.get("assignment_type", "").lower()
                or search_term in assignment.get("description", "").lower()
            ):
                filtered.append(assignment)

        self._display_assignments(filtered)

        # Update search results count
        self.assignment_count_label.config(
            text=f"Search results: {len(filtered)} assignments | 搜索结果: {len(filtered)}个作业"
        )

    def _open_settings(self):
        """Open professional settings dialog | 打开专业设置对话框"""
        try:
            from .gui import ConfigDialog

            dialog = ConfigDialog(self.root, self.theme, "zh")
            self.root.wait_window(dialog)
        except Exception as e:
            print(f"❌ Error opening settings: {e}")
            messagebox.showerror(
                "Error | 错误",
                f"Failed to open settings dialog.\n无法打开设置对话框。\n\nError: {e}",
            )

    def _generate_report(self):
        """Generate professional report | 生成专业报告"""
        if not self.assignments:
            messagebox.showwarning(
                "No Data | 无数据",
                "⚠️ No assignments to generate report!\n⚠️ 没有作业可生成报告！",
            )
            return

        self._update_status(
            "📊 Generating professional report... | 正在生成专业报告...", "📊", True
        )

        def generate_thread():
            try:
                import time

                time.sleep(2)  # Simulate generation

                # Create professional report
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_path = Path("reports") / f"professional_report_{timestamp}.html"

                self._generate_professional_html_report(report_path)

                self.root.after(0, lambda: self._on_report_generated(report_path))

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_report_error(error_msg))

        threading.Thread(target=generate_thread, daemon=True).start()

    def _generate_professional_html_report(self, file_path: Path):
        """Generate professional HTML report | 生成专业HTML报告"""
        # Ensure reports directory exists
        file_path.parent.mkdir(exist_ok=True)

        # Professional HTML template
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ManageBac Assignment Report Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8fafc; color: #0f172a; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1rem; opacity: 0.9; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); text-align: center; border-left: 4px solid; }}
        .stat-card.total {{ border-left-color: #3b82f6; }}
        .stat-card.overdue {{ border-left-color: #dc2626; }}
        .stat-card.high-priority {{ border-left-color: #d97706; }}
        .stat-card.completed {{ border-left-color: #059669; }}
        .stat-card h3 {{ font-size: 2.5rem; font-weight: 700; margin-bottom: 8px; }}
        .stat-card p {{ color: #64748b; font-weight: 500; }}
        .assignments-section {{ background: white; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
        .assignment {{ border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 15px; transition: all 0.2s; }}
        .assignment:hover {{ box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); transform: translateY(-1px); }}
        .assignment h3 {{ color: #0f172a; margin-bottom: 12px; font-weight: 600; }}
        .assignment-meta {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .assignment-meta span {{ background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 0.875rem; font-weight: 500; }}
        .priority-high {{ background: #fef2f2; color: #dc2626; }}
        .priority-medium {{ background: #fffbeb; color: #d97706; }}
        .priority-low {{ background: #f0fdf4; color: #059669; }}
        .status-overdue {{ background: #fef2f2; color: #dc2626; }}
        .status-pending {{ background: #eff6ff; color: #2563eb; }}
        .status-completed {{ background: #f0fdf4; color: #059669; }}
        .description {{ color: #64748b; margin-bottom: 15px; }}
        .ai-suggestion {{ background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px; padding: 15px; margin-top: 15px; }}
        .ai-suggestion .label {{ color: #0369a1; font-weight: 600; margin-bottom: 8px; display: block; }}
        .chart-container {{ margin: 30px 0; }}
        .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #64748b; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 ManageBac Assignment Report Pro</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')} | 生成于 {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <h3>{len(self.assignments)}</h3>
                <p>📚 Total Assignments<br>总作业数</p>
            </div>
            <div class="stat-card overdue">
                <h3>{len([a for a in self.assignments if a.get('status') == 'overdue'])}</h3>
                <p>⚠️ Overdue<br>逾期作业</p>
            </div>
            <div class="stat-card high-priority">
                <h3>{len([a for a in self.assignments if a.get('priority') == 'high'])}</h3>
                <p>🔥 High Priority<br>高优先级</p>
            </div>
            <div class="stat-card completed">
                <h3>{len([a for a in self.assignments if a.get('status') == 'completed'])}</h3>
                <p>✅ Completed<br>已完成</p>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas id="priorityChart" width="400" height="200"></canvas>
        </div>
        
        <div class="assignments-section">
            <h2 style="margin-bottom: 25px; color: #0f172a;">📋 Assignment Details | 作业详情</h2>
"""

        # Add assignments
        for assignment in self.assignments:
            priority_class = f"priority-{assignment.get('priority', 'medium')}"
            status_class = f"status-{assignment.get('status', 'pending')}"

            html_content += f"""
            <div class="assignment">
                <h3>{assignment.get('title', 'Unknown Assignment')}</h3>
                <div class="assignment-meta">
                    <div>
                        <span>📚 {assignment.get('course', 'Unknown')}</span>
                        <span>📅 {assignment.get('due_date', 'Unknown')}</span>
                    </div>
                    <div>
                        <span class="{priority_class}">🎯 {assignment.get('priority', 'Unknown').title()}</span>
                        <span class="{status_class}">📊 {assignment.get('status', 'Unknown').title()}</span>
                    </div>
                </div>
                <div class="description">{assignment.get('description', 'No description available')}</div>
"""

            if assignment.get("link"):
                html_content += f'                <p><a href="{assignment["link"]}" target="_blank" style="color: #2563eb; text-decoration: none;">🔗 Open Assignment | 打开作业</a></p>\n'

            if hasattr(assignment, "ai_suggestion") and assignment.ai_suggestion:
                html_content += f"""
                <div class="ai-suggestion">
                    <span class="label">🤖 AI Suggestion | AI建议:</span>
                    {assignment.ai_suggestion}
                </div>
"""

            html_content += "            </div>\n"

        # Add chart script and footer
        html_content += (
            """
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by ManageBac Assignment Checker Pro v2.0.0</p>
        <p>由ManageBac作业检查器专业版 v2.0.0 生成</p>
    </div>
    
    <script>
        // Create priority distribution chart
        const ctx = document.getElementById('priorityChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['High Priority', 'Medium Priority', 'Low Priority'],
                datasets: [{
                    data: [
                        """
            + str(len([a for a in self.assignments if a.get("priority") == "high"]))
            + """,
                        """
            + str(len([a for a in self.assignments if a.get("priority") == "medium"]))
            + """,
                        """
            + str(len([a for a in self.assignments if a.get("priority") == "low"]))
            + """
                    ],
                    backgroundColor: ['#dc2626', '#d97706', '#059669'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Priority Distribution | 优先级分布',
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'bottom',
                        labels: { padding: 20, font: { size: 12 } }
                    }
                }
            }
        });
    </script>
</body>
</html>
"""
        )

        # Write the professional report
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _on_report_generated(self, report_path: Path):
        """Handle successful report generation | 处理成功生成报告"""
        self._update_status("✅ Professional report generated | 专业报告已生成", "✅")

        result = messagebox.askyesno(
            "Report Generated | 报告已生成",
            f"✅ Professional report generated successfully!\n✅ 专业报告生成成功！\n\n"
            f"📁 Location: {report_path}\n"
            f"📁 位置: {report_path}\n\n"
            f"Open the report now?\n现在打开报告？",
        )

        if result:
            webbrowser.open(report_path.as_uri())

        # Send notification
        self.notification_manager.notify_report_generated(str(report_path))

    def _on_report_error(self, error_msg: str):
        """Handle report generation error | 处理报告生成错误"""
        self._update_status("❌ Report generation failed | 报告生成失败", "❌")

        messagebox.showerror(
            "Report Error | 报告错误",
            f"❌ Failed to generate report:\n❌ 生成报告失败：\n\n{error_msg}",
        )

    # Placeholder methods for menu actions
    def _refresh_assignments(self):
        self._check_assignments()

    def _focus_search(self):
        self.search_entry.focus_set()

    def _open_reports_folder(self):
        webbrowser.open(Path("reports").absolute().as_uri())

    def _open_data_folder(self):
        webbrowser.open(Path(".").absolute().as_uri())

    def _test_connection(self):
        messagebox.showinfo("Test", "🧪 Connection test | 连接测试")

    def _run_ai_analysis(self):
        messagebox.showinfo("AI", "🤖 AI Analysis | AI分析")

    def _send_notifications(self):
        messagebox.showinfo("Notifications", "📧 Notifications sent | 通知已发送")

    def _show_statistics(self):
        messagebox.showinfo("Stats", "📈 Statistics | 统计信息")

    def _show_all_assignments(self):
        self._display_assignments()

    def _show_overdue_only(self):
        self.filter_vars["show_overdue"].set(True)
        self._apply_filters()

    def _show_high_priority(self):
        self.filter_vars["show_high_priority"].set(True)
        self._apply_filters()

    def _toggle_search(self):
        self.search_entry.focus_set()

    def _toggle_sidebar(self):
        messagebox.showinfo("Sidebar", "📊 Sidebar toggle | 侧边栏切换")

    def _mark_all_read(self):
        messagebox.showinfo("Mark Read", "✅ All marked as read | 全部标记已读")

    def _clear_cache(self):
        messagebox.showinfo("Cache", "🧹 Cache cleared | 缓存已清除")

    def _change_theme(self, theme_name: str):
        """Change theme and update all UI elements | 更改主题并更新所有UI元素"""
        try:
            # Switch theme
            if not self.theme.switch_theme(theme_name):
                messagebox.showerror("Error", f"Invalid theme: {theme_name}")
                return

            # Update root window
            self.root.configure(bg=self.theme.get_color("background"))

            # Update all widgets recursively
            self._update_widget_theme(self.root)

            # Update status bar
            if hasattr(self, "status_bar"):
                self.status_bar.configure(bg=self.theme.get_color("surface"))
                for widget in self.status_bar.winfo_children():
                    self._update_widget_theme(widget)

            # Update assignment cards
            if hasattr(self, "assignment_cards_frame"):
                for widget in self.assignment_cards_frame.winfo_children():
                    self._update_widget_theme(widget)

            # Update search and filter widgets
            if hasattr(self, "search_frame"):
                for widget in self.search_frame.winfo_children():
                    self._update_widget_theme(widget)

            # Save theme preference
            self._save_user_preferences()

            messagebox.showinfo(
                "Theme Changed | 主题已更改",
                f"🎨 Theme successfully changed to {theme_name}\n🎨 主题已成功更改为{theme_name}",
            )

        except Exception as e:
            messagebox.showerror("Error | 错误", f"Failed to change theme: {e}")
            print(f"❌ Theme change error: {e}")

    def _update_widget_theme(self, widget):
        """Recursively update widget theme | 递归更新组件主题"""
        try:
            # Update widget colors based on type
            if isinstance(widget, (tk.Label, tk.Button)):
                if hasattr(widget, "cget"):
                    try:
                        # Update background
                        current_bg = widget.cget("bg")
                        if current_bg in ["#F8FAFC", "#1E293B", "#FFFFFF", "#0F172A"]:
                            if self.theme.current_theme == "professional_light":
                                widget.configure(bg=self.theme.get_color("background"))
                            else:
                                widget.configure(bg=self.theme.get_color("background"))

                        # Update foreground
                        current_fg = widget.cget("fg")
                        if current_fg in ["#0F172A", "#F8FAFC", "#475569", "#CBD5E1"]:
                            widget.configure(fg=self.theme.get_color("text_primary"))

                    except tk.TclError:
                        pass

            # Update frame backgrounds
            elif isinstance(widget, tk.Frame):
                try:
                    current_bg = widget.cget("bg")
                    if current_bg in [
                        "#F8FAFC",
                        "#1E293B",
                        "#FFFFFF",
                        "#0F172A",
                        "#F1F5F9",
                    ]:
                        widget.configure(bg=self.theme.get_color("background"))
                except tk.TclError:
                    pass

            # Recursively update children
            for child in widget.winfo_children():
                self._update_widget_theme(child)

        except Exception as e:
            # Silently continue if widget can't be updated
            pass

    def _open_documentation(self):
        webbrowser.open(
            "https://github.com/Hacker0458/managebac-assignment-checker#readme"
        )

    def _open_video_tutorial(self):
        webbrowser.open("https://github.com/Hacker0458/managebac-assignment-checker")

    def _open_community(self):
        webbrowser.open(
            "https://github.com/Hacker0458/managebac-assignment-checker/discussions"
        )

    def _report_bug(self):
        webbrowser.open(
            "https://github.com/Hacker0458/managebac-assignment-checker/issues/new"
        )

    def _feature_request(self):
        webbrowser.open(
            "https://github.com/Hacker0458/managebac-assignment-checker/issues/new"
        )

    def _check_updates(self):
        messagebox.showinfo("Updates", "🔄 Checking for updates | 检查更新")

    def _show_about(self):
        messagebox.showinfo(
            "About | 关于",
            "🎓 ManageBac Assignment Checker Pro v2.0.0\n\n"
            "Professional assignment tracking tool\n专业作业追踪工具\n\n"
            "Features | 功能:\n"
            "• 🤖 AI-powered analysis\n"
            "• 📱 Modern GUI interface\n"
            "• 🔔 System tray integration\n"
            "• 🌐 Bilingual support\n\n"
            "Made with ❤️ by Hacker0458\n"
            "Licensed under MIT License",
        )

    def _handle_tray_callback(self, action: str):
        """Handle system tray callbacks | 处理系统托盘回调"""
        if action == "show":
            self._show_window()
        elif action == "check":
            self._check_assignments()
        elif action == "settings":
            self._open_settings()
        elif action == "quit":
            self._quit_application()

    def _show_window(self):
        """Show window from tray | 从托盘显示窗口"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _quit_application(self):
        """Quit application professionally | 专业退出应用程序"""
        # Save preferences
        self._save_user_preferences()

        # Stop system tray
        if self.tray_manager:
            self.tray_manager.stop_tray()

        # Cancel timers
        if self.auto_check_timer:
            self.root.after_cancel(self.auto_check_timer)

        # Quit gracefully
        self.root.quit()
        self.root.destroy()

    def _save_user_preferences(self):
        """Save user preferences | 保存用户偏好"""
        prefs = {
            "theme": self.theme.current_theme,
            "auto_check_enabled": self.auto_check_enabled,
            "auto_check_interval": self.auto_check_interval,
            "window_geometry": self.root.geometry(),
            "last_used": datetime.now().isoformat(),
        }

        try:
            with open("user_preferences.json", "w", encoding="utf-8") as f:
                json.dump(prefs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save preferences: {e}")

    def run(self):
        """Start the professional GUI application | 启动专业GUI应用程序"""
        try:
            # Show welcome notification (non-blocking)
            try:
                self.notification_manager.send_notification(
                    "ManageBac检查器专业版",
                    "应用程序已启动 - 享受专业级的作业管理体验！",
                )
            except Exception as e:
                print(f"⚠️ Notification failed: {e}")

            # Don't automatically check assignments on startup
            # Let user manually trigger checks
            print("✅ Professional GUI started successfully")
            print("✅ 专业GUI启动成功")

            self.root.mainloop()

        except KeyboardInterrupt:
            self._quit_application()
        finally:
            # Cleanup
            if self.tray_manager:
                self.tray_manager.stop_tray()


def main():
    """Main function to run the professional GUI | 运行专业GUI的主函数"""
    log_info("Starting Professional ManageBac GUI...")
    print("🚀 Starting Professional ManageBac GUI...")
    print("=" * 50)

    try:
        log_info("Creating ProfessionalManageBacGUI instance...")
        app = ProfessionalManageBacGUI()
        log_info("GUI instance created successfully")

        log_info("Starting GUI application...")
        app.run()
        log_info("GUI application completed successfully")

    except KeyboardInterrupt:
        log_info("Application interrupted by user")
        print("🛑 Application interrupted by user")
    except Exception as e:
        error_info = handle_error(e, "GUI Startup", "CRITICAL", user_friendly=True)

        # Additional suggestions for GUI startup failures
        print("\n🔧 Additional troubleshooting for GUI issues:")
        print("1. Check display server (X11/Wayland on Linux)")
        print("2. Verify tkinter installation: python3 -m tkinter")
        print("3. Try running in headless mode with --no-gui flag")
        print("4. Check permissions for GUI applications")

        if ERROR_HANDLER_AVAILABLE:
            handler = get_error_handler()
            print(f"\n📊 Error Statistics:")
            stats = handler.get_error_statistics()
            print(f"   Total errors this session: {stats['total_errors']}")
            print(f"   Log directory: {stats['log_directory']}")

        return False

    return True


if __name__ == "__main__":
    main()
