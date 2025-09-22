# 📚 ManageBac Assignment Checker

一个基于Playwright的自动化工具，用于登录ManageBac并生成丰富的作业报告（待提交/已提交/逾期），支持HTML/Markdown/JSON输出格式。

> ⚠️ **仅供教育用途**。您必须遵守学校和ManageBac的使用条款。

## ✨ 功能特性

- 🔐 **自动化登录** - 使用Playwright和Chromium自动登录ManageBac
- 📊 **全面抓取** - 抓取所有作业（待提交/已提交/逾期）
- 📋 **多格式报告** - 生成HTML/Markdown/JSON格式报告（带可视化KPI）
- 🔍 **详情抓取** - 可选功能：打开作业页面收集描述/附件信息
- ⚙️ **环境配置** - 基于环境变量的配置（代码中不包含凭据）
- 📧 **邮件通知** - 可选的邮件提醒功能
- 🎯 **智能分析** - 优先级分析和紧急程度评估
- 🖥️ **CLI接口** - 友好的命令行界面

## 🚀 快速开始

### 1. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入您的凭据
# MANAGEBAC_EMAIL=your_email@example.com
# MANAGEBAC_PASSWORD=your_password
```

### 4. 运行工具

```bash
# 使用新的模块化版本
python main_new.py

# 或者使用CLI接口
python -m managebac_checker.cli

# 或者安装后使用
pip install -e .
managebac-checker
```

## 📖 使用方法

### 基本用法

```bash
# 使用默认配置运行
python main_new.py

# 开启调试模式
python main_new.py --debug

# 显示浏览器窗口（非无头模式）
python main_new.py --headless=false

# 只生成HTML和JSON报告
python main_new.py --format html,json

# 抓取作业详情
python main_new.py --fetch-details --details-limit 5
```

### 环境变量配置

在 `.env` 文件中设置以下变量：

#### 必需配置
- `MANAGEBAC_EMAIL`: 您的ManageBac邮箱
- `MANAGEBAC_PASSWORD`: 您的ManageBac密码

#### 可选配置
- `MANAGEBAC_URL`: ManageBac URL（默认: https://shtcs.managebac.cn）
- `HEADLESS`: 浏览器无头模式（默认: true）
- `TIMEOUT`: 超时时间（默认: 30000ms）
- `DEBUG`: 调试模式（默认: false）
- `REPORT_FORMAT`: 报告格式，逗号分隔（默认: console,json）
- `OUTPUT_DIR`: 报告输出目录（默认: ./reports）
- `FETCH_DETAILS`: 是否抓取详情（默认: false）
- `DETAILS_LIMIT`: 详情抓取数量限制（默认: 10）

#### 邮件通知配置
- `ENABLE_NOTIFICATIONS`: 启用邮件通知（默认: false）
- `SMTP_SERVER`: SMTP服务器
- `SMTP_PORT`: SMTP端口（默认: 587）
- `EMAIL_USER`: 发送邮箱
- `EMAIL_PASSWORD`: 邮箱密码
- `NOTIFICATION_EMAIL`: 接收通知的邮箱

## 📁 项目结构

```
managebac-assignment-checker/
├── managebac_checker/          # 主要包
│   ├── __init__.py            # 包初始化
│   ├── checker.py             # 主检查器类
│   ├── config.py              # 配置管理
│   ├── scraper.py             # 网页抓取
│   ├── analyzer.py            # 数据分析
│   ├── reporter.py            # 报告生成
│   ├── notifications.py       # 邮件通知
│   └── cli.py                 # 命令行接口
├── tests/                     # 测试文件
│   ├── test_analysis.py       # 分析模块测试
│   └── test_reporting.py      # 报告模块测试
├── reports/                   # 生成的报告
├── .github/workflows/         # GitHub Actions
├── main.py                    # 原始单文件版本
├── main_new.py               # 新的模块化版本
├── requirements.txt           # 依赖列表
├── setup.py                  # 安装配置
├── .env.example              # 环境变量示例
└── README.md                 # 项目说明
```

## 🧪 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_analysis.py -v

# 带覆盖率报告
pytest tests/ --cov=managebac_checker --cov-report=html
```

### 代码质量检查

```bash
# 代码格式化
black managebac_checker tests

# 代码检查
flake8 managebac_checker tests

# 类型检查
mypy managebac_checker
```

### 安全扫描

```bash
# 安全漏洞扫描
bandit -r managebac_checker/

# 依赖安全检查
safety check
```

## 📊 报告格式

### HTML报告
- 现代化的响应式设计
- 可视化KPI指标
- 按优先级和状态分类显示
- 支持移动端查看

### Markdown报告
- 适合在GitHub等平台查看
- 结构化的作业列表
- 包含优先级和紧急程度标识

### JSON报告
- 机器可读的格式
- 包含完整的作业数据
- 适合进一步处理和分析

## 🔧 故障排除

### 常见问题

1. **登录失败**
   - 检查邮箱和密码是否正确
   - 确认ManageBac URL是否正确
   - 尝试设置 `HEADLESS=false` 查看浏览器行为

2. **找不到作业**
   - 页面结构可能已更改
   - 尝试设置 `DEBUG=true` 查看详细信息
   - 检查是否需要手动导航到作业页面

3. **浏览器启动失败**
   - 确保已安装Playwright浏览器：`playwright install chromium`
   - 在受限环境中可能需要设置 `--no-sandbox` 参数

### 调试模式

```bash
# 开启调试模式
DEBUG=true python main_new.py

# 或使用CLI参数
python main_new.py --debug
```

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建Pull Request

### 开发指南

- 遵循PEP 8代码风格
- 添加适当的测试
- 更新文档
- 确保所有测试通过

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

- 本工具仅供教育和个人使用
- 请遵守学校和ManageBac的使用条款
- 不要将凭据提交到版本控制系统
- 使用本工具的风险由用户自行承担

## 📞 支持

如果您遇到问题或有建议，请：

1. 查看[故障排除](#故障排除)部分
2. 搜索现有的[Issues](https://github.com/yourusername/managebac-assignment-checker/issues)
3. 创建新的Issue描述您的问题

## 🎯 路线图

- [ ] 支持更多学校系统
- [ ] 添加数据库存储功能
- [ ] 实现定时任务调度
- [ ] 添加移动端应用
- [ ] 支持多语言界面

---

**⭐ 如果这个项目对您有帮助，请给它一个星标！**