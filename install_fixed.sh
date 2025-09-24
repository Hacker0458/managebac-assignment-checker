#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker - Fixed Install Script
# 🚀 ManageBac作业检查器 - 修复版安装脚本
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
DOWNLOAD="📥"

# Repository URLs
REPO_URL="https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main"

echo -e "${PURPLE}${ROCKET} ManageBac Assignment Checker - Fixed Install${NC}"
echo -e "${PURPLE}${ROCKET} ManageBac作业检查器 - 修复版安装${NC}"
echo "========================================================"

# Function to print status messages
print_status() { echo -e "${BLUE}${GEAR} $1${NC}"; }
print_success() { echo -e "${GREEN}${CHECK} $1${NC}"; }
print_error() { echo -e "${RED}${CROSS} $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Check if Python is installed | 检查Python是否已安装
print_status "Checking Python installation... | 检查Python安装..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_VERSION=$(python --version)
    print_success "Python found: $PYTHON_VERSION"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_error "Python 3 not found! Please install Python 3.9+ first."
    print_error "未找到Python 3！请先安装Python 3.9+。"
    exit 1
fi

# Check if curl is available | 检查curl是否可用
if ! command -v curl &> /dev/null; then
    print_error "curl not found! Please install curl first."
    print_error "未找到curl！请先安装curl。"
    exit 1
fi

# Create project directory | 创建项目目录
PROJECT_DIR="managebac-assignment-checker"
print_status "Creating project directory... | 创建项目目录..."
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
print_success "Project directory created: $PROJECT_DIR"

# Download requirements.txt file | 下载requirements.txt文件
print_status "Downloading requirements.txt... | 下载requirements.txt..."
if curl -sL "$REPO_URL/requirements.txt" -o requirements.txt && [ -s requirements.txt ]; then
    print_success "requirements.txt downloaded successfully"
else
    print_warning "Failed to download requirements.txt, creating fallback version"
    print_warning "requirements.txt下载失败，创建后备版本"
    cat > requirements.txt << 'EOF'
# ManageBac Assignment Checker - Core Dependencies
playwright>=1.45.0
python-dotenv>=1.0.0
jinja2>=3.1.4
openai>=1.0.0
pystray>=0.19.0
pillow>=10.0.0
pytest>=8.4.2
pytest-asyncio>=0.23.0
black>=24.4.0
flake8>=7.1.0
mypy>=1.10.0
EOF
    print_success "Fallback requirements.txt created"
fi

# Download other essential files | 下载其他必要文件
print_status "Downloading configuration files... | 下载配置文件..."
curl -sL "$REPO_URL/config.example.env" -o config.example.env && print_success "config.example.env downloaded" || print_warning "config.example.env download failed"

print_status "Downloading main scripts... | 下载主要脚本..."
curl -sL "$REPO_URL/main_new.py" -o main_new.py && print_success "main_new.py downloaded" || print_warning "main_new.py download failed"
curl -sL "$REPO_URL/gui_launcher.py" -o gui_launcher.py && print_success "gui_launcher.py downloaded" || print_warning "gui_launcher.py download failed"

# Create project structure | 创建项目结构
print_status "Creating project structure... | 创建项目结构..."
mkdir -p logs cache reports managebac_checker
print_success "Project structure created"

# Upgrade pip first | 先升级pip
print_status "Upgrading pip... | 升级pip..."
$PIP_CMD install --upgrade pip

# Install dependencies | 安装依赖
print_status "Installing dependencies... | 正在安装依赖..."
if [ -f "requirements.txt" ] && [ -s "requirements.txt" ]; then
    if $PIP_CMD install -r requirements.txt; then
        print_success "Dependencies installed successfully!"
        print_success "依赖安装成功！"
    else
        print_warning "Some dependencies failed, trying individual installation..."
        print_warning "部分依赖安装失败，尝试单独安装..."

        # Install core packages individually
        CORE_PACKAGES=("playwright>=1.45.0" "python-dotenv>=1.0.0" "jinja2>=3.1.4")
        for package in "${CORE_PACKAGES[@]}"; do
            if $PIP_CMD install "$package"; then
                print_success "Installed: $package"
            else
                print_warning "Failed to install: $package"
            fi
        done
    fi
else
    print_error "requirements.txt not found or empty!"
    exit 1
fi

# Install Playwright browsers | 安装Playwright浏览器
print_status "Installing Playwright browsers... | 正在安装Playwright浏览器..."
if $PYTHON_CMD -m playwright install chromium; then
    print_success "Playwright browsers installed successfully!"
    print_success "Playwright浏览器安装成功！"
else
    print_warning "Playwright browser installation failed, but you can continue."
    print_warning "Playwright浏览器安装失败，但您可以继续使用。"
fi

# Create config if not exists | 如果配置不存在则创建
if [ ! -f ".env" ]; then
    if [ -f "config.example.env" ]; then
        print_status "Creating configuration file... | 正在创建配置文件..."
        cp config.example.env .env
        print_success "Configuration template created as .env"
        print_success "配置模板已创建为.env文件"
    else
        print_status "Creating basic .env file... | 创建基本.env文件..."
        cat > .env << 'EOF'
# ManageBac Configuration
MANAGEBAC_EMAIL=your_email@school.edu
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://your_school.managebac.com
HEADLESS=true
DEBUG=false
REPORT_FORMAT=console,json
OUTPUT_DIR=./reports
ENABLE_NOTIFICATIONS=false
EOF
        print_success "Basic .env file created"
    fi
fi

# Final success message
echo ""
print_success "${ROCKET} Installation completed successfully!"
print_success "${ROCKET} 安装完成！"
echo "========================================================"
echo ""
echo -e "${CYAN}${BOOK} Next Steps | 下一步操作:${NC}"
echo ""
echo -e "${YELLOW}1.${NC} Edit .env file with your ManageBac credentials"
echo -e "${YELLOW}1.${NC} 编辑.env文件，填入您的ManageBac凭据"
echo ""
echo -e "${YELLOW}2.${NC} Run the program:"
echo -e "${YELLOW}2.${NC} 运行程序："
if [ -f "gui_launcher.py" ]; then
    echo -e "   ${COMPUTER} $PYTHON_CMD gui_launcher.py  ${GREEN}(GUI界面)${NC}"
fi
if [ -f "main_new.py" ]; then
    echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py     ${BLUE}(命令行)${NC}"
fi
echo ""
echo -e "${YELLOW}3.${NC} For interactive mode:"
echo -e "${YELLOW}3.${NC} 交互模式："
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --interactive"
echo ""
echo -e "${CYAN}${BOOK} For help | 获取帮助:${NC}"
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --help"
echo ""
echo -e "${PURPLE}${ROCKET} Happy assignment tracking! | 愉快地追踪作业！${NC}"
echo ""

# Show installation path
echo -e "${CYAN}Installation path | 安装路径: $(pwd)${NC}"