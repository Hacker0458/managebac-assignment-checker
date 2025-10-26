# ManageBac 作业检查器

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![iOS](https://img.shields.io/badge/iOS-18.0+-blue.svg)
![Swift](https://img.shields.io/badge/swift-6.1+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

一款功能强大的跨平台工具,帮助学生追踪ManageBac作业,提供智能分析和通知功能。

[English](README.md) | [中文](README.zh.md)

</div>

## ✨ 功能特性

### 🖥️ 多平台支持
- **iOS原生应用**: 使用SwiftUI为iOS 18+构建
- **桌面应用**: Windows、macOS和Linux跨平台GUI
- **命令行工具**: 灵活的CLI接口,支持自动化

### 🤖 智能分析
- 自动追踪作业截止日期
- 基于优先级的作业排序
- AI驱动的学习建议(集成OpenAI)
- 全面的统计和可视化

### 🔔 智能通知
- 实时桌面通知
- 即将到期作业的邮件提醒
- 后台任务调度(iOS)
- 可自定义通知间隔

### 📊 丰富的报告
- 多种导出格式(HTML、JSON、Markdown)
- 交互式仪表板
- 作业时间线可视化
- 进度追踪和统计

## 🚀 快速开始

### iOS应用

#### 系统要求
- iOS 18.0或更高版本
- Xcode 16+(用于开发)

#### 安装步骤
1. 克隆仓库:
```bash
git clone https://github.com/yourusername/managebac-assignment-checker.git
cd managebac-assignment-checker
```

2. 在Xcode中打开:
```bash
open ManageBacChecker.xcodeproj
```

3. 在iOS设备或模拟器上构建并运行

### Python桌面应用

#### 系统要求
- Python 3.8或更高版本
- pip包管理器

#### 一键安装
```bash
# Linux/macOS
bash install.sh

# Windows
install.bat
```

#### 手动安装
```bash
# 安装依赖
pip install -r requirements.txt

# 启动GUI
python intelligent_launcher.py
```

## 📁 项目结构

```
managebac-assignment-checker/
├── ManageBacChecker/              # iOS应用源代码
│   ├── ManageBacCheckerApp.swift  # 应用入口
│   ├── ContentView.swift          # 主视图
│   ├── AssignmentListView.swift   # 作业列表
│   ├── StatisticsView.swift       # 统计仪表板
│   ├── SettingsView.swift         # 设置界面
│   └── AssignmentManager.swift    # 核心业务逻辑
├── ManageBacChecker.xcodeproj/    # Xcode项目
├── Config/                        # iOS配置
│   ├── Shared.xcconfig            # 共享构建设置
│   └── ManageBacChecker.entitlements
├── managebac_checker/             # Python包
│   ├── checker.py                 # 主检查逻辑
│   ├── analyzer.py                # 分析引擎
│   ├── reporter.py                # 报告生成
│   ├── notifier.py                # 通知系统
│   └── gui.py                     # 桌面GUI
├── tests/                         # 测试套件
├── scripts/                       # 辅助脚本
├── docs/                          # 文档
└── archive/                       # 历史版本
```

## 🎯 使用方法

### iOS应用

1. **登录**: 首次启动时输入ManageBac凭据
2. **查看作业**: 按优先级浏览作业
3. **查看统计**: 查看全面的统计数据和图表
4. **配置通知**: 在设置中自定义提醒偏好
5. **后台同步**: 启用后台刷新以自动更新

### 桌面应用

#### GUI模式(推荐)
```bash
python intelligent_launcher.py
```

#### 命令行模式
```bash
# 检查作业
python main.py

# 使用自定义配置
python main.py --config my_config.env

# 生成特定格式报告
python main.py --format html
```

## 🔧 配置

### iOS应用
- 在应用的设置界面中配置
- 凭据使用iOS钥匙串安全存储
- 通知偏好通过UserDefaults同步

### Python应用

创建`config.env`文件(或从`config.example.env`复制):

```env
# ManageBac凭据
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password
MANAGEBAC_SCHOOL=your-school-name

# 通知设置
ENABLE_EMAIL_NOTIFICATIONS=true
EMAIL_ADDRESS=your-email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-app-password

# AI功能(可选)
OPENAI_API_KEY=your-openai-key
ENABLE_AI_ANALYSIS=true

# 报告设置
DEFAULT_REPORT_FORMAT=html
OUTPUT_DIRECTORY=./reports
```

## 🏗️ 架构设计

### iOS应用(Swift + SwiftUI)
- **架构模式**: MVVM模式配合SwiftUI
- **UI框架**: SwiftUI with iOS 18+ features
- **数据管理**: @ObservableObject + UserDefaults
- **后台任务**: BGTaskScheduler
- **通知系统**: UNUserNotificationCenter
- **网页集成**: WKWebView用于ManageBac数据抓取

### Python桌面应用
- **核心**: Python 3.8+ with async/await
- **网页抓取**: Playwright + BeautifulSoup4
- **GUI框架**: tkinter配合现代主题
- **AI集成**: OpenAI GPT API
- **测试框架**: pytest配合工厂模式
- **通知系统**: 跨平台通知系统

## 🧪 测试

### iOS应用
```bash
# 运行单元测试
xcodebuild test -scheme ManageBacChecker -destination 'platform=iOS Simulator,name=iPhone 15'

# 运行UI测试
xcodebuild test -scheme ManageBacChecker -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:ManageBacCheckerUITests
```

### Python应用
```bash
# 运行所有测试
pytest

# 运行并生成覆盖率报告
pytest --cov=managebac_checker --cov-report=html

# 运行特定测试文件
pytest tests/test_checker.py
```

## 📖 文档

- [iOS项目概览](docs/iOS_PROJECT_FINAL_STATUS.md)
- [安装指南](docs/INSTALLATION_TROUBLESHOOTING.md)
- [详细使用教程](docs/详细使用教程.md)
- [API文档](docs/API.md)
- [贡献指南](CONTRIBUTING.md)
- [更新日志](CHANGELOG.md)

## 🤝 贡献

欢迎贡献! 在提交pull request之前,请阅读我们的[贡献指南](CONTRIBUTING.md)。

### 开发环境设置

#### iOS开发
1. 安装Xcode 16+
2. 克隆仓库
3. 打开`ManageBacChecker.xcodeproj`
4. 构建并运行

#### Python开发
1. Fork仓库
2. 创建虚拟环境:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. 安装开发依赖:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. 进行修改
5. 运行测试:
   ```bash
   pytest
   ```
6. 提交pull request

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 👨‍💻 作者

**方籽杰 (Fang Zijie)**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 致谢

- ManageBac平台提供的作业管理系统
- OpenAI提供的AI分析能力
- 开源社区提供的优秀库和工具

## 📊 项目状态

- ✅ Python桌面应用: **生产就绪**
- ✅ iOS原生应用: **95%完成** (等待App Store提交)
- 🔄 Android应用: **计划中**
- 🔄 Web仪表板: **计划中**

## 🐛 错误报告和功能请求

请使用[GitHub Issues](https://github.com/yourusername/managebac-assignment-checker/issues)报告错误或请求新功能。

## 📈 路线图

### 版本2.0 (2025年第四季度)
- [ ] Android原生应用
- [ ] Web仪表板
- [ ] 多用户支持
- [ ] 高级AI功能
- [ ] 自定义报告模板

### 版本1.5 (2025年第三季度)
- [x] iOS原生应用
- [x] 后台任务调度
- [x] 增强通知
- [ ] iCloud同步
- [ ] 小组件支持

---

<div align="center">

**用❤️为使用ManageBac的学生打造**

⭐ 如果觉得有帮助,请给项目点个星!

</div>

