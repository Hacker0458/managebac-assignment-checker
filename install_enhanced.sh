#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker - Enhanced Install Script with Smart Setup
# 🚀 ManageBac作业检查器 - 增强版安装脚本（智能配置）
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
WIZARD="🧙‍♂️"

# Repository URLs
REPO_URL="https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main"

echo -e "${PURPLE}${ROCKET} ManageBac Assignment Checker - Smart Install${NC}"
echo -e "${PURPLE}${ROCKET} ManageBac作业检查器 - 智能安装${NC}"
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
    echo ""
    echo -e "${CYAN}📋 Installation guides | 安装指南:${NC}"
    echo "  • macOS: brew install python3"
    echo "  • Ubuntu: sudo apt install python3 python3-pip"
    echo "  • Windows: https://python.org/downloads"
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
plyer>=2.1.0
pytest>=8.4.2
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0
black>=24.4.0
flake8>=7.1.0
mypy>=1.10.0
bandit[toml]>=1.7.8
safety>=3.0.1
pip-audit>=2.7.0
radon>=6.0.0
xenon>=0.9.0
build>=1.2.1
twine>=5.1.1
check-manifest>=0.49
pre-commit>=3.7.0
EOF
    print_success "Fallback requirements.txt created"
fi

# Download essential files | 下载必要文件
print_status "Downloading project files... | 下载项目文件..."

# Download setup wizard
curl -sL "$REPO_URL/setup_wizard.py" -o setup_wizard.py && print_success "Setup wizard downloaded" || print_warning "Setup wizard download failed"

# Download configuration template
curl -sL "$REPO_URL/config.example.env" -o config.example.env && print_success "config.example.env downloaded" || print_warning "config.example.env download failed"

# Download main scripts
curl -sL "$REPO_URL/main_new.py" -o main_new.py && print_success "main_new.py downloaded" || print_warning "main_new.py download failed"
curl -sL "$REPO_URL/gui_launcher.py" -o gui_launcher.py && print_success "gui_launcher.py downloaded" || print_warning "gui_launcher.py download failed"
curl -sL "$REPO_URL/professional_gui.py" -o professional_gui.py && print_success "professional_gui.py downloaded" || print_warning "professional_gui.py download failed"

# Download additional useful files
curl -sL "$REPO_URL/create_shortcuts.py" -o create_shortcuts.py && print_success "Shortcut creator downloaded" || print_warning "Shortcut creator download failed"

# Create project structure | 创建项目结构
print_status "Creating project structure... | 创建项目结构..."
mkdir -p logs cache reports screenshots backups managebac_checker templates
print_success "Project structure created"

# Create managebac_checker package structure
mkdir -p managebac_checker
touch managebac_checker/__init__.py

# Download core package files if available
curl -sL "$REPO_URL/managebac_checker/__init__.py" -o managebac_checker/__init__.py 2>/dev/null || echo ""
curl -sL "$REPO_URL/managebac_checker/config.py" -o managebac_checker/config.py 2>/dev/null || echo ""
curl -sL "$REPO_URL/managebac_checker/scraper.py" -o managebac_checker/scraper.py 2>/dev/null || echo ""

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
        CORE_PACKAGES=("playwright>=1.45.0" "python-dotenv>=1.0.0" "jinja2>=3.1.4" "pillow>=10.0.0")
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
    print_warning "You can install manually later: python -m playwright install chromium"
    print_warning "您可以稍后手动安装：python -m playwright install chromium"
fi

# Create desktop shortcuts if available
if [ -f "create_shortcuts.py" ]; then
    print_status "Creating desktop shortcuts... | 创建桌面快捷方式..."
    $PYTHON_CMD create_shortcuts.py 2>/dev/null && print_success "Desktop shortcuts created" || print_warning "Shortcut creation skipped"
fi

echo ""
print_success "${ROCKET} Installation completed successfully!"
print_success "${ROCKET} 安装完成！"
echo "========================================================"

