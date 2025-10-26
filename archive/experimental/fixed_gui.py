#!/usr/bin/env python3
"""
Fixed GUI - Simplified version to identify and fix crash issues
修复的GUI - 简化版本来识别和修复闪退问题
"""

import sys
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from managebac_checker.professional_gui import ProfessionalTheme
    from managebac_checker.system_tray import NotificationManager
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class FixedManageBacGUI:
    """Simplified ManageBac GUI for debugging crashes"""

    def __init__(self):
        print("🔍 Initializing FixedManageBacGUI...")

        # Step 1: Basic setup
        self.root = tk.Tk()
        print("  ✅ Created root window")

        # Step 2: Theme
        try:
            self.theme = ProfessionalTheme("professional_light")
            print("  ✅ Created theme")
        except Exception as e:
            print(f"  ❌ Theme creation failed: {e}")
            # Fallback to basic colors
            self.theme = None

        # Step 3: Basic window setup
        try:
            self._setup_basic_window()
            print("  ✅ Basic window setup complete")
        except Exception as e:
            print(f"  ❌ Basic window setup failed: {e}")
            raise

        # Step 4: Notification manager
        try:
            self.notification_manager = NotificationManager("zh")
            print("  ✅ Notification manager created")
        except Exception as e:
            print(f"  ❌ Notification manager failed: {e}")
            self.notification_manager = None

        # Step 5: Basic UI
        try:
            self._create_basic_ui()
            print("  ✅ Basic UI created")
        except Exception as e:
            print(f"  ❌ Basic UI creation failed: {e}")
            raise

        print("✅ FixedManageBacGUI initialization complete")

    def _setup_basic_window(self):
        """Setup basic window properties"""
        self.root.title("🎓 ManageBac Checker - Fixed Version")
        self.root.geometry("800x600")

        if self.theme:
            self.root.configure(bg=self.theme.get_color("background"))
        else:
            self.root.configure(bg="#ffffff")

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 800) // 2
        y = (self.root.winfo_screenheight() - 600) // 2
        self.root.geometry(f"800x600+{x}+{y}")

    def _create_basic_ui(self):
        """Create basic user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="ManageBac Assignment Checker",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Status
        status_label = ttk.Label(
            main_frame,
            text="✅ Application started successfully! GUI is working.",
            font=("Helvetica", 12)
        )
        status_label.pack(pady=(0, 20))

        # Test button
        test_button = ttk.Button(
            main_frame,
            text="Test Button",
            command=self._test_button_click
        )
        test_button.pack(pady=10)

        # Quit button
        quit_button = ttk.Button(
            main_frame,
            text="Quit",
            command=self._quit_application
        )
        quit_button.pack(pady=10)

    def _test_button_click(self):
        """Test button click handler"""
        print("✅ Test button clicked!")
        if self.notification_manager:
            try:
                self.notification_manager.send_notification(
                    "Test", "Button clicked successfully!"
                )
            except Exception as e:
                print(f"❌ Notification failed: {e}")

    def _quit_application(self):
        """Quit application cleanly"""
        print("👋 Quitting application...")
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Start the application"""
        try:
            print("🚀 Starting application mainloop...")

            # Show welcome notification if available
            if self.notification_manager:
                try:
                    self.notification_manager.send_notification(
                        "ManageBac Checker",
                        "Application started successfully!"
                    )
                except Exception as e:
                    print(f"⚠️ Welcome notification failed: {e}")

            # Start main loop
            self.root.mainloop()
            print("✅ Application mainloop completed")

        except KeyboardInterrupt:
            print("🛑 Keyboard interrupt received")
            self._quit_application()
        except Exception as e:
            print(f"❌ Error in run(): {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("🧹 Cleanup completed")


def main():
    """Main function"""
    print("🚀 Starting Fixed ManageBac GUI...")
    print("=" * 50)

    try:
        app = FixedManageBacGUI()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start Fixed GUI: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("✅ Fixed GUI completed successfully")
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)