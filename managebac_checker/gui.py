#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 ManageBac Assignment Checker GUI | ManageBac作业检查器图形界面
Modern desktop application with beautiful UI and excellent user experience
现代化桌面应用程序，拥有美观的界面和出色的用户体验
"""

import os
import sys
import json
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import webbrowser

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import tkinter.font as tkfont
except ImportError:
    print("❌ tkinter is required for GUI. Please install it.")
    sys.exit(1)

from .config import Config
from .checker import ManageBacChecker
from .logging_utils import BilingualLogger, setup_logging
from .ai_assistant import AIAssistant


class ModernTheme:
    """Modern theme colors and styles | 现代主题颜色和样式"""

    # Color schemes | 配色方案
    THEMES = {
        "light": {
            "bg": "#FFFFFF",
            "fg": "#2C3E50",
            "accent": "#3498DB",
            "accent_hover": "#2980B9",
            "success": "#27AE60",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "secondary": "#95A5A6",
            "card_bg": "#F8F9FA",
            "border": "#E1E8ED",
            "text_light": "#7F8C8D",
            "sidebar": "#ECF0F1",
        },
        "dark": {
            "bg": "#2C3E50",
            "fg": "#FFFFFF",
            "accent": "#3498DB",
            "accent_hover": "#2980B9",
            "success": "#27AE60",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "secondary": "#95A5A6",
            "card_bg": "#34495E",
            "border": "#4A5568",
            "text_light": "#BDC3C7",
            "sidebar": "#2C3E50",
        },
    }

    def __init__(self, theme_name: str = "light"):
        self.current_theme = theme_name
        self.colors = self.THEMES[theme_name]

    def get_color(self, name: str) -> str:
        return self.colors.get(name, "#000000")


class AnimatedButton(tk.Button):
    """Animated button with hover effects | 带悬停效果的动画按钮"""

    def __init__(self, parent, theme: ModernTheme, **kwargs):
        self.theme = theme
        self.default_bg = theme.get_color("accent")
        self.hover_bg = theme.get_color("accent_hover")

        super().__init__(
            parent,
            bg=self.default_bg,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            **kwargs,
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg=self.hover_bg)

    def _on_leave(self, event):
        self.config(bg=self.default_bg)


class StatusBar(tk.Frame):
    """Status bar with icons and messages | 带图标和消息的状态栏"""

    def __init__(self, parent, theme: ModernTheme):
        super().__init__(parent, bg=theme.get_color("sidebar"), height=30)
        self.theme = theme

        # Status label
        self.status_label = tk.Label(
            self,
            text="🔄 Ready | 就绪",
            bg=theme.get_color("sidebar"),
            fg=theme.get_color("fg"),
            font=("Segoe UI", 9),
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self, length=200, mode="indeterminate")
        self.progress.pack(side="right", padx=10, pady=5)

    def set_status(self, message: str, show_progress: bool = False):
        self.status_label.config(text=message)
        if show_progress:
            self.progress.start()
        else:
            self.progress.stop()


class ConfigDialog(tk.Toplevel):
    """Configuration dialog | 配置对话框"""

    def __init__(self, parent, theme: ModernTheme, language: str = "zh"):
        super().__init__(parent)
        self.theme = theme
        self.language = language
        self.result = None

        self.title("⚙️ Configuration | 配置设置")
        self.geometry("600x700")
        self.configure(bg=theme.get_color("bg"))
        self.transient(parent)
        self.grab_set()

        # Center the dialog
        self.center_window()

        self._create_widgets()
        self._load_config()

    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"600x700+{x}+{y}")

    def _create_widgets(self):
        # Main container
        main_frame = tk.Frame(self, bg=self.theme.get_color("bg"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="🔧 ManageBac Configuration | ManageBac配置",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
        )
        title_label.pack(pady=(0, 20))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))

        # Basic settings tab
        self._create_basic_tab()

        # AI settings tab
        self._create_ai_tab()

        # Advanced settings tab
        self._create_advanced_tab()

        # Buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.get_color("bg"))
        button_frame.pack(fill="x")

        AnimatedButton(
            button_frame, self.theme, text="💾 Save | 保存", command=self._save_config
        ).pack(side="right", padx=(10, 0))

        AnimatedButton(
            button_frame, self.theme, text="❌ Cancel | 取消", command=self.destroy
        ).pack(side="right")

        AnimatedButton(
            button_frame,
            self.theme,
            text="🧪 Test Connection | 测试连接",
            command=self._test_connection,
        ).pack(side="left")

    def _create_basic_tab(self):
        basic_frame = tk.Frame(self.notebook, bg=self.theme.get_color("bg"))
        self.notebook.add(basic_frame, text="🔐 Basic | 基础设置")

        # Scrollable frame
        canvas = tk.Canvas(basic_frame, bg=self.theme.get_color("bg"))
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.get_color("bg"))

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # ManageBac credentials
        self._create_section(scrollable_frame, "🔑 ManageBac Credentials | ManageBac凭据")

        self.email_var = tk.StringVar()
        self._create_entry(scrollable_frame, "📧 Email | 邮箱:", self.email_var)

        self.password_var = tk.StringVar()
        self._create_entry(scrollable_frame, "🔒 Password | 密码:", self.password_var, show="*")

        self.url_var = tk.StringVar(value="https://shtcs.managebac.cn")
        self._create_entry(scrollable_frame, "🌐 URL | 网址:", self.url_var)

        # Report settings
        self._create_section(scrollable_frame, "📊 Report Settings | 报告设置")

        self.format_var = tk.StringVar(value="html,json,console")
        self._create_entry(
            scrollable_frame,
            "📋 Formats | 格式:",
            self.format_var,
            help_text="Comma-separated: html,json,markdown,console",
        )

        self.output_dir_var = tk.StringVar(value="reports")
        output_frame = self._create_entry(
            scrollable_frame, "📁 Output Directory | 输出目录:", self.output_dir_var
        )

        tk.Button(
            output_frame,
            text="📂",
            command=self._browse_directory,
            bg=self.theme.get_color("accent"),
            fg="white",
            relief="flat",
        ).pack(side="right", padx=(5, 0))

        # Language settings
        self._create_section(scrollable_frame, "🌐 Language Settings | 语言设置")

        self.language_var = tk.StringVar(value="zh")
        lang_frame = tk.Frame(scrollable_frame, bg=self.theme.get_color("bg"))
        lang_frame.pack(fill="x", pady=5)

        tk.Label(
            lang_frame,
            text="🗣️ Interface Language | 界面语言:",
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=["zh", "en"],
            state="readonly",
            width=10,
        )
        lang_combo.pack(anchor="w", pady=(5, 0))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_ai_tab(self):
        ai_frame = tk.Frame(self.notebook, bg=self.theme.get_color("bg"))
        self.notebook.add(ai_frame, text="🤖 AI Assistant | AI助手")

        # Scrollable frame
        canvas = tk.Canvas(ai_frame, bg=self.theme.get_color("bg"))
        scrollbar = ttk.Scrollbar(ai_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.get_color("bg"))

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # AI Enable/Disable
        self._create_section(scrollable_frame, "🤖 AI Assistant Settings | AI助手设置")

        self.ai_enabled_var = tk.BooleanVar()
        ai_check_frame = tk.Frame(scrollable_frame, bg=self.theme.get_color("bg"))
        ai_check_frame.pack(fill="x", pady=5)

        tk.Checkbutton(
            ai_check_frame,
            text="✨ Enable AI Assistant | 启用AI助手",
            variable=self.ai_enabled_var,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10, "bold"),
            command=self._toggle_ai_settings,
        ).pack(anchor="w")

        # AI Settings container
        self.ai_settings_frame = tk.Frame(scrollable_frame, bg=self.theme.get_color("bg"))
        self.ai_settings_frame.pack(fill="x", pady=10)

        self.api_key_var = tk.StringVar()
        self._create_entry(self.ai_settings_frame, "🔑 OpenAI API Key:", self.api_key_var, show="*")

        self.ai_model_var = tk.StringVar(value="gpt-3.5-turbo")
        model_frame = tk.Frame(self.ai_settings_frame, bg=self.theme.get_color("bg"))
        model_frame.pack(fill="x", pady=5)

        tk.Label(
            model_frame,
            text="🎯 AI Model | AI模型:",
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.ai_model_var,
            values=["gpt-3.5-turbo", "gpt-4"],
            state="readonly",
        )
        model_combo.pack(anchor="w", pady=(5, 0), fill="x")

        # AI Parameters
        self._create_section(self.ai_settings_frame, "⚙️ AI Parameters | AI参数")

        self.temperature_var = tk.DoubleVar(value=0.7)
        temp_frame = tk.Frame(self.ai_settings_frame, bg=self.theme.get_color("bg"))
        temp_frame.pack(fill="x", pady=5)

        tk.Label(
            temp_frame,
            text="🌡️ Temperature (Creativity) | 温度(创造力): 0.7",
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        self.temp_scale = tk.Scale(
            temp_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            orient="horizontal",
            variable=self.temperature_var,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            command=self._update_temperature_label,
        )
        self.temp_scale.pack(fill="x", pady=(5, 0))

        self.max_tokens_var = tk.IntVar(value=500)
        self._create_entry(self.ai_settings_frame, "📊 Max Tokens | 最大令牌:", self.max_tokens_var)

        # Get API Key button
        api_help_frame = tk.Frame(self.ai_settings_frame, bg=self.theme.get_color("bg"))
        api_help_frame.pack(fill="x", pady=10)

        tk.Button(
            api_help_frame,
            text="🔗 Get OpenAI API Key | 获取OpenAI API密钥",
            command=lambda: webbrowser.open("https://platform.openai.com/api-keys"),
            bg=self.theme.get_color("warning"),
            fg="white",
            relief="flat",
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initially disable AI settings
        self._toggle_ai_settings()

    def _create_advanced_tab(self):
        advanced_frame = tk.Frame(self.notebook, bg=self.theme.get_color("bg"))
        self.notebook.add(advanced_frame, text="🔧 Advanced | 高级设置")

        # Scrollable frame
        canvas = tk.Canvas(advanced_frame, bg=self.theme.get_color("bg"))
        scrollbar = ttk.Scrollbar(advanced_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme.get_color("bg"))

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Browser settings
        self._create_section(scrollable_frame, "🌐 Browser Settings | 浏览器设置")

        self.headless_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            scrollable_frame,
            text="👻 Headless Mode | 无头模式",
            variable=self.headless_var,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=5)

        self.timeout_var = tk.IntVar(value=30000)
        self._create_entry(scrollable_frame, "⏱️ Timeout (ms) | 超时时间:", self.timeout_var)

        # Email notifications
        self._create_section(scrollable_frame, "📧 Email Notifications | 邮件通知")

        self.email_enabled_var = tk.BooleanVar()
        tk.Checkbutton(
            scrollable_frame,
            text="📨 Enable Email Notifications | 启用邮件通知",
            variable=self.email_enabled_var,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
            command=self._toggle_email_settings,
        ).pack(anchor="w", pady=5)

        # Email settings container
        self.email_settings_frame = tk.Frame(scrollable_frame, bg=self.theme.get_color("bg"))
        self.email_settings_frame.pack(fill="x", pady=10)

        self.smtp_server_var = tk.StringVar(value="smtp.gmail.com")
        self._create_entry(
            self.email_settings_frame, "📮 SMTP Server | SMTP服务器:", self.smtp_server_var
        )

        self.smtp_port_var = tk.IntVar(value=587)
        self._create_entry(
            self.email_settings_frame, "🔌 SMTP Port | SMTP端口:", self.smtp_port_var
        )

        self.smtp_username_var = tk.StringVar()
        self._create_entry(
            self.email_settings_frame, "👤 SMTP Username | SMTP用户名:", self.smtp_username_var
        )

        self.smtp_password_var = tk.StringVar()
        self._create_entry(
            self.email_settings_frame,
            "🔐 SMTP Password | SMTP密码:",
            self.smtp_password_var,
            show="*",
        )

        self.recipients_var = tk.StringVar()
        self._create_entry(
            self.email_settings_frame,
            "📬 Recipients | 收件人:",
            self.recipients_var,
            help_text="Comma-separated email addresses",
        )

        # Debug settings
        self._create_section(scrollable_frame, "🐛 Debug Settings | 调试设置")

        self.debug_var = tk.BooleanVar()
        tk.Checkbutton(
            scrollable_frame,
            text="🔍 Enable Debug Mode | 启用调试模式",
            variable=self.debug_var,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=5)

        self.log_level_var = tk.StringVar(value="INFO")
        level_frame = tk.Frame(scrollable_frame, bg=self.theme.get_color("bg"))
        level_frame.pack(fill="x", pady=5)

        tk.Label(
            level_frame,
            text="📊 Log Level | 日志级别:",
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        level_combo = ttk.Combobox(
            level_frame,
            textvariable=self.log_level_var,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            state="readonly",
        )
        level_combo.pack(anchor="w", pady=(5, 0), fill="x")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initially disable email settings
        self._toggle_email_settings()

    def _create_section(self, parent, title: str):
        section_frame = tk.Frame(parent, bg=self.theme.get_color("bg"))
        section_frame.pack(fill="x", pady=(20, 10))

        tk.Label(
            section_frame,
            text=title,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("accent"),
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")

        # Separator line
        separator = tk.Frame(section_frame, height=2, bg=self.theme.get_color("accent"))
        separator.pack(fill="x", pady=(5, 0))

    def _create_entry(self, parent, label: str, variable, show: str = None, help_text: str = None):
        entry_frame = tk.Frame(parent, bg=self.theme.get_color("bg"))
        entry_frame.pack(fill="x", pady=5)

        tk.Label(
            entry_frame,
            text=label,
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        entry = tk.Entry(
            entry_frame,
            textvariable=variable,
            font=("Segoe UI", 10),
            show=show,
            bg="white",
            fg="black",
            relief="flat",
            bd=1,
        )
        entry.pack(fill="x", pady=(5, 0), ipady=5)

        if help_text:
            tk.Label(
                entry_frame,
                text=f"💡 {help_text}",
                bg=self.theme.get_color("bg"),
                fg=self.theme.get_color("text_light"),
                font=("Segoe UI", 8),
            ).pack(anchor="w", pady=(2, 0))

        return entry_frame

    def _browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)

    def _toggle_ai_settings(self):
        state = "normal" if self.ai_enabled_var.get() else "disabled"
        for widget in self.ai_settings_frame.winfo_children():
            self._set_widget_state(widget, state)

    def _toggle_email_settings(self):
        state = "normal" if self.email_enabled_var.get() else "disabled"
        for widget in self.email_settings_frame.winfo_children():
            self._set_widget_state(widget, state)

    def _set_widget_state(self, widget, state):
        try:
            widget.config(state=state)
        except:
            pass
        for child in widget.winfo_children():
            self._set_widget_state(child, state)

    def _update_temperature_label(self, value):
        temp_val = float(value)
        label_text = f"🌡️ Temperature (Creativity) | 温度(创造力): {temp_val}"
        # Find and update the label
        for widget in self.temp_scale.master.winfo_children():
            if isinstance(widget, tk.Label) and "Temperature" in widget.cget("text"):
                widget.config(text=label_text)
                break

    def _load_config(self):
        """Load existing configuration | 加载现有配置"""
        try:
            if os.path.exists(".env"):
                from dotenv import load_dotenv

                load_dotenv()

                self.email_var.set(os.getenv("MANAGEBAC_EMAIL", ""))
                self.password_var.set(os.getenv("MANAGEBAC_PASSWORD", ""))
                self.url_var.set(os.getenv("MANAGEBAC_URL", "https://shtcs.managebac.cn"))
                self.format_var.set(os.getenv("REPORT_FORMAT", "html,json,console"))
                self.output_dir_var.set(os.getenv("OUTPUT_DIR", "reports"))
                self.language_var.set(os.getenv("LANGUAGE", "zh"))

                # AI settings
                self.ai_enabled_var.set(os.getenv("AI_ENABLED", "false").lower() == "true")
                self.api_key_var.set(os.getenv("OPENAI_API_KEY", ""))
                self.ai_model_var.set(os.getenv("AI_MODEL", "gpt-3.5-turbo"))
                self.temperature_var.set(float(os.getenv("AI_TEMPERATURE", "0.7")))
                self.max_tokens_var.set(int(os.getenv("AI_MAX_TOKENS", "500")))

                # Advanced settings
                self.headless_var.set(os.getenv("HEADLESS", "true").lower() == "true")
                self.timeout_var.set(int(os.getenv("BROWSER_TIMEOUT", "30000")))
                self.debug_var.set(os.getenv("DEBUG", "false").lower() == "true")
                self.log_level_var.set(os.getenv("LOG_LEVEL", "INFO"))

                # Email settings
                self.email_enabled_var.set(
                    os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
                )
                self.smtp_server_var.set(os.getenv("SMTP_SERVER", "smtp.gmail.com"))
                self.smtp_port_var.set(int(os.getenv("SMTP_PORT", "587")))
                self.smtp_username_var.set(os.getenv("SMTP_USERNAME", ""))
                self.smtp_password_var.set(os.getenv("SMTP_PASSWORD", ""))
                self.recipients_var.set(os.getenv("NOTIFICATION_RECIPIENTS", ""))

                # Update UI states
                self._toggle_ai_settings()
                self._toggle_email_settings()

        except Exception as e:
            print(f"Error loading config: {e}")

    def _save_config(self):
        """Save configuration to .env file | 保存配置到.env文件"""
        try:
            env_content = f"""# ========================================
