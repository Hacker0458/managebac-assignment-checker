#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker GitHub Installer
# 🚀 ManageBac作业检查器GitHub安装器
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

# Configuration
REPO_URL="https://github.com/Hacker0458/managebac-assignment-checker"
INSTALL_DIR="managebac-assignment-checker"
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

# Function to check if command exists | 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version | 检查Python版本
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    elif command_exists python; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    else
        print_error "Python not found! Please install Python 3.8+ first."
        print_error "未找到Python！请先安装Python 3.8+。"
        exit 1
    fi
    
    # Check version
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        print_error "Python 3.8+ is required, but found $PYTHON_VERSION"
        print_error "需要Python 3.8+，但找到的是$PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION found"
}

# Function to check pip | 检查pip
check_pip() {
    if command_exists pip3; then
        PIP_CMD="pip3"
    elif command_exists pip; then
        PIP_CMD="pip"
    else
        print_error "pip not found! Please install pip first."
        print_error "未找到pip！请先安装pip。"
        exit 1
    fi
    
    print_success "pip found"
}

# Function to download and extract project | 下载并解压项目
download_project() {
    print_status "Downloading ManageBac Assignment Checker... | 正在下载ManageBac作业检查器..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Download as zip
    print_status "Downloading from GitHub... | 正在从GitHub下载..."
    if command_exists curl; then
        curl -L "$REPO_URL/archive/$BRANCH.zip" -o project.zip
    elif command_exists wget; then
        wget "$REPO_URL/archive/$BRANCH.zip" -O project.zip
    else
        print_error "Neither curl nor wget found. Please install one of them."
        print_error "未找到curl或wget。请安装其中一个。"
        exit 1
    fi
    
    # Extract zip
    if command_exists unzip; then
        unzip -q project.zip
    else
        print_error "unzip not found. Please install unzip."
        print_error "未找到unzip。请安装unzip。"
        exit 1
    fi
    
    # Move to final location
    EXTRACTED_DIR=$(ls -d */ | head -n1)
    if [ -d "$HOME/$INSTALL_DIR" ]; then
        print_warning "Directory $HOME/$INSTALL_DIR already exists. Removing..."
        print_warning "目录$HOME/$INSTALL_DIR已存在。正在删除..."
        rm -rf "$HOME/$INSTALL_DIR"
    fi
    
    mv "$EXTRACTED_DIR" "$HOME/$INSTALL_DIR"
    cd "$HOME/$INSTALL_DIR"
    
    print_success "Project downloaded to $HOME/$INSTALL_DIR"
    print_success "项目已下载到$HOME/$INSTALL_DIR"
}

# Function to install dependencies | 安装依赖
install_dependencies() {
    print_status "Installing dependencies... | 正在安装依赖..."
    
    # Upgrade pip
    $PIP_CMD install --upgrade pip
    
    # Install dependencies
    if [ -f "requirements-core.txt" ]; then
        $PIP_CMD install -r requirements-core.txt
    elif [ -f "requirements.txt" ]; then
        $PIP_CMD install -r requirements.txt
    else
        # Fallback: install essential packages
        $PIP_CMD install playwright python-dotenv jinja2 openai pystray pillow
    fi
    
    print_success "Dependencies installed | 依赖已安装"
}

# Function to install Playwright | 安装Playwright
install_playwright() {
    print_status "Installing Playwright browsers... | 正在安装Playwright浏览器..."
    
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

# Function to create shortcuts | 创建快捷方式
create_shortcuts() {
    print_status "Creating shortcuts... | 正在创建快捷方式..."
    
    # Create desktop shortcut
    DESKTOP="$HOME/Desktop"
    if [ -d "$DESKTOP" ]; then
        cat > "$DESKTOP/ManageBac-Checker.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=ManageBac Assignment Checker
Comment=ManageBac作业检查器
Exec=$PYTHON_CMD $HOME/$INSTALL_DIR/gui_launcher.py
Icon=$HOME/$INSTALL_DIR/icon.png
Path=$HOME/$INSTALL_DIR
Terminal=false
Categories=Education;
EOF
        chmod +x "$DESKTOP/ManageBac-Checker.desktop"
        print_success "Desktop shortcut created | 桌面快捷方式已创建"
    fi
    
    # Create command line alias
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        echo "" >> "$SHELL_RC"
        echo "# ManageBac Assignment Checker" >> "$SHELL_RC"
        echo "alias managebac='cd $HOME/$INSTALL_DIR && $PYTHON_CMD gui_launcher.py'" >> "$SHELL_RC"
        print_success "Command line alias created | 命令行别名已创建"
        print_status "Run 'source $SHELL_RC' to activate the alias | 运行'source $SHELL_RC'以激活别名"
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

# Main installation process | 主安装过程
main() {
    print_header "ManageBac Assignment Checker GitHub Installer"
    print_header "ManageBac作业检查器GitHub安装器"
    echo "========================================================"
    
    # Check prerequisites
    check_python
    check_pip
    
    # Download project
    download_project
    
    # Install dependencies
    install_dependencies
    
    # Install Playwright
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
    echo -e "${YELLOW}1. ${NC}Navigate to the installation directory:"
    echo -e "${YELLOW}1. ${NC}导航到安装目录："
    echo -e "   ${COMPUTER} cd $HOME/$INSTALL_DIR"
    echo ""
    echo -e "${YELLOW}2. ${NC}Edit .env file with your ManageBac credentials:"
    echo -e "${YELLOW}2. ${NC}编辑.env文件，填入您的ManageBac凭据："
    echo -e "   ${COMPUTER} nano .env"
    echo ""
    echo -e "${YELLOW}3. ${NC}Run the application:"
    echo -e "${YELLOW}3. ${NC}运行应用程序："
    echo -e "   ${COMPUTER} $PYTHON_CMD gui_launcher.py"
    echo ""
    echo -e "${YELLOW}4. ${NC}Or use the command line alias (after restarting terminal):"
    echo -e "${YELLOW}4. ${NC}或使用命令行别名（重启终端后）："
    echo -e "   ${COMPUTER} managebac"
    echo ""
    print_header "For help | 获取帮助:"
    echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --help"
    echo ""
    print_header "Happy assignment tracking! | 愉快地追踪作业！"
}

# Run main function
main "$@"
