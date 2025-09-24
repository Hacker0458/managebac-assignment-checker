# 🔧 ManageBac Assignment Checker - 安装问题排查指南
# Installation Troubleshooting Guide

## 常见安装问题及解决方案 | Common Installation Issues & Solutions

### 1. ❌ requirements.txt 文件未找到错误
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

#### 原因分析 | Root Cause
- 网络连接问题导致文件下载失败
- GitHub访问受限
- 文件下载被中断

#### 解决方案 | Solutions

**方案A: 使用增强版安装脚本**
```bash
# 使用最新的稳定安装脚本
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install_robust.sh | bash
```

**方案B: 手动下载requirements.txt**
```bash
# 1. 创建项目目录
mkdir -p ~/managebac-assignment-checker
cd ~/managebac-assignment-checker

# 2. 手动下载requirements.txt
curl -L "https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt" -o requirements.txt

# 3. 验证文件下载成功
ls -la requirements.txt
head -5 requirements.txt

# 4. 如果上述失败，创建基本的requirements.txt
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
```

**方案C: 直接安装核心依赖**
```bash
# 不依赖requirements.txt文件，直接安装核心包
pip3 install playwright python-dotenv jinja2 openai pystray pillow
python3 -m playwright install chromium
```

### 2. 🌐 网络连接问题

#### 症状 | Symptoms
- 下载超时
- 连接被拒绝
- SSL证书错误

#### 解决方案 | Solutions

**检查网络连接**
```bash
# 测试GitHub连接
ping github.com

# 测试文件下载
curl -I https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/requirements.txt
```

**使用代理或镜像**
```bash
# 如果在中国大陆，可能需要使用代理
# 或尝试使用GitHub的镜像站点

# 方法1: 使用代理（如果有）
export https_proxy=your_proxy_server:port
curl -sSL https://raw.githubusercontent.com/Hacker0458/managebac-assignment-checker/main/install.sh | bash

# 方法2: 下载完整项目包
wget https://github.com/Hacker0458/managebac-assignment-checker/archive/main.zip
unzip main.zip
cd managebac-assignment-checker-main
```

### 3. 🐍 Python版本问题

#### 症状 | Symptoms
```
ERROR: Python 3.8 is required
SyntaxError: invalid syntax
```

#### 解决方案 | Solutions

**检查Python版本**
```bash
python3 --version
python --version
```

**安装正确的Python版本**
```bash
# macOS (使用Homebrew)
brew install python@3.9

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-pip

# Windows
# 从 python.org 下载并安装Python 3.9+
```

### 4. 📦 pip 安装问题

#### 症状 | Symptoms
```
ERROR: Could not install packages
Permission denied
```

#### 解决方案 | Solutions

**使用虚拟环境（推荐）**
```bash
python3 -m venv managebac_venv
source managebac_venv/bin/activate  # Linux/Mac
# managebac_venv\Scripts\activate  # Windows
pip install --upgrade pip
```

**解决权限问题**
```bash
# 使用用户安装
pip3 install --user -r requirements.txt

# 或升级pip
python3 -m pip install --upgrade pip
```

### 5. 🎭 Playwright浏览器安装失败

#### 症状 | Symptoms
```
ERROR: Failed to install browsers
Playwright browsers not found
```

#### 解决方案 | Solutions

**手动安装Playwright浏览器**
```bash
python3 -m playwright install chromium
```

**如果安装失败，尝试**
```bash
# 安装所有浏览器
python3 -m playwright install

# 或仅安装必需的
python3 -m playwright install --with-deps chromium
```

### 6. 🔒 权限和文件访问问题

#### 症状 | Symptoms
```
Permission denied
Cannot create directory
```

#### 解决方案 | Solutions

**检查目录权限**
```bash
# 确保在用户目录下安装
cd ~
mkdir -p managebac-assignment-checker
cd managebac-assignment-checker
```

**修复权限问题**
```bash
# 修复文件权限
chmod +x install.sh
chmod +x gui_launcher.py
```

## 🆘 紧急安装方法 | Emergency Installation Method

如果所有上述方法都失败，使用这个最小化安装：

```bash
#!/bin/bash
# 紧急安装脚本

echo "🚨 Emergency Installation | 紧急安装"

# 创建项目目录
mkdir -p ~/managebac-assignment-checker
cd ~/managebac-assignment-checker

# 安装最基本的依赖
pip3 install playwright python-dotenv

# 安装Playwright浏览器
python3 -m playwright install chromium

# 创建基本的配置文件
cat > .env << 'EOF'
# ManageBac Configuration
MANAGEBAC_EMAIL=your_email@school.edu
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://your_school.managebac.com
HEADLESS=true
DEBUG=false
EOF

# 创建简单的启动脚本
cat > run.py << 'EOF'
#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def main():
    print("🎓 ManageBac Assignment Checker - Emergency Mode")
    print("Please configure your .env file and run the full installation later.")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://managebac.com")
        print("✅ Basic browser functionality working")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x run.py

echo "✅ Emergency installation completed!"
echo "📝 Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python3 run.py"
echo "3. Download full version later when network is stable"
```

## 📞 获取帮助 | Getting Help

如果仍然遇到问题，请：

1. **检查系统要求**：Python 3.9+, 稳定网络连接
2. **查看详细错误信息**：运行安装脚本时保存完整的错误输出
3. **提供系统信息**：操作系统版本、Python版本、网络环境
4. **尝试不同的安装方法**：本地安装、手动下载、使用代理

## 🔄 验证安装是否成功

运行以下命令验证安装：

```bash
# 检查Python模块
python3 -c "import playwright; print('✅ Playwright installed')"
python3 -c "import dotenv; print('✅ python-dotenv installed')"

# 检查文件结构
ls -la ~/managebac-assignment-checker/

# 测试基本功能
python3 -c "
from playwright.async_api import async_playwright
print('✅ Playwright import successful')
"
```

---

🎯 **记住**：安装脚本现在包含了多重后备方案，即使部分文件下载失败，也能确保核心功能正常工作。