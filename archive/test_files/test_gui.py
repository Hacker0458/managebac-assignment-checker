#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GUI启动
"""

import sys
import os

def test_basic_gui():
    """测试基础GUI"""
    try:
        import tkinter as tk
        print("✅ tkinter available")
        
        # 创建简单窗口测试
        root = tk.Tk()
        root.title("Test GUI")
        root.geometry("300x200")
        
        label = tk.Label(root, text="GUI Test Successful!")
        label.pack(pady=50)
        
        # 3秒后自动关闭
        root.after(3000, root.destroy)
        root.mainloop()
        
        print("✅ Basic GUI test passed")
        return True
        
    except Exception as e:
        print(f"❌ Basic GUI test failed: {e}")
        return False

def test_professional_gui():
    """测试专业GUI"""
    try:
        from managebac_checker.professional_gui import ProfessionalManageBacGUI
        print("✅ Professional GUI import successful")
        
        # 不实际启动GUI，只测试导入
        print("✅ Professional GUI import test passed")
        return True
        
    except Exception as e:
        print(f"❌ Professional GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 Testing GUI components...")
    print("🧪 测试GUI组件...")
    
    # 测试基础GUI
    if not test_basic_gui():
        print("❌ Basic GUI test failed")
        return False
    
    # 测试专业GUI导入
    if not test_professional_gui():
        print("❌ Professional GUI import test failed")
        return False
    
    print("✅ All GUI tests passed!")
    print("✅ 所有GUI测试通过！")
    return True

if __name__ == "__main__":
    main()