# Interactive Configuration Setup
echo ""
echo -e "${CYAN}${WIZARD} Smart Configuration Setup | 智能配置设置${NC}"
echo ""
echo "Now let's configure your ManageBac Assignment Checker!"
echo "现在让我们配置您的ManageBac作业检查器！"
echo ""

# Ask user if they want to run the setup wizard
echo "You have two options for configuration:"
echo "您有两种配置选项："
echo ""
echo -e "${GREEN}1. ${WIZARD} Smart Setup Wizard${NC} - Interactive configuration (recommended)"
echo "   智能配置向导 - 交互式配置（推荐）"
echo ""
echo -e "${BLUE}2. ⚙️  Manual Configuration${NC} - Edit .env file yourself"
echo "   手动配置 - 自己编辑.env文件"
echo ""

# Wait for user choice with timeout
read -t 30 -p "Choose option (1/2) or press Enter for Smart Setup [1]: " choice
choice=${choice:-1}

case $choice in
    1|"")
        echo ""
        echo -e "${CYAN}${WIZARD} Starting Smart Setup Wizard...${NC}"
        echo -e "${CYAN}${WIZARD} 启动智能配置向导...${NC}"
        echo ""

        if [ -f "setup_wizard.py" ]; then
            if $PYTHON_CMD setup_wizard.py; then
                print_success "Configuration completed successfully!"
                SETUP_COMPLETED=true
            else
                print_warning "Setup wizard failed, falling back to manual configuration"
                print_warning "配置向导失败，回退到手动配置"
                SETUP_COMPLETED=false
            fi
        else
            print_warning "Setup wizard not available, creating basic configuration"
            print_warning "配置向导不可用，创建基本配置"
            SETUP_COMPLETED=false
        fi
        ;;
    2)
        echo ""
        echo -e "${BLUE}⚙️  Manual Configuration Selected${NC}"
        echo -e "${BLUE}⚙️  已选择手动配置${NC}"
        SETUP_COMPLETED=false
        ;;
    *)
        print_warning "Invalid choice, using Smart Setup Wizard"
        print_warning "无效选择，使用智能配置向导"
        if [ -f "setup_wizard.py" ] && $PYTHON_CMD setup_wizard.py; then
            print_success "Configuration completed successfully!"
            SETUP_COMPLETED=true
        else
            SETUP_COMPLETED=false
        fi
        ;;
esac

# Manual configuration fallback
if [ "$SETUP_COMPLETED" != "true" ]; then
    echo ""
    print_status "Creating basic configuration file... | 创建基本配置文件..."

    if [ -f "config.example.env" ]; then
        cp config.example.env .env
        print_success "Configuration template created as .env"
        print_success "配置模板已创建为.env文件"

        echo ""
        echo -e "${YELLOW}📝 Please edit the .env file with your settings:${NC}"
        echo -e "${YELLOW}📝 请编辑.env文件并填入您的设置：${NC}"
        echo ""
        echo -e "  ${BLUE}🏫 MANAGEBAC_URL${NC}=https://yourschool.managebac.cn"
        echo -e "  ${BLUE}📧 MANAGEBAC_EMAIL${NC}=your.email@example.com"
        echo -e "  ${BLUE}🔑 MANAGEBAC_PASSWORD${NC}=your_password"
        echo ""
        echo "Required settings | 必需设置："
        echo "• Your school's ManageBac URL | 您学校的ManageBac网址"
        echo "• Your ManageBac login email | 您的ManageBac登录邮箱"
        echo "• Your ManageBac login password | 您的ManageBac登录密码"

    else
        print_status "Creating basic .env file... | 创建基本.env文件..."
        cat > .env << 'EOF'
# ManageBac Configuration | ManageBac配置
# Please fill in your information | 请填入您的信息

# Your school's ManageBac URL | 您学校的ManageBac网址
# Example: https://shtcs.managebac.cn
MANAGEBAC_URL=https://your-school.managebac.cn