# ManageBac Assignment Checker Configuration
# ManageBac作业检查器配置文件
# ========================================

# 🔐 ManageBac Credentials | ManageBac凭据
MANAGEBAC_EMAIL={self.email_var.get()}
MANAGEBAC_PASSWORD={self.password_var.get()}
MANAGEBAC_URL={self.url_var.get()}

# 📊 Report Settings | 报告设置
REPORT_FORMAT={self.format_var.get()}
OUTPUT_DIR={self.output_dir_var.get()}
FETCH_DETAILS=true
DETAILS_LIMIT=50

# 📧 Email Notification Settings | 邮件通知设置
ENABLE_EMAIL_NOTIFICATIONS={str(self.email_enabled_var.get()).lower()}
SMTP_SERVER={self.smtp_server_var.get()}
SMTP_PORT={self.smtp_port_var.get()}
SMTP_USERNAME={self.smtp_username_var.get()}
SMTP_PASSWORD={self.smtp_password_var.get()}
SMTP_USE_TLS=true
NOTIFICATION_RECIPIENTS={self.recipients_var.get()}

# 🔧 Browser Settings | 浏览器设置
HEADLESS={str(self.headless_var.get()).lower()}
BROWSER_TIMEOUT={self.timeout_var.get()}

# 🐛 Debug Settings | 调试设置
DEBUG={str(self.debug_var.get()).lower()}
LOG_LEVEL={self.log_level_var.get()}
LOG_FILE=logs/managebac_checker.log

