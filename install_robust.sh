#!/bin/bash

# ========================================
# 🎓 ManageBac Assignment Checker - Robust Installation Script
# 🎓 ManageBac作业检查器 - 稳定安装脚本
# ========================================
#
# This script provides a more reliable installation with fallback options
# 此脚本提供更可靠的安装，包含后备选项
#
# Usage: curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_robust.sh | bash
# ========================================

set -e

# Color definitions | 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
CHECK='✅'
CROSS='❌'
INFO='ℹ️'

# Configuration | 配置
REPO_URL="https://github.com/Hacker0458/managebac-assignment-checker"
RAW_URL="https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main"
PROJECT_DIR="managebac-assignment-checker"

# Print functions | 打印函数
print_success() { echo -e "${GREEN}${CHECK} $1${NC}"; }
print_error() { echo -e "${RED}${CROSS} $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}${INFO} $1${NC}"; }
print_status() { echo -e "${BLUE}🔄 $1${NC}"; }

# Function to detect Python command | 检测Python命令
detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python 3 not found! Please install Python 3.9+ first."
        print_error "Python 3 未找到！请先安装 Python 3.9+。"
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_info "Found Python: $PYTHON_VERSION"
}

# Function to download file with fallback | 下载文件的函数（含后备方案）
download_file() {
    local url="$1"
    local filename="$2"
    local essential="$3"  # true/false

    print_status "Downloading $filename..."

    # Try curl first
    if command -v curl &> /dev/null; then
        if curl -sL "$url" -o "$filename" && [ -s "$filename" ]; then
            print_success "$filename downloaded successfully"
            return 0
        fi
    fi

    # Try wget as fallback
    if command -v wget &> /dev/null; then
        if wget -q "$url" -O "$filename" && [ -s "$filename" ]; then
            print_success "$filename downloaded successfully (via wget)"
            return 0
        fi
    fi

    # If essential file fails, exit
    if [ "$essential" = "true" ]; then
        print_error "Failed to download essential file: $filename"
        print_error "Please check your internet connection and try again."
        exit 1
    else
        print_warning "Failed to download optional file: $filename"
        return 1
    fi
}

# Function to create fallback requirements | 创建后备依赖文件
create_fallback_requirements() {
    print_warning "Creating fallback requirements.txt..."
    cat > requirements.txt << 'EOF'
# ========================================
# ManageBac Assignment Checker - Core Dependencies
# ========================================

# Core Dependencies
playwright>=1.45.0
python-dotenv>=1.0.0

# Optional Dependencies
jinja2>=3.1.4
openai>=1.0.0
pystray>=0.19.0
pillow>=10.0.0

# Testing (optional)
pytest>=8.4.2
pytest-asyncio>=0.23.0
EOF
    print_success "Fallback requirements.txt created"
}

# Function to install dependencies with multiple methods | 多种方法安装依赖
install_dependencies() {
    print_status "Installing Python dependencies..."

    # Upgrade pip first
    $PIP_CMD install --upgrade pip

    # Method 1: Try requirements.txt
    if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
        print_status "Installing from requirements.txt..."
        if $PIP_CMD install -r requirements.txt; then
            print_success "Dependencies installed from requirements.txt"
            return 0
        else
            print_warning "Failed to install from requirements.txt, trying individual packages..."
        fi
    fi

    # Method 2: Install core packages individually
    print_status "Installing core packages individually..."
    CORE_PACKAGES=(
        "playwright>=1.45.0"
        "python-dotenv>=1.0.0"
        "jinja2>=3.1.4"
    )

    for package in "${CORE_PACKAGES[@]}"; do
        if $PIP_CMD install "$package"; then
            print_success "Installed: $package"
        else
            print_warning "Failed to install: $package"
        fi
    done

    # Method 3: Install optional packages
    print_status "Installing optional packages..."
    OPTIONAL_PACKAGES=(
        "openai>=1.0.0"
        "pystray>=0.19.0"
        "pillow>=10.0.0"
    )

    for package in "${OPTIONAL_PACKAGES[@]}"; do
        if $PIP_CMD install "$package"; then
            print_success "Installed optional: $package"
        else
            print_warning "Skipped optional: $package"
        fi
    done

    print_success "Dependency installation completed"
}

# Function to setup playwright | 设置playwright
setup_playwright() {
    print_status "Setting up Playwright browsers..."
    if $PYTHON_CMD -m playwright install chromium; then
        print_success "Playwright browsers installed"
    else
        print_warning "Playwright browser installation failed, you may need to run it manually later"
    fi
}

# Function to create project structure | 创建项目结构
create_project_structure() {
    print_status "Creating project structure..."

    # Create necessary directories
    mkdir -p logs cache reports

    # Create minimal launcher if main files are missing
    if [ ! -f "gui_launcher.py" ]; then
        print_warning "Creating minimal GUI launcher..."
        cat > gui_launcher.py << 'EOF'
#!/usr/bin/env python3
"""
Minimal GUI Launcher for ManageBac Assignment Checker
"""

import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def main():
    try:
        # Try to import and run the main application
        from managebac_checker.professional_gui import ProfessionalManageBacGUI

        app = ProfessionalManageBacGUI()
        app.run()
    except ImportError as e:
        # Fallback message
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Import Error",
            f"Could not import ManageBac Checker modules.\n"
            f"Please ensure all dependencies are installed.\n\n"
            f"Error: {str(e)}\n\n"
            f"Try running: pip install -r requirements.txt"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF
        chmod +x gui_launcher.py
    fi

    print_success "Project structure created"
}

# Main installation function | 主安装函数
main() {
    echo -e "${BLUE}"
    echo "========================================"
    echo "🎓 ManageBac Assignment Checker"
    echo "   Robust Installation Script"
    echo "========================================"
    echo -e "${NC}"

    # Detect Python
    detect_python

    # Create project directory
    if [ ! -d "$PROJECT_DIR" ]; then
        print_status "Creating project directory..."
        mkdir -p "$PROJECT_DIR"
        print_success "Project directory created"
    fi

    cd "$PROJECT_DIR"

    # Download essential files with fallback
    print_status "Downloading project files..."

    # Download requirements.txt (try multiple sources)
    if ! download_file "$RAW_URL/requirements.txt" "requirements.txt" false; then
        create_fallback_requirements
    fi

    # Download other essential files
    download_file "$RAW_URL/config.example.env" "config.example.env" false
    download_file "$RAW_URL/gui_launcher.py" "gui_launcher.py" false
    download_file "$RAW_URL/main_new.py" "main_new.py" false

    # Create project structure
    create_project_structure

    # Install dependencies
    install_dependencies

    # Setup Playwright
    setup_playwright

    # Create config file if it doesn't exist
    if [ ! -f ".env" ] && [ -f "config.example.env" ]; then
        cp config.example.env .env
        print_success "Environment config file created"
        print_info "Please edit .env file with your ManageBac credentials"
    fi

    # Final success message
    echo -e "${GREEN}"
    echo "========================================"
    echo "✅ Installation Completed Successfully!"
    echo "✅ 安装成功完成！"
    echo "========================================"
    echo -e "${NC}"

    echo ""
    print_info "Next steps | 下一步："
    echo "1. Edit .env file with your credentials | 编辑.env文件填入凭据"
    echo "2. Run: python3 gui_launcher.py | 运行GUI程序"
    echo "3. Or run: python3 main_new.py | 或运行命令行版本"
    echo ""

    print_success "Ready to use! | 准备就绪！"
}

# Run main function
main "$@"