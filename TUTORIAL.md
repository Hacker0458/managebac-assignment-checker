# 📚 ManageBac Assignment Checker - Complete Tutorial
# 📚 ManageBac作业检查器 - 完整教程

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**🎯 Complete guide to using ManageBac Assignment Checker**  
**🎯 ManageBac作业检查器完整使用指南**

[English](#english) | [中文](#中文)

</div>

---

## English

### 🚀 Quick Start Guide

#### Option 1: Ultimate One-Click Install (Recommended)
```bash
# Download and run the ultimate installer
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash
```

#### Option 2: Quick Install
```bash
# Download and run the quick installer
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

#### Option 3: Manual Installation
```bash
# Clone the repository
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# Install dependencies
pip install -r requirements-core.txt

# Install Playwright browsers
python -m playwright install chromium

# Run the application
python gui_launcher.py
```

### 📋 Prerequisites

Before installing, make sure you have:

- **Python 3.8+** installed on your system
- **Internet connection** for downloading dependencies
- **ManageBac account** with valid credentials
- **Basic terminal/command line knowledge**

### 🔧 Installation Methods

#### Method 1: Ultimate Installer (Best Experience)

The ultimate installer provides the most comprehensive installation experience:

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash
```

**Features:**
- ✅ Automatic system dependency detection and installation
- ✅ Virtual environment support
- ✅ Desktop shortcuts creation
- ✅ Command line aliases
- ✅ Comprehensive error handling
- ✅ Post-installation testing

#### Method 2: Quick Installer (Fast Setup)

For users who want a quick setup:

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

**Features:**
- ✅ Fast download and installation
- ✅ Essential dependencies only
- ✅ Basic configuration setup

#### Method 3: GitHub Installer (From Source)

For developers or advanced users:

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_github.sh | bash
```

**Features:**
- ✅ Downloads complete source code
- ✅ Creates desktop shortcuts
- ✅ Sets up command line aliases
- ✅ Full project structure

### ⚙️ Configuration

After installation, you need to configure your ManageBac credentials:

#### 1. Edit Configuration File
```bash
# Navigate to installation directory
cd ~/managebac-assignment-checker

# Edit the configuration file
nano .env
```

#### 2. Required Settings
```env
# ManageBac Credentials (Required)
MANAGEBAC_EMAIL=your_email@example.com
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://your-school.managebac.com

# Optional AI Features
AI_ENABLED=true
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-3.5-turbo

# Report Settings
REPORT_FORMAT=html,json
OUTPUT_DIR=reports
```

#### 3. Save and Exit
- Press `Ctrl+X` to exit
- Press `Y` to save
- Press `Enter` to confirm

### 🖥️ Running the Application

#### GUI Mode (Recommended)
```bash
# Using the launcher script
managebac

# Or directly
cd ~/managebac-assignment-checker
python gui_launcher.py
```

#### Command Line Mode
```bash
# Using the CLI alias
managebac-cli

# Or directly
cd ~/managebac-assignment-checker
python main_new.py
```

#### Interactive Mode
```bash
# Interactive command line interface
python main_new.py --interactive
```

### 🎨 GUI Features

#### Main Interface
- **📊 Dashboard**: Overview of all assignments
- **🔍 Search & Filter**: Find specific assignments
- **📈 Statistics**: Assignment analytics and insights
- **⚙️ Settings**: Configure preferences and credentials

#### Professional GUI Features
- **🌞 Light Theme**: Clean, modern interface
- **🌙 Dark Theme**: Easy on the eyes
- **📱 Responsive Design**: Works on different screen sizes
- **🔔 Notifications**: Desktop notifications for deadlines

#### AI Assistant Features
- **🤖 Smart Analysis**: AI-powered assignment insights
- **📚 Study Recommendations**: Personalized study strategies
- **⏰ Time Management**: Optimized scheduling suggestions
- **📊 Progress Tracking**: Learning analytics

### 📊 Report Types

#### HTML Reports
- **📱 Responsive Design**: Works on all devices
- **📈 Interactive Charts**: Visual data representation
- **🔍 Searchable Content**: Find assignments quickly
- **🎨 Modern UI**: Professional appearance

#### JSON Reports
- **🔧 API Integration**: Machine-readable format
- **📊 Data Analysis**: Easy to process programmatically
- **🔄 Automation**: Perfect for scripts and tools

#### Markdown Reports
- **📝 Documentation**: Human-readable format
- **📋 Plain Text**: Works everywhere
- **📧 Email Friendly**: Easy to share via email

### 🔧 Advanced Usage

#### Command Line Options
```bash
# Show help
python main_new.py --help

# Generate specific report format
python main_new.py --format html

# Enable email notifications
python main_new.py --notify

# Run in background
python main_new.py --daemon

# Check specific courses
python main_new.py --courses "Math,Science"
```

#### Configuration Options
```env
# Auto-check interval (minutes)
AUTO_CHECK_INTERVAL=30

# Notification settings
NOTIFICATIONS_ENABLED=true
EMAIL_NOTIFICATIONS=true

# Report preferences
REPORT_FORMAT=html,json,markdown
INCLUDE_AI_ANALYSIS=true

# Performance settings
MAX_BROWSER_INSTANCES=1
PAGE_LOAD_TIMEOUT=30
```

### 🛠️ Troubleshooting

#### Common Issues

**1. Python Not Found**
```bash
# Install Python 3.8+
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# Windows
# Download from python.org
```

**2. Playwright Installation Failed**
```bash
# Install system dependencies
python -m playwright install-deps chromium

# Or install manually
python -m playwright install chromium
```

**3. GUI Not Starting**
```bash
# Try CLI mode first
python main_new.py --interactive

# Check logs
cat logs/managebac_checker.log

# Reinstall dependencies
pip install -r requirements-core.txt
```

**4. Authentication Issues**
```bash
# Check credentials in .env file
cat .env

# Test connection
python -c "from managebac_checker.checker import ManageBacChecker; checker = ManageBacChecker(); print('Connection test:', checker.test_connection())"
```

#### Getting Help

1. **Check Logs**: Look in `logs/managebac_checker.log`
2. **Test Connection**: Use the built-in connection test
3. **Update Dependencies**: Run `pip install -r requirements-core.txt --upgrade`
4. **Report Issues**: Create an issue on GitHub

### 📱 Mobile Usage

#### Progressive Web App (PWA)
- **📱 Mobile Friendly**: Responsive HTML reports
- **🔔 Push Notifications**: Get alerts on mobile
- **📊 Touch Interface**: Optimized for touch screens

#### Mobile Reports
- **📱 Responsive Design**: Works on all screen sizes
- **🔍 Touch Navigation**: Easy to navigate on mobile
- **📧 Share Reports**: Send reports via email or messaging

### 🔒 Security & Privacy

#### Data Protection
- **🔐 Local Storage**: All data stored locally
- **🔑 Secure Credentials**: Environment variables for sensitive data
- **🚫 No Data Collection**: No personal data sent to external servers

#### Best Practices
- **🔒 Keep Credentials Secure**: Don't share your .env file
- **🔄 Regular Updates**: Keep the application updated
- **📱 Secure Devices**: Use on trusted devices only

### 🚀 Performance Optimization

#### System Requirements
- **💻 RAM**: 2GB minimum, 4GB recommended
- **💾 Storage**: 500MB for application and dependencies
- **🌐 Internet**: Stable connection for ManageBac access

#### Performance Tips
- **🔄 Regular Cleanup**: Clear cache and logs periodically
- **⚡ Close Other Apps**: Free up system resources
- **📊 Monitor Usage**: Check system resource usage

### 📚 Additional Resources

#### Documentation
- **📖 README.md**: Main documentation
- **🔧 API Reference**: Code documentation
- **📋 Changelog**: Version history

#### Community
- **💬 GitHub Discussions**: Community support
- **🐛 Issue Tracker**: Bug reports and feature requests
- **⭐ Star the Project**: Show your support

#### Video Tutorials
- **🎥 Installation Guide**: Step-by-step video
- **📱 Usage Tutorial**: How to use the application
- **🔧 Troubleshooting**: Common issues and solutions

---

## 中文

### 🚀 快速开始指南

#### 选项1: 终极一键安装（推荐）
```bash
# 下载并运行终极安装器
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash
```

#### 选项2: 快速安装
```bash
# 下载并运行快速安装器
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

#### 选项3: 手动安装
```bash
# 克隆仓库
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 安装依赖
pip install -r requirements-core.txt

# 安装Playwright浏览器
python -m playwright install chromium

# 运行应用程序
python gui_launcher.py
```

### 📋 系统要求

安装前，请确保您有：

- **Python 3.8+** 已安装在您的系统上
- **互联网连接** 用于下载依赖
- **ManageBac账户** 具有有效凭据
- **基本终端/命令行知识**

### 🔧 安装方法

#### 方法1: 终极安装器（最佳体验）

终极安装器提供最全面的安装体验：

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/ultimate_install.sh | bash
```

**功能：**
- ✅ 自动系统依赖检测和安装
- ✅ 虚拟环境支持
- ✅ 桌面快捷方式创建
- ✅ 命令行别名
- ✅ 全面的错误处理
- ✅ 安装后测试

#### 方法2: 快速安装器（快速设置）

适合想要快速设置的用户：

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash
```

**功能：**
- ✅ 快速下载和安装
- ✅ 仅基本依赖
- ✅ 基本配置设置

#### 方法3: GitHub安装器（从源码）

适合开发者或高级用户：

```bash
curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_github.sh | bash
```

**功能：**
- ✅ 下载完整源代码
- ✅ 创建桌面快捷方式
- ✅ 设置命令行别名
- ✅ 完整项目结构

### ⚙️ 配置

安装后，您需要配置ManageBac凭据：

#### 1. 编辑配置文件
```bash
# 导航到安装目录
cd ~/managebac-assignment-checker

# 编辑配置文件
nano .env
```

#### 2. 必需设置
```env
# ManageBac凭据（必需）
MANAGEBAC_EMAIL=your_email@example.com
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://your-school.managebac.com

# 可选AI功能
AI_ENABLED=true
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-3.5-turbo

# 报告设置
REPORT_FORMAT=html,json
OUTPUT_DIR=reports
```

#### 3. 保存并退出
- 按 `Ctrl+X` 退出
- 按 `Y` 保存
- 按 `Enter` 确认

### 🖥️ 运行应用程序

#### GUI模式（推荐）
```bash
# 使用启动脚本
managebac

# 或直接运行
cd ~/managebac-assignment-checker
python gui_launcher.py
```

#### 命令行模式
```bash
# 使用CLI别名
managebac-cli

# 或直接运行
cd ~/managebac-assignment-checker
python main_new.py
```

#### 交互模式
```bash
# 交互式命令行界面
python main_new.py --interactive
```

### 🎨 GUI功能

#### 主界面
- **📊 仪表板**: 所有作业概览
- **🔍 搜索和筛选**: 查找特定作业
- **📈 统计**: 作业分析和洞察
- **⚙️ 设置**: 配置偏好和凭据

#### 专业GUI功能
- **🌞 浅色主题**: 简洁、现代界面
- **🌙 深色主题**: 护眼模式
- **📱 响应式设计**: 适配不同屏幕尺寸
- **🔔 通知**: 截止日期桌面通知

#### AI助手功能
- **🤖 智能分析**: AI驱动的作业洞察
- **📚 学习建议**: 个性化学习策略
- **⏰ 时间管理**: 优化调度建议
- **📊 进度跟踪**: 学习分析

### 📊 报告类型

#### HTML报告
- **📱 响应式设计**: 在所有设备上工作
- **📈 交互式图表**: 可视化数据表示
- **🔍 可搜索内容**: 快速查找作业
- **🎨 现代UI**: 专业外观

#### JSON报告
- **🔧 API集成**: 机器可读格式
- **📊 数据分析**: 易于程序化处理
- **🔄 自动化**: 适合脚本和工具

#### Markdown报告
- **📝 文档**: 人类可读格式
- **📋 纯文本**: 到处都能工作
- **📧 邮件友好**: 易于通过邮件分享

### 🔧 高级用法

#### 命令行选项
```bash
# 显示帮助
python main_new.py --help

# 生成特定报告格式
python main_new.py --format html

# 启用邮件通知
python main_new.py --notify

# 后台运行
python main_new.py --daemon

# 检查特定课程
python main_new.py --courses "数学,科学"
```

#### 配置选项
```env
# 自动检查间隔（分钟）
AUTO_CHECK_INTERVAL=30

# 通知设置
NOTIFICATIONS_ENABLED=true
EMAIL_NOTIFICATIONS=true

# 报告偏好
REPORT_FORMAT=html,json,markdown
INCLUDE_AI_ANALYSIS=true

# 性能设置
MAX_BROWSER_INSTANCES=1
PAGE_LOAD_TIMEOUT=30
```

### 🛠️ 故障排除

#### 常见问题

**1. 找不到Python**
```bash
# 安装Python 3.8+
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3

# Windows
# 从python.org下载
```

**2. Playwright安装失败**
```bash
# 安装系统依赖
python -m playwright install-deps chromium

# 或手动安装
python -m playwright install chromium
```

**3. GUI无法启动**
```bash
# 先尝试CLI模式
python main_new.py --interactive

# 检查日志
cat logs/managebac_checker.log

# 重新安装依赖
pip install -r requirements-core.txt
```

**4. 认证问题**
```bash
# 检查.env文件中的凭据
cat .env

# 测试连接
python -c "from managebac_checker.checker import ManageBacChecker; checker = ManageBacChecker(); print('连接测试:', checker.test_connection())"
```

#### 获取帮助

1. **检查日志**: 查看 `logs/managebac_checker.log`
2. **测试连接**: 使用内置连接测试
3. **更新依赖**: 运行 `pip install -r requirements-core.txt --upgrade`
4. **报告问题**: 在GitHub上创建问题

### 📱 移动端使用

#### 渐进式网页应用（PWA）
- **📱 移动友好**: 响应式HTML报告
- **🔔 推送通知**: 在移动设备上获取提醒
- **📊 触摸界面**: 针对触摸屏优化

#### 移动报告
- **📱 响应式设计**: 适配所有屏幕尺寸
- **🔍 触摸导航**: 在移动设备上易于导航
- **📧 分享报告**: 通过邮件或消息发送报告

### 🔒 安全和隐私

#### 数据保护
- **🔐 本地存储**: 所有数据本地存储
- **🔑 安全凭据**: 敏感数据使用环境变量
- **🚫 无数据收集**: 不向外部服务器发送个人数据

#### 最佳实践
- **🔒 保护凭据安全**: 不要分享您的.env文件
- **🔄 定期更新**: 保持应用程序更新
- **📱 安全设备**: 仅在受信任的设备上使用

### 🚀 性能优化

#### 系统要求
- **💻 内存**: 最少2GB，推荐4GB
- **💾 存储**: 应用程序和依赖500MB
- **🌐 网络**: 稳定的ManageBac访问连接

#### 性能提示
- **🔄 定期清理**: 定期清除缓存和日志
- **⚡ 关闭其他应用**: 释放系统资源
- **📊 监控使用**: 检查系统资源使用情况

### 📚 其他资源

#### 文档
- **📖 README.md**: 主要文档
- **🔧 API参考**: 代码文档
- **📋 变更日志**: 版本历史

#### 社区
- **💬 GitHub讨论**: 社区支持
- **🐛 问题跟踪**: 错误报告和功能请求
- **⭐ 给项目点赞**: 表达您的支持

#### 视频教程
- **🎥 安装指南**: 分步视频
- **📱 使用教程**: 如何使用应用程序
- **🔧 故障排除**: 常见问题和解决方案

---

<div align="center">

**Made with ❤️ by [Hacker0458](https://github.com/Hacker0458)**

**⭐ 如果这个项目对您有帮助，请给它一个星标！**  
**⭐ If this project helps you, please give it a star!**

</div>
