#!/usr/bin/env python3
"""
Detailed GUI Crash Diagnosis
详细的GUI闪退诊断
"""

import sys
import traceback

def test_detailed_init():
    """Test each initialization step in detail"""
    print("🔍 Testing detailed initialization...")
    try:
        import tkinter as tk
        from managebac_checker.professional_gui import ProfessionalTheme, NotificationManager

        print("  📋 Step 1: Create root window")
        root = tk.Tk()

        print("  📋 Step 2: Create theme")
        theme = ProfessionalTheme("professional_light")

        print("  📋 Step 3: Setup high DPI")
        try:
            root.tk.call("tk", "scaling", 2.0)
        except Exception as e:
            print(f"    ⚠️ High DPI setup failed: {e}")

        print("  📋 Step 4: Setup professional window")
        root.title("🎓 ManageBac Assignment Checker Pro | ManageBac作业检查器专业版")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(max(int(screen_width * 0.8), 1200), 1600)
        window_height = min(max(int(screen_height * 0.8), 800), 1000)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg=theme.get_color("background"))
        root.minsize(1000, 700)

        print("  📋 Step 5: Initialize variables")
        config = None
        checker = None
        assignments = []
        filtered_assignments = []
        tray_manager = None
        notification_manager = NotificationManager("zh")
        auto_check_enabled = False
        auto_check_interval = 30
        auto_check_timer = None

        print("  📋 Step 6: Test create_professional_ui (simulated)")
        # Instead of calling the actual method, let's simulate creating a basic UI
        import tkinter.ttk as ttk
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        test_label = ttk.Label(main_frame, text="Test GUI")
        test_label.pack()

        print("  📋 Step 7: Test system integration (simulated)")
        # Skip actual system integration for now

        print("  📋 Step 8: Test load configuration (simulated)")
        # Skip actual configuration loading for now

        print("  📋 Step 9: Test window display")
        root.after(100, root.quit)
        root.mainloop()
        root.destroy()

        print("✅ Detailed initialization successful")
        return True
    except Exception as e:
        print(f"❌ Detailed initialization failed: {e}")
        traceback.print_exc()
        return False

def test_actual_professional_gui():
    """Test the actual ProfessionalManageBacGUI but with timeout"""
    print("🔍 Testing actual professional GUI with timeout...")
    try:
        from managebac_checker.professional_gui import ProfessionalManageBacGUI
        print("  📋 Creating ProfessionalManageBacGUI instance...")
        app = ProfessionalManageBacGUI()
        print("  📋 Starting run method with timeout...")

        # Add a timeout to prevent hanging
        app.root.after(2000, app.root.quit)  # Quit after 2 seconds
        app.root.mainloop()
        app.root.destroy()

        print("✅ Actual professional GUI test successful")
        return True
    except Exception as e:
        print(f"❌ Actual professional GUI test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run detailed diagnostic tests"""
    print("🚀 Starting detailed GUI crash diagnosis...")
    print("=" * 60)

    tests = [
        ("Detailed Initialization", test_detailed_init),
        ("Actual Professional GUI", test_actual_professional_gui),
    ]

    results = {}
    for test_name, test_func in tests:
        print(f"\n📝 Running: {test_name}")
        print("-" * 40)
        results[test_name] = test_func()

    print("\n" + "=" * 60)
    print("📊 DETAILED DIAGNOSIS RESULTS:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")

if __name__ == "__main__":
    main()