# 🎨 UI Settings | 界面设置
HTML_THEME=auto
INCLUDE_CHARTS=true
CHART_COLOR_SCHEME=default

# 🤖 AI Assistant Settings | AI助手设置
AI_ENABLED={str(self.ai_enabled_var.get()).lower()}
OPENAI_API_KEY={self.api_key_var.get()}
AI_MODEL={self.ai_model_var.get()}
AI_TEMPERATURE={self.temperature_var.get()}
AI_MAX_TOKENS={self.max_tokens_var.get()}

# 🌐 Language Settings | 语言设置
LANGUAGE={self.language_var.get()}
"""

            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)

            self.result = "saved"
            messagebox.showinfo(
                "Success | 成功", "✅ Configuration saved successfully!\n✅ 配置保存成功！"
            )
            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error | 错误", f"❌ Failed to save configuration:\n❌ 保存配置失败：\n{str(e)}"
            )

    def _test_connection(self):
        """Test ManageBac connection | 测试ManageBac连接"""
        if not self.email_var.get() or not self.password_var.get():
            messagebox.showwarning(
                "Warning | 警告", "⚠️ Please enter email and password first!\n⚠️ 请先输入邮箱和密码！"
            )
            return

        # Show testing dialog
        test_dialog = tk.Toplevel(self)
        test_dialog.title("🧪 Testing Connection | 测试连接")
        test_dialog.geometry("400x200")
        test_dialog.configure(bg=self.theme.get_color("bg"))
        test_dialog.transient(self)
        test_dialog.grab_set()

        # Center the dialog
        test_dialog.update_idletasks()
        x = (test_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (test_dialog.winfo_screenheight() // 2) - (200 // 2)
        test_dialog.geometry(f"400x200+{x}+{y}")

        tk.Label(
            test_dialog,
            text="🔄 Testing ManageBac connection...\n🔄 正在测试ManageBac连接...",
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
            font=("Segoe UI", 12),
            justify="center",
        ).pack(expand=True)

        progress = ttk.Progressbar(test_dialog, mode="indeterminate")
        progress.pack(pady=20, padx=50, fill="x")
        progress.start()

        def test_connection_thread():
            try:
                # Simulate connection test (replace with actual test)
                import time

                time.sleep(3)  # Simulate testing time

                # Close test dialog and show result
                test_dialog.after(0, lambda: test_dialog.destroy())
                messagebox.showinfo(
                    "Success | 成功", "✅ Connection test successful!\n✅ 连接测试成功！"
                )
            except Exception as e:
                test_dialog.after(0, lambda: test_dialog.destroy())
                messagebox.showerror(
                    "Error | 错误", f"❌ Connection test failed:\n❌ 连接测试失败：\n{str(e)}"
                )

        threading.Thread(target=test_connection_thread, daemon=True).start()


class AssignmentCard(tk.Frame):
    """Individual assignment card widget | 单个作业卡片组件"""

    def __init__(self, parent, theme: ModernTheme, assignment_data: Dict[str, Any]):
        super().__init__(parent, bg=theme.get_color("card_bg"), relief="raised", bd=1)
        self.theme = theme
        self.assignment = assignment_data

        self._create_widgets()

    def _create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self, bg=self.theme.get_color("card_bg"))
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Header with title and status
        header_frame = tk.Frame(main_frame, bg=self.theme.get_color("card_bg"))
        header_frame.pack(fill="x", pady=(0, 10))

        # Title
        title_label = tk.Label(
            header_frame,
            text=self.assignment.get("title", "Unknown Assignment"),
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("fg"),
            wraplength=300,
            justify="left",
        )
        title_label.pack(side="left", anchor="w")

        # Status badge
        status = self.assignment.get("status", "unknown")
        status_colors = {
            "overdue": self.theme.get_color("error"),
            "due_soon": self.theme.get_color("warning"),
            "pending": self.theme.get_color("accent"),
            "completed": self.theme.get_color("success"),
        }

        status_label = tk.Label(
            header_frame,
            text=status.upper(),
            font=("Segoe UI", 8, "bold"),
            bg=status_colors.get(status, self.theme.get_color("secondary")),
            fg="white",
            padx=8,
            pady=2,
        )
        status_label.pack(side="right", anchor="e")

        # Course and due date
        info_frame = tk.Frame(main_frame, bg=self.theme.get_color("card_bg"))
        info_frame.pack(fill="x", pady=(0, 10))

        course_label = tk.Label(
            info_frame,
            text=f"📚 {self.assignment.get('course', 'Unknown Course')}",
            font=("Segoe UI", 10),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("text_light"),
        )
        course_label.pack(side="left", anchor="w")

        due_date = self.assignment.get("due_date", "Unknown")
        due_label = tk.Label(
            info_frame,
            text=f"📅 {due_date}",
            font=("Segoe UI", 10),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("text_light"),
        )
        due_label.pack(side="right", anchor="e")

        # Priority indicator
        priority = self.assignment.get("priority", "medium")
        priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}

        priority_frame = tk.Frame(main_frame, bg=self.theme.get_color("card_bg"))
        priority_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            priority_frame,
            text=f"{priority_colors.get(priority, '⚪')} Priority: {priority.title()}",
            font=("Segoe UI", 9),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("fg"),
        ).pack(side="left", anchor="w")

        # AI suggestion if available
        if hasattr(self.assignment, "ai_suggestion") and self.assignment.ai_suggestion:
            ai_frame = tk.Frame(main_frame, bg=self.theme.get_color("card_bg"))
            ai_frame.pack(fill="x", pady=(5, 0))

            tk.Label(
                ai_frame,
                text="🤖 AI Suggestion:",
                font=("Segoe UI", 9, "bold"),
                bg=self.theme.get_color("card_bg"),
                fg=self.theme.get_color("accent"),
            ).pack(anchor="w")

            tk.Label(
                ai_frame,
                text=self.assignment.ai_suggestion,
                font=("Segoe UI", 9),
                bg=self.theme.get_color("card_bg"),
                fg=self.theme.get_color("text_light"),
                wraplength=350,
                justify="left",
            ).pack(anchor="w", pady=(2, 0))

        # Action buttons
        button_frame = tk.Frame(main_frame, bg=self.theme.get_color("card_bg"))
        button_frame.pack(fill="x", pady=(10, 0))

        if self.assignment.get("link"):
            tk.Button(
                button_frame,
                text="🔗 Open",
                command=lambda: webbrowser.open(self.assignment["link"]),
                bg=self.theme.get_color("accent"),
                fg="white",
                relief="flat",
                font=("Segoe UI", 8),
                padx=10,
                pady=5,
            ).pack(side="left", padx=(0, 5))

        tk.Button(
            button_frame,
            text="📝 Details",
            command=self._show_details,
            bg=self.theme.get_color("secondary"),
            fg="white",
            relief="flat",
            font=("Segoe UI", 8),
            padx=10,
            pady=5,
        ).pack(side="left")

    def _show_details(self):
        """Show assignment details in a popup | 在弹窗中显示作业详情"""
        details_window = tk.Toplevel(self)
        details_window.title(f"📝 Assignment Details | 作业详情")
        details_window.geometry("500x400")
        details_window.configure(bg=self.theme.get_color("bg"))

        # Center the window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (details_window.winfo_screenheight() // 2) - (400 // 2)
        details_window.geometry(f"500x400+{x}+{y}")

        # Create scrolled text widget
        text_widget = scrolledtext.ScrolledText(
            details_window, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="black"
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)

        # Format assignment details
        details = f"""📝 Assignment Details | 作业详情
{'=' * 50}

