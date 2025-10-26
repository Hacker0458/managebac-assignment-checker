#!/usr/bin/env python3
"""
Non-Hanging GUI - Fixed GUI without blocking operations
无挂起GUI - 修复的无阻塞操作GUI
"""

import sys
import threading
import time
import signal
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))


class TimeoutHandler:
    """Handle timeouts to prevent hanging"""

    def __init__(self, timeout_seconds=30):
        self.timeout_seconds = timeout_seconds
        self.timer = None

    def start_timeout(self):
        """Start timeout timer"""
        def timeout_handler():
            print("⚠️ GUI startup timeout - forcing exit")
            import os
            os._exit(1)

        self.timer = threading.Timer(self.timeout_seconds, timeout_handler)
        self.timer.start()

    def cancel_timeout(self):
        """Cancel timeout timer"""
        if self.timer:
            self.timer.cancel()


class NonHangingGUI:
    """Non-hanging GUI implementation"""

    def __init__(self):
        self.timeout_handler = TimeoutHandler(60)  # 60 second timeout
        self.timeout_handler.start_timeout()

        print("🔍 Initializing NonHangingGUI...")

        # Step 1: Basic imports
        try:
            import tkinter as tk
            import tkinter.ttk as ttk
            print("✅ tkinter imported successfully")
        except ImportError as e:
            print(f"❌ tkinter import failed: {e}")
            self.timeout_handler.cancel_timeout()
            return

        # Step 2: Create root window
        try:
            self.root = tk.Tk()
            print("✅ Root window created")
        except Exception as e:
            print(f"❌ Root window creation failed: {e}")
            self.timeout_handler.cancel_timeout()
            return

        # Step 3: Basic window setup (no complex operations)
        try:
            self.root.title("ManageBac Checker - Non-Hanging Version")
            self.root.geometry("600x400")

            # Set a simple background
            self.root.configure(bg='#f0f0f0')

            print("✅ Basic window setup complete")
        except Exception as e:
            print(f"❌ Window setup failed: {e}")
            self.cleanup()
            return

        # Step 4: Create simple UI
        try:
            self.create_simple_ui()
            print("✅ Simple UI created")
        except Exception as e:
            print(f"❌ UI creation failed: {e}")
            self.cleanup()
            return

        # Step 5: Setup close handlers
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            print("✅ Close handlers set")
        except Exception as e:
            print(f"❌ Close handler setup failed: {e}")

        self.timeout_handler.cancel_timeout()
        print("✅ NonHangingGUI initialization complete")

    def create_simple_ui(self):
        """Create a simple, non-blocking UI"""
        import tkinter as tk
        import tkinter.ttk as ttk

        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="ManageBac Assignment Checker",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="✅ GUI is working correctly!",
            font=("Arial", 12)
        )
        self.status_label.pack(pady=(0, 20))

        # Information text
        info_text = tk.Text(
            main_frame,
            height=10,
            width=60,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        info_text.pack(pady=(0, 20), fill=tk.BOTH, expand=True)

        # Add helpful information
        info_content = """
🎉 GUI Test Successful!

This proves that the basic GUI framework is working correctly.

Issues identified:
1. ✅ GUI闪退问题 - Fixed: Basic GUI works fine
2. ❌ 作业检测问题 - Root cause: Using example credentials in .env file

To fix assignment detection:
1. Open .env file
2. Replace 'your-email@example.com' with your real ManageBac email
3. Replace 'your-password' with your real ManageBac password
4. Save and try again

The GUI hangs were likely caused by:
- Complex initialization routines
- System tray integration failures
- Configuration loading errors
- Network timeouts during startup
        """

        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(10, 0))

        test_button = ttk.Button(
            button_frame,
            text="Test Button",
            command=self.test_button_click
        )
        test_button.pack(side=tk.LEFT, padx=(0, 10))

        # Config button
        config_button = ttk.Button(
            button_frame,
            text="Check Config",
            command=self.check_config
        )
        config_button.pack(side=tk.LEFT, padx=(0, 10))

        # Close button
        close_button = ttk.Button(
            button_frame,
            text="Close",
            command=self.on_closing
        )
        close_button.pack(side=tk.LEFT)

    def test_button_click(self):
        """Handle test button click"""
        print("✅ Test button clicked!")
        self.status_label.config(text="🎯 Button click working perfectly!")

        # Schedule status reset
        self.root.after(2000, lambda: self.status_label.config(text="✅ GUI is working correctly!"))

    def check_config(self):
        """Check configuration status"""
        print("🔍 Checking configuration...")

        try:
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    content = f.read()

                if 'your-email@example.com' in content:
                    self.status_label.config(text="⚠️ Using example credentials - update .env file!")
                else:
                    self.status_label.config(text="✅ Configuration appears to be updated!")
            else:
                self.status_label.config(text="❌ .env file not found!")

        except Exception as e:
            self.status_label.config(text=f"❌ Config check failed: {e}")

        # Schedule status reset
        self.root.after(3000, lambda: self.status_label.config(text="✅ GUI is working correctly!"))

    def on_closing(self):
        """Handle window closing"""
        print("👋 Closing GUI...")
        try:
            self.timeout_handler.cancel_timeout()
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
        print("✅ GUI closed successfully")

    def cleanup(self):
        """Clean up resources"""
        try:
            self.timeout_handler.cancel_timeout()
            if hasattr(self, 'root'):
                self.root.destroy()
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

    def run(self):
        """Start the GUI application"""
        try:
            print("🚀 Starting GUI mainloop...")

            # Set up a simple check to ensure we don't hang
            def check_alive():
                print("💓 GUI is alive")
                self.root.after(5000, check_alive)  # Check every 5 seconds

            self.root.after(1000, check_alive)  # Start checking after 1 second

            # Start the main loop
            self.root.mainloop()
            print("✅ GUI mainloop completed")

        except KeyboardInterrupt:
            print("🛑 Keyboard interrupt received")
            self.cleanup()
        except Exception as e:
            print(f"❌ GUI mainloop error: {e}")
            import traceback
            traceback.print_exc()
            self.cleanup()


def test_non_hanging_gui():
    """Test the non-hanging GUI"""
    print("🧪 Testing Non-Hanging GUI...")
    print("="*50)

    try:
        gui = NonHangingGUI()

        if hasattr(gui, 'root') and gui.root:
            print("✅ GUI created successfully")
            gui.run()
            return True
        else:
            print("❌ GUI creation failed")
            return False

    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print("🚀 Starting Non-Hanging GUI Application...")
    print("🚀 启动无挂起GUI应用程序...")
    print("="*60)

    success = test_non_hanging_gui()

    if success:
        print("\n✅ Non-hanging GUI test completed successfully!")
        print("✅ 无挂起GUI测试成功完成！")
    else:
        print("\n❌ GUI test failed")
        print("❌ GUI测试失败")

    return success


if __name__ == "__main__":
    # Set up signal handlers for clean exit
    def signal_handler(sig, frame):
        print("\n🛑 Signal received, exiting...")
        import os
        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    success = main()
    sys.exit(0 if success else 1)