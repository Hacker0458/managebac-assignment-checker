#!/usr/bin/env python3
"""
Fixed Professional GUI - Patched version to prevent crashes
修复的专业GUI - 防止闪退的补丁版本
"""

import sys
import traceback
from pathlib import Path

# Add the package to Python path
sys.path.insert(0, str(Path(__file__).parent))

def patch_professional_gui():
    """Apply patches to the professional GUI to prevent crashes"""

    # Import the original module
    from managebac_checker import professional_gui

    # Store original methods
    original_setup_system_integration = professional_gui.ProfessionalManageBacGUI._setup_system_integration
    original_load_configuration = professional_gui.ProfessionalManageBacGUI._load_configuration
    original_load_user_preferences = professional_gui.ProfessionalManageBacGUI._load_user_preferences

    def safe_setup_system_integration(self):
        """Safe version of system integration setup"""
        try:
            print("🔧 Setting up system integration...")
            original_setup_system_integration(self)
            print("✅ System integration setup complete")
        except Exception as e:
            print(f"⚠️ System integration failed (non-critical): {e}")
            self.tray_manager = None

    def safe_load_configuration(self):
        """Safe version of configuration loading"""
        try:
            print("🔧 Loading configuration...")
            original_load_configuration(self)
            print("✅ Configuration loaded successfully")
        except Exception as e:
            print(f"⚠️ Configuration loading failed (using defaults): {e}")
            self.config = None
            try:
                self._update_status("⚠️ Using default configuration | 使用默认配置", "⚠️")
            except:
                pass  # Status update might also fail

    def safe_load_user_preferences(self):
        """Safe version of user preferences loading"""
        try:
            print("🔧 Loading user preferences...")
            original_load_user_preferences(self)
            print("✅ User preferences loaded successfully")
        except Exception as e:
            print(f"⚠️ User preferences loading failed (using defaults): {e}")
            # Set safe defaults
            self.auto_check_enabled = False
            self.auto_check_interval = 30

    # Apply patches
    professional_gui.ProfessionalManageBacGUI._setup_system_integration = safe_setup_system_integration
    professional_gui.ProfessionalManageBacGUI._load_configuration = safe_load_configuration
    professional_gui.ProfessionalManageBacGUI._load_user_preferences = safe_load_user_preferences

    print("✅ Professional GUI patches applied successfully")

def main():
    """Main function with patched GUI"""
    print("🚀 Starting Fixed Professional ManageBac GUI...")
    print("=" * 60)

    try:
        # Apply patches first
        patch_professional_gui()

        # Import and run the patched GUI
        from managebac_checker.professional_gui import ProfessionalManageBacGUI

        print("🔧 Creating ProfessionalManageBacGUI instance...")
        app = ProfessionalManageBacGUI()

        print("🔧 Starting GUI run method...")
        app.run()

        print("✅ GUI completed successfully")

    except Exception as e:
        print(f"❌ Failed to start fixed professional GUI: {e}")
        print("📋 Full error traceback:")
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("❌ Application failed to start")
        sys.exit(1)
    else:
        print("✅ Application completed successfully")