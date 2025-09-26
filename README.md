# 🎓 ManageBac Assignment Checker | ManageBac作业检查器

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)](https://github.com/Hacker0458/managebac-assignment-checker)

> 🚀 **智能化ManageBac作业追踪工具** - 自动检查作业状态，生成详细报告，永远不再错过作业！
> **Intelligent ManageBac Assignment Tracking Tool** - Automatically check assignment status, generate detailed reports, never miss an assignment again!

## ✨ 核心特性 | Key Features

### 🎯 一键启动体验 | One-Click Launch Experience
- 🌟 **默认自动启动** - 运行安装器后自动打开应用
- 🧠 **智能环境检测** - 自动选择最佳启动方式 (GUI/命令行)
- 🔧 **自动错误修复** - 智能诊断并自动解决常见问题
- 📱 **跨平台支持** - macOS, Windows, Linux全平台兼容

### 📊 强大功能 | Powerful Features
- 📚 **自动作业检查** - 定期扫描ManageBac获取最新作业信息
- ⏰ **智能提醒系统** - 逾期作业和紧急任务及时提醒
- 📋 **多格式报告** - 支持HTML、JSON、Markdown等多种报告格式
- 🔔 **系统通知** - macOS原生通知系统集成
- 🤖 **AI智能分析** - 可选的AI助手提供作业优先级建议

### 💻 现代化界面 | Modern Interface
- 🎨 **专业GUI界面** - 现代化的桌面应用程序
- 🌙 **深色模式支持** - 护眼的深色主题
- 📱 **响应式设计** - 自适应不同屏幕尺寸
- 🗂️ **系统托盘集成** - 后台运行，随时可用

## 🚀 快速开始 | Quick Start

### 🌟 推荐方式：一键安装+自动启动

```bash
# 🎯 第一步：克隆项目
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 🚀 第二步：运行优化安装器（推荐）
python3 优化安装器.py
```

**就这么简单！** 安装器会：
- ✅ 自动检查系统要求
- ✅ 安装所有必需的依赖
- ✅ 创建基础配置文件
- ✅ **自动启动应用程序**

### 🔧 替代安装方式

如果优化安装器不可用，可以使用以下替代方案：

```bash
# 方案1：Ultimate Installer（现在默认自动启动）
python3 ultimate_installer.py

# 方案2：高级安装器
python3 advanced_installer.py

# 方案3：经典安装向导
python3 setup_wizard.py

# 方案4：图形界面安装向导
python3 enhanced_setup_gui.py
```

### 📋 配置设置

安装完成后，编辑 `.env` 文件填入你的ManageBac账户信息：

```bash
# ManageBac Configuration
MANAGEBAC_URL=https://your-school.managebac.cn
MANAGEBAC_EMAIL=your.email@school.edu
MANAGEBAC_PASSWORD=your_password

# 可选配置
REPORT_FORMAT=html,console
OUTPUT_DIR=reports
LANGUAGE=zh
HEADLESS=true
```

## 🚀 启动应用 | Launch Application

### 🧠 智能启动器（推荐）

```bash
# 🌟 智能启动器 - 最佳用户体验
python3 intelligent_launcher.py

# 🤖 智能启动器功能：
# ✅ 自动环境检测
# ✅ 智能选择最佳启动方式
# ✅ 进程管理和冲突处理
# ✅ 失败时自动重试
# ✅ 详细的错误诊断
```

### 🎨 GUI启动选项

```bash
# GUI启动器
python3 gui_launcher.py

# 智能启动器（自动检测GUI）
python3 smart_launcher.py

# 专业GUI应用
python3 run_app.py
```

### 💻 命令行选项

```bash
# 基础命令行界面
python3 main_new.py

# 交互式模式
python3 main_new.py --interactive

# 指定输出格式
python3 -m managebac_checker.cli --format html

# 启用通知
python3 -m managebac_checker.cli --notify
```

## 📱 双击启动（小白用户友好）

安装后会自动创建桌面快捷方式：

### macOS
```bash
# 双击桌面上的 "ManageBac作业检查器.command" 文件
# 或使用终端：
./START.sh
```

### Windows
```batch
:: 双击 START.bat 文件
START.bat
```

### Linux
```bash
# 双击 managebac-checker.desktop 文件
# 或使用终端：
./START.sh
```

## 📚 详细文档 | Documentation

### 📖 完整使用教程
- **[📘 详细使用教程](详细使用教程.md)** - 最完整的使用指南，包含所有功能说明
- **[📋 技术文档](CLAUDE.md)** - 开发和配置相关的技术细节

### 🍎 macOS用户专享
- **[🍎 macOS应用转换指南](macos_conversion_guide.md)** - 创建原生macOS应用的完整方案

### 🛠️ 开发者资源
- [🏗️ 项目架构](CLAUDE.md#project-architecture) - 代码结构说明
- [🧪 测试指南](CLAUDE.md#testing-strategy) - 测试方法和工具
- [🔒 安全考虑](CLAUDE.md#security-considerations) - 安全最佳实践

## 🔧 故障排除 | Troubleshooting

### 快速修复

#### 1. 应用不自动启动
```bash
# 解决方案：
python3 优化安装器.py  # 重新运行优化安装器
python3 intelligent_launcher.py  # 直接使用智能启动器
```

#### 2. 依赖安装失败
```bash
# 手动安装依赖：
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

#### 3. GUI无法启动
```bash
# 检查tkinter：
python3 -c "import tkinter; print('tkinter OK')"

# 使用命令行模式：
python3 smart_launcher.py --cli
```

### 🧪 诊断工具

```bash
# 运行完整系统测试
python3 test_auto_launch.py

# 运行错误诊断
python3 error_handler.py
```

**更多详细的故障排除指南请参考：[📘 详细使用教程](详细使用教程.md#-故障排除指南)**

## 📁 项目结构 | Project Structure

```
managebac-assignment-checker/
├── 🌟 优化安装器.py              # 推荐的一键安装器（默认自动启动）
├── 🚀 ultimate_installer.py     # 多模式安装器
├── 🧠 intelligent_launcher.py    # 智能启动器（最佳体验）
├── 🎨 ultimate_user_experience.py # 终极用户体验启动器
├── 🤖 smart_launcher.py          # 自适应启动器
├── 🎯 gui_launcher.py            # GUI专用启动器
├── 📋 main_new.py               # 主应用程序
├── 🔧 enhanced_error_handler.py  # 增强错误处理和日志系统
├── 🚨 error_handler.py          # 基础错误处理系统
├── 🧪 test_auto_launch.py       # 自动启动测试工具
├── ✨ fixed_gui.py              # 修复版GUI应用（诊断用）
├── 🛠️ professional_gui_fixed.py  # 专业GUI修复版
├── managebac_checker/           # 核心包目录
│   ├── checker.py              # 主检查逻辑
│   ├── scraper.py             # Web爬虫引擎
│   ├── analyzer.py            # 数据分析器
│   ├── reporter.py            # 报告生成器
│   ├── professional_gui.py     # 专业GUI界面（已修复）
│   ├── system_tray.py         # 系统托盘（原生通知）
│   └── notifications.py       # 多平台通知系统
├── 📁 logs/                    # 日志文件目录
├── 📖 README.md                # 本文档
├── 📘 详细使用教程.md           # 完整使用指南
├── 📋 CLAUDE.md                # 技术开发文档
├── 🍎 macos_conversion_guide.md # macOS应用转换指南
├── ⚙️ config.example.env       # 配置文件模板
└── 📦 requirements.txt         # Python依赖清单
```

## 🌟 最新更新 | Latest Updates

### ✅ 已解决的问题

- **🎯 一键安装后自动启动** - 优化安装器现在默认自动启动应用
- **🔧 依赖兼容性修复** - 解决了Python 3.13下pyobjus编译问题
- **🍎 macOS原生通知** - 使用osascript替代plyer，完美支持macOS通知
- **🧠 智能启动器** - 新增intelligent_launcher.py，提供最佳启动体验
- **🚨 错误处理系统** - 新增enhanced_error_handler.py，智能诊断和修复
- **💻 GUI闪退修复** - 完全解决了GUI应用程序闪退问题
- **🎨 用户体验优化** - 新增ultimate_user_experience.py，提供终极用户体验

### 🔥 核心改进

- **零配置体验** - 新手用户只需运行一条命令
- **智能环境检测** - 自动选择GUI或命令行模式
- **自动错误修复** - 常见问题自动解决
- **跨平台通知** - 统一的通知体验

## 🤝 贡献指南 | Contributing

欢迎贡献代码和建议！

### 快速开始贡献

1. **Fork项目**
2. **创建特性分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送到分支** (`git push origin feature/AmazingFeature`)
5. **开启Pull Request**

### 开发环境设置

```bash
# 克隆开发版本
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 使用优化安装器设置开发环境
python3 优化安装器.py

# 运行测试
python3 test_auto_launch.py
```

## 📄 许可证 | License

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 👨‍💻 作者 | Author

**Hacker0458**
- GitHub: [@Hacker0458](https://github.com/Hacker0458)
- 项目主页: [ManageBac Assignment Checker](https://github.com/Hacker0458/managebac-assignment-checker)

## 🙏 致谢 | Acknowledgments

- 感谢所有贡献者和用户的反馈
- 特别感谢为改进用户体验提出建议的朋友们
- 感谢ManageBac平台提供的服务
- 感谢开源社区的支持

## 📞 支持与反馈 | Support & Feedback

### 🆘 获取帮助

- 🐛 [报告Bug](https://github.com/Hacker0458/managebac-assignment-checker/issues/new?template=bug_report.md)
- 💡 [功能建议](https://github.com/Hacker0458/managebac-assignment-checker/issues/new?template=feature_request.md)
- 💬 [讨论交流](https://github.com/Hacker0458/managebac-assignment-checker/discussions)
- 📧 [邮件支持](mailto:support@example.com)

### 📚 文档索引

- **新手指南**: [📘 详细使用教程](详细使用教程.md) - 从安装到高级功能的完整指南
- **技术文档**: [📋 CLAUDE.md](CLAUDE.md) - 开发者和高级用户文档
- **macOS用户**: [🍎 macOS转换指南](macos_conversion_guide.md) - 原生应用构建方案

---

## 🎉 立即开始使用！

### 🌟 最简单的方式

```bash
# 一条命令，开始你的智能作业管理之旅！
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker
python3 优化安装器.py
```

### ⭐ 现在包含的功能

✅ **零配置安装** - 一键完成所有设置
✅ **自动启动应用** - 安装完成立即可用
✅ **智能错误修复** - 自动诊断和解决问题
✅ **跨平台支持** - 在任何系统上都能完美运行
✅ **原生系统集成** - macOS通知、桌面快捷方式
✅ **现代化界面** - 专业GUI和命令行双模式

**享受再也不会忘记作业的轻松学习生活！** 🎓✨

---

*如果这个项目帮助到了你，请考虑给我们一个⭐Star！这将激励我们继续改进和添加新功能。*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![GitHub Actions](https://github.com/Hacker0458/managebac-assignment-checker/workflows/🚀%20ManageBac%20Assignment%20Checker%20CI/CD/badge.svg)
![Downloads](https://img.shields.io/github/downloads/Hacker0458/managebac-assignment-checker/total.svg)

**🎯 An intelligent automation tool for ManageBac assignment tracking**  
**一个用于ManageBac作业追踪的智能自动化工具**

[English](#english) | [中文](#中文)

</div>

---

## English

### 🌟 Features

#### 🖥️ **Modern GUI Application**
- 📱 **Beautiful Desktop Interface**: Modern, responsive GUI with intuitive design
- 🎨 **Multiple Themes**: Light and Dark themes with smooth animations
- 🔔 **System Tray Integration**: Minimize to tray with desktop notifications
- 📊 **Interactive Assignment Cards**: Visual assignment management with filtering and search
- ⚙️ **Comprehensive Settings**: Tabbed configuration dialog with all options
- 🔄 **Auto-refresh**: Automatic background checking with customizable intervals

#### 🤖 **AI Assistant Integration**
- 💡 **Intelligent Analysis**: Powered by OpenAI for smart assignment insights
- 📚 **Personalized Recommendations**: AI-powered study strategies and time management
- 🎯 **Priority Assessment**: Smart urgency and importance evaluation
- 📈 **Learning Analytics**: Detailed analysis of study patterns and progress

#### 🔐 **Security & Authentication**
- 🛡️ **Secure Login**: Automated ManageBac authentication with credential protection
- 🔑 **Environment Variables**: Safe credential storage with .env files
- 🌐 **Bilingual Support**: Full English and Chinese interface throughout

#### 📊 **Advanced Reporting**
- 📋 **Multi-format Reports**: Generate HTML, Markdown, JSON, and console reports
- 📈 **Visual Analytics**: Interactive charts and detailed statistics
- 📧 **Email Notifications**: Automated assignment reminders and updates
- 🎨 **Beautiful HTML Reports**: Modern responsive design with Chart.js integration

#### 🚀 **Easy Installation & Deployment**
- 🎯 **One-click Installation**: Complete setup script with dependency management
- 🔗 **Desktop Shortcuts**: Automatic shortcut creation for all platforms
- 📦 **Cross-platform**: Windows, macOS, and Linux support
- 🧪 **Full Test Coverage**: Comprehensive unit testing suite
- 🚀 **CI/CD Ready**: GitHub Actions workflow included

### 🚀 Quick Start

#### 🎯 **One-Click Installation (Recommended)**

**🚀 Main Installer (Fixed & Stable)**
```bash
# Download and run the main installer (FIXED for requirements.txt issue)
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh | bash
```

**💪 Robust Installer (Most Stable)**
```bash
# Download and run the most robust installer with multiple fallbacks
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_robust.sh | bash
```

**🔧 Quick Fix (If Installation Failed)**
```bash
# If you encountered installation issues, use this fix script
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/fix_installation.sh | bash
```

**⚡ Alternative Installers**
```bash
# Ultimate installer with full features
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash

# Quick installer for minimal setup
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

**🔧 GitHub Installer (From Source)**
```bash
# Download and run the GitHub installer
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_github.sh | bash
```

**📦 Manual Installation**
```bash
# Clone and install everything automatically
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker
python install_complete.py
```

This will:
- ✅ Install all dependencies (including GUI libraries)
- ✅ Set up Playwright browsers
- ✅ Create desktop shortcuts
- ✅ Configure environment
- ✅ Test installation
- 🚀 Optionally start the GUI application

#### 🖥️ **Manual GUI Installation**

**🎯 Auto Install Scripts:**
- **Linux/macOS**: `./start_gui.sh`
- **Windows**: `start_gui.bat`

**📋 Step by Step:**
```bash
# Clone the repository
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# Install dependencies (including GUI)
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Start the GUI application
python gui_launcher.py
```

#### 📱 **Command Line Version**
```bash
# For CLI-only usage (no GUI)
pip install playwright python-dotenv jinja2
python main_new.py --interactive
```

#### Configuration

1. **Copy environment template:**
   ```bash
   cp config.example.env .env
   ```

2. **Edit `.env` file with your ManageBac credentials:**
   ```env
   # Required | 必需
   MANAGEBAC_EMAIL=your_email@example.com
   MANAGEBAC_PASSWORD=your_password
   MANAGEBAC_URL=https://your-school.managebac.com
   
   # Optional AI Features | 可选AI功能
   AI_ENABLED=true
   OPENAI_API_KEY=your_openai_api_key
   AI_MODEL=gpt-3.5-turbo
   
   # Report Settings | 报告设置
   REPORT_FORMAT=html,json
   OUTPUT_DIR=reports
   ```

#### Usage

```bash
# Basic usage
python main_new.py

# Command line interface
python -m managebac_checker.cli --help

# Generate specific format
python -m managebac_checker.cli --format html

# Enable email notifications
python -m managebac_checker.cli --notify
```

### 📁 Project Structure

```
managebac-assignment-checker/
├── 📦 managebac_checker/          # Main package
│   ├── 🔧 config.py               # Configuration management
│   ├── 🕷️ scraper.py              # Web scraping engine
│   ├── 📊 analyzer.py             # Data analysis
│   ├── 📋 reporter.py             # Report generation
│   ├── 🔍 checker.py              # Main checker
│   ├── 📧 notifications.py        # Email notifications
│   └── 💻 cli.py                  # Command line interface
├── 🧪 tests/                      # Unit tests
├── ⚙️ .github/workflows/          # CI/CD configuration
├── 📄 setup.py                    # Package setup
├── 📋 requirements.txt            # Dependencies
├── 📖 README.md                   # Documentation
└── 📜 LICENSE                     # MIT License
```

### 🔧 Development

#### Running Tests
```bash
pytest tests/
```

#### Code Formatting
```bash
black managebac_checker/
flake8 managebac_checker/
```

### 📊 Report Examples

#### HTML Report Features:
- 📱 Responsive design
- 🎨 Modern UI with charts
- 📈 Interactive statistics
- 🔍 Searchable assignments

#### Console Output:
```
╭─────────────────────────────────────────────────────────╮
│                ManageBac Assignment Report              │
├─────────────────────────────────────────────────────────┤
│ 📚 Total Assignments: 15                               │
│ ⚠️  Overdue: 2                                         │
│ 🔥 High Priority: 5                                    │
│ ✅ Completed: 8                                        │
╰─────────────────────────────────────────────────────────╯
```

### ⚠️ Important Notes

- Ensure you have permission to access the ManageBac system
- Comply with your school's terms of use and privacy policies
- Test in a development environment first
- Keep your credentials secure

### 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## 中文

### 🌟 功能特性

#### 🖥️ **现代化GUI应用程序**
- 📱 **美观的桌面界面**: 现代化、响应式GUI，设计直观易用
- 🎨 **多种主题**: 浅色和深色主题，支持流畅动画
- 🔔 **系统托盘集成**: 最小化到托盘，支持桌面通知
- 📊 **交互式作业卡片**: 可视化作业管理，支持筛选和搜索
- ⚙️ **综合设置界面**: 标签式配置对话框，包含所有选项
- 🔄 **自动刷新**: 后台自动检查，可自定义检查间隔

#### 🤖 **AI助手集成**
- 💡 **智能分析**: 基于OpenAI的智能作业洞察
- 📚 **个性化建议**: AI驱动的学习策略和时间管理
- 🎯 **优先级评估**: 智能的紧急程度和重要性评估
- 📈 **学习分析**: 详细的学习模式和进度分析

#### 🔐 **安全与身份验证**
- 🛡️ **安全登录**: 自动化ManageBac身份验证，保护凭据安全
- 🔑 **环境变量**: 使用.env文件安全存储凭据
- 🌐 **双语支持**: 全程支持中英文界面

#### 📊 **高级报告功能**
- 📋 **多格式报告**: 生成HTML、Markdown、JSON和控制台报告
- 📈 **可视化分析**: 交互式图表和详细统计信息
- 📧 **邮件通知**: 自动化作业提醒和更新
- 🎨 **美观的HTML报告**: 现代响应式设计，集成Chart.js

#### 🚀 **简易安装与部署**
- 🎯 **一键安装**: 完整的安装脚本，自动管理依赖
- 🔗 **桌面快捷方式**: 自动为所有平台创建快捷方式
- 📦 **跨平台**: 支持Windows、macOS和Linux
- 🧪 **完整测试**: 全面的单元测试套件
- 🚀 **CI/CD就绪**: 包含GitHub Actions工作流

### 🚀 快速开始

#### 🎯 **一键安装（推荐）**

**🚀 主安装器（修复且稳定）**
```bash
# 下载并运行主安装器（已修复requirements.txt问题）
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh | bash
```

**💪 稳定安装器（最稳定）**
```bash
# 下载并运行最稳定的安装器，包含多重后备方案
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_robust.sh | bash
```

**🔧 快速修复（如果安装失败）**
```bash
# 如果遇到安装问题，使用此修复脚本
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/fix_installation.sh | bash
```

**⚡ 其他安装器**
```bash
# 终极安装器，包含完整功能
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash

# 快速安装器，最小化设置
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

**🔧 GitHub安装器（从源码）**
```bash
# 下载并运行GitHub安装器
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_github.sh | bash
```

**📦 手动安装**
```bash
# 克隆并自动安装所有组件
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker
python install_complete.py
```

这将会：
- ✅ 安装所有依赖（包括GUI库）
- ✅ 设置Playwright浏览器
- ✅ 创建桌面快捷方式
- ✅ 配置环境
- ✅ 测试安装
- 🚀 可选择启动GUI应用程序

#### 🖥️ **手动GUI安装**

**🎯 自动安装脚本：**
- **Linux/macOS**: `./start_gui.sh`
- **Windows**: `start_gui.bat`

**📋 分步安装：**
```bash
# 克隆仓库
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 安装依赖（包括GUI）
pip install -r requirements.txt

# 安装Playwright浏览器
python -m playwright install chromium

# 启动GUI应用程序
python gui_launcher.py
```

#### 📱 **命令行版本**
```bash
# 仅命令行使用（无GUI）
pip install playwright python-dotenv jinja2
python main_new.py --interactive
```

#### 配置

1. **复制环境变量模板:**
   ```bash
   cp config.example.env .env
   ```

2. **编辑 `.env` 文件，填入您的ManageBac凭据:**
   ```env
   # 必需 | Required
   MANAGEBAC_EMAIL=your_email@example.com
   MANAGEBAC_PASSWORD=your_password
   MANAGEBAC_URL=https://your-school.managebac.com
   
   # 可选AI功能 | Optional AI Features
   AI_ENABLED=true
   OPENAI_API_KEY=your_openai_api_key
   AI_MODEL=gpt-3.5-turbo
   
   # 报告设置 | Report Settings
   REPORT_FORMAT=html,json
   OUTPUT_DIR=reports
   ```

#### 使用方法

```bash
# 基本使用
python main_new.py

# 命令行接口
python -m managebac_checker.cli --help

# 生成指定格式
python -m managebac_checker.cli --format html

# 启用邮件通知
python -m managebac_checker.cli --notify
```

### 📁 项目结构

```
managebac-assignment-checker/
├── 📦 managebac_checker/          # 主要包
│   ├── 🔧 config.py               # 配置管理
│   ├── 🕷️ scraper.py              # 网页抓取引擎
│   ├── 📊 analyzer.py             # 数据分析
│   ├── 📋 reporter.py             # 报告生成
│   ├── 🔍 checker.py              # 主检查器
│   ├── 📧 notifications.py        # 邮件通知
│   └── 💻 cli.py                  # 命令行接口
├── 🧪 tests/                      # 单元测试
├── ⚙️ .github/workflows/          # CI/CD配置
├── 📄 setup.py                    # 包设置
├── 📋 requirements.txt            # 依赖列表
├── 📖 README.md                   # 文档
└── 📜 LICENSE                     # MIT许可证
```

### 🔧 开发

#### 运行测试
```bash
pytest tests/
```

#### 代码格式化
```bash
black managebac_checker/
flake8 managebac_checker/
```

### 📊 报告示例

#### HTML报告特性:
- 📱 响应式设计
- 🎨 现代化UI与图表
- 📈 交互式统计
- 🔍 可搜索作业

#### 控制台输出:
```
╭─────────────────────────────────────────────────────────╮
│                ManageBac作业报告                        │
├─────────────────────────────────────────────────────────┤
│ 📚 总作业数: 15                                         │
│ ⚠️  逾期: 2                                            │
│ 🔥 高优先级: 5                                          │
│ ✅ 已完成: 8                                           │
╰─────────────────────────────────────────────────────────╯
```

### ⚠️ 重要提示

- 请确保您有权限访问ManageBac系统
- 请遵守学校的使用条款和隐私政策
- 建议先在测试环境中验证功能
- 请保护好您的登录凭据

### 📜 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 🤝 贡献

欢迎贡献！请随时提交问题和拉取请求。

---

<div align="center">

**Made with ❤️ by [Hacker0458](https://github.com/Hacker0458)**

**⭐ 如果这个项目对您有帮助，请给它一个星标！**  
**⭐ If this project helps you, please give it a star!**

</div>