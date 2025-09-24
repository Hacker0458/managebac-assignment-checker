#!/bin/bash
# ========================================
# 🚀 ManageBac Assignment Checker Quick Install
# 🚀 ManageBac作业检查器快速安装
# ========================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 ManageBac Assignment Checker Quick Install${NC}"
echo -e "${BLUE}🚀 ManageBac作业检查器快速安装${NC}"
echo "========================================================"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Python3 found${NC}"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo -e "${GREEN}✅ Python found${NC}"
else
    echo -e "${RED}❌ Python not found! Please install Python 3.8+ first.${NC}"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${RED}❌ pip not found! Please install pip first.${NC}"
    exit 1
fi

# Create project directory
PROJECT_DIR="$HOME/managebac-assignment-checker"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo -e "${BLUE}📦 Downloading project files...${NC}"

# Download main files
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements-core.txt" -o requirements-core.txt
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt" -o requirements.txt
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/config.example.env" -o config.example.env
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/gui_launcher.py" -o gui_launcher.py
curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/main_new.py" -o main_new.py

# Download package files
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

echo -e "${GREEN}✅ Project files downloaded${NC}"

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
$PIP_CMD install --upgrade pip

# Install core dependencies
if [ -f "requirements-core.txt" ]; then
    $PIP_CMD install -r requirements-core.txt
else
    $PIP_CMD install playwright python-dotenv jinja2 openai pystray pillow
fi

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Install Playwright browsers
echo -e "${BLUE}🌐 Installing Playwright browsers...${NC}"
if $PYTHON_CMD -m playwright install chromium; then
    echo -e "${GREEN}✅ Playwright browsers installed${NC}"
else
    echo -e "${YELLOW}⚠️ Playwright installation failed, but you can continue${NC}"
fi

# Create config
if [ ! -f ".env" ]; then
    if [ -f "config.example.env" ]; then
        cp config.example.env .env
        echo -e "${GREEN}✅ Configuration file created${NC}"
    fi
fi

# Create directories
mkdir -p logs reports cache

echo ""
echo -e "${GREEN}🚀 Installation completed successfully!${NC}"
echo -e "${GREEN}🚀 安装完成！${NC}"
echo "========================================================"
echo ""
echo -e "${YELLOW}Next Steps | 下一步操作:${NC}"
echo ""
echo -e "${YELLOW}1. ${NC}Edit .env file with your ManageBac credentials:"
echo -e "${YELLOW}1. ${NC}编辑.env文件，填入您的ManageBac凭据："
echo -e "   ${BLUE}nano .env${NC}"
echo ""
echo -e "${YELLOW}2. ${NC}Run the application:"
echo -e "${YELLOW}2. ${NC}运行应用程序："
echo -e "   ${BLUE}$PYTHON_CMD gui_launcher.py${NC}"
echo ""
echo -e "${YELLOW}3. ${NC}Or use command line mode:"
echo -e "${YELLOW}3. ${NC}或使用命令行模式："
echo -e "   ${BLUE}$PYTHON_CMD main_new.py${NC}"
echo ""
echo -e "${BLUE}💻 Happy assignment tracking! | 愉快地追踪作业！${NC}"
