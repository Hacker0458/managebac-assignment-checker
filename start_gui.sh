#!/bin/bash
# ========================================
# 🎓 ManageBac Assignment Checker GUI Launcher (Linux/macOS)
# 🎓 ManageBac作业检查器GUI启动器 (Linux/macOS)
# ========================================

set -e  # Exit on any error

# Colors for output
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

echo -e "${PURPLE}========================================"
echo -e "${ROCKET} ManageBac Assignment Checker GUI"
echo -e "${ROCKET} ManageBac作业检查器GUI"
echo -e "========================================${NC}"
echo ""

# Check if Python is installed
echo -e "${BLUE}${GEAR} Checking Python installation...${NC}"
echo -e "${BLUE}${GEAR} 检查Python安装...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}${CHECK} Python found: $PYTHON_VERSION${NC}"
    echo -e "${GREEN}${CHECK} 找到Python: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}${CHECK} Python found: $PYTHON_VERSION${NC}"
    echo -e "${GREEN}${CHECK} 找到Python: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}${CROSS} Python not found! Please install Python 3.8+${NC}"
    echo -e "${RED}${CROSS} 未找到Python！请安装Python 3.8+${NC}"
    echo ""
    echo -e "${YELLOW}Please install Python from: https://python.org/downloads/${NC}"
    echo -e "${YELLOW}请从以下网址安装Python: https://python.org/downloads/${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -d "managebac_checker" ]; then
    echo -e "${RED}${CROSS} Please run this script from the project root directory${NC}"
    echo -e "${RED}${CROSS} 请从项目根目录运行此脚本${NC}"
    exit 1
fi

# Check if pip is available
echo -e "${BLUE}${GEAR} Checking pip installation...${NC}"
echo -e "${BLUE}${GEAR} 检查pip安装...${NC}"

if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}${CROSS} pip not found! Please install pip${NC}"
    echo -e "${RED}${CROSS} 未找到pip！请安装pip${NC}"
    exit 1
fi

echo -e "${GREEN}${CHECK} pip is available${NC}"
echo -e "${GREEN}${CHECK} pip可用${NC}"

# Install dependencies
echo ""
echo -e "${BLUE}📦 Installing dependencies...${NC}"
echo -e "${BLUE}📦 安装依赖...${NC}"

$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}${CHECK} Dependencies installed successfully${NC}"
    echo -e "${GREEN}${CHECK} 依赖安装成功${NC}"
else
    echo -e "${RED}${CROSS} Failed to install dependencies${NC}"
    echo -e "${RED}${CROSS} 依赖安装失败${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo -e "${BLUE}${GEAR} Setting up environment...${NC}"
echo -e "${BLUE}${GEAR} 设置环境...${NC}"

mkdir -p logs reports

# Copy config template if needed
if [ ! -f ".env" ] && [ -f "config.example.env" ]; then
    cp config.example.env .env
    echo -e "${GREEN}${CHECK} Created .env file from template${NC}"
    echo -e "${GREEN}${CHECK} 从模板创建了.env文件${NC}"
fi

# Launch GUI
echo ""
echo -e "${PURPLE}${ROCKET} Starting GUI application...${NC}"
echo -e "${PURPLE}${ROCKET} 启动GUI应用程序...${NC}"
echo ""

$PYTHON_CMD gui_launcher.py

# Exit message
echo ""
echo -e "${GREEN}👋 Thank you for using ManageBac Assignment Checker!${NC}"
echo -e "${GREEN}👋 感谢使用ManageBac作业检查器！${NC}"
