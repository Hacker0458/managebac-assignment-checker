#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker Quick Install Script
# 🚀 ManageBac作业检查器快速安装脚本
# ========================================

set -e  # Exit on any error

# Colors for output | 输出颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
GEAR="⚙️"
BOOK="📚"
COMPUTER="💻"
WARNING="⚠️"

# Function to print colored output | 打印彩色输出函数
print_status() {
    echo -e "${BLUE}${GEAR} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

print_header() {
    echo -e "${PURPLE}${ROCKET} $1${NC}"
}

# Function to check if command exists | 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get Python version | 获取Python版本
get_python_version() {
    if command_exists python3; then
        python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    elif command_exists python; then
        python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    else
        echo "0.0"
    fi
}

# Function to check Python version | 检查Python版本
check_python_version() {
    local version=$1
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -gt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -ge 8 ]); then
        return 0
    else
        return 1
    fi
}

# Function to install system dependencies | 安装系统依赖
install_system_deps() {
    print_status "Installing system dependencies... | 正在安装系统依赖..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv python3-tk curl
        elif command_exists yum; then
            sudo yum install -y python3-pip python3-venv tkinter curl
        elif command_exists dnf; then
            sudo dnf install -y python3-pip python3-venv tkinter curl
        elif command_exists pacman; then
            sudo pacman -S python-pip python-tkinter curl
        else
            print_warning "Could not detect package manager. Please install Python 3.8+, pip, and tkinter manually."
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install python3
        else
            print_warning "Homebrew not found. Please install Python 3.8+ manually."
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash)
        print_warning "Windows detected. Please install Python 3.8+ from python.org"
    fi
}

# Function to create virtual environment | 创建虚拟环境
create_venv() {
    local venv_dir="managebac_venv"
    
    if [ ! -d "$venv_dir" ]; then
        print_status "Creating virtual environment... | 正在创建虚拟环境..."
        $PYTHON_CMD -m venv "$venv_dir"
        print_success "Virtual environment created | 虚拟环境已创建"
    else
        print_success "Virtual environment already exists | 虚拟环境已存在"
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        source "$venv_dir/Scripts/activate"
    else
        # Unix-like systems
        source "$venv_dir/bin/activate"
    fi
    
    print_success "Virtual environment activated | 虚拟环境已激活"
}

