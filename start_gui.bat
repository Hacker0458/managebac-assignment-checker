@echo off
REM ========================================
REM 🎓 ManageBac Assignment Checker GUI Launcher (Windows)
REM 🎓 ManageBac作业检查器GUI启动器 (Windows)
REM ========================================

echo.
echo ========================================
echo 🎓 ManageBac Assignment Checker GUI
echo 🎓 ManageBac作业检查器GUI
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Python found
    echo ✅ 找到Python
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Python3 found
        echo ✅ 找到Python3
        set PYTHON_CMD=python3
    ) else (
        echo ❌ Python not found! Please install Python 3.8+
        echo ❌ 未找到Python！请安装Python 3.8+
        echo.
        echo Please download Python from: https://python.org/downloads/
        echo 请从以下网址下载Python: https://python.org/downloads/
        pause
        exit /b 1
    )
)

REM Check if we're in the right directory
if not exist "managebac_checker" (
    echo ❌ Please run this script from the project root directory
    echo ❌ 请从项目根目录运行此脚本
    pause
    exit /b 1
)

REM Install dependencies if needed
echo.
echo 📦 Checking and installing dependencies...
echo 📦 检查并安装依赖...
%PYTHON_CMD% -m pip install -r requirements.txt

REM Launch GUI
echo.
echo 🚀 Starting GUI application...
echo 🚀 启动GUI应用程序...
%PYTHON_CMD% gui_launcher.py

echo.
echo 👋 Thank you for using ManageBac Assignment Checker!
echo 👋 感谢使用ManageBac作业检查器！
pause
