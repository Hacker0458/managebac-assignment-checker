# 🛠️ ManageBac Assignment Checker - Troubleshooting Guide
# 🛠️ ManageBac作业检查器 - 故障排除指南

<div align="center">

![Troubleshooting](https://img.shields.io/badge/Status-Troubleshooting-orange.svg)
![Support](https://img.shields.io/badge/Support-Available-green.svg)
![Community](https://img.shields.io/badge/Community-Active-blue.svg)

**🔧 Complete troubleshooting guide for common issues**  
**🔧 常见问题完整故障排除指南**

[English](#english) | [中文](#中文)

</div>

---

## English

### 🚨 Common Issues & Solutions

#### 1. Installation Problems

##### ❌ Python Not Found
**Error:** `python: command not found` or `python3: command not found`

**Solutions:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip
# or
sudo dnf install python3 python3-pip

# macOS
brew install python3

# Windows
# Download from https://python.org
```

##### ❌ Pip Not Found
**Error:** `pip: command not found`

**Solutions:**
```bash
# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Or use package manager
sudo apt-get install python3-pip  # Ubuntu/Debian
sudo yum install python3-pip      # CentOS/RHEL
brew install python3-pip          # macOS
```

##### ❌ Permission Denied
**Error:** `Permission denied` during installation

**Solutions:**
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

#### 2. Playwright Issues

##### ❌ Playwright Installation Failed
**Error:** `Playwright installation failed`

**Solutions:**
```bash
# Install system dependencies
python -m playwright install-deps chromium

# Manual installation
python -m playwright install chromium

# Check system dependencies
python -m playwright install-deps --dry-run
```

##### ❌ Browser Not Found
**Error:** `Browser not found` or `Chromium not found`

**Solutions:**
```bash
# Reinstall browsers
python -m playwright install chromium

# Install all browsers
python -m playwright install

# Check browser installation
python -m playwright install --help
```

#### 3. Authentication Issues

##### ❌ Login Failed
**Error:** `Authentication failed` or `Login failed`

**Solutions:**
1. **Check credentials in .env file:**
```bash
cat .env
```

2. **Verify ManageBac URL:**
```env
MANAGEBAC_URL=https://your-school.managebac.com
```

3. **Test credentials manually:**
```bash
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
result = checker.test_connection()
print('Connection test:', result)
"
```

4. **Check network connectivity:**
```bash
ping your-school.managebac.com
```

##### ❌ Invalid Credentials
**Error:** `Invalid username or password`

**Solutions:**
1. **Reset password on ManageBac website**
2. **Check for typos in .env file**
3. **Verify email format**
4. **Contact school IT support**

#### 4. GUI Issues

##### ❌ GUI Not Starting
**Error:** GUI window doesn't appear or crashes

**Solutions:**
1. **Try CLI mode first:**
```bash
python main_new.py --interactive
```

2. **Check system dependencies:**
```bash
# Linux
sudo apt-get install python3-tk

# macOS (usually included)
# Windows (usually included)
```

3. **Check logs:**
```bash
cat logs/managebac_checker.log
```

4. **Reinstall GUI dependencies:**
```bash
pip install --upgrade tkinter
```

##### ❌ Theme Issues
**Error:** Dark theme text not visible or GUI looks broken

**Solutions:**
1. **Switch to light theme:**
```bash
# In GUI: View -> Light Theme
```

2. **Reset theme:**
```bash
rm -f user_preferences.json
```

3. **Update GUI:**
```bash
pip install --upgrade managebac-checker
```

#### 5. Network Issues

##### ❌ Connection Timeout
**Error:** `Connection timeout` or `Network error`

**Solutions:**
1. **Check internet connection:**
```bash
ping google.com
```

2. **Check ManageBac server:**
```bash
ping your-school.managebac.com
```

3. **Increase timeout in .env:**
```env
PAGE_LOAD_TIMEOUT=60
ELEMENT_WAIT_TIMEOUT=20
```

4. **Check firewall settings**

##### ❌ SSL Certificate Issues
**Error:** `SSL certificate verification failed`

**Solutions:**
1. **Update certificates:**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates

# CentOS/RHEL
sudo yum update ca-certificates

# macOS
brew install ca-certificates
```

2. **Disable SSL verification (not recommended):**
```env
SSL_VERIFY=false
```

#### 6. Performance Issues

##### ❌ Slow Performance
**Symptoms:** Application runs slowly or freezes

**Solutions:**
1. **Check system resources:**
```bash
# Linux/macOS
top
htop

# Windows
Task Manager
```

2. **Reduce browser instances:**
```env
MAX_BROWSER_INSTANCES=1
```

3. **Clear cache:**
```bash
rm -rf cache/*
```

4. **Restart application**

##### ❌ Memory Issues
**Error:** `Out of memory` or application crashes

**Solutions:**
1. **Close other applications**
2. **Increase system memory**
3. **Reduce concurrent operations:**
```env
MAX_BROWSER_INSTANCES=1
AUTO_CHECK_INTERVAL=60
```

#### 7. Report Issues

##### ❌ Report Generation Failed
**Error:** `Report generation failed` or empty reports

**Solutions:**
1. **Check output directory:**
```bash
mkdir -p reports
chmod 755 reports
```

2. **Check file permissions:**
```bash
ls -la reports/
```

3. **Verify template files:**
```bash
ls -la managebac_checker/templates/
```

4. **Test report generation:**
```bash
python -c "
from managebac_checker.reporter import Reporter
reporter = Reporter()
reporter.generate_report([], 'test.html')
"
```

##### ❌ Empty Reports
**Error:** Reports are generated but contain no data

**Solutions:**
1. **Check assignment data:**
```bash
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
assignments = checker.get_assignments()
print('Assignments found:', len(assignments))
"
```

2. **Verify credentials and connection**
3. **Check ManageBac website manually**

#### 8. Notification Issues

##### ❌ Notifications Not Working
**Error:** No desktop notifications appear

**Solutions:**
1. **Check notification settings:**
```env
NOTIFICATIONS_ENABLED=true
```

2. **Test notification system:**
```bash
python -c "
from managebac_checker.notifications import NotificationManager
notifier = NotificationManager('en')
notifier.send_notification('Test', 'This is a test notification')
"
```

3. **Check system notification settings**
4. **Install notification dependencies:**
```bash
pip install plyer
```

### 🔍 Debugging Tools

#### Log Analysis
```bash
# View recent logs
tail -f logs/managebac_checker.log

# Search for errors
grep -i error logs/managebac_checker.log

# Search for warnings
grep -i warning logs/managebac_checker.log
```

#### Connection Testing
```bash
# Test ManageBac connection
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
print('Testing connection...')
result = checker.test_connection()
print('Result:', result)
"
```

#### Dependency Check
```bash
# Check installed packages
pip list | grep -E "(playwright|tkinter|requests)"

# Check Python version
python --version

# Check system info
python -c "import sys, platform; print(f'Python: {sys.version}'); print(f'Platform: {platform.platform()}')"
```

### 📞 Getting Help

#### 1. Self-Diagnosis
1. **Check logs** in `logs/managebac_checker.log`
2. **Test connection** using built-in tools
3. **Verify configuration** in `.env` file
4. **Update dependencies** to latest versions

#### 2. Community Support
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and get help
- **Documentation**: Check README and tutorial

#### 3. Professional Support
- **School IT Support**: Contact your school's IT department
- **ManageBac Support**: Contact ManageBac support for account issues

---

## 中文

### 🚨 常见问题及解决方案

#### 1. 安装问题

##### ❌ 找不到Python
**错误:** `python: command not found` 或 `python3: command not found`

**解决方案:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip
# 或
sudo dnf install python3 python3-pip

# macOS
brew install python3

# Windows
# 从 https://python.org 下载
```

##### ❌ 找不到Pip
**错误:** `pip: command not found`

**解决方案:**
```bash
# 安装pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# 或使用包管理器
sudo apt-get install python3-pip  # Ubuntu/Debian
sudo yum install python3-pip      # CentOS/RHEL
brew install python3-pip          # macOS
```

##### ❌ 权限被拒绝
**错误:** 安装时出现 `Permission denied`

**解决方案:**
```bash
# 使用用户安装
pip install --user -r requirements.txt

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

#### 2. Playwright问题

##### ❌ Playwright安装失败
**错误:** `Playwright installation failed`

**解决方案:**
```bash
# 安装系统依赖
python -m playwright install-deps chromium

# 手动安装
python -m playwright install chromium

# 检查系统依赖
python -m playwright install-deps --dry-run
```

##### ❌ 找不到浏览器
**错误:** `Browser not found` 或 `Chromium not found`

**解决方案:**
```bash
# 重新安装浏览器
python -m playwright install chromium

# 安装所有浏览器
python -m playwright install

# 检查浏览器安装
python -m playwright install --help
```

#### 3. 认证问题

##### ❌ 登录失败
**错误:** `Authentication failed` 或 `Login failed`

**解决方案:**
1. **检查.env文件中的凭据:**
```bash
cat .env
```

2. **验证ManageBac URL:**
```env
MANAGEBAC_URL=https://your-school.managebac.com
```

3. **手动测试凭据:**
```bash
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
result = checker.test_connection()
print('连接测试:', result)
"
```

4. **检查网络连接:**
```bash
ping your-school.managebac.com
```

##### ❌ 无效凭据
**错误:** `Invalid username or password`

**解决方案:**
1. **在ManageBac网站上重置密码**
2. **检查.env文件中的拼写错误**
3. **验证邮箱格式**
4. **联系学校IT支持**

#### 4. GUI问题

##### ❌ GUI无法启动
**错误:** GUI窗口不出现或崩溃

**解决方案:**
1. **先尝试CLI模式:**
```bash
python main_new.py --interactive
```

2. **检查系统依赖:**
```bash
# Linux
sudo apt-get install python3-tk

# macOS (通常已包含)
# Windows (通常已包含)
```

3. **检查日志:**
```bash
cat logs/managebac_checker.log
```

4. **重新安装GUI依赖:**
```bash
pip install --upgrade tkinter
```

##### ❌ 主题问题
**错误:** 深色主题文字不可见或GUI看起来损坏

**解决方案:**
1. **切换到浅色主题:**
```bash
# 在GUI中: 查看 -> 浅色主题
```

2. **重置主题:**
```bash
rm -f user_preferences.json
```

3. **更新GUI:**
```bash
pip install --upgrade managebac-checker
```

#### 5. 网络问题

##### ❌ 连接超时
**错误:** `Connection timeout` 或 `Network error`

**解决方案:**
1. **检查互联网连接:**
```bash
ping google.com
```

2. **检查ManageBac服务器:**
```bash
ping your-school.managebac.com
```

3. **在.env中增加超时时间:**
```env
PAGE_LOAD_TIMEOUT=60
ELEMENT_WAIT_TIMEOUT=20
```

4. **检查防火墙设置**

##### ❌ SSL证书问题
**错误:** `SSL certificate verification failed`

**解决方案:**
1. **更新证书:**
```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ca-certificates

# CentOS/RHEL
sudo yum update ca-certificates

# macOS
brew install ca-certificates
```

2. **禁用SSL验证（不推荐）:**
```env
SSL_VERIFY=false
```

#### 6. 性能问题

##### ❌ 性能缓慢
**症状:** 应用程序运行缓慢或冻结

**解决方案:**
1. **检查系统资源:**
```bash
# Linux/macOS
top
htop

# Windows
任务管理器
```

2. **减少浏览器实例:**
```env
MAX_BROWSER_INSTANCES=1
```

3. **清除缓存:**
```bash
rm -rf cache/*
```

4. **重启应用程序**

##### ❌ 内存问题
**错误:** `Out of memory` 或应用程序崩溃

**解决方案:**
1. **关闭其他应用程序**
2. **增加系统内存**
3. **减少并发操作:**
```env
MAX_BROWSER_INSTANCES=1
AUTO_CHECK_INTERVAL=60
```

#### 7. 报告问题

##### ❌ 报告生成失败
**错误:** `Report generation failed` 或空报告

**解决方案:**
1. **检查输出目录:**
```bash
mkdir -p reports
chmod 755 reports
```

2. **检查文件权限:**
```bash
ls -la reports/
```

3. **验证模板文件:**
```bash
ls -la managebac_checker/templates/
```

4. **测试报告生成:**
```bash
python -c "
from managebac_checker.reporter import Reporter
reporter = Reporter()
reporter.generate_report([], 'test.html')
"
```

##### ❌ 空报告
**错误:** 报告已生成但不包含数据

**解决方案:**
1. **检查作业数据:**
```bash
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
assignments = checker.get_assignments()
print('找到的作业:', len(assignments))
"
```

2. **验证凭据和连接**
3. **手动检查ManageBac网站**

#### 8. 通知问题

##### ❌ 通知不工作
**错误:** 没有桌面通知出现

**解决方案:**
1. **检查通知设置:**
```env
NOTIFICATIONS_ENABLED=true
```

2. **测试通知系统:**
```bash
python -c "
from managebac_checker.notifications import NotificationManager
notifier = NotificationManager('en')
notifier.send_notification('测试', '这是一个测试通知')
"
```

3. **检查系统通知设置**
4. **安装通知依赖:**
```bash
pip install plyer
```

### 🔍 调试工具

#### 日志分析
```bash
# 查看最近日志
tail -f logs/managebac_checker.log

# 搜索错误
grep -i error logs/managebac_checker.log

# 搜索警告
grep -i warning logs/managebac_checker.log
```

#### 连接测试
```bash
# 测试ManageBac连接
python -c "
from managebac_checker.checker import ManageBacChecker
checker = ManageBacChecker()
print('测试连接...')
result = checker.test_connection()
print('结果:', result)
"
```

#### 依赖检查
```bash
# 检查已安装的包
pip list | grep -E "(playwright|tkinter|requests)"

# 检查Python版本
python --version

# 检查系统信息
python -c "import sys, platform; print(f'Python: {sys.version}'); print(f'平台: {platform.platform()}')"
```

### 📞 获取帮助

#### 1. 自我诊断
1. **检查日志** 在 `logs/managebac_checker.log`
2. **测试连接** 使用内置工具
3. **验证配置** 在 `.env` 文件中
4. **更新依赖** 到最新版本

#### 2. 社区支持
- **GitHub问题**: 报告错误和请求功能
- **GitHub讨论**: 提问和获取帮助
- **文档**: 查看README和教程

#### 3. 专业支持
- **学校IT支持**: 联系您学校的IT部门
- **ManageBac支持**: 联系ManageBac支持解决账户问题

---

<div align="center">

**Made with ❤️ by [Hacker0458](https://github.com/Hacker0458)**

**⭐ 如果这个项目对您有帮助，请给它一个星标！**  
**⭐ If this project helps you, please give it a star!**

</div>
