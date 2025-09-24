#!/bin/bash
# ========================================
# 🧪 Test Install Script for ManageBac Assignment Checker
# 🧪 ManageBac作业检查器安装脚本测试
# ========================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing ManageBac Assignment Checker Installation${NC}"
echo -e "${BLUE}🧪 测试ManageBac作业检查器安装${NC}"
echo "========================================================"

# Test 1: Check if quick_install.sh exists and is executable
echo -e "${YELLOW}Test 1: Checking quick_install.sh${NC}"
if [ -f "quick_install.sh" ]; then
    echo -e "${GREEN}✅ quick_install.sh exists${NC}"
    if [ -x "quick_install.sh" ]; then
        echo -e "${GREEN}✅ quick_install.sh is executable${NC}"
    else
        echo -e "${YELLOW}⚠️ Making quick_install.sh executable${NC}"
        chmod +x quick_install.sh
    fi
else
    echo -e "${RED}❌ quick_install.sh not found${NC}"
    exit 1
fi

# Test 2: Check if install.sh exists and is executable
echo -e "${YELLOW}Test 2: Checking install.sh${NC}"
if [ -f "install.sh" ]; then
    echo -e "${GREEN}✅ install.sh exists${NC}"
    if [ -x "install.sh" ]; then
        echo -e "${GREEN}✅ install.sh is executable${NC}"
    else
        echo -e "${YELLOW}⚠️ Making install.sh executable${NC}"
        chmod +x install.sh
    fi
else
    echo -e "${RED}❌ install.sh not found${NC}"
    exit 1
fi

# Test 3: Check if install_github.sh exists and is executable
echo -e "${YELLOW}Test 3: Checking install_github.sh${NC}"
if [ -f "install_github.sh" ]; then
    echo -e "${GREEN}✅ install_github.sh exists${NC}"
    if [ -x "install_github.sh" ]; then
        echo -e "${GREEN}✅ install_github.sh is executable${NC}"
    else
        echo -e "${YELLOW}⚠️ Making install_github.sh executable${NC}"
        chmod +x install_github.sh
    fi
else
    echo -e "${RED}❌ install_github.sh not found${NC}"
    exit 1
fi

# Test 4: Check if required files exist
echo -e "${YELLOW}Test 4: Checking required files${NC}"
REQUIRED_FILES=(
    "requirements-core.txt"
    "requirements.txt"
    "config.example.env"
    "gui_launcher.py"
    "main_new.py"
    "managebac_checker/__init__.py"
    "managebac_checker/config.py"
    "managebac_checker/checker.py"
    "managebac_checker/professional_gui.py"
    "managebac_checker/gui.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
    else
        echo -e "${RED}❌ $file not found${NC}"
    fi
done

# Test 5: Check Python syntax
echo -e "${YELLOW}Test 5: Checking Python syntax${NC}"
PYTHON_FILES=(
    "gui_launcher.py"
    "main_new.py"
    "managebac_checker/__init__.py"
    "managebac_checker/config.py"
    "managebac_checker/checker.py"
    "managebac_checker/professional_gui.py"
    "managebac_checker/gui.py"
)

for file in "${PYTHON_FILES[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo -e "${GREEN}✅ $file syntax OK${NC}"
        else
            echo -e "${RED}❌ $file syntax error${NC}"
        fi
    fi
done

# Test 6: Check if curl can download files
echo -e "${YELLOW}Test 6: Testing curl download${NC}"
if command -v curl &> /dev/null; then
    echo -e "${GREEN}✅ curl is available${NC}"
    
    # Test downloading a small file
    if curl -s -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements-core.txt" -o /tmp/test_download.txt; then
        echo -e "${GREEN}✅ curl download test passed${NC}"
        rm -f /tmp/test_download.txt
    else
        echo -e "${RED}❌ curl download test failed${NC}"
    fi
else
    echo -e "${RED}❌ curl not found${NC}"
fi

# Test 7: Check if wget is available as fallback
echo -e "${YELLOW}Test 7: Checking wget availability${NC}"
if command -v wget &> /dev/null; then
    echo -e "${GREEN}✅ wget is available${NC}"
else
    echo -e "${YELLOW}⚠️ wget not found (curl is preferred)${NC}"
fi

# Test 8: Check if unzip is available
echo -e "${YELLOW}Test 8: Checking unzip availability${NC}"
if command -v unzip &> /dev/null; then
    echo -e "${GREEN}✅ unzip is available${NC}"
else
    echo -e "${YELLOW}⚠️ unzip not found (needed for GitHub installer)${NC}"
fi

# Test 9: Check Python version
echo -e "${YELLOW}Test 9: Checking Python version${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
    
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        echo -e "${GREEN}✅ Python version is compatible (3.8+)${NC}"
    else
        echo -e "${RED}❌ Python version is too old (need 3.8+)${NC}"
    fi
else
    echo -e "${RED}❌ Python3 not found${NC}"
fi

# Test 10: Check pip availability
echo -e "${YELLOW}Test 10: Checking pip availability${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 is available${NC}"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}✅ pip is available${NC}"
else
    echo -e "${RED}❌ pip not found${NC}"
fi

echo ""
echo -e "${GREEN}🧪 Installation test completed!${NC}"
echo -e "${GREEN}🧪 安装测试完成！${NC}"
echo "========================================================"
echo ""
echo -e "${BLUE}📋 Test Summary:${NC}"
echo -e "${BLUE}📋 测试摘要:${NC}"
echo ""
echo -e "${YELLOW}To test the installation scripts:${NC}"
echo -e "${YELLOW}测试安装脚本:${NC}"
echo ""
echo -e "${BLUE}1. Test quick install:${NC}"
echo -e "   ${BLUE}curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/quick_install.sh | bash${NC}"
echo ""
echo -e "${BLUE}2. Test full install:${NC}"
echo -e "   ${BLUE}curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh | bash${NC}"
echo ""
echo -e "${BLUE}3. Test GitHub install:${NC}"
echo -e "   ${BLUE}curl -L https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_github.sh | bash${NC}"
echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"
