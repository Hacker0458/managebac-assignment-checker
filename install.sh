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

echo -e "${PURPLE}${ROCKET} ManageBac Assignment Checker Quick Install${NC}"
echo -e "${PURPLE}${ROCKET} ManageBac作业检查器快速安装${NC}"
echo "========================================================"

# Check if Python is installed | 检查Python是否已安装
echo -e "${BLUE}${GEAR} Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}${CHECK} Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}${CHECK} Python found: $PYTHON_VERSION${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}${CROSS} Python not found! Please install Python 3.8+ first.${NC}"
    echo -e "${RED}${CROSS} 未找到Python！请先安装Python 3.8+。${NC}"
    exit 1
fi

# Check if pip is installed | 检查pip是否已安装
echo -e "${BLUE}${GEAR} Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}${CHECK} pip3 found${NC}"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}${CHECK} pip found${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}${CROSS} pip not found! Please install pip first.${NC}"
    echo -e "${RED}${CROSS} 未找到pip！请先安装pip。${NC}"
    exit 1
fi

# Install dependencies | 安装依赖
echo -e "${BLUE}${GEAR} Installing dependencies...${NC}"
echo -e "${BLUE}${GEAR} 正在安装依赖...${NC}"

if $PIP_CMD install -r requirements.txt; then
    echo -e "${GREEN}${CHECK} Dependencies installed successfully!${NC}"
    echo -e "${GREEN}${CHECK} 依赖安装成功！${NC}"
else
    echo -e "${RED}${CROSS} Failed to install dependencies!${NC}"
    echo -e "${RED}${CROSS} 依赖安装失败！${NC}"
    exit 1
fi

# Install Playwright browsers | 安装Playwright浏览器
echo -e "${BLUE}${GEAR} Installing Playwright browsers...${NC}"
echo -e "${BLUE}${GEAR} 正在安装Playwright浏览器...${NC}"

if $PYTHON_CMD -m playwright install chromium; then
    echo -e "${GREEN}${CHECK} Playwright browsers installed successfully!${NC}"
    echo -e "${GREEN}${CHECK} Playwright浏览器安装成功！${NC}"
else
    echo -e "${YELLOW}⚠️ Playwright browser installation failed, but you can continue.${NC}"
    echo -e "${YELLOW}⚠️ Playwright浏览器安装失败，但您可以继续使用。${NC}"
fi

# Create config if not exists | 如果配置不存在则创建
if [ ! -f ".env" ]; then
    if [ -f "config.example.env" ]; then
        echo -e "${BLUE}${GEAR} Creating configuration file...${NC}"
        echo -e "${BLUE}${GEAR} 正在创建配置文件...${NC}"
        cp config.example.env .env
        echo -e "${GREEN}${CHECK} Configuration template created as .env${NC}"
        echo -e "${GREEN}${CHECK} 配置模板已创建为.env文件${NC}"
    fi
fi

echo ""
echo -e "${GREEN}${ROCKET} Installation completed successfully!${NC}"
echo -e "${GREEN}${ROCKET} 安装完成！${NC}"
echo "========================================================"
echo ""
echo -e "${CYAN}${BOOK} Next Steps | 下一步操作:${NC}"
echo ""
echo -e "${YELLOW}1. ${NC}Edit .env file with your ManageBac credentials"
echo -e "${YELLOW}1. ${NC}编辑.env文件，填入您的ManageBac凭据"
echo ""
echo -e "${YELLOW}2. ${NC}Run the program:"
echo -e "${YELLOW}2. ${NC}运行程序："
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py"
echo ""
echo -e "${YELLOW}3. ${NC}Or use interactive mode:"
echo -e "${YELLOW}3. ${NC}或使用交互模式："
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --interactive"
echo ""
echo -e "${CYAN}${BOOK} For help | 获取帮助:${NC}"
echo -e "   ${COMPUTER} $PYTHON_CMD main_new.py --help"
echo ""
echo -e "${PURPLE}${ROCKET} Happy assignment tracking! | 愉快地追踪作业！${NC}"