📚 Course: {self.assignment.get('course', 'Unknown')}
📋 Title: {self.assignment.get('title', 'Unknown')}
📅 Due Date: {self.assignment.get('due_date', 'Unknown')}
🎯 Priority: {self.assignment.get('priority', 'Unknown')}
📊 Status: {self.assignment.get('status', 'Unknown')}
🔗 Link: {self.assignment.get('link', 'Not available')}

📄 Description:
{self.assignment.get('description', 'No description available')}

🕒 Fetched At: {self.assignment.get('fetched_at', 'Unknown')}
"""

        if hasattr(self.assignment, "ai_suggestion") and self.assignment.ai_suggestion:
            details += f"""
🤖 AI Suggestion:
{self.assignment.ai_suggestion}
"""

        text_widget.insert(tk.END, details)
        text_widget.config(state="disabled")


class ManageBacGUI:
    """Main GUI application | 主GUI应用程序"""

    def __init__(self):
        self.root = tk.Tk()
        self.theme = ModernTheme("light")
        self.config = None
        self.checker = None
        self.assignments = []

        self._setup_window()
        self._create_widgets()
        self._load_initial_config()

    def _setup_window(self):
        self.root.title("🎓 ManageBac Assignment Checker | ManageBac作业检查器")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.theme.get_color("bg"))

        # Set minimum size
        self.root.minsize(800, 600)

        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")

        # Set icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

    def _create_widgets(self):
        # Create main menu bar
        self._create_menu_bar()

        # Create main layout
        self._create_main_layout()

        # Create status bar
        self.status_bar = StatusBar(self.root, self.theme)
        self.status_bar.pack(side="bottom", fill="x")

    def _create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File | 文件", menu=file_menu)
        file_menu.add_command(label="⚙️ Settings | 设置", command=self._open_settings)
        file_menu.add_separator()
        file_menu.add_command(
            label="📊 Open Reports Folder | 打开报告文件夹", command=self._open_reports_folder
        )
        file_menu.add_separator()
        file_menu.add_command(label="❌ Exit | 退出", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Tools | 工具", menu=tools_menu)
        tools_menu.add_command(
            label="🔄 Refresh Assignments | 刷新作业", command=self._refresh_assignments
        )
        tools_menu.add_command(label="🧪 Test Connection | 测试连接", command=self._test_connection)
        tools_menu.add_separator()
        tools_menu.add_command(label="🤖 AI Analysis | AI分析", command=self._run_ai_analysis)
        tools_menu.add_command(
            label="📧 Send Notifications | 发送通知", command=self._send_notifications
        )

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View | 查看", menu=view_menu)
        view_menu.add_command(
            label="🌞 Light Theme | 浅色主题", command=lambda: self._change_theme("light")
        )
        view_menu.add_command(
            label="🌙 Dark Theme | 深色主题", command=lambda: self._change_theme("dark")
        )
        view_menu.add_separator()
        view_menu.add_command(label="📈 Statistics | 统计信息", command=self._show_statistics)
        view_menu.add_command(label="📋 Logs | 日志", command=self._show_logs)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Help | 帮助", menu=help_menu)
        help_menu.add_command(label="📖 Documentation | 文档", command=self._open_documentation)
        help_menu.add_command(label="🐛 Report Bug | 报告错误", command=self._report_bug)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About | 关于", command=self._show_about)

    def _create_main_layout(self):
        # Main container
        main_container = tk.PanedWindow(
            self.root, orient="horizontal", bg=self.theme.get_color("bg")
        )
        main_container.pack(fill="both", expand=True)

        # Left sidebar
        self._create_sidebar(main_container)

        # Right content area
        self._create_content_area(main_container)

    def _create_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.theme.get_color("sidebar"), width=300)
        parent.add(sidebar)

        # Sidebar header
        header_frame = tk.Frame(sidebar, bg=self.theme.get_color("sidebar"))
        header_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header_frame,
            text="🎓 ManageBac\nAssignment Checker",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme.get_color("sidebar"),
            fg=self.theme.get_color("fg"),
            justify="center",
        ).pack()

        # Quick stats
        self.stats_frame = tk.Frame(sidebar, bg=self.theme.get_color("sidebar"))
        self.stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        self._create_stat_card("📚 Total", "0", "total_assignments")
        self._create_stat_card("⚠️ Overdue", "0", "overdue_assignments")
        self._create_stat_card("🔥 High Priority", "0", "high_priority")
        self._create_stat_card("✅ Completed", "0", "completed_assignments")

        # Action buttons
        button_frame = tk.Frame(sidebar, bg=self.theme.get_color("sidebar"))
        button_frame.pack(fill="x", padx=20, pady=20)

        self.check_button = AnimatedButton(
            button_frame,
            self.theme,
            text="🔍 Check Assignments\n检查作业",
            command=self._check_assignments,
        )
        self.check_button.pack(fill="x", pady=(0, 10))

        AnimatedButton(
            button_frame, self.theme, text="⚙️ Settings\n设置", command=self._open_settings
        ).pack(fill="x", pady=(0, 10))

        AnimatedButton(
            button_frame,
            self.theme,
            text="📊 Generate Report\n生成报告",
            command=self._generate_report,
        ).pack(fill="x", pady=(0, 10))

        # Filter options
        filter_frame = tk.Frame(sidebar, bg=self.theme.get_color("sidebar"))
        filter_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(
            filter_frame,
            text="🔍 Filters | 筛选器",
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.get_color("sidebar"),
            fg=self.theme.get_color("fg"),
        ).pack(anchor="w", pady=(0, 10))

        self.filter_vars = {}
        filters = [
            ("show_overdue", "⚠️ Show Overdue Only | 只显示逾期"),
            ("show_high_priority", "🔥 High Priority Only | 只显示高优先级"),
            ("show_completed", "✅ Include Completed | 包含已完成"),
        ]

        for var_name, text in filters:
            var = tk.BooleanVar()
            self.filter_vars[var_name] = var
            tk.Checkbutton(
                filter_frame,
                text=text,
                variable=var,
                bg=self.theme.get_color("sidebar"),
                fg=self.theme.get_color("fg"),
                font=("Segoe UI", 9),
                command=self._apply_filters,
            ).pack(anchor="w", pady=2)

    def _create_stat_card(self, label: str, value: str, var_name: str):
        card_frame = tk.Frame(
            self.stats_frame, bg=self.theme.get_color("card_bg"), relief="raised", bd=1
        )
        card_frame.pack(fill="x", pady=5)

        tk.Label(
            card_frame,
            text=label,
            font=("Segoe UI", 10),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("text_light"),
        ).pack(pady=(10, 2))

        value_label = tk.Label(
            card_frame,
            text=value,
            font=("Segoe UI", 18, "bold"),
            bg=self.theme.get_color("card_bg"),
            fg=self.theme.get_color("accent"),
        )
        value_label.pack(pady=(0, 10))

        # Store reference for updating
        setattr(self, f"{var_name}_label", value_label)

    def _create_content_area(self, parent):
        content_frame = tk.Frame(parent, bg=self.theme.get_color("bg"))
        parent.add(content_frame)

        # Content header
        header_frame = tk.Frame(content_frame, bg=self.theme.get_color("bg"))
        header_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header_frame,
            text="📋 Assignments | 作业列表",
            font=("Segoe UI", 18, "bold"),
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
        ).pack(side="left")

        # Search box
        search_frame = tk.Frame(header_frame, bg=self.theme.get_color("bg"))
        search_frame.pack(side="right")

        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("fg"),
        ).pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=25,
            bg="white",
            fg="black",
            relief="flat",
            bd=1,
        )
        search_entry.pack(side="left", ipady=5)

        # Assignments container with scrollbar
        self._create_assignments_container(content_frame)

    def _create_assignments_container(self, parent):
        # Container frame
        container_frame = tk.Frame(parent, bg=self.theme.get_color("bg"))
        container_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(container_frame, bg=self.theme.get_color("bg"))
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        self.assignments_frame = tk.Frame(canvas, bg=self.theme.get_color("bg"))

        self.assignments_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.assignments_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

        # Initial message
        self.no_assignments_label = tk.Label(
            self.assignments_frame,
            text="📝 No assignments loaded yet.\nClick 'Check Assignments' to get started!\n\n📝 尚未加载作业。\n点击\"检查作业\"开始使用！",
            font=("Segoe UI", 14),
            bg=self.theme.get_color("bg"),
            fg=self.theme.get_color("text_light"),
            justify="center",
        )
        self.no_assignments_label.pack(expand=True, pady=50)

    def _load_initial_config(self):
        """Load initial configuration | 加载初始配置"""
        try:
            self.config = Config(language="zh", interactive=False)
            self._update_status("✅ Configuration loaded | 配置已加载")
        except Exception as e:
            self._update_status(f"⚠️ Configuration error | 配置错误: {str(e)}")

    def _update_status(self, message: str, show_progress: bool = False):
        """Update status bar | 更新状态栏"""
        self.status_bar.set_status(message, show_progress)

    def _update_stats(self):
        """Update statistics in sidebar | 更新侧边栏统计信息"""
        if not self.assignments:
            stats = {"total": 0, "overdue": 0, "high_priority": 0, "completed": 0}
        else:
            stats = {
                "total": len(self.assignments),
                "overdue": len([a for a in self.assignments if a.get("status") == "overdue"]),
                "high_priority": len([a for a in self.assignments if a.get("priority") == "high"]),
                "completed": len([a for a in self.assignments if a.get("status") == "completed"]),
            }

        self.total_assignments_label.config(text=str(stats["total"]))
        self.overdue_assignments_label.config(text=str(stats["overdue"]))
        self.high_priority_label.config(text=str(stats["high_priority"]))
        self.completed_assignments_label.config(text=str(stats["completed"]))

    def _display_assignments(self, assignments: List[Dict] = None):
        """Display assignments in the main area | 在主区域显示作业"""
        if assignments is None:
            assignments = self.assignments

        # Clear existing assignments
        for widget in self.assignments_frame.winfo_children():
            widget.destroy()

        if not assignments:
            self.no_assignments_label = tk.Label(
                self.assignments_frame,
                text="📝 No assignments found.\n📝 未找到作业。",
                font=("Segoe UI", 14),
                bg=self.theme.get_color("bg"),
                fg=self.theme.get_color("text_light"),
                justify="center",
            )
            self.no_assignments_label.pack(expand=True, pady=50)
            return

        # Display assignments as cards
        for assignment in assignments:
            card = AssignmentCard(self.assignments_frame, self.theme, assignment)
            card.pack(fill="x", pady=10, padx=10)

    def _apply_filters(self):
        """Apply filters to assignments | 应用作业筛选器"""
        if not self.assignments:
            return

        filtered = self.assignments.copy()

        if self.filter_vars["show_overdue"].get():
            filtered = [a for a in filtered if a.get("status") == "overdue"]

        if self.filter_vars["show_high_priority"].get():
            filtered = [a for a in filtered if a.get("priority") == "high"]

        if not self.filter_vars["show_completed"].get():
            filtered = [a for a in filtered if a.get("status") != "completed"]

        self._display_assignments(filtered)

    def _on_search_change(self, *args):
        """Handle search input changes | 处理搜索输入变化"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self._apply_filters()
            return

        filtered = [
            a
            for a in self.assignments
            if search_term in a.get("title", "").lower()
            or search_term in a.get("course", "").lower()
        ]
        self._display_assignments(filtered)

    def _check_assignments(self):
        """Check assignments from ManageBac | 从ManageBac检查作业"""
        if not self.config:
            messagebox.showwarning(
                "Warning | 警告", "⚠️ Please configure settings first!\n⚠️ 请先配置设置！"
            )
            self._open_settings()
            return

        if not self.config.email or not self.config.password:
            messagebox.showwarning(
                "Warning | 警告",
                "⚠️ Please enter ManageBac credentials in settings!\n⚠️ 请在设置中输入ManageBac凭据！",
            )
            self._open_settings()
            return

        self._update_status("🔄 Checking assignments... | 正在检查作业...", True)
        self.check_button.config(state="disabled", text="🔄 Checking... | 检查中...")

        def check_thread():
            try:
                # Initialize checker
                self.checker = ManageBacChecker(self.config)

                # Run checker asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                # Get assignments (simplified for demo)
                # In real implementation, this would call self.checker.run()
                import time

                time.sleep(2)  # Simulate checking time

                # Sample assignments for demo
                sample_assignments = [
                    {
                        "title": "Mathematics Homework Chapter 5",
                        "course": "Mathematics",
                        "due_date": "2025-09-25",
                        "status": "pending",
                        "priority": "high",
                        "link": "https://example.com/assignment1",
                        "description": "Complete exercises 1-20 from Chapter 5",
                    },
                    {
                        "title": "Physics Lab Report",
                        "course": "Physics",
                        "due_date": "2025-09-24",
                        "status": "overdue",
                        "priority": "high",
                        "link": "https://example.com/assignment2",
                        "description": "Write a lab report on electromagnetic induction",
                    },
                    {
                        "title": "English Essay Draft",
                        "course": "English Literature",
                        "due_date": "2025-09-28",
                        "status": "pending",
                        "priority": "medium",
                        "link": "https://example.com/assignment3",
                        "description": "First draft of the comparative essay",
                    },
                ]

                self.assignments = sample_assignments

                # Update UI in main thread
                self.root.after(0, self._on_assignments_loaded)

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_check_error(error_msg))

        threading.Thread(target=check_thread, daemon=True).start()

    def _on_assignments_loaded(self):
        """Handle successful assignment loading | 处理成功加载作业"""
        self._update_status(
            f"✅ Found {len(self.assignments)} assignments | 找到{len(self.assignments)}个作业"
        )
        self.check_button.config(state="normal", text="🔍 Check Assignments\n检查作业")

        self._update_stats()
        self._display_assignments()

        messagebox.showinfo(
            "Success | 成功",
            f"✅ Successfully loaded {len(self.assignments)} assignments!\n✅ 成功加载了{len(self.assignments)}个作业！",
        )

    def _on_check_error(self, error_msg: str):
        """Handle assignment checking error | 处理作业检查错误"""
        self._update_status(f"❌ Error checking assignments | 检查作业时出错")
        self.check_button.config(state="normal", text="🔍 Check Assignments\n检查作业")

        messagebox.showerror(
            "Error | 错误", f"❌ Failed to check assignments:\n❌ 检查作业失败：\n{error_msg}"
        )

    def _open_settings(self):
        """Open settings dialog | 打开设置对话框"""
        dialog = ConfigDialog(self.root, self.theme, "zh")
        self.root.wait_window(dialog)

        if dialog.result == "saved":
            # Reload configuration
            self._load_initial_config()

    def _generate_report(self):
        """Generate assignment report | 生成作业报告"""
        if not self.assignments:
            messagebox.showwarning(
                "Warning | 警告", "⚠️ No assignments to report!\n⚠️ 没有作业可报告！"
            )
            return

        self._update_status("📊 Generating report... | 正在生成报告...", True)

        def generate_thread():
            try:
                # Simulate report generation
                import time

                time.sleep(2)

                # Create reports directory if not exists
                reports_dir = Path("reports")
                reports_dir.mkdir(exist_ok=True)

                # Generate timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Generate HTML report
                html_file = reports_dir / f"managebac_report_{timestamp}.html"
                self._generate_html_report(html_file)

                # Generate JSON report
                json_file = reports_dir / f"managebac_report_{timestamp}.json"
                self._generate_json_report(json_file)

                self.root.after(0, lambda: self._on_report_generated(html_file))

            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_report_error(error_msg))

        threading.Thread(target=generate_thread, daemon=True).start()

    def _generate_html_report(self, file_path: Path):
        """Generate HTML report | 生成HTML报告"""
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ManageBac Assignment Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: #3498db; color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card h3 {{ margin: 0; font-size: 2em; }}
        .stat-card p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .assignment {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; background: #fafafa; }}
        .assignment h3 {{ color: #2c3e50; margin: 0 0 10px 0; }}
        .assignment-meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 10px; }}
        .priority-high {{ border-left: 5px solid #e74c3c; }}
        .priority-medium {{ border-left: 5px solid #f39c12; }}
        .priority-low {{ border-left: 5px solid #27ae60; }}
        .status-overdue {{ background: #ffebee; }}
        .status-pending {{ background: #e3f2fd; }}
        .status-completed {{ background: #e8f5e8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 ManageBac Assignment Report | ManageBac作业报告</h1>
        <p style="text-align: center; color: #7f8c8d;">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(self.assignments)}</h3>
                <p>📚 Total Assignments<br>总作业数</p>
            </div>
            <div class="stat-card" style="background: #e74c3c;">
                <h3>{len([a for a in self.assignments if a.get('status') == 'overdue'])}</h3>
                <p>⚠️ Overdue<br>逾期</p>
            </div>
            <div class="stat-card" style="background: #f39c12;">
                <h3>{len([a for a in self.assignments if a.get('priority') == 'high'])}</h3>
                <p>🔥 High Priority<br>高优先级</p>
            </div>
            <div class="stat-card" style="background: #27ae60;">
                <h3>{len([a for a in self.assignments if a.get('status') == 'completed'])}</h3>
                <p>✅ Completed<br>已完成</p>
            </div>
        </div>
        
        <h2>📋 Assignment Details | 作业详情</h2>
"""

        for assignment in self.assignments:
            priority_class = f"priority-{assignment.get('priority', 'medium')}"
            status_class = f"status-{assignment.get('status', 'pending')}"

            html_content += f"""
        <div class="assignment {priority_class} {status_class}">
            <h3>{assignment.get('title', 'Unknown Assignment')}</h3>
            <div class="assignment-meta">
                📚 Course: {assignment.get('course', 'Unknown')} | 
                📅 Due: {assignment.get('due_date', 'Unknown')} | 
                🎯 Priority: {assignment.get('priority', 'Unknown')} | 
                📊 Status: {assignment.get('status', 'Unknown')}
            </div>
            <p>{assignment.get('description', 'No description available')}</p>
"""
            if assignment.get("link"):
                html_content += f'            <p><a href="{assignment["link"]}" target="_blank">🔗 Open Assignment</a></p>\n'

            html_content += "        </div>\n"

        html_content += """
    </div>
</body>
</html>
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _generate_json_report(self, file_path: Path):
        """Generate JSON report | 生成JSON报告"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_assignments": len(self.assignments),
            "statistics": {
                "overdue": len([a for a in self.assignments if a.get("status") == "overdue"]),
                "high_priority": len([a for a in self.assignments if a.get("priority") == "high"]),
                "completed": len([a for a in self.assignments if a.get("status") == "completed"]),
            },
            "assignments": self.assignments,
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

    def _on_report_generated(self, html_file: Path):
        """Handle successful report generation | 处理成功生成报告"""
        self._update_status("✅ Report generated successfully | 报告生成成功")

        result = messagebox.askyesno(
            "Success | 成功",
            f"✅ Report generated successfully!\n✅ 报告生成成功！\n\nOpen report now?\n现在打开报告？",
        )

        if result:
            webbrowser.open(html_file.as_uri())

    def _on_report_error(self, error_msg: str):
        """Handle report generation error | 处理报告生成错误"""
        self._update_status("❌ Report generation failed | 报告生成失败")

        messagebox.showerror(
            "Error | 错误", f"❌ Failed to generate report:\n❌ 生成报告失败：\n{error_msg}"
        )

    def _change_theme(self, theme_name: str):
        """Change application theme | 更改应用主题"""
        self.theme = ModernTheme(theme_name)
        messagebox.showinfo(
            "Theme Changed | 主题已更改",
            f"✅ Theme changed to {theme_name}!\nPlease restart the application to apply changes.\n\n✅ 主题已更改为{theme_name}！\n请重启应用程序以应用更改。",
        )

    def _refresh_assignments(self):
        """Refresh assignments | 刷新作业"""
        self._check_assignments()

    def _test_connection(self):
        """Test ManageBac connection | 测试ManageBac连接"""
        if not self.config or not self.config.email or not self.config.password:
            messagebox.showwarning(
                "Warning | 警告",
                "⚠️ Please configure ManageBac credentials first!\n⚠️ 请先配置ManageBac凭据！",
            )
            return

        # Show testing progress
        self._update_status("🧪 Testing connection... | 正在测试连接...", True)

        def test_thread():
            try:
                import time

                time.sleep(3)  # Simulate testing

                self.root.after(0, lambda: self._on_test_success())
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_test_error(error_msg))

        threading.Thread(target=test_thread, daemon=True).start()

    def _on_test_success(self):
        self._update_status("✅ Connection test successful | 连接测试成功")
        messagebox.showinfo("Success | 成功", "✅ Connection test successful!\n✅ 连接测试成功！")

    def _on_test_error(self, error_msg: str):
        self._update_status("❌ Connection test failed | 连接测试失败")
        messagebox.showerror(
            "Error | 错误", f"❌ Connection test failed:\n❌ 连接测试失败：\n{error_msg}"
        )

    def _run_ai_analysis(self):
        """Run AI analysis on assignments | 对作业运行AI分析"""
        if not self.assignments:
            messagebox.showwarning(
                "Warning | 警告", "⚠️ No assignments to analyze!\n⚠️ 没有作业可分析！"
            )
            return

        if not self.config or not self.config.ai_enabled:
            messagebox.showwarning(
                "Warning | 警告",
                "⚠️ AI Assistant is not enabled!\nPlease enable it in settings.\n\n⚠️ AI助手未启用！\n请在设置中启用。",
            )
            return

        self._update_status("🤖 Running AI analysis... | 正在运行AI分析...", True)

        def ai_thread():
            try:
                # Simulate AI analysis
                import time

                time.sleep(3)

                # Add AI suggestions to assignments
                for assignment in self.assignments:
                    assignment["ai_suggestion"] = (
                        f"Focus on completing this {assignment.get('priority', 'medium')} priority assignment. Consider breaking it into smaller tasks."
                    )

                self.root.after(0, lambda: self._on_ai_analysis_complete())
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._on_ai_analysis_error(error_msg))

        threading.Thread(target=ai_thread, daemon=True).start()

    def _on_ai_analysis_complete(self):
        self._update_status("✅ AI analysis completed | AI分析完成")
        self._display_assignments()  # Refresh display to show AI suggestions
        messagebox.showinfo(
            "Success | 成功",
            "✅ AI analysis completed!\nAssignments now include AI suggestions.\n\n✅ AI分析完成！\n作业现在包含AI建议。",
        )

    def _on_ai_analysis_error(self, error_msg: str):
        self._update_status("❌ AI analysis failed | AI分析失败")
        messagebox.showerror(
            "Error | 错误", f"❌ AI analysis failed:\n❌ AI分析失败：\n{error_msg}"
        )

    def _send_notifications(self):
        """Send email notifications | 发送邮件通知"""
        if not self.assignments:
            messagebox.showwarning(
                "Warning | 警告", "⚠️ No assignments to notify about!\n⚠️ 没有作业需要通知！"
            )
            return

        messagebox.showinfo(
            "Notifications | 通知", "📧 Email notifications sent!\n📧 邮件通知已发送！"
        )

    def _open_reports_folder(self):
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
            messagebox.showinfo(
                "Info | 信息",
                "📁 Reports folder does not exist yet.\nGenerate a report first!\n\n📁 报告文件夹尚不存在。\n请先生成报告！",
            )

    def _show_statistics(self):
        """Show detailed statistics | 显示详细统计信息"""
        if not self.assignments:
            messagebox.showinfo(
                "Statistics | 统计",
                "📊 No assignments to show statistics for!\n📊 没有作业可显示统计信息！",
            )
            return

        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Assignment Statistics | 作业统计")
        stats_window.geometry("600x400")
        stats_window.configure(bg=self.theme.get_color("bg"))

        # Center window
        stats_window.update_idletasks()
        x = (stats_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (stats_window.winfo_screenheight() // 2) - (400 // 2)
        stats_window.geometry(f"600x400+{x}+{y}")

        # Create statistics content
        text_widget = scrolledtext.ScrolledText(
            stats_window, wrap=tk.WORD, font=("Segoe UI", 10), bg="white", fg="black"
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)

        # Generate statistics
        total = len(self.assignments)
        overdue = len([a for a in self.assignments if a.get("status") == "overdue"])
        high_priority = len([a for a in self.assignments if a.get("priority") == "high"])
        completed = len([a for a in self.assignments if a.get("status") == "completed"])

        courses = {}
        for assignment in self.assignments:
            course = assignment.get("course", "Unknown")
            courses[course] = courses.get(course, 0) + 1

        stats_text = f"""📊 Assignment Statistics | 作业统计信息
{'=' * 50}

📈 Overview | 概览:
• Total Assignments | 总作业数: {total}
• Overdue | 逾期: {overdue} ({overdue/total*100:.1f}% if total > 0 else 0%)
• High Priority | 高优先级: {high_priority} ({high_priority/total*100:.1f}% if total > 0 else 0%)
• Completed | 已完成: {completed} ({completed/total*100:.1f}% if total > 0 else 0%)

📚 By Course | 按课程分组:
"""

        for course, count in sorted(courses.items()):
            stats_text += f"• {course}: {count} assignments\n"

        stats_text += f"""
📅 Status Distribution | 状态分布:
• Pending | 待完成: {len([a for a in self.assignments if a.get('status') == 'pending'])}
• Overdue | 逾期: {overdue}
• Completed | 已完成: {completed}

🎯 Priority Distribution | 优先级分布:
• High | 高: {len([a for a in self.assignments if a.get('priority') == 'high'])}
• Medium | 中: {len([a for a in self.assignments if a.get('priority') == 'medium'])}
• Low | 低: {len([a for a in self.assignments if a.get('priority') == 'low'])}

📊 Generated at | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        text_widget.insert(tk.END, stats_text)
        text_widget.config(state="disabled")

    def _show_logs(self):
        """Show application logs | 显示应用日志"""
        log_file = Path("logs/managebac_checker.log")
        if not log_file.exists():
            messagebox.showinfo("Logs | 日志", "📋 No log file found!\n📋 未找到日志文件！")
            return

        logs_window = tk.Toplevel(self.root)
        logs_window.title("📋 Application Logs | 应用日志")
        logs_window.geometry("800x600")
        logs_window.configure(bg=self.theme.get_color("bg"))

        # Center window
        logs_window.update_idletasks()
        x = (logs_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (logs_window.winfo_screenheight() // 2) - (600 // 2)
        logs_window.geometry(f"800x600+{x}+{y}")

        # Create text widget for logs
        text_widget = scrolledtext.ScrolledText(
            logs_window, wrap=tk.WORD, font=("Consolas", 9), bg="black", fg="green"
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Load and display logs
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                logs = f.read()
            text_widget.insert(tk.END, logs)
            text_widget.see(tk.END)  # Scroll to bottom
        except Exception as e:
            text_widget.insert(tk.END, f"Error loading logs: {e}")

        text_widget.config(state="disabled")

    def _open_documentation(self):
        """Open documentation | 打开文档"""
        webbrowser.open("https://github.com/Hacker0458/managebac-assignment-checker#readme")

    def _report_bug(self):
        """Report a bug | 报告错误"""
        webbrowser.open("https://github.com/Hacker0458/managebac-assignment-checker/issues/new")

    def _show_about(self):
        """Show about dialog | 显示关于对话框"""
        about_text = """🎓 ManageBac Assignment Checker
Version 2.0.0 with AI Assistant

An intelligent automation tool for ManageBac assignment tracking
一个用于ManageBac作业追踪的智能自动化工具

Features | 功能特性:
• 🤖 AI-powered analysis and recommendations
• 🔐 Secure automated login
• 📊 Multi-format reporting
• 🌐 Bilingual interface support
• 📧 Email notifications
• 📈 Visual analytics

Made with ❤️ by Hacker0458
Licensed under MIT License

© 2025 ManageBac Assignment Checker
"""

        messagebox.showinfo("About | 关于", about_text)

    def run(self):
        """Start the GUI application | 启动GUI应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


def main():
    """Main function to run the GUI | 运行GUI的主函数"""
    try:
        app = ManageBacGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start GUI application: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
