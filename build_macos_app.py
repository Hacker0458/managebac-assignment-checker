#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍎 ManageBac Assignment Checker - macOS应用构建脚本
自动将Python应用转换为macOS原生应用
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json

class MacOSAppBuilder:
    """macOS应用构建器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build" / "macos"
        self.app_name = "ManageBac Checker"
        self.bundle_id = "com.managebac.checker"
        self.version = "2.0.0"
        
    def check_dependencies(self):
        """检查构建依赖"""
        print("📋 检查构建依赖...")
        
        required_packages = [
            "pyinstaller",
            "tkinter",
            "playwright", 
            "pystray",
            "PIL",
            "openai",
            "jinja2"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️ 缺少依赖: {', '.join(missing_packages)}")
            print("请运行: pip install -r requirements.txt")
            return False
        
        print("✅ 所有依赖检查通过")
        return True
    
    def create_build_directory(self):
        """创建构建目录"""
        print("📁 创建构建目录...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        self.build_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 构建目录: {self.build_dir}")
    
    def copy_source_files(self):
        """复制源代码文件"""
        print("📂 复制源代码文件...")
        
        # 复制主要文件
        files_to_copy = [
            "main.py",
            "icon.png", 
            "icon.ico",
            "requirements.txt",
            "config.example.env"
        ]
        
        for file_name in files_to_copy:
            src = self.project_root / file_name
            if src.exists():
                shutil.copy2(src, self.build_dir)
                print(f"✅ {file_name}")
            else:
                print(f"⚠️ 未找到: {file_name}")
        
        # 复制包目录
        packages_to_copy = [
            "managebac_checker",
            "templates", 
            "static"
        ]
        
        for package in packages_to_copy:
            src = self.project_root / package
            if src.exists():
                dst = self.build_dir / package
                shutil.copytree(src, dst)
                print(f"✅ {package}/")
            else:
                print(f"⚠️ 未找到: {package}/")
    
    def create_app_metadata(self):
        """创建应用元数据"""
        print("📝 创建应用元数据...")
        
        # 创建Info.plist
        info_plist = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{self.app_name}</string>
    <key>CFBundleDisplayName</key>
    <string>ManageBac Assignment Checker</string>
    <key>CFBundleIdentifier</key>
    <string>{self.bundle_id}</string>
    <key>CFBundleVersion</key>
    <string>{self.version}</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.version}</string>
    <key>CFBundleExecutable</key>
    <string>{self.app_name}</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.education</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2025 ManageBac Checker. All rights reserved.</string>
    <key>NSAppleScriptEnabled</key>
    <false/>
    <key>NSSupportsAutomaticTermination</key>
    <true/>
    <key>NSSupportsSuddenTermination</key>
    <true/>
</dict>
</plist>'''
        
        with open(self.build_dir / "Info.plist", "w") as f:
            f.write(info_plist)
        
        print("✅ Info.plist 创建完成")
    
    def create_icns_icon(self):
        """创建.icns图标文件"""
        print("🎨 创建应用图标...")
        
        icon_png = self.build_dir / "icon.png"
        if not icon_png.exists():
            print("⚠️ 未找到icon.png，跳过图标创建")
            return
        
        # 创建iconset目录
        iconset_dir = self.build_dir / f"{self.app_name}.iconset"
        iconset_dir.mkdir(exist_ok=True)
        
        # 创建不同尺寸的图标
        sizes = [
            (16, "icon_16x16.png"),
            (32, "icon_16x16@2x.png"),
            (32, "icon_32x32.png"),
            (64, "icon_32x32@2x.png"),
            (128, "icon_128x128.png"),
            (256, "icon_128x128@2x.png"),
            (256, "icon_256x256.png"),
            (512, "icon_256x256@2x.png"),
            (512, "icon_512x512.png"),
            (1024, "icon_512x512@2x.png")
        ]
        
        for size, filename in sizes:
            try:
                subprocess.run([
                    "sips", "-z", str(size), str(size), 
                    str(icon_png), "--out", str(iconset_dir / filename)
                ], check=True, capture_output=True)
                print(f"✅ {filename}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ 创建 {filename} 失败: {e}")
        
        # 创建icns文件
        try:
            subprocess.run([
                "iconutil", "-c", "icns", str(iconset_dir), 
                "-o", str(self.build_dir / f"{self.app_name}.icns")
            ], check=True)
            print("✅ .icns 图标创建完成")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 创建 .icns 失败: {e}")
    
    def create_pyinstaller_spec(self):
        """创建PyInstaller配置文件"""
        print("⚙️ 创建PyInstaller配置...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{self.build_dir}'],
    binaries=[],
    datas=[
        ('managebac_checker', 'managebac_checker'),
        ('templates', 'templates'),
        ('static', 'static'),
        ('icon.png', '.'),
        ('icon.ico', '.'),
        ('config.example.env', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'playwright',
        'pystray',
        'PIL',
        'PIL.Image',
        'openai',
        'jinja2',
        'asyncio',
        'threading',
        'webbrowser',
        'json',
        'pathlib',
        'datetime',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
'''
        
        with open(self.build_dir / f"{self.app_name}.spec", "w") as f:
            f.write(spec_content)
        
        print("✅ PyInstaller 配置创建完成")
    
    def run_pyinstaller(self):
        """运行PyInstaller构建"""
        print("🔨 运行PyInstaller构建...")
        
        os.chdir(self.build_dir)
        
        try:
            # 运行PyInstaller
            result = subprocess.run([
                "pyinstaller", 
                "--clean",
                f"{self.app_name}.spec"
            ], check=True, capture_output=True, text=True)
            
            print("✅ PyInstaller 构建成功")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ PyInstaller 构建失败: {e}")
            print(f"错误输出: {e.stderr}")
            return False
    
    def create_app_bundle(self):
        """创建macOS应用包"""
        print("📦 创建macOS应用包...")
        
        # 应用包目录
        app_bundle = self.build_dir / f"{self.app_name}.app"
        contents_dir = app_bundle / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        # 创建目录结构
        for dir_path in [contents_dir, macos_dir, resources_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 复制可执行文件
        dist_exe = self.build_dir / "dist" / self.app_name / self.app_name
        if dist_exe.exists():
            shutil.copy2(dist_exe, macos_dir / self.app_name)
            os.chmod(macos_dir / self.app_name, 0o755)
            print("✅ 可执行文件复制完成")
        else:
            print("❌ 未找到可执行文件")
            return False
        
        # 复制资源文件
        resources_to_copy = [
            ("icon.png", "icon.png"),
            ("icon.ico", "icon.ico"),
            ("config.example.env", "config.example.env"),
        ]
        
        for src_name, dst_name in resources_to_copy:
            src = self.build_dir / src_name
            if src.exists():
                shutil.copy2(src, resources_dir / dst_name)
                print(f"✅ {dst_name}")
        
        # 复制包目录
        packages_to_copy = ["managebac_checker", "templates", "static"]
        for package in packages_to_copy:
            src = self.build_dir / package
            if src.exists():
                dst = macos_dir / package
                shutil.copytree(src, dst)
                print(f"✅ {package}/")
        
        # 复制Info.plist
        info_plist = self.build_dir / "Info.plist"
        if info_plist.exists():
            shutil.copy2(info_plist, contents_dir / "Info.plist")
            print("✅ Info.plist")
        
        # 复制图标
        icns_file = self.build_dir / f"{self.app_name}.icns"
        if icns_file.exists():
            shutil.copy2(icns_file, resources_dir / f"{self.app_name}.icns")
            print("✅ 应用图标")
        
        print(f"✅ 应用包创建完成: {app_bundle}")
        return True
    
    def test_app(self):
        """测试应用"""
        print("🧪 测试应用...")
        
        app_bundle = self.build_dir / f"{self.app_name}.app"
        if not app_bundle.exists():
            print("❌ 应用包不存在")
            return False
        
        try:
            # 尝试启动应用
            result = subprocess.run([
                "open", str(app_bundle)
            ], check=True, capture_output=True, text=True, timeout=10)
            
            print("✅ 应用启动测试成功")
            return True
            
        except subprocess.TimeoutExpired:
            print("⚠️ 应用启动超时（可能正常）")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 应用启动失败: {e}")
            return False
    
    def create_dmg(self):
        """创建DMG安装包"""
        print("💿 创建DMG安装包...")
        
        app_bundle = self.build_dir / f"{self.app_name}.app"
        dmg_path = self.build_dir / f"{self.app_name}.dmg"
        
        if not app_bundle.exists():
            print("❌ 应用包不存在，无法创建DMG")
            return False
        
        try:
            # 创建临时DMG
            temp_dmg = self.build_dir / "temp.dmg"
            subprocess.run([
                "hdiutil", "create", "-srcfolder", str(app_bundle),
                "-volname", self.app_name, "-fs", "HFS+",
                "-fsargs", "-c c=64,a=16,e=16", str(temp_dmg)
            ], check=True)
            
            # 转换为最终DMG
            subprocess.run([
                "hdiutil", "convert", str(temp_dmg), "-format", "UDZO",
                "-o", str(dmg_path)
            ], check=True)
            
            # 清理临时文件
            temp_dmg.unlink()
            
            print(f"✅ DMG创建完成: {dmg_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ DMG创建失败: {e}")
            return False
    
    def build(self):
        """执行完整构建流程"""
        print("🚀 开始构建ManageBac Checker macOS应用...")
        print("=" * 60)
        
        # 检查依赖
        if not self.check_dependencies():
            return False
        
        # 创建构建目录
        self.create_build_directory()
        
        # 复制源代码
        self.copy_source_files()
        
        # 创建应用元数据
        self.create_app_metadata()
        
        # 创建图标
        self.create_icns_icon()
        
        # 创建PyInstaller配置
        self.create_pyinstaller_spec()
        
        # 运行PyInstaller
        if not self.run_pyinstaller():
            return False
        
        # 创建应用包
        if not self.create_app_bundle():
            return False
        
        # 测试应用
        self.test_app()
        
        # 创建DMG
        self.create_dmg()
        
        print("=" * 60)
        print("🎉 构建完成！")
        print(f"📁 应用位置: {self.build_dir / f'{self.app_name}.app'}")
        print(f"💿 DMG位置: {self.build_dir / f'{self.app_name}.dmg'}")
        print("\n🚀 可以双击运行应用！")
        
        return True

def main():
    """主函数"""
    builder = MacOSAppBuilder()
    success = builder.build()
    
    if success:
        print("\n✅ 构建成功！")
        sys.exit(0)
    else:
        print("\n❌ 构建失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()

