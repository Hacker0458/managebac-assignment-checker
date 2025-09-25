@echo off
chcp 65001 > nul
title ManageBac Assignment Checker - 一键启动

echo.
echo ========================================
echo 🎯 ManageBac Assignment Checker
echo 🎯 ManageBac作业检查器
echo ========================================
echo.
echo 🚀 正在启动应用程序...
echo 🚀 Starting application...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Try Python 3 first, then Python
python3 one_click_run.py 2>nul
if errorlevel 1 (
    python one_click_run.py 2>nul
    if errorlevel 1 (
        echo.
        echo ❌ 未找到Python，请安装Python 3.8+
        echo ❌ Python not found, please install Python 3.8+
        echo.
        echo 📥 下载地址: https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
)

echo.
pause