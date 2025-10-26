#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Auto Launch | 测试自动启动
Test script to verify auto-launch functionality
测试脚本以验证自动启动功能
"""

import sys
import subprocess
import time
from pathlib import Path

def test_optimized_installer():
    """测试优化安装器"""
    print("🧪 Testing 优化安装器.py...")
    try:
        result = subprocess.run([
            sys.executable, "优化安装器.py"
        ], timeout=30, capture_output=True, text=True)

        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - installer taking too long")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ultimate_installer():
    """测试Ultimate安装器"""
    print("🧪 Testing ultimate_installer.py...")
    try:
        result = subprocess.run([
            sys.executable, "ultimate_installer.py"
        ], timeout=30, capture_output=True, text=True)

        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - installer taking too long")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_intelligent_launcher():
    """测试智能启动器"""
    print("🧪 Testing intelligent_launcher.py...")
    try:
        # 先检查依赖
        import psutil

        result = subprocess.run([
            sys.executable, "intelligent_launcher.py"
        ], timeout=20, capture_output=True, text=True)

        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")

        return result.returncode == 0
    except ImportError:
        print("❌ Missing psutil dependency")
        print("💡 Run: pip install psutil")
        return False
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - launcher taking too long")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_files():
    """检查必要文件"""
    print("🔍 Checking required files...")
    files_to_check = [
        "优化安装器.py",
        "ultimate_installer.py",
        "intelligent_launcher.py",
        "smart_launcher.py",
        "gui_launcher.py"
    ]

    missing = []
    for file in files_to_check:
        if not Path(file).exists():
            missing.append(file)
        else:
            print(f"✅ {file}")

    if missing:
        print(f"❌ Missing files: {missing}")
        return False

    return True

def main():
    print("🚀 ManageBac Assignment Checker - Auto Launch Test")
    print("=" * 60)

    # 检查文件
    if not check_files():
        print("\n💡 Solution: Pull latest changes from GitHub")
        print("   git pull origin main")
        return False

    print("\n" + "=" * 60)

    # 测试方案1：优化安装器
    print("\n📋 Test 1: 优化安装器")
    success1 = test_optimized_installer()

    if not success1:
        print("\n📋 Test 2: Ultimate Installer (fallback)")
        success2 = test_ultimate_installer()

        if not success2:
            print("\n📋 Test 3: Intelligent Launcher (direct)")
            success3 = test_intelligent_launcher()

            if not success3:
                print("\n❌ All tests failed")
                print("\n🔧 Troubleshooting steps:")
                print("1. Check Python version: python --version")
                print("2. Install dependencies: pip install -r requirements.txt")
                print("3. Check tkinter: python -c 'import tkinter; print(\"OK\")'")
                print("4. Run with verbose: python 优化安装器.py --verbose")
                return False

    print("\n✅ Auto-launch test completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)