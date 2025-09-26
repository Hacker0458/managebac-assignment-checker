# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=managebac_checker

# Run specific test types
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run parallel tests
pytest -n auto
```

### Code Quality
```bash
# Format code with Black
black managebac_checker/

# Check code style with flake8
flake8 managebac_checker/

# Type checking with mypy
mypy managebac_checker/

# Security scan with bandit
bandit -r managebac_checker/

# Import sorting
isort managebac_checker/
```

### Installation & Setup

#### 🌟 Ultimate Installer (推荐 | Recommended)
```bash
# 🚀 一键智能安装 - 自动选择最佳方式
# One-click smart installation - automatically selects best method
python ultimate_installer.py

# 🎨 图形界面安装 - 美观的安装向导
# GUI installation - beautiful installation wizard
python ultimate_installer.py --mode gui

# ⚡ 快速安装 - 使用默认设置
# Quick installation - uses default settings
python ultimate_installer.py --mode quick --auto-launch

# 🧙‍♂️ 交互式向导 - 逐步配置
# Interactive wizard - step-by-step configuration
python ultimate_installer.py --mode wizard

# 🔧 修复安装 - 修复现有问题
# Repair installation - fix existing issues
python ultimate_installer.py --repair
```

#### 🎯 Alternative Installers
```bash
# 高级命令行安装器 - 智能检测和自动启动
# Advanced command-line installer with smart detection
python advanced_installer.py

# 图形界面安装向导 - 现代化界面
# Enhanced GUI setup wizard
python enhanced_setup_gui.py

# 经典安装向导 - 交互式配置
# Classic interactive setup wizard
python setup_wizard.py

# 完整安装脚本 - 包含GUI库
# Complete installation script with GUI libraries
python install_complete.py
```

#### 🛠️ Manual Installation
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Install Playwright browsers (required for web scraping)
python -m playwright install chromium

# Set up environment
cp config.example.env .env
# Edit .env with ManageBac credentials

# Create desktop shortcuts
python create_desktop_shortcut.py
```

### Running the Application

#### 🎯 For Novice Users (Zero Configuration)
```bash
# 🌟 优化安装器 - 默认自动启动应用（推荐）
# Optimized installer - auto-launches by default (recommended)
python 优化安装器.py

# Ultimate installer - now with auto-launch by default
python ultimate_installer.py

# Double-click these files to start
./START.sh           # macOS/Linux
START.bat            # Windows

# One-click Python launcher (fully automated)
python one_click_run.py
```

#### 🧠 Intelligent Launchers (New & Improved)
```bash
# 🧠 智能启动器 - 最佳用户体验和错误处理
# Intelligent launcher - best UX with error handling
python intelligent_launcher.py

# Smart launcher - auto-detects best startup method
python smart_launcher.py

# User-friendly launcher with GUI options
python run_app.py

# Launch helper for post-setup options
python launch_helper.py
```

#### 🎨 Traditional Methods
```bash
# GUI application (recommended)
python gui_launcher.py

# Command-line interface
python main.py

# CLI with specific options
python -m managebac_checker.cli --format html
python -m managebac_checker.cli --notify

# Interactive mode
python main_new.py --interactive
```

### Build and Distribution
```bash
# Build package
python -m build

# Check package quality
check-manifest
twine check dist/*

# Performance analysis
pytest tests/ --benchmark-only
```

## Project Architecture

### Core Components

The project follows a modular architecture with separation of concerns:

**Main Package (`managebac_checker/`)**:
- `config.py` - Configuration management with environment variable support
- `scraper.py` - Playwright-based web scraping for ManageBac authentication and data extraction
- `analyzer.py` - Assignment data analysis and processing
- `reporter.py` - Multi-format report generation (HTML, JSON, Markdown)
- `checker.py` - Main orchestration logic
- `cli.py` - Command-line interface with argparse
- `runner.py` - Async execution runner
- `notifications.py` - Email notification system

**GUI Components**:
- `professional_gui.py` - Main tkinter-based GUI application
- `enhanced_gui.py` - Enhanced GUI features
- `system_tray.py` - System tray integration
- `gui_launcher.py` - GUI launcher script

**Installation System**:
- `ultimate_installer.py` - Master installer with multiple modes and smart fallbacks
- `advanced_installer.py` - Advanced command-line installer with state tracking
- `enhanced_setup_gui.py` - Beautiful graphical installation wizard
- `setup_wizard.py` - Interactive setup wizard with enhanced error handling
- `install_complete.py` - Complete installation script with GUI libraries
- `error_handler.py` - Comprehensive error handling and user feedback system

**Novice User Experience**:
- `one_click_run.py` - Zero-configuration startup script with full automation
- `smart_launcher.py` - Intelligent launcher with environment detection
- `run_app.py` - User-friendly launcher with GUI dialogs
- `launch_helper.py` - Post-setup launch options assistant
- `start.py` - Fool-proof startup script with animations
- `create_desktop_shortcut.py` - Cross-platform desktop integration
- `START.sh` / `START.bat` - Double-click startup scripts

**AI Integration**:
- `ai_assistant.py` - OpenAI integration for intelligent assignment analysis

### Data Flow

1. **Configuration Loading**: Environment variables and CLI arguments are merged through `Config` class
2. **Authentication**: `ManageBacScraper` handles secure login using Playwright
3. **Data Extraction**: Web scraping extracts assignment data from ManageBac
4. **Analysis**: `AssignmentAnalyzer` processes raw data and calculates metrics
5. **AI Processing**: Optional AI analysis provides insights and recommendations
6. **Report Generation**: `ReportGenerator` creates multiple output formats
7. **Notifications**: Email alerts sent for important assignments

### Key Design Patterns

- **Factory Pattern**: Used in report generation for different output formats
- **Strategy Pattern**: Multiple analysis strategies for different assignment types
- **Observer Pattern**: GUI components observe data changes for real-time updates
- **Async/Await**: Non-blocking operations throughout the scraping and processing pipeline

### Security Considerations

- Credentials stored in `.env` files (never committed)
- Secure authentication flow with Playwright
- Input validation and sanitization
- No sensitive data in logs or reports

### GUI Architecture

The GUI uses tkinter with a modern design approach:
- **Main Window**: Tabbed interface for different views
- **System Tray**: Background operation support
- **Settings Dialog**: Comprehensive configuration interface
- **Assignment Cards**: Visual representation of assignments with filtering

### Testing Strategy

- **Unit Tests**: Individual component testing in `tests/`
- **Integration Tests**: End-to-end workflow testing
- **Factory Pattern**: Test data generation using `factories.py`
- **Coverage**: Comprehensive test coverage with pytest-cov
- **Security Testing**: Bandit for security vulnerability scanning

### Environment Setup

The application requires:
- Python 3.8+ with asyncio support
- Playwright for browser automation
- tkinter for GUI (usually included with Python)
- Optional: OpenAI API key for AI features
- ManageBac school credentials

Configuration is managed through:
- `.env` file for sensitive data
- `pyproject.toml` for project metadata and tool configuration
- Command-line arguments for runtime options