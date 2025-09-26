#!/bin/bash
# 🍎 ManageBac Assignment Checker - macOS应用构建脚本
# 自动将Python应用转换为macOS原生应用

set -e  # 遇到错误时退出

echo "🍎 开始构建ManageBac Checker macOS应用..."
echo "================================================"

# 检查系统要求
echo "📋 检查系统要求..."
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ 此脚本只能在macOS上运行"
    exit 1
fi

# 检查Python版本
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.9"
if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ 需要Python 3.9或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 检查依赖
echo "📦 检查依赖..."
missing_deps=()

# 检查Python包
python_packages=("tkinter" "playwright" "pystray" "PIL" "openai" "jinja2")
for package in "${python_packages[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        missing_deps+=("$package")
    fi
done

# 检查系统工具
system_tools=("sips" "iconutil" "hdiutil" "codesign")
for tool in "${system_tools[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "⚠️ 未找到系统工具: $tool"
    fi
done

if [ ${#missing_deps[@]} -ne 0 ]; then
    echo "❌ 缺少Python依赖: ${missing_deps[*]}"
    echo "请运行: pip3 install -r requirements-macos.txt"
    exit 1
fi

echo "✅ 依赖检查通过"

# 创建构建目录
echo "📁 创建构建目录..."
BUILD_DIR="build/macos"
APP_NAME="ManageBac Checker"
BUNDLE_ID="com.managebac.checker"
VERSION="2.0.0"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# 复制源代码
echo "📂 复制源代码..."
files_to_copy=(
    "main.py"
    "icon.png"
    "icon.ico"
    "requirements.txt"
    "config.example.env"
    "managebac_checker"
    "templates"
    "static"
)

for item in "${files_to_copy[@]}"; do
    if [ -e "$item" ]; then
        if [ -d "$item" ]; then
            cp -r "$item" "$BUILD_DIR/"
            echo "✅ $item/"
        else
            cp "$item" "$BUILD_DIR/"
            echo "✅ $item"
        fi
    else
        echo "⚠️ 未找到: $item"
    fi
done

# 进入构建目录
cd "$BUILD_DIR"

# 创建Info.plist
echo "📝 创建应用元数据..."
cat > Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleDisplayName</key>
    <string>ManageBac Assignment Checker</string>
    <key>CFBundleIdentifier</key>
    <string>$BUNDLE_ID</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
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
</dict>
</plist>
EOF

echo "✅ Info.plist 创建完成"

# 创建应用图标
echo "🎨 创建应用图标..."
if [ -f "icon.png" ]; then
    # 创建iconset目录
    mkdir -p "${APP_NAME}.iconset"
    
    # 创建不同尺寸的图标
    sizes=(
        "16:icon_16x16.png"
        "32:icon_16x16@2x.png"
        "32:icon_32x32.png"
        "64:icon_32x32@2x.png"
        "128:icon_128x128.png"
        "256:icon_128x128@2x.png"
        "256:icon_256x256.png"
        "512:icon_256x256@2x.png"
        "512:icon_512x512.png"
        "1024:icon_512x512@2x.png"
    )
    
    for size_info in "${sizes[@]}"; do
        size=$(echo "$size_info" | cut -d: -f1)
        filename=$(echo "$size_info" | cut -d: -f2)
        sips -z "$size" "$size" icon.png --out "${APP_NAME}.iconset/$filename" > /dev/null 2>&1
        echo "✅ $filename"
    done
    
    # 创建icns文件
    iconutil -c icns "${APP_NAME}.iconset" -o "${APP_NAME}.icns" > /dev/null 2>&1
    echo "✅ 应用图标创建完成"
else
    echo "⚠️ 未找到icon.png，跳过图标创建"
fi

# 创建PyInstaller配置
echo "⚙️ 创建PyInstaller配置..."
cat > "${APP_NAME}.spec" << EOF
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
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
    hooksconfig={},
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
    name='$APP_NAME',
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
EOF

echo "✅ PyInstaller 配置创建完成"

# 运行PyInstaller
echo "🔨 运行PyInstaller构建..."
if pyinstaller --clean "${APP_NAME}.spec"; then
    echo "✅ PyInstaller 构建成功"
else
    echo "❌ PyInstaller 构建失败"
    exit 1
fi

# 创建应用包
echo "📦 创建macOS应用包..."
APP_BUNDLE="${APP_NAME}.app"
CONTENTS_DIR="${APP_BUNDLE}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

# 创建目录结构
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# 复制可执行文件
if [ -f "dist/$APP_NAME/$APP_NAME" ]; then
    cp "dist/$APP_NAME/$APP_NAME" "$MACOS_DIR/$APP_NAME"
    chmod +x "$MACOS_DIR/$APP_NAME"
    echo "✅ 可执行文件复制完成"
else
    echo "❌ 未找到可执行文件"
    exit 1
fi

# 复制资源文件
resources=(
    "icon.png:icon.png"
    "icon.ico:icon.ico"
    "config.example.env:config.example.env"
    "Info.plist:Info.plist"
)

for resource in "${resources[@]}"; do
    src=$(echo "$resource" | cut -d: -f1)
    dst=$(echo "$resource" | cut -d: -f2)
    if [ -f "$src" ]; then
        cp "$src" "$RESOURCES_DIR/$dst"
        echo "✅ $dst"
    fi
done

# 复制包目录
packages=("managebac_checker" "templates" "static")
for package in "${packages[@]}"; do
    if [ -d "$package" ]; then
        cp -r "$package" "$MACOS_DIR/"
        echo "✅ $package/"
    fi
done

# 复制图标
if [ -f "${APP_NAME}.icns" ]; then
    cp "${APP_NAME}.icns" "$RESOURCES_DIR/${APP_NAME}.icns"
    echo "✅ 应用图标"
fi

echo "✅ 应用包创建完成: $APP_BUNDLE"

# 测试应用
echo "🧪 测试应用..."
if open "$APP_BUNDLE" &>/dev/null; then
    echo "✅ 应用启动测试成功"
else
    echo "⚠️ 应用启动测试失败（可能正常）"
fi

# 创建DMG
echo "💿 创建DMG安装包..."
if hdiutil create -srcfolder "$APP_BUNDLE" -volname "$APP_NAME" -fs HFS+ -fsargs "-c c=64,a=16,e=16" temp.dmg && \
   hdiutil convert temp.dmg -format UDZO -o "${APP_NAME}.dmg" && \
   rm temp.dmg; then
    echo "✅ DMG创建完成: ${APP_NAME}.dmg"
else
    echo "⚠️ DMG创建失败"
fi

# 返回项目根目录
cd - > /dev/null

echo "================================================"
echo "🎉 构建完成！"
echo "📁 应用位置: $BUILD_DIR/$APP_BUNDLE"
echo "💿 DMG位置: $BUILD_DIR/${APP_NAME}.dmg"
echo ""
echo "🚀 可以双击运行应用！"
echo "📦 可以分发DMG文件！"

