#!/bin/bash
# ManageBac Assignment Checker - 一键启动脚本

# Set UTF-8 encoding
export LC_ALL=en_US.UTF-8 2>/dev/null || export LC_ALL=C.UTF-8 2>/dev/null || true

clear
echo ""
echo "========================================"
echo "🎯 ManageBac Assignment Checker"
echo "🎯 ManageBac作业检查器"
echo "========================================"
echo ""
echo "🚀 正在启动应用程序..."
echo "🚀 Starting application..."
echo ""

# Change to script directory
cd "$(dirname "$0")" || exit 1

# Find Python executable
PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &> /dev/null; then
        # Check if it's Python 3
        if "$cmd" --version 2>&1 | grep -q "Python 3"; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo "❌ 未找到Python 3，请安装Python 3.8+"
    echo "❌ Python 3 not found, please install Python 3.8+"
    echo ""
    echo "📥 安装方法："
    echo "   macOS: brew install python3"
    echo "   Ubuntu/Debian: sudo apt-get install python3"
    echo "   CentOS/RHEL: sudo yum install python3"
    echo ""
    echo "或访问官网: https://www.python.org/downloads/"
    echo ""
    read -p "按回车键退出... Press Enter to exit..." -r
    exit 1
fi

# Run the application
"$PYTHON_CMD" one_click_run.py

# Keep terminal open
echo ""
read -p "按回车键退出... Press Enter to exit..." -r