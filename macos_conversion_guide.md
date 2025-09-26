# 🍎 macOS App Conversion Guide | macOS应用转换指南

将ManageBac Assignment Checker转换为原生macOS应用程序的完整指南。

## 📋 Overview | 概览

本项目提供了多种方式将Python应用转换为macOS原生应用：
- **自动化构建脚本**: 使用 `build_macos_app.py`
- **手动构建方法**: 使用 py2app 或其他工具
- **分发选项**: 创建DMG安装包或提交到App Store

## 🛠️ Prerequisites | 先决条件

### 系统要求
- macOS 10.14+ (推荐 macOS 11+)
- Python 3.8+
- Xcode Command Line Tools
- 足够的磁盘空间 (至少 2GB)

### 安装必需工具
```bash
# 安装Xcode Command Line Tools
xcode-select --install

# 安装py2app和其他构建工具
pip install py2app setuptools wheel
pip install pyinstaller  # 备选方案

# 可选：安装create-dmg用于创建安装包
brew install create-dmg
```

## 🚀 Quick Start | 快速开始

### 方法1: 使用自动化构建脚本（推荐）

```bash
# 运行自动化构建脚本
python build_macos_app.py

# 构建完成后测试应用
./run_macos_app.sh

# 创建DMG安装包
./create_dmg.sh
```

### 方法2: 手动使用py2app

```bash
# 创建setup.py文件
python create_setup_py.py

# 构建应用
python setup.py py2app

# 清理构建文件（可选）
python setup.py py2app --alias  # 开发模式
```

## 📁 项目结构 | Project Structure

构建后的应用结构：
```
ManageBac作业检查器.app/
├── Contents/
│   ├── Info.plist              # 应用信息和配置
│   ├── MacOS/
│   │   └── ManageBacChecker    # 启动脚本
│   ├── Resources/              # 应用资源
│   │   ├── AppIcon.icns       # 应用图标
│   │   ├── intelligent_launcher.py
│   │   ├── managebac_checker/ # Python包
│   │   ├── lib/               # Python依赖
│   │   └── browsers/          # Playwright浏览器
│   └── Frameworks/            # 系统框架（如需要）
```

## ⚙️ Configuration | 配置

### Info.plist 主要配置项

```xml
<key>CFBundleName</key>
<string>ManageBac作业检查器</string>

<key>CFBundleIdentifier</key>
<string>com.managebac.assignment.checker</string>

<key>CFBundleVersion</key>
<string>1.0.0</string>

<key>LSMinimumSystemVersion</key>
<string>10.14</string>

<key>NSApplicationCategoryType</key>
<string>public.app-category.education</string>
```

### 启动脚本配置

启动脚本会：
1. 设置Python路径和环境变量
2. 切换到应用资源目录
3. 启动 `intelligent_launcher.py`
4. 处理应用生命周期

## 🔧 Advanced Configuration | 高级配置

### 依赖管理

```bash
# 安装所有依赖到应用包中
pip install -r requirements.txt --target ./Resources/lib/python3.x/site-packages

# 安装Playwright浏览器到应用包
PLAYWRIGHT_BROWSERS_PATH=./Resources/browsers python -m playwright install chromium
```

### 图标创建

```bash
# 从PNG创建ICNS图标
sips -s format icns icon.png --out AppIcon.icns

# 或使用iconutil（需要iconset文件夹）
iconutil -c icns AppIcon.iconset
```

### 代码签名

```bash
# 签名应用（需要开发者证书）
codesign --deep --sign "Developer ID Application: Your Name" "ManageBac作业检查器.app"

# 验证签名
codesign --verify --deep --verbose "ManageBac作业检查器.app"

# 公证（App Store外分发需要）
xcrun altool --notarize-app --primary-bundle-id "com.managebac.assignment.checker" --username "your@email.com" --password "@keychain:AC_PASSWORD"
```

## 📦 Distribution | 分发

### 创建DMG安装包

```bash
# 使用自动脚本
./create_dmg.sh

# 或手动创建
hdiutil create -volname "ManageBac作业检查器" -srcfolder ./dist -ov -format UDZO "ManageBac-Assignment-Checker-v1.0.0.dmg"
```

### App Store 提交准备

1. **沙盒配置**:
   ```xml
   <key>com.apple.security.app-sandbox</key>
   <true/>
   <key>com.apple.security.network.client</key>
   <true/>
   ```

2. **创建App Store构建**:
   ```bash
   python setup.py py2app --app-store
   ```

3. **使用Application Loader提交**

## 🚨 Troubleshooting | 故障排除

### 常见问题

1. **应用无法启动**
   ```bash
   # 检查控制台日志
   Console.app -> 搜索应用名称

   # 或命令行查看
   log stream --predicate 'process == "ManageBacChecker"'
   ```

2. **依赖缺失**
   ```bash
   # 检查Python路径
   otool -L "ManageBac作业检查器.app/Contents/MacOS/ManageBacChecker"

   # 手动添加缺失依赖
   cp missing_module.so ./Resources/lib/python3.x/site-packages/
   ```

3. **权限问题**
   ```bash
   # 修复权限
   chmod +x "ManageBac作业检查器.app/Contents/MacOS/ManageBacChecker"
   chmod -R 755 "ManageBac作业检查器.app"
   ```

4. **Gatekeeper阻止**
   ```bash
   # 临时允许（仅用于开发测试）
   sudo spctl --master-disable

   # 或为特定应用添加例外
   sudo spctl --add "ManageBac作业检查器.app"
   ```

### 调试技巧

1. **启用调试模式**:
   修改启动脚本，添加调试输出和错误日志

2. **测试依赖**:
   ```bash
   # 在终端中测试Python导入
   cd "ManageBac作业检查器.app/Contents/Resources"
   python3 -c "import managebac_checker; print('OK')"
   ```

3. **查看系统日志**:
   ```bash
   # 实时查看系统日志
   log stream --style syslog --predicate 'process == "ManageBacChecker"'
   ```

## 🎯 Best Practices | 最佳实践

### 性能优化
- 使用 `--optimize 2` 编译Python字节码
- 排除不必要的依赖和文件
- 使用延迟加载减少启动时间

### 用户体验
- 添加启动画面或进度指示器
- 提供清晰的错误信息和解决方案
- 支持macOS原生特性（Dark Mode、Touch Bar等）

### 维护性
- 保持清晰的版本控制
- 自动化构建和测试流程
- 文档化所有配置和依赖

## 📚 Resources | 资源

### 官方文档
- [py2app Documentation](https://py2app.readthedocs.io/)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [macOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/macos/)

### 工具和库
- **py2app**: Python应用打包工具
- **PyInstaller**: 跨平台Python应用打包
- **create-dmg**: DMG安装包创建工具
- **AppIcon.co**: 在线图标转换工具

### 社区资源
- [Python Packaging User Guide](https://packaging.python.org/)
- [macOS App Distribution Guide](https://developer.apple.com/library/archive/documentation/IDEs/Conceptual/AppDistributionGuide/)

---

## 🎉 Success Checklist | 成功检查清单

- [ ] 应用能够正常启动
- [ ] 所有功能正常工作
- [ ] 应用图标显示正确
- [ ] 应用可以独立运行（不依赖外部Python环境）
- [ ] 依赖包正确包含在应用包中
- [ ] 应用符合macOS设计规范
- [ ] 代码签名和公证完成（如需要）
- [ ] DMG安装包创建成功
- [ ] 在不同macOS版本上测试通过

完成所有项目后，你就拥有了一个专业的macOS原生应用！🎊