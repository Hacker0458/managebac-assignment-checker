@echo off
REM ========================================
REM 🚀 ManageBac Assignment Checker Quick Install Script (Windows)
REM 🚀 ManageBac作业检查器快速安装脚本 (Windows)
REM ========================================

echo 🚀 ManageBac Assignment Checker Quick Install
echo 🚀 ManageBac作业检查器快速安装
echo ========================================================

REM Check if Python is installed | 检查Python是否已安装
echo ⚙️ Checking Python installation...
echo ⚙️ 检查Python安装...

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
        echo ❌ Python not found! Please install Python 3.8+ first.
        echo ❌ 未找到Python！请先安装Python 3.8+。
        pause
        exit /b 1
    )
)

REM Check if pip is installed | 检查pip是否已安装
echo ⚙️ Checking pip installation...
echo ⚙️ 检查pip安装...

pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ pip found
    echo ✅ 找到pip
    set PIP_CMD=pip
) else (
    echo ❌ pip not found! Please install pip first.
    echo ❌ 未找到pip！请先安装pip。
    pause
    exit /b 1
)

REM Install dependencies | 安装依赖
echo ⚙️ Installing dependencies...
echo ⚙️ 正在安装依赖...

%PIP_CMD% install -r requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo ✅ Dependencies installed successfully!
    echo ✅ 依赖安装成功！
) else (
    echo ❌ Failed to install dependencies!
    echo ❌ 依赖安装失败！
    pause
    exit /b 1
)

REM Install Playwright browsers | 安装Playwright浏览器
echo ⚙️ Installing Playwright browsers...
echo ⚙️ 正在安装Playwright浏览器...

%PYTHON_CMD% -m playwright install chromium
if %ERRORLEVEL% EQU 0 (
    echo ✅ Playwright browsers installed successfully!
    echo ✅ Playwright浏览器安装成功！
) else (
    echo ⚠️ Playwright browser installation failed, but you can continue.
    echo ⚠️ Playwright浏览器安装失败，但您可以继续使用。
)

REM Create config if not exists | 如果配置不存在则创建
if not exist ".env" (
    if exist "config.example.env" (
        echo ⚙️ Creating configuration file...
        echo ⚙️ 正在创建配置文件...
        copy config.example.env .env
        echo ✅ Configuration template created as .env
        echo ✅ 配置模板已创建为.env文件
    )
)

echo.
echo 🚀 Installation completed successfully!
echo 🚀 安装完成！
echo ========================================================
echo.
echo 📚 Next Steps ^| 下一步操作:
echo.
echo 1. Edit .env file with your ManageBac credentials
echo 1. 编辑.env文件，填入您的ManageBac凭据
echo.
echo 2. Run the program:
echo 2. 运行程序：
echo    💻 %PYTHON_CMD% main_new.py
echo.
echo 3. Or use interactive mode:
echo 3. 或使用交互模式：
echo    💻 %PYTHON_CMD% main_new.py --interactive
echo.
echo 📚 For help ^| 获取帮助:
echo    💻 %PYTHON_CMD% main_new.py --help
echo.
echo 🚀 Happy assignment tracking! ^| 愉快地追踪作业！

pause
