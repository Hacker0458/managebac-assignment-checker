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

- 🔐 **Secure Login**: Automated ManageBac authentication with credential protection
- 📊 **Multi-format Reports**: Generate HTML, Markdown, JSON, and console reports
- 🎯 **Smart Analysis**: Intelligent priority and urgency assessment
- 📧 **Email Notifications**: Automated assignment reminders
- 📈 **Visual Analytics**: Detailed statistics and data visualization
- ⚙️ **Flexible Configuration**: Customizable settings via environment variables
- 🧪 **Full Test Coverage**: Comprehensive unit testing suite
- 🚀 **CI/CD Ready**: GitHub Actions workflow included

### 🚀 Quick Start

#### Installation

**🚀 Quick Install (One Command):**
```bash
git clone https://github.com/Hacker0458/managebac-assignment-checker.git && cd managebac-assignment-checker && pip install -r requirements.txt && python main_new.py --interactive
```

**🎯 Auto Install Scripts:**
- **Linux/macOS**: `./install.sh`
- **Windows**: `install.bat`

**📋 Step by Step:**
```bash
# Clone the repository
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

#### Configuration

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file with your ManageBac credentials:**
   ```env
   MANAGEBAC_EMAIL=your_email@example.com
   MANAGEBAC_PASSWORD=your_password
   MANAGEBAC_URL=https://your-school.managebac.com
   REPORT_FORMAT=html
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

- 🔐 **安全登录**: 自动化ManageBac身份验证，保护凭据安全
- 📊 **多格式报告**: 生成HTML、Markdown、JSON和控制台报告
- 🎯 **智能分析**: 智能优先级和紧急程度评估
- 📧 **邮件通知**: 自动化作业提醒功能
- 📈 **可视化分析**: 详细的统计数据和数据可视化
- ⚙️ **灵活配置**: 通过环境变量自定义设置
- 🧪 **完整测试**: 全面的单元测试套件
- 🚀 **CI/CD就绪**: 包含GitHub Actions工作流

### 🚀 快速开始

#### 安装

**🚀 快速安装（一键命令）：**
```bash
git clone https://github.com/Hacker0458/managebac-assignment-checker.git && cd managebac-assignment-checker && pip install -r requirements.txt && python main_new.py --interactive
```

**🎯 自动安装脚本：**
- **Linux/macOS**: `./install.sh`
- **Windows**: `install.bat`

**📋 分步安装：**
```bash
# 克隆仓库
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 安装依赖
pip install -r requirements.txt

# 或者作为包安装
pip install -e .
```

#### 配置

1. **复制环境变量模板:**
   ```bash
   cp .env.example .env
   ```

2. **编辑 `.env` 文件，填入您的ManageBac凭据:**
   ```env
   MANAGEBAC_EMAIL=your_email@example.com
   MANAGEBAC_PASSWORD=your_password
   MANAGEBAC_URL=https://your-school.managebac.com
   REPORT_FORMAT=html
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