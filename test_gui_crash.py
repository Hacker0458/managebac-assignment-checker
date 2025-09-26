#!/usr/bin/env python3
"""
GUI Crash Diagnosis Tool
用于诊断GUI闪退的详细测试工具
"""

import sys
import traceback
import tkinter as tk

def test_basic_tkinter():
    """Test basic tkinter functionality"""
    print("🔍 Testing basic tkinter...")
    try:
        root = tk.Tk()
        root.title("Test")
        root.geometry("300x200")
        root.after(100, root.quit)  # Close after 100ms
        root.mainloop()
        root.destroy()
        print("✅ Basic tkinter works")
        return True
    except Exception as e:
        print(f"❌ Basic tkinter failed: {e}")
        traceback.print_exc()
        return False

def test_professional_gui_import():
    """Test importing the professional GUI"""
    print("🔍 Testing professional GUI import...")
    try:
        from managebac_checker.professional_gui import ProfessionalManageBacGUI
        print("✅ Professional GUI import successful")
        return True
    except Exception as e:
        print(f"❌ Professional GUI import failed: {e}")
        traceback.print_exc()
        return False

def test_professional_gui_init():
    """Test professional GUI initialization"""
    print("🔍 Testing professional GUI initialization...")
    try:
        from managebac_checker.professional_gui import ProfessionalManageBacGUI
        app = ProfessionalManageBacGUI()
        print("✅ Professional GUI initialization successful")

        # Try to show window briefly
        app.root.after(100, app.root.quit)
        app.root.mainloop()
        app.root.destroy()
        print("✅ Professional GUI window display successful")
        return True
    except Exception as e:
        print(f"❌ Professional GUI initialization failed: {e}")
        traceback.print_exc()
        return False

def test_step_by_step_init():
    """Test step-by-step initialization"""
    print("🔍 Testing step-by-step initialization...")
    try:
        print("  📋 Step 1: Import tkinter")
        import tkinter as tk

        print("  📋 Step 2: Create root window")
        root = tk.Tk()

        print("  📋 Step 3: Import theme")
        from managebac_checker.professional_gui import ProfessionalTheme

        print("  📋 Step 4: Create theme")
        theme = ProfessionalTheme("professional_light")

        print("  📋 Step 5: Setup high DPI")
        try:
            root.tk.call("tk", "scaling", 2.0)
        except Exception as e:
            print(f"    ⚠️ High DPI setup failed: {e}")

        print("  📋 Step 6: Setup window")
        root.title("Test Professional Window")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(max(int(screen_width * 0.8), 1200), 1600)
        window_height = min(max(int(screen_height * 0.8), 800), 1000)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.configure(bg=theme.get_color("background"))
        root.minsize(1000, 700)

        print("  📋 Step 7: Test display")
        root.after(100, root.quit)
        root.mainloop()
        root.destroy()

        print("✅ Step-by-step initialization successful")
        return True
    except Exception as e:
        print(f"❌ Step-by-step initialization failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("🚀 Starting GUI crash diagnosis...")
    print("=" * 60)

    tests = [
        ("Basic Tkinter", test_basic_tkinter),
        ("Professional GUI Import", test_professional_gui_import),
        ("Step-by-Step Init", test_step_by_step_init),
        ("Professional GUI Init", test_professional_gui_init),
    ]

    results = {}
    for test_name, test_func in tests:
        print(f"\n📝 Running: {test_name}")
        print("-" * 40)
        results[test_name] = test_func()

    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS RESULTS:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")

    # Analysis
    print("\n🔍 ANALYSIS:")
    if not results["Basic Tkinter"]:
        print("  ❌ Problem: Basic tkinter is not working")
        print("  💡 Solution: Check Python installation and tkinter availability")
    elif not results["Professional GUI Import"]:
        print("  ❌ Problem: Cannot import professional GUI modules")
        print("  💡 Solution: Check module dependencies and paths")
    elif not results["Step-by-Step Init"]:
        print("  ❌ Problem: Initialization fails at a specific step")
        print("  💡 Solution: Check the failed step in detail")
    elif not results["Professional GUI Init"]:
        print("  ❌ Problem: Professional GUI full initialization fails")
        print("  💡 Solution: Simplify initialization or fix specific component")
    else:
        print("  ✅ All tests passed - the crash might be in the run() method")

if __name__ == "__main__":
    main()