# Your ManageBac login credentials | 您的ManageBac登录凭据
MANAGEBAC_EMAIL=your.email@example.com
MANAGEBAC_PASSWORD=your_password

# Basic settings | 基本设置
HEADLESS=true
DEBUG=false
REPORT_FORMAT=html,json,console
OUTPUT_DIR=reports
LANGUAGE=zh
AI_ENABLED=false

# Advanced AI settings (optional) | 高级AI设置（可选）
# OPENAI_API_KEY=your_openai_api_key
# AI_MODEL=gpt-3.5-turbo

# Email notifications (optional) | 邮件通知（可选）
ENABLE_EMAIL_NOTIFICATIONS=false
# SMTP_SERVER=smtp.gmail.com
# SMTP_USERNAME=your.email@gmail.com
# SMTP_PASSWORD=your_app_password
EOF
        print_success "Basic .env file created"
    fi
fi

# Final success message and next steps
echo ""
print_success "${ROCKET} Setup completed successfully!"
print_success "${ROCKET} 设置完成！"
echo "========================================================"
echo ""
echo -e "${CYAN}${BOOK} What's Next | 下一步操作:${NC}"
echo ""

if [ "$SETUP_COMPLETED" = "true" ]; then
    echo -e "${GREEN}${CHECK} Your ManageBac Assignment Checker is fully configured and ready to use!${NC}"
    echo -e "${GREEN}${CHECK} 您的ManageBac作业检查器已完全配置并准备使用！${NC}"
    echo ""
else
    echo -e "${YELLOW}1.${NC} Complete configuration | 完成配置:"
    echo -e "   ${COMPUTER} Edit the .env file with your ManageBac credentials"
    echo -e "   ${COMPUTER} 编辑.env文件，填入您的ManageBac凭据"
    echo -e "   ${COMPUTER} Or run: $PYTHON_CMD setup_wizard.py"
    echo ""
fi

echo -e "${BLUE}2.${NC} Run the application | 运行应用程序:"
if [ -f "gui_launcher.py" ]; then
    echo -e "   ${COMPUTER} GUI Mode: $PYTHON_CMD gui_launcher.py  ${GREEN}(Recommended | 推荐)${NC}"
fi
if [ -f "main_new.py" ]; then
    echo -e "   ${COMPUTER} CLI Mode: $PYTHON_CMD main_new.py"
fi
echo -e "   ${COMPUTER} Interactive: $PYTHON_CMD main_new.py --interactive"
echo ""

echo -e "${BLUE}3.${NC} Test your setup | 测试设置:"
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --test-config"
echo ""

echo -e "${BLUE}4.${NC} Generate reports | 生成报告:"
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --format html"
echo -e "   ${COMPUTER} Open reports/assignment_report.html"
echo ""

echo -e "${CYAN}${BOOK} Helpful Resources | 有用资源:${NC}"
echo -e "   ${COMPUTER} Configuration help: $PYTHON_CMD setup_wizard.py"
echo -e "   ${COMPUTER} Command help: $PYTHON_CMD main_new.py --help"
echo -e "   ${COMPUTER} Logs location: logs/managebac_checker.log"
echo ""

echo -e "${PURPLE}${ROCKET} Happy assignment tracking! | 愉快地追踪作业！${NC}"
echo ""

# Show installation path
echo -e "${CYAN}Installation path | 安装路径: $(pwd)${NC}"

# Create quick start script
cat > quick_start.sh << 'EOF'
#!/bin/bash
# Quick Start Script for ManageBac Assignment Checker
echo "🚀 Starting ManageBac Assignment Checker..."
if [ -f "gui_launcher.py" ]; then
    python3 gui_launcher.py
elif [ -f "main_new.py" ]; then
    python3 main_new.py --interactive
else
    echo "❌ Application files not found!"
fi
EOF
chmod +x quick_start.sh

echo -e "${GREEN}${CHECK} Quick start script created: ./quick_start.sh${NC}"
echo ""