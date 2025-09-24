# ManageBac Assignment Checker | ManageBac作业检查器

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