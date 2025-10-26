#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 ManageBac Assignment Checker - First Run Setup GUI
🎬 ManageBac作业检查器 - 首次运行设置GUI

A beautiful first-time setup experience with GUI integration.
漂亮的首次设置体验，集成GUI界面。
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import re
from typing import Dict, Optional
from urllib.parse import urlparse
import threading
import json

try:
    from config_templates import ConfigTemplates
except ImportError:
    ConfigTemplates = None

class FirstRunSetupGUI:
    """First run setup GUI for ManageBac Assignment Checker"""

    def __init__(self, parent=None):
        self.parent = parent
        self.config = {}
        self.templates = ConfigTemplates() if ConfigTemplates else None

        # Create main window
        self.setup_window = tk.Toplevel(parent) if parent else tk.Tk()
        self.setup_window.title("ManageBac Assignment Checker - First Time Setup")
        self.setup_window.geometry("800x700")
        self.setup_window.resizable(True, True)

        # Center window
        self.center_window()

        # Configure styles
        self.setup_styles()

        # Setup variables
        self.setup_variables()

        # Create UI
        self.create_ui()

        # Make modal if parent exists
        if parent:
            self.setup_window.transient(parent)
            self.setup_window.grab_set()

    def center_window(self):
        """Center the window on screen"""
        self.setup_window.update_idletasks()
        width = self.setup_window.winfo_width()
        height = self.setup_window.winfo_height()
        x = (self.setup_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.setup_window.winfo_screenheight() // 2) - (height // 2)
        self.setup_window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_styles(self):
        """Setup UI styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.colors = {
            'primary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'bg': '#ecf0f1',
            'card': '#ffffff',
            'text': '#2c3e50',
            'text_light': '#7f8c8d'
        }

        # Title font
        self.title_font = font.Font(family="SF Pro Display", size=20, weight="bold")
        self.header_font = font.Font(family="SF Pro Display", size=14, weight="bold")
        self.body_font = font.Font(family="SF Pro Text", size=11)

        # Configure ttk styles
        self.style.configure('Title.TLabel', font=self.title_font, foreground=self.colors['text'])
        self.style.configure('Header.TLabel', font=self.header_font, foreground=self.colors['text'])
        self.style.configure('Body.TLabel', font=self.body_font, foreground=self.colors['text'])
        self.style.configure('Success.TLabel', font=self.body_font, foreground=self.colors['success'])
        self.style.configure('Error.TLabel', font=self.body_font, foreground=self.colors['error'])

    def setup_variables(self):
        """Setup UI variables"""
        self.current_step = tk.IntVar(value=0)
        self.total_steps = 5

        # Configuration variables
        self.managebac_url = tk.StringVar(value="https://shtcs.managebac.cn")
        self.managebac_email = tk.StringVar()
        self.managebac_password = tk.StringVar()

        self.ai_enabled = tk.BooleanVar(value=False)
        self.openai_api_key = tk.StringVar()
        self.ai_model = tk.StringVar(value="gpt-3.5-turbo")

        self.notifications_enabled = tk.BooleanVar(value=False)
        self.notification_email = tk.StringVar()
        self.smtp_password = tk.StringVar()

        self.report_formats = {
            'html': tk.BooleanVar(value=True),
            'json': tk.BooleanVar(value=True),
            'markdown': tk.BooleanVar(value=False),
            'console': tk.BooleanVar(value=True)
        }

        self.language = tk.StringVar(value="zh")
        self.template_choice = tk.StringVar(value="student_basic")

    def create_ui(self):
        """Create the main UI"""
        # Main frame
        main_frame = ttk.Frame(self.setup_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.create_header(main_frame)

        # Progress bar
        self.create_progress_bar(main_frame)

        # Content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Navigation buttons
        self.create_navigation(main_frame)

        # Show first step
        self.show_step(0)

    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Icon and title
        title_frame = ttk.Frame(header_frame)
        title_frame.pack()

        ttk.Label(title_frame, text="🧙‍♂️", font=("SF Pro Display", 32)).pack(side=tk.LEFT, padx=(0, 15))

        title_text_frame = ttk.Frame(title_frame)
        title_text_frame.pack(side=tk.LEFT)

        ttk.Label(title_text_frame, text="Welcome to ManageBac Assignment Checker", style='Title.TLabel').pack(anchor=tk.W)
        ttk.Label(title_text_frame, text="欢迎使用ManageBac作业检查器", style='Body.TLabel').pack(anchor=tk.W)
        ttk.Label(title_text_frame, text="Let's get you set up in just a few steps!", style='Body.TLabel', foreground=self.colors['text_light']).pack(anchor=tk.W)

    def create_progress_bar(self, parent):
        """Create progress bar"""
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.pack(pady=5)

        self.progress_label = ttk.Label(progress_frame, text="Step 1 of 5", style='Body.TLabel')
        self.progress_label.pack()

    def create_navigation(self, parent):
        """Create navigation buttons"""
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, pady=(20, 0))

        self.back_btn = ttk.Button(nav_frame, text="← Back", command=self.previous_step)
        self.back_btn.pack(side=tk.LEFT)

        self.next_btn = ttk.Button(nav_frame, text="Next →", command=self.next_step)
        self.next_btn.pack(side=tk.RIGHT)

        self.skip_btn = ttk.Button(nav_frame, text="Skip Setup", command=self.skip_setup)
        self.skip_btn.pack(side=tk.RIGHT, padx=(0, 10))

    def show_step(self, step):
        """Show specific setup step"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Update progress
        progress_value = (step + 1) / self.total_steps * 100
        self.progress['value'] = progress_value
        self.progress_label.config(text=f"Step {step + 1} of {self.total_steps}")

        # Update navigation buttons
        self.back_btn.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        if step < self.total_steps - 1:
            self.next_btn.config(text="Next →")
        else:
            self.next_btn.config(text="Complete Setup")

        # Show appropriate step
        if step == 0:
            self.show_template_selection()
        elif step == 1:
            self.show_basic_config()
        elif step == 2:
            self.show_ai_config()
        elif step == 3:
            self.show_notification_config()
        elif step == 4:
            self.show_summary()

        self.current_step.set(step)

    def show_template_selection(self):
        """Show template selection step"""
        ttk.Label(self.content_frame, text="🎯 Choose Your Setup Template", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 15))

        if self.templates:
            template_list = self.templates.list_templates()

            for key, info in template_list.items():
                template_frame = ttk.LabelFrame(self.content_frame, text=info['name'], padding=10)
                template_frame.pack(fill=tk.X, pady=5)

                ttk.Radiobutton(template_frame, text=info['description'],
                              variable=self.template_choice, value=key).pack(anchor=tk.W)
                ttk.Label(template_frame, text=info['description_zh'],
                         style='Body.TLabel', foreground=self.colors['text_light']).pack(anchor=tk.W, padx=(20, 0))
        else:
            ttk.Label(self.content_frame, text="Templates not available. Using manual configuration.",
                     style='Body.TLabel').pack(anchor=tk.W, pady=5)

    def show_basic_config(self):
        """Show basic configuration step"""
        ttk.Label(self.content_frame, text="🏫 School Information", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 15))

        # School URL
        url_frame = ttk.Frame(self.content_frame)
        url_frame.pack(fill=tk.X, pady=5)
        ttk.Label(url_frame, text="School ManageBac URL:", style='Body.TLabel').pack(anchor=tk.W)
        url_entry = ttk.Entry(url_frame, textvariable=self.managebac_url, font=self.body_font, width=50)
        url_entry.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(url_frame, text="Example: https://shtcs.managebac.cn", style='Body.TLabel',
                 foreground=self.colors['text_light']).pack(anchor=tk.W)

        ttk.Separator(self.content_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        # Credentials
        ttk.Label(self.content_frame, text="🔐 Login Credentials", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 10))

        # Email
        email_frame = ttk.Frame(self.content_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="Email:", style='Body.TLabel').pack(anchor=tk.W)
        email_entry = ttk.Entry(email_frame, textvariable=self.managebac_email, font=self.body_font, width=50)
        email_entry.pack(fill=tk.X, pady=(5, 0))

        # Password
        password_frame = ttk.Frame(self.content_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="Password:", style='Body.TLabel').pack(anchor=tk.W)
        password_entry = ttk.Entry(password_frame, textvariable=self.managebac_password, show="*", font=self.body_font, width=50)
        password_entry.pack(fill=tk.X, pady=(5, 0))

    def show_ai_config(self):
        """Show AI configuration step"""
        ttk.Label(self.content_frame, text="🤖 AI Assistant (Optional)", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 15))

        # AI Enable checkbox
        ai_check = ttk.Checkbutton(self.content_frame, text="Enable AI-powered analysis and insights",
                                  variable=self.ai_enabled, command=self.toggle_ai_options)
        ai_check.pack(anchor=tk.W, pady=5)

        # AI options frame
        self.ai_options_frame = ttk.Frame(self.content_frame)
        self.ai_options_frame.pack(fill=tk.X, pady=10)

        # API Key
        api_key_frame = ttk.Frame(self.ai_options_frame)
        api_key_frame.pack(fill=tk.X, pady=5)
        ttk.Label(api_key_frame, text="OpenAI API Key:", style='Body.TLabel').pack(anchor=tk.W)
        api_key_entry = ttk.Entry(api_key_frame, textvariable=self.openai_api_key, show="*", font=self.body_font, width=50)
        api_key_entry.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(api_key_frame, text="Get your key from: https://platform.openai.com/api-keys", style='Body.TLabel',
                 foreground=self.colors['text_light']).pack(anchor=tk.W)

        # Model selection
        model_frame = ttk.Frame(self.ai_options_frame)
        model_frame.pack(fill=tk.X, pady=10)
        ttk.Label(model_frame, text="AI Model:", style='Body.TLabel').pack(anchor=tk.W)
        model_combo = ttk.Combobox(model_frame, textvariable=self.ai_model, values=["gpt-3.5-turbo", "gpt-4"], state="readonly")
        model_combo.pack(anchor=tk.W, pady=(5, 0))

        # Benefits
        benefits_frame = ttk.LabelFrame(self.content_frame, text="AI Features", padding=10)
        benefits_frame.pack(fill=tk.X, pady=10)

        benefits = [
            "📊 Analyze assignment patterns and workload",
            "📈 Generate insights about academic performance",
            "💡 Provide study suggestions and time management tips",
            "🎯 Prioritize assignments based on difficulty"
        ]

        for benefit in benefits:
            ttk.Label(benefits_frame, text=benefit, style='Body.TLabel').pack(anchor=tk.W, pady=2)

        self.toggle_ai_options()

    def show_notification_config(self):
        """Show notification configuration step"""
        ttk.Label(self.content_frame, text="📧 Email Notifications (Optional)", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 15))

        # Notifications enable checkbox
        notif_check = ttk.Checkbutton(self.content_frame, text="Enable email notifications for assignments",
                                     variable=self.notifications_enabled, command=self.toggle_notification_options)
        notif_check.pack(anchor=tk.W, pady=5)

        # Notification options frame
        self.notif_options_frame = ttk.Frame(self.content_frame)
        self.notif_options_frame.pack(fill=tk.X, pady=10)

        # Email
        notif_email_frame = ttk.Frame(self.notif_options_frame)
        notif_email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(notif_email_frame, text="Notification Email:", style='Body.TLabel').pack(anchor=tk.W)
        notif_email_entry = ttk.Entry(notif_email_frame, textvariable=self.notification_email, font=self.body_font, width=50)
        notif_email_entry.pack(fill=tk.X, pady=(5, 0))

        # SMTP Password
        smtp_pass_frame = ttk.Frame(self.notif_options_frame)
        smtp_pass_frame.pack(fill=tk.X, pady=5)
        ttk.Label(smtp_pass_frame, text="Email App Password:", style='Body.TLabel').pack(anchor=tk.W)
        smtp_pass_entry = ttk.Entry(smtp_pass_frame, textvariable=self.smtp_password, show="*", font=self.body_font, width=50)
        smtp_pass_entry.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(smtp_pass_frame, text="For Gmail: Use App Password, not your regular password", style='Body.TLabel',
                 foreground=self.colors['text_light']).pack(anchor=tk.W)

        # Report formats
        format_frame = ttk.LabelFrame(self.content_frame, text="Report Formats", padding=10)
        format_frame.pack(fill=tk.X, pady=15)

        for format_name, var in self.report_formats.items():
            ttk.Checkbutton(format_frame, text=format_name.upper(), variable=var).pack(side=tk.LEFT, padx=10)

        self.toggle_notification_options()

    def show_summary(self):
        """Show configuration summary"""
        ttk.Label(self.content_frame, text="📋 Configuration Summary", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 15))

        # Create scrollable summary
        summary_frame = tk.Frame(self.content_frame, bg='white', relief=tk.SUNKEN, bd=1)
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(summary_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.summary_text = tk.Text(summary_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                                   font=self.body_font, bg='white', fg=self.colors['text'])
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.summary_text.yview)

        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate configuration summary"""
        summary = "🎯 Your Configuration:\n\n"

        summary += f"Template: {self.template_choice.get()}\n"
        summary += f"School URL: {self.managebac_url.get()}\n"
        summary += f"Email: {self.managebac_email.get()}\n"
        summary += f"Password: {'*' * len(self.managebac_password.get()) if self.managebac_password.get() else 'Not set'}\n\n"

        summary += f"AI Assistant: {'Enabled' if self.ai_enabled.get() else 'Disabled'}\n"
        if self.ai_enabled.get():
            summary += f"AI Model: {self.ai_model.get()}\n"
            summary += f"API Key: {'Set' if self.openai_api_key.get() else 'Not set'}\n\n"

        summary += f"Email Notifications: {'Enabled' if self.notifications_enabled.get() else 'Disabled'}\n"
        if self.notifications_enabled.get():
            summary += f"Notification Email: {self.notification_email.get()}\n\n"

        formats = [name for name, var in self.report_formats.items() if var.get()]
        summary += f"Report Formats: {', '.join(formats)}\n\n"

        summary += "✅ Ready to save configuration!"

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def toggle_ai_options(self):
        """Toggle AI options visibility"""
        if self.ai_enabled.get():
            for widget in self.ai_options_frame.winfo_children():
                widget.pack()
        else:
            for widget in self.ai_options_frame.winfo_children():
                widget.pack_forget()

    def toggle_notification_options(self):
        """Toggle notification options visibility"""
        if self.notifications_enabled.get():
            for widget in self.notif_options_frame.winfo_children():
                widget.pack()
        else:
            for widget in self.notif_options_frame.winfo_children():
                widget.pack_forget()

    def validate_step(self, step):
        """Validate current step"""
        if step == 1:  # Basic config
            if not self.managebac_url.get().strip():
                messagebox.showerror("Error", "Please enter your school's ManageBac URL")
                return False
            if not self.managebac_email.get().strip():
                messagebox.showerror("Error", "Please enter your email")
                return False
            if not self.managebac_password.get().strip():
                messagebox.showerror("Error", "Please enter your password")
                return False

            # Validate URL format
            url = self.managebac_url.get().strip()
            if not url.startswith('http'):
                url = f"https://{url}"
                self.managebac_url.set(url)

            try:
                parsed = urlparse(url)
                if not parsed.netloc or 'managebac' not in parsed.netloc.lower():
                    messagebox.showerror("Error", "Please enter a valid ManageBac URL")
                    return False
            except:
                messagebox.showerror("Error", "Please enter a valid URL")
                return False

            # Validate email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.managebac_email.get().strip()):
                messagebox.showerror("Error", "Please enter a valid email address")
                return False

        elif step == 2:  # AI config
            if self.ai_enabled.get() and not self.openai_api_key.get().strip():
                result = messagebox.askyesno("Warning", "AI is enabled but no API key provided. Continue without AI?")
                if result:
                    self.ai_enabled.set(False)
                else:
                    return False

        elif step == 3:  # Notifications
            if self.notifications_enabled.get():
                if not self.notification_email.get().strip():
                    messagebox.showerror("Error", "Please enter notification email")
                    return False
                if not self.smtp_password.get().strip():
                    result = messagebox.askyesno("Warning", "No email password provided. Continue without notifications?")
                    if result:
                        self.notifications_enabled.set(False)
                    else:
                        return False

        return True

    def next_step(self):
        """Go to next step"""
        current = self.current_step.get()

        if not self.validate_step(current):
            return

        if current < self.total_steps - 1:
            self.show_step(current + 1)
        else:
            self.complete_setup()

    def previous_step(self):
        """Go to previous step"""
        current = self.current_step.get()
        if current > 0:
            self.show_step(current - 1)

    def skip_setup(self):
        """Skip setup and create basic config"""
        result = messagebox.askyesno("Skip Setup", "Are you sure you want to skip the setup?\nYou can run the setup wizard later.")
        if result:
            self.create_basic_config()
            self.setup_window.destroy()

    def complete_setup(self):
        """Complete the setup process"""
        # Collect all configuration
        user_config = {
            'MANAGEBAC_URL': self.managebac_url.get().strip(),
            'MANAGEBAC_EMAIL': self.managebac_email.get().strip(),
            'MANAGEBAC_PASSWORD': self.managebac_password.get().strip(),
            'AI_ENABLED': str(self.ai_enabled.get()).lower(),
            'ENABLE_EMAIL_NOTIFICATIONS': str(self.notifications_enabled.get()).lower(),
            'LANGUAGE': self.language.get()
        }

        if self.ai_enabled.get():
            user_config['OPENAI_API_KEY'] = self.openai_api_key.get().strip()
            user_config['AI_MODEL'] = self.ai_model.get()

        if self.notifications_enabled.get():
            user_config['NOTIFICATION_RECIPIENTS'] = self.notification_email.get().strip()
            user_config['SMTP_USERNAME'] = self.notification_email.get().strip()
            user_config['SMTP_PASSWORD'] = self.smtp_password.get().strip()

        # Report formats
        formats = [name for name, var in self.report_formats.items() if var.get()]
        user_config['REPORT_FORMAT'] = ','.join(formats)

        # Apply template if available
        if self.templates:
            try:
                success = self.templates.create_env_from_template(
                    self.template_choice.get(), user_config, ".env"
                )
                if success:
                    messagebox.showinfo("Success", "Configuration saved successfully!\n\nYour ManageBac Assignment Checker is ready to use!")
                    self.setup_window.destroy()
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {e}")

        # Fallback to basic config creation
        if self.create_basic_config(user_config):
            messagebox.showinfo("Success", "Basic configuration saved successfully!")
            self.setup_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to save configuration")

    def create_basic_config(self, config=None):
        """Create basic .env file"""
        try:
            if config is None:
                config = {
                    'MANAGEBAC_URL': 'https://your-school.managebac.cn',
                    'MANAGEBAC_EMAIL': 'your.email@example.com',
                    'MANAGEBAC_PASSWORD': 'your_password',
                    'AI_ENABLED': 'false',
                    'ENABLE_EMAIL_NOTIFICATIONS': 'false',
                    'REPORT_FORMAT': 'html,console',
                    'LANGUAGE': 'zh'
                }

            # Basic .env content
            env_content = """# ManageBac Assignment Checker Configuration