# Function to install Python dependencies | 安装Python依赖
install_python_deps() {
    print_status "Installing Python dependencies... | 正在安装Python依赖..."
    
    # Upgrade pip first
    $PIP_CMD install --upgrade pip
    
    # Install core dependencies
    if [ -f "requirements-core.txt" ]; then
        $PIP_CMD install -r requirements-core.txt
        print_success "Core dependencies installed | 核心依赖已安装"
    elif [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
        print_success "Dependencies installed | 依赖已安装"
    else
        # Fallback: install essential packages
        $PIP_CMD install playwright python-dotenv jinja2 openai pystray pillow
        print_success "Essential dependencies installed | 基本依赖已安装"
    fi
}

# Function to install Playwright browsers | 安装Playwright浏览器
install_playwright() {
    print_status "Installing Playwright browsers... | 正在安装Playwright浏览器..."
    
    if $PYTHON_CMD -m playwright install chromium; then
        print_success "Playwright browsers installed | Playwright浏览器已安装"
    else
        print_warning "Playwright installation failed, but you can continue | Playwright安装失败，但您可以继续使用"
        print_warning "You may need to install system dependencies for Playwright | 您可能需要安装Playwright的系统依赖"
        
        # Try to install system dependencies
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            print_status "Installing Playwright system dependencies... | 正在安装Playwright系统依赖..."
            $PYTHON_CMD -m playwright install-deps chromium || true
        fi
    fi
}

# Function to setup configuration | 设置配置
setup_config() {
    if [ ! -f ".env" ]; then
        if [ -f "config.example.env" ]; then
            print_status "Creating configuration file... | 正在创建配置文件..."
            cp config.example.env .env
            print_success "Configuration template created as .env | 配置模板已创建为.env文件"
        else
            print_warning "No configuration template found | 未找到配置模板"
        fi
    else
        print_success "Configuration file already exists | 配置文件已存在"
    fi
}

# Function to create desktop shortcuts | 创建桌面快捷方式
create_shortcuts() {
    print_status "Creating desktop shortcuts... | 正在创建桌面快捷方式..."
    
    if command_exists python3; then
        $PYTHON_CMD create_shortcuts.py 2>/dev/null || print_warning "Could not create shortcuts | 无法创建快捷方式"
    fi
}

# Function to test installation | 测试安装
test_installation() {
    print_status "Testing installation... | 正在测试安装..."
    
    if $PYTHON_CMD -c "import managebac_checker; print('✅ ManageBac Checker module imported successfully')" 2>/dev/null; then
        print_success "Installation test passed | 安装测试通过"
        return 0
    else
        print_warning "Installation test failed, but you can still try running the application | 安装测试失败，但您仍可以尝试运行应用程序"
        return 1
    fi
}

# Function to download project files | 下载项目文件函数
download_project_files() {
    print_status "Downloading project files... | 正在下载项目文件..."
    
    # Create project directory
    PROJECT_DIR="$HOME/managebac-assignment-checker"
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    
    # Download essential files
    print_status "Downloading requirements files... | 正在下载依赖文件..."
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements-core.txt" -o requirements-core.txt
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt" -o requirements.txt
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/config.example.env" -o config.example.env
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/gui_launcher.py" -o gui_launcher.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/main_new.py" -o main_new.py
    
    # Download package files
    print_status "Downloading package files... | 正在下载包文件..."
    mkdir -p managebac_checker
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/__init__.py" -o managebac_checker/__init__.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/config.py" -o managebac_checker/config.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/checker.py" -o managebac_checker/checker.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/professional_gui.py" -o managebac_checker/professional_gui.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/gui.py" -o managebac_checker/gui.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/scraper.py" -o managebac_checker/scraper.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/analysis.py" -o managebac_checker/analysis.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/reporter.py" -o managebac_checker/reporter.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/notifications.py" -o managebac_checker/notifications.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/cli.py" -o managebac_checker/cli.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/runner.py" -o managebac_checker/runner.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/analyzer.py" -o managebac_checker/analyzer.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/logging_utils.py" -o managebac_checker/logging_utils.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/models.py" -o managebac_checker/models.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/reporting.py" -o managebac_checker/reporting.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/ai_assistant.py" -o managebac_checker/ai_assistant.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/enhanced_gui.py" -o managebac_checker/enhanced_gui.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/system_tray.py" -o managebac_checker/system_tray.py
    curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/managebac_checker/improved_system_tray.py" -o managebac_checker/improved_system_tray.py
    
    print_success "Project files downloaded to $PROJECT_DIR"
    print_success "项目文件已下载到 $PROJECT_DIR"
}

# Main installation process | 主安装过程
main() {
    print_header "ManageBac Assignment Checker Quick Install"
    print_header "ManageBac作业检查器快速安装"
    echo "========================================================"
    
    # Check if we're in the right directory, if not download files
    if [ ! -f "managebac_checker/__init__.py" ] && [ ! -f "main.py" ]; then
        print_status "Not in project directory, downloading files... | 不在项目目录中，正在下载文件..."
        download_project_files
    fi
    
    # Check Python installation | 检查Python安装
    print_status "Checking Python installation... | 正在检查Python安装..."
    if command_exists python3; then
        PYTHON_VERSION=$(get_python_version)
        print_success "Python found: $PYTHON_VERSION"
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_VERSION=$(get_python_version)
        print_success "Python found: $PYTHON_VERSION"
        PYTHON_CMD="python"
    else
        print_error "Python not found! Please install Python 3.8+ first."
        print_error "未找到Python！请先安装Python 3.8+。"
        install_system_deps
        exit 1
    fi
    
    # Check Python version
    if ! check_python_version "$PYTHON_VERSION"; then
        print_error "Python 3.8+ is required, but found $PYTHON_VERSION"
        print_error "需要Python 3.8+，但找到的是$PYTHON_VERSION"
        install_system_deps
        exit 1
    fi
    
    # Check pip installation | 检查pip安装
    print_status "Checking pip installation... | 正在检查pip安装..."
    if command_exists pip3; then
        print_success "pip3 found"
        PIP_CMD="pip3"
    elif command_exists pip; then
        print_success "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found! Please install pip first."
        print_error "未找到pip！请先安装pip。"
        install_system_deps
        exit 1
    fi
    
    # Create virtual environment (optional but recommended)
    if [ "$1" = "--venv" ] || [ "$1" = "-v" ]; then
        create_venv
    fi
    
    # Install Python dependencies
    install_python_deps
    
    # Install Playwright browsers
    install_playwright
    
    # Setup configuration
    setup_config
    
    # Create shortcuts
    create_shortcuts
    
    # Test installation
    test_installation
    
    echo ""
    print_success "Installation completed successfully! | 安装完成！"
    echo "========================================================"
    echo ""
    print_header "Next Steps | 下一步操作:"
    echo ""
    echo -e "${YELLOW}1. ${NC}Edit .env file with your ManageBac credentials"
    echo -e "${YELLOW}1. ${NC}编辑.env文件，填入您的ManageBac凭据"
    echo ""
    echo -e "${YELLOW}2. ${NC}Navigate to the installation directory:"
    echo -e "${YELLOW}2. ${NC}导航到安装目录："
    echo -e "   ${COMPUTER} cd $HOME/managebac-assignment-checker"
    echo ""
    echo -e "${YELLOW}3. ${NC}Run the program:"
    echo -e "${YELLOW}3. ${NC}运行程序："
    if [ -d "managebac_venv" ]; then
        echo -e "   ${COMPUTER} source managebac_venv/bin/activate && $PYTHON_CMD gui_launcher.py"
    else
        echo -e "   ${COMPUTER} $PYTHON_CMD gui_launcher.py"
    fi
    echo ""
    echo -e "${YELLOW}4. ${NC}Or use command line mode:"
    echo -e "${YELLOW}4. ${NC}或使用命令行模式："
    if [ -d "managebac_venv" ]; then
        echo -e "   ${COMPUTER} source managebac_venv/bin/activate && $PYTHON_CMD main_new.py"
    else
        echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py"
    fi
    echo ""
    print_header "For help | 获取帮助:"
    echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --help"
    echo ""
    print_header "Happy assignment tracking! | 愉快地追踪作业！"
}

# Handle script arguments | 处理脚本参数
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [options]"
        echo "Options:"
        echo "  --venv, -v    Create virtual environment"
        echo "  --help, -h    Show this help message"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac