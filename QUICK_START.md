# 🚀 ManageBac快速开始指南

> 5分钟快速上手ManageBac Assignment Checker

---

## 📦 一键安装

### 方式1: 自动安装（推荐）

```bash
# 克隆项目
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 一键安装
python unified_installer.py --mode auto
```

### 方式2: 快速安装

```bash
# 使用默认配置快速安装
python unified_installer.py --mode quick
```

### 方式3: 交互式向导

```bash
# 逐步配置
python unified_installer.py --mode wizard
```

---

## ⚙️ 配置

安装完成后，编辑 `.env` 文件：

```bash
# 编辑配置文件
nano .env  # 或使用你喜欢的编辑器
```

必填项：
```env
MANAGEBAC_EMAIL=your_email@example.com
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://shtcs.managebac.cn
```

---

## ▶️ 启动应用

### 自动启动（推荐）

```bash
python unified_launcher.py --mode auto
```

### 图形界面模式

```bash
python unified_launcher.py --mode gui
```

### 命令行模式

```bash
python unified_launcher.py --mode cli
```

或者直接运行：

```bash
# Windows
START.bat

# macOS/Linux
./START.sh
```

---

## 📊 查看结果

运行后，报告会自动生成在 `reports/` 目录：

```bash
reports/
  └── managebac_report_20250124_120000.json
  └── managebac_report_20250124_120000.html
  └── managebac_report_20250124_120000.md
```

---

## 🎯 常用命令

```bash
# 查看帮助
python main.py --help

# 生成HTML报告
python main.py --format html

# 启用调试模式
python main.py --debug

# 发送邮件通知
python main.py --notify
```

---

## 🆘 遇到问题？

1. 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. 运行诊断工具:
   ```bash
   python comprehensive_diagnostic.py
   ```
3. 查看日志:
   ```bash
   cat logs/managebac_checker.log
   ```

---

## 📚 更多信息

- 📖 [完整文档](README.md)
- 🔧 [配置指南](TUTORIAL.md)
- 🚀 [优化报告](OPTIMIZATION_REPORT.md)
- 🧹 [清理指南](CLEANUP_GUIDE.md)

---

**享受自动化作业管理的便利！** 🎉