# Please fill in your information

# School Information
MANAGEBAC_URL={managebac_url}
MANAGEBAC_EMAIL={managebac_email}
MANAGEBAC_PASSWORD={managebac_password}

# Basic Settings
HEADLESS=true
DEBUG=false
REPORT_FORMAT={report_format}
OUTPUT_DIR=reports
LANGUAGE={language}

# AI Settings
AI_ENABLED={ai_enabled}
{ai_key_line}

# Email Notifications
ENABLE_EMAIL_NOTIFICATIONS={notifications_enabled}
{notification_lines}
""".format(
                managebac_url=config.get('MANAGEBAC_URL', ''),
                managebac_email=config.get('MANAGEBAC_EMAIL', ''),
                managebac_password=config.get('MANAGEBAC_PASSWORD', ''),
                report_format=config.get('REPORT_FORMAT', 'html,console'),
                language=config.get('LANGUAGE', 'zh'),
                ai_enabled=config.get('AI_ENABLED', 'false'),
                ai_key_line=f"OPENAI_API_KEY={config.get('OPENAI_API_KEY', '')}" if config.get('OPENAI_API_KEY') else "# OPENAI_API_KEY=your_api_key_here",
                notifications_enabled=config.get('ENABLE_EMAIL_NOTIFICATIONS', 'false'),
                notification_lines=f"""SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME={config.get('SMTP_USERNAME', '')}
SMTP_PASSWORD={config.get('SMTP_PASSWORD', '')}
NOTIFICATION_RECIPIENTS={config.get('NOTIFICATION_RECIPIENTS', '')}""" if config.get('ENABLE_EMAIL_NOTIFICATIONS') == 'true' else """# SMTP_SERVER=smtp.gmail.com
# SMTP_USERNAME=your.email@gmail.com
# SMTP_PASSWORD=your_app_password
# NOTIFICATION_RECIPIENTS=student@example.com"""
            )

            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)

            return True
        except Exception:
            return False

def show_first_run_setup(parent=None):
    """Show first run setup dialog"""
    setup = FirstRunSetupGUI(parent)
    if parent:
        parent.wait_window(setup.setup_window)
    else:
        setup.setup_window.mainloop()

def main():
    """Main entry point for testing"""
    show_first_run_setup()

if __name__ == "__main__":
    main()