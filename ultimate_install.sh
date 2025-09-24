#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker - Ultimate One-Click Installer
# 🚀 ManageBac作业检查器 - 终极一键安装器
# ========================================

set -e  # Exit on any error

# Colors for output | 输出颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Emojis
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
GEAR="⚙️"
BOOK="📚"
COMPUTER="💻"
WARNING="⚠️"
STAR="⭐"
HEART="❤️"
FIRE="🔥"

# Configuration
REPO_URL="https://github.com/Hacker0458/managebac-assignment-checker"
INSTALL_DIR="$HOME/managebac-assignment-checker"
BRANCH="main"

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

print_info() {
    echo -e "${CYAN}${BOOK} $1${NC}"
}

print_step() {
    echo -e "${WHITE}${STAR} $1${NC}"
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

# Function to check Python version compatibility | 检查Python版本兼容性
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
    print_step "Installing system dependencies... | 正在安装系统依赖..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            print_status "Using apt-get (Ubuntu/Debian) | 使用apt-get (Ubuntu/Debian)"
            sudo apt-get update
            sudo apt-get install -y python3-pip python3-venv python3-tk curl wget unzip git
        elif command_exists yum; then
            print_status "Using yum (CentOS/RHEL) | 使用yum (CentOS/RHEL)"
            sudo yum install -y python3-pip python3-venv tkinter curl wget unzip git
        elif command_exists dnf; then
            print_status "Using dnf (Fedora) | 使用dnf (Fedora)"
            sudo dnf install -y python3-pip python3-venv tkinter curl wget unzip git
        elif command_exists pacman; then
            print_status "Using pacman (Arch Linux) | 使用pacman (Arch Linux)"
            sudo pacman -S python-pip python-tkinter curl wget unzip git
        else
            print_warning "Could not detect package manager. Please install Python 3.8+, pip, and tkinter manually."
            print_warning "无法检测包管理器。请手动安装Python 3.8+、pip和tkinter。"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            print_status "Using Homebrew (macOS) | 使用Homebrew (macOS)"
            brew install python3 curl wget git
        else
            print_warning "Homebrew not found. Please install Python 3.8+ manually."
            print_warning "未找到Homebrew。请手动安装Python 3.8+。"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash)
        print_warning "Windows detected. Please install Python 3.8+ from python.org"
        print_warning "检测到Windows。请从python.org安装Python 3.8+。"
    fi
}

# Function to create project directory and download files | 创建项目目录并下载文件
setup_project() {
    print_step "Setting up project directory... | 正在设置项目目录..."
    
    # Create project directory
    mkdir -p "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    print_status "Downloading project files... | 正在下载项目文件..."
    
    # Download essential files
    curl -s -L "$REPO_URL/raw/$BRANCH/requirements-core.txt" -o requirements-core.txt
    curl -s -L "$REPO_URL/raw/$BRANCH/requirements.txt" -o requirements.txt
    curl -s -L "$REPO_URL/raw/$BRANCH/config.example.env" -o config.example.env
    curl -s -L "$REPO_URL/raw/$BRANCH/gui_launcher.py" -o gui_launcher.py
    curl -s -L "$REPO_URL/raw/$BRANCH/main_new.py" -o main_new.py
    curl -s -L "$REPO_URL/raw/$BRANCH/install_complete.py" -o install_complete.py
    
    # Download package files
    print_status "Downloading package files... | 正在下载包文件..."
    mkdir -p managebac_checker
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/__init__.py" -o managebac_checker/__init__.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/config.py" -o managebac_checker/config.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/checker.py" -o managebac_checker/checker.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/professional_gui.py" -o managebac_checker/professional_gui.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/gui.py" -o managebac_checker/gui.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/scraper.py" -o managebac_checker/scraper.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/analysis.py" -o managebac_checker/analysis.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/reporter.py" -o managebac_checker/reporter.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/notifications.py" -o managebac_checker/notifications.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/cli.py" -o managebac_checker/cli.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/runner.py" -o managebac_checker/runner.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/analyzer.py" -o managebac_checker/analyzer.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/logging_utils.py" -o managebac_checker/logging_utils.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/models.py" -o managebac_checker/models.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/reporting.py" -o managebac_checker/reporting.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/ai_assistant.py" -o managebac_checker/ai_assistant.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/enhanced_gui.py" -o managebac_checker/enhanced_gui.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/system_tray.py" -o managebac_checker/system_tray.py
    curl -s -L "$REPO_URL/raw/$BRANCH/managebac_checker/improved_system_tray.py" -o managebac_checker/improved_system_tray.py
    
    # Download additional files
    curl -s -L "$REPO_URL/raw/$BRANCH/icon.png" -o icon.png 2>/dev/null || true
    curl -s -L "$REPO_URL/raw/$BRANCH/icon.ico" -o icon.ico 2>/dev/null || true
    
    print_success "Project files downloaded to $INSTALL_DIR"
    print_success "项目文件已下载到 $INSTALL_DIR"
}

# Function to create virtual environment | 创建虚拟环境
create_venv() {
    local venv_dir="managebac_venv"
    
    if [ ! -d "$venv_dir" ]; then
        print_step "Creating virtual environment... | 正在创建虚拟环境..."
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
    print_step "Installing Python dependencies... | 正在安装Python依赖..."
    
    # Upgrade pip first
    print_status "Upgrading pip... | 正在升级pip..."
    $PIP_CMD install --upgrade pip
    
    # Install core dependencies
    if [ -f "requirements-core.txt" ]; then
        print_status "Installing core dependencies... | 正在安装核心依赖..."
        $PIP_CMD install -r requirements-core.txt
        print_success "Core dependencies installed | 核心依赖已安装"
    elif [ -f "requirements.txt" ]; then
        print_status "Installing all dependencies... | 正在安装所有依赖..."
        $PIP_CMD install -r requirements.txt
        print_success "Dependencies installed | 依赖已安装"
    else
        # Fallback: install essential packages
        print_status "Installing essential packages... | 正在安装基本包..."
        $PIP_CMD install playwright python-dotenv jinja2 openai pystray pillow
        print_success "Essential dependencies installed | 基本依赖已安装"
    fi
}

# Function to install Playwright browsers | 安装Playwright浏览器
install_playwright() {
    print_step "Installing Playwright browsers... | 正在安装Playwright浏览器..."
    
    if $PYTHON_CMD -m playwright install chromium; then
        print_success "Playwright browsers installed | Playwright浏览器已安装"
    else
        print_warning "Playwright installation failed, but you can continue | Playwright安装失败，但您可以继续使用"
        
        # Try to install system dependencies
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            print_status "Installing Playwright system dependencies... | 正在安装Playwright系统依赖..."
            $PYTHON_CMD -m playwright install-deps chromium || true
        fi
    fi
}

# Function to setup configuration | 设置配置
setup_config() {
    print_step "Setting up configuration... | 正在设置配置..."
    
    if [ ! -f ".env" ]; then
        if [ -f "config.example.env" ]; then
            cp config.example.env .env
            print_success "Configuration template created as .env | 配置模板已创建为.env文件"
        else
            print_warning "No configuration template found | 未找到配置模板"
        fi
    else
        print_success "Configuration file already exists | 配置文件已存在"
    fi
    
    # Create necessary directories
    mkdir -p logs reports cache
    print_success "Directories created | 目录已创建"
}

# Function to create shortcuts and aliases | 创建快捷方式和别名
create_shortcuts() {
    print_step "Creating shortcuts and aliases... | 正在创建快捷方式和别名..."
    
    # Create desktop shortcut (Linux/macOS)
    DESKTOP="$HOME/Desktop"
    if [ -d "$DESKTOP" ]; then
        cat > "$DESKTOP/ManageBac-Checker.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ManageBac Assignment Checker
Comment=ManageBac作业检查器
Exec=$PYTHON_CMD $INSTALL_DIR/gui_launcher.py
Icon=$INSTALL_DIR/icon.png
Path=$INSTALL_DIR
Terminal=false
Categories=Education;
EOF
        chmod +x "$DESKTOP/ManageBac-Checker.desktop"
        print_success "Desktop shortcut created | 桌面快捷方式已创建"
    fi
    
    # Create command line aliases
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.profile" ]; then
        SHELL_RC="$HOME/.profile"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        # Check if alias already exists
        if ! grep -q "managebac" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# ManageBac Assignment Checker Aliases" >> "$SHELL_RC"
            echo "alias managebac='cd $INSTALL_DIR && $PYTHON_CMD gui_launcher.py'" >> "$SHELL_RC"
            echo "alias managebac-cli='cd $INSTALL_DIR && $PYTHON_CMD main_new.py'" >> "$SHELL_RC"
            print_success "Command line aliases created | 命令行别名已创建"
        else
            print_success "Command line aliases already exist | 命令行别名已存在"
        fi
    fi
    
    # Create launcher script
    cat > "$HOME/managebac" << EOF
#!/bin/bash
cd $INSTALL_DIR
$PYTHON_CMD gui_launcher.py
EOF
    chmod +x "$HOME/managebac"
    print_success "Launcher script created | 启动脚本已创建"
}

# Function to test installation | 测试安装
test_installation() {
    print_step "Testing installation... | 正在测试安装..."
    
    if $PYTHON_CMD -c "import managebac_checker; print('✅ ManageBac Checker module imported successfully')" 2>/dev/null; then
        print_success "Installation test passed | 安装测试通过"
        return 0
    else
        print_warning "Installation test failed, but you can still try running the application | 安装测试失败，但您仍可以尝试运行应用程序"
        return 1
    fi
}

# Function to show final instructions | 显示最终说明
show_final_instructions() {
    echo ""
    print_header "🎉 Installation Completed Successfully! | 安装成功完成！"
    echo "========================================================"
    echo ""
    print_info "📋 Next Steps | 下一步操作:"
    echo ""
    print_step "1. Configure your ManageBac credentials:"
    print_step "1. 配置您的ManageBac凭据："
    echo -e "   ${COMPUTER} nano $INSTALL_DIR/.env"
    echo ""
    print_step "2. Run the application:"
    print_step "2. 运行应用程序："
    echo -e "   ${COMPUTER} cd $INSTALL_DIR"
    echo -e "   ${COMPUTER} $PYTHON_CMD gui_launcher.py"
    echo ""
    print_step "3. Or use the shortcuts:"
    print_step "3. 或使用快捷方式："
    echo -e "   ${COMPUTER} managebac          # GUI mode | GUI模式"
    echo -e "   ${COMPUTER} managebac-cli      # CLI mode | 命令行模式"
    echo ""
    print_info "📚 Documentation | 文档:"
    echo -e "   ${COMPUTER} GitHub: $REPO_URL"
    echo -e "   ${COMPUTER} Help: $PYTHON_CMD main_new.py --help"
    echo ""
    print_info "🔧 Troubleshooting | 故障排除:"
    echo -e "   ${COMPUTER} If GUI doesn't work, try CLI mode | 如果GUI不工作，尝试命令行模式"
    echo -e "   ${COMPUTER} Check logs in: $INSTALL_DIR/logs/"
    echo ""
    print_header "Happy assignment tracking! | 愉快地追踪作业！"
    print_header "$HEART Made with love by Hacker0458 $HEART"
}

# Main installation process | 主安装过程
main() {
    # Show welcome message
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 ManageBac Assignment Checker            ║"
    echo "║                    🚀 ManageBac作业检查器                      ║"
    echo "║                                                              ║"
    echo "║              Ultimate One-Click Installer                    ║"
    echo "║              终极一键安装器                                   ║"
    echo "║                                                              ║"
    echo "║  $FIRE Professional-grade desktop application              ║"
    echo "║  $FIRE 专业级桌面应用程序                                   ║"
    echo "║                                                              ║"
    echo "║  $STAR AI-powered insights & analysis                      ║"
    echo "║  $STAR AI智能洞察和分析                                     ║"
    echo "║                                                              ║"
    echo "║  $HEART Made with love by Hacker0458                      ║"
    echo "║  $HEART 由Hacker0458用心制作                                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    
    # Check Python installation
    print_step "Checking Python installation... | 正在检查Python安装..."
    if command_exists python3; then
        PYTHON_VERSION=$(get_python_version)
        PYTHON_CMD="python3"
        print_success "Python $PYTHON_VERSION found"
    elif command_exists python; then
        PYTHON_VERSION=$(get_python_version)
        PYTHON_CMD="python"
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python not found! Installing system dependencies... | 未找到Python！正在安装系统依赖..."
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
    
    # Check pip installation
    print_step "Checking pip installation... | 正在检查pip安装..."
    if command_exists pip3; then
        PIP_CMD="pip3"
        print_success "pip3 found"
    elif command_exists pip; then
        PIP_CMD="pip"
        print_success "pip found"
    else
        print_error "pip not found! Installing system dependencies... | 未找到pip！正在安装系统依赖..."
        install_system_deps
        exit 1
    fi
    
    # Setup project
    setup_project
    
    # Create virtual environment (optional)
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
    
    # Show final instructions
    show_final_instructions
}

# Handle script arguments | 处理脚本参数
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [options]"
        echo "Options:"
        echo "  --venv, -v    Create virtual environment"
        echo "  --help, -h    Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0              # Basic installation"
        echo "  $0 --venv       # Installation with virtual environment"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
