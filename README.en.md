# 🎓 ManageBac Assignment Checker

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)](https://github.com/Hacker0458/managebac-assignment-checker)

> 🚀 **Intelligent ManageBac Assignment Tracking Tool** - Automatically check assignment status, generate detailed reports, never miss an assignment again!

## ✨ Key Features

### 🎯 One-Click Launch Experience
- 🌟 **Auto-Launch by Default** - Application opens automatically after installation
- 🧠 **Smart Environment Detection** - Automatically selects the best launch method (GUI/CLI)
- 🔧 **Auto Error Fixing** - Intelligently diagnoses and fixes common issues
- 📱 **Cross-Platform Support** - Compatible with macOS, Windows, and Linux

### 📊 Powerful Features
- 📚 **Automatic Assignment Checking** - Regular ManageBac scanning for latest assignments
- ⏰ **Smart Notification System** - Timely alerts for overdue and urgent tasks
- 📋 **Multi-Format Reports** - Support for HTML, JSON, Markdown and more
- 🔔 **System Notifications** - Native macOS notification system integration
- 🤖 **AI-Powered Analysis** - Optional AI assistant for assignment priority suggestions

### 💻 Modern Interface
- 🎨 **Professional GUI** - Modern desktop application
- 🌙 **Dark Mode Support** - Eye-friendly dark theme
- 📱 **Responsive Design** - Adapts to different screen sizes
- 🗂️ **System Tray Integration** - Background operation, always available

## 🚀 Quick Start

### 🌟 Recommended: One-Click Install + Auto-Launch

```bash
# 🎯 Step 1: Clone the project
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# 🚀 Step 2: Run the optimized installer (Recommended)
python3 优化安装器.py
```

**That's it!** The installer will:
- ✅ Automatically check system requirements
- ✅ Install all necessary dependencies
- ✅ Create basic configuration files
- ✅ **Automatically launch the application**

### 🔧 Alternative Installation Methods

If the optimized installer is not available, you can use these alternatives:

```bash
# Option 1: Ultimate Installer (now auto-launches by default)
python3 ultimate_installer.py

# Option 2: Advanced Installer
python3 advanced_installer.py

# Option 3: Classic Setup Wizard
python3 setup_wizard.py

# Option 4: GUI Setup Wizard
python3 enhanced_setup_gui.py
```

### 📋 Configuration Setup

After installation, edit the `.env` file with your ManageBac account information:

```bash
# ManageBac Configuration
MANAGEBAC_URL=https://your-school.managebac.cn
MANAGEBAC_EMAIL=your.email@school.edu
MANAGEBAC_PASSWORD=your_password

# Optional Configuration
REPORT_FORMAT=html,console
OUTPUT_DIR=reports
LANGUAGE=en
HEADLESS=true
```

## 🚀 Launch Application

### 🧠 Smart Launcher (Recommended)

```bash
# 🌟 Intelligent Launcher - Best User Experience
python3 intelligent_launcher.py

# 🤖 Smart Launcher Features:
# ✅ Automatic environment detection
# ✅ Intelligent selection of best launch method
# ✅ Process management and conflict resolution
# ✅ Automatic retry on failure
# ✅ Detailed error diagnostics
```

### 🎨 GUI Launch Options

```bash
# GUI Launcher
python3 gui_launcher.py

# Smart Launcher (auto-detects GUI)
python3 smart_launcher.py

# Professional GUI Application
python3 run_app.py
```

### 💻 Command Line Options

```bash
# Basic command line interface
python3 main_new.py

# Interactive mode
python3 main_new.py --interactive

# Specify output format
python3 -m managebac_checker.cli --format html

# Enable notifications
python3 -m managebac_checker.cli --notify
```

## 📱 Double-Click Launch (Beginner-Friendly)

Desktop shortcuts are automatically created after installation:

### macOS
```bash
# Double-click the "ManageBac Assignment Checker.command" file on desktop
# Or use terminal:
./START.sh
```

### Windows
```batch
:: Double-click START.bat file
START.bat
```

### Linux
```bash
# Double-click managebac-checker.desktop file
# Or use terminal:
./START.sh
```

## 🔧 Troubleshooting

### Quick Fixes

#### 1. Application doesn't auto-launch
```bash
# Solution:
python3 优化安装器.py  # Re-run the optimized installer
python3 intelligent_launcher.py  # Use intelligent launcher directly
```

#### 2. Dependency installation fails
```bash
# Manual dependency installation:
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

#### 3. GUI won't start
```bash
# Check tkinter:
python3 -c "import tkinter; print('tkinter OK')"

# Use command line mode:
python3 smart_launcher.py --cli
```

### 🧪 Diagnostic Tools

```bash
# Run complete system test
python3 test_auto_launch.py

# Run error diagnostics
python3 error_handler.py
```

**For more detailed troubleshooting, see: [📘 Detailed User Guide](详细使用教程.md#-troubleshooting-guide)**

## 📁 Project Structure

```
managebac-assignment-checker/
├── 🌟 优化安装器.py              # Recommended one-click installer (auto-launch by default)
├── 🚀 ultimate_installer.py     # Multi-mode installer
├── 🧠 intelligent_launcher.py    # Intelligent launcher (best experience)
├── 🎨 ultimate_user_experience.py # Ultimate user experience launcher
├── 🤖 smart_launcher.py          # Adaptive launcher
├── 🎯 gui_launcher.py            # GUI-specific launcher
├── 📋 main_new.py               # Main application
├── 🔧 enhanced_error_handler.py  # Enhanced error handling and logging system
├── 🚨 error_handler.py          # Basic error handling system
├── 🧪 test_auto_launch.py       # Auto-launch testing tool
├── ✨ fixed_gui.py              # Fixed GUI app (diagnostic)
├── 🛠️ professional_gui_fixed.py  # Professional GUI fixed version
├── managebac_checker/           # Core package directory
│   ├── checker.py              # Main checking logic
│   ├── scraper.py             # Web scraping engine
│   ├── analyzer.py            # Data analyzer
│   ├── reporter.py            # Report generator
│   ├── professional_gui.py     # Professional GUI interface (fixed)
│   ├── system_tray.py         # System tray (native notifications)
│   └── notifications.py       # Multi-platform notification system
├── 📁 logs/                    # Log files directory
├── 📖 README.md                # Main documentation (bilingual)
├── 📘 详细使用教程.md           # Complete user guide (Chinese)
├── 📋 CLAUDE.md                # Technical development documentation
├── 🍎 macos_conversion_guide.md # macOS app conversion guide
├── ⚙️ config.example.env       # Configuration file template
└── 📦 requirements.txt         # Python dependencies list
```

## 🌟 Latest Updates

### ✅ Issues Resolved

- **🎯 One-click install auto-launch** - Optimized installer now auto-launches application by default
- **🔧 Dependency compatibility fixes** - Resolved Python 3.13 pyobjus compilation issues
- **🍎 macOS native notifications** - Using osascript instead of plyer for perfect macOS support
- **🧠 Intelligent launcher** - New intelligent_launcher.py provides best startup experience
- **🚨 Error handling system** - New enhanced_error_handler.py for intelligent diagnosis and fixes
- **💻 GUI crash fixes** - Completely resolved GUI application crash issues
- **🎨 User experience optimization** - New ultimate_user_experience.py for ultimate user experience

### 🔥 Core Improvements

- **Zero-configuration experience** - New users only need to run one command
- **Smart environment detection** - Automatically selects GUI or command line mode
- **Automatic error fixing** - Common issues resolved automatically
- **Cross-platform notifications** - Unified notification experience

## 🤝 Contributing

Contributions and suggestions are welcome!

### Quick Start Contributing

1. **Fork the project**
2. **Create feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to branch** (`git push origin feature/AmazingFeature`)
5. **Open Pull Request**

### Development Environment Setup

```bash
# Clone development version
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker

# Use optimized installer to set up development environment
python3 优化安装器.py

# Run tests
python3 test_auto_launch.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Hacker0458**
- GitHub: [@Hacker0458](https://github.com/Hacker0458)
- Project: [ManageBac Assignment Checker](https://github.com/Hacker0458/managebac-assignment-checker)

## 🙏 Acknowledgments

- Thanks to all contributors and users for their feedback
- Special thanks to friends who suggested user experience improvements
- Thanks to the ManageBac platform for providing the service
- Thanks to the open source community for support

## 📞 Support & Feedback

### 🆘 Get Help

- 🐛 [Report Bug](https://github.com/Hacker0458/managebac-assignment-checker/issues/new?template=bug_report.md)
- 💡 [Feature Request](https://github.com/Hacker0458/managebac-assignment-checker/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/Hacker0458/managebac-assignment-checker/discussions)
- 📧 [Email Support](mailto:support@example.com)

### 📚 Documentation Index

- **Beginner Guide**: [📘 Detailed User Guide](详细使用教程.md) - Complete guide from installation to advanced features
- **Technical Docs**: [📋 CLAUDE.md](CLAUDE.md) - Developer and advanced user documentation
- **macOS Users**: [🍎 macOS Conversion Guide](macos_conversion_guide.md) - Native app building solution

---

## 🎉 Start Using Now!

### 🌟 The Simplest Way

```bash
# One command to start your intelligent assignment management journey!
git clone https://github.com/Hacker0458/managebac-assignment-checker.git
cd managebac-assignment-checker
python3 优化安装器.py
```

### ⭐ What's Included Now

✅ **Zero-configuration installation** - One-click complete setup
✅ **Auto-launch application** - Ready to use immediately after installation
✅ **Intelligent error fixing** - Automatically diagnoses and solves problems
✅ **Cross-platform support** - Runs perfectly on any system
✅ **Native system integration** - macOS notifications, desktop shortcuts
✅ **Modern interface** - Professional GUI and command line dual modes

**Enjoy never forgetting assignments again in your relaxed study life!** 🎓✨

---

*If this project helps you, please consider giving us a ⭐Star! This will encourage us to continue improving and adding new features.*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**🎯 An intelligent automation tool for ManageBac assignment tracking**

[View Chinese Version](README.md) | **English**

</div>

---

## 🌟 Features in Detail

### 🖥️ **Modern GUI Application**
- 📱 **Beautiful Desktop Interface**: Modern, responsive GUI with intuitive design
- 🎨 **Multiple Themes**: Light and Dark themes with smooth animations
- 🔔 **System Tray Integration**: Minimize to tray with desktop notifications
- 📊 **Interactive Assignment Cards**: Visual assignment management with filtering and search
- ⚙️ **Comprehensive Settings**: Tabbed configuration dialog with all options
- 🔄 **Auto-refresh**: Automatic background checking with customizable intervals

### 🤖 **AI Assistant Integration**
- 💡 **Intelligent Analysis**: Powered by OpenAI for smart assignment insights
- 📚 **Personalized Recommendations**: AI-powered study strategies and time management
- 🎯 **Priority Assessment**: Smart urgency and importance evaluation
- 📈 **Learning Analytics**: Detailed analysis of study patterns and progress

### 🔐 **Security & Authentication**
- 🛡️ **Secure Login**: Automated ManageBac authentication with credential protection
- 🔑 **Environment Variables**: Safe credential storage with .env files
- 🌐 **Bilingual Support**: Full English and Chinese interface throughout

### 📊 **Advanced Reporting**
- 📋 **Multi-format Reports**: Generate HTML, Markdown, JSON, and console reports
- 📈 **Visual Analytics**: Interactive charts and detailed statistics
- 📧 **Email Notifications**: Automated assignment reminders and updates
- 🎨 **Beautiful HTML Reports**: Modern responsive design with Chart.js integration

### 🚀 **Easy Installation & Deployment**
- 🎯 **One-click Installation**: Complete setup script with dependency management
- 🔗 **Desktop Shortcuts**: Automatic shortcut creation for all platforms
- 📦 **Cross-platform**: Windows, macOS, and Linux support
- 🧪 **Full Test Coverage**: Comprehensive unit testing suite
- 🚀 **CI/CD Ready**: GitHub Actions workflow included

## 🔧 Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black managebac_checker/
flake8 managebac_checker/
```

## 📊 Report Examples

### HTML Report Features:
- 📱 Responsive design
- 🎨 Modern UI with charts
- 📈 Interactive statistics
- 🔍 Searchable assignments

### Console Output:
```
╭─────────────────────────────────────────────────────────╮
│                ManageBac Assignment Report              │
├─────────────────────────────────────────────────────────┤
│ 📚 Total Assignments: 15                               │
│ ⚠️  Overdue: 2                                         │
│ 🔥 High Priority: 5                                    │
│ ✅ Completed: 8                                        │
╰─────────────────────────────────────────────────────────╯
```

## ⚠️ Important Notes

- Ensure you have permission to access the ManageBac system
- Comply with your school's terms of use and privacy policies
- Test in a development environment first
- Keep your credentials secure

## 🆘 Common Issues & Solutions

### Issue: "Application crashes on startup"
**Solution**:
1. Run diagnostic: `python3 comprehensive_diagnostic.py`
2. Try simple GUI: `python3 non_hanging_gui.py`
3. Check logs in `./logs/` directory

### Issue: "Login successful but no assignments found"
**Solution**:
1. Check `.env` file - ensure real credentials (not example ones)
2. Verify ManageBac URL is correct
3. Run assignment test: `python3 fixed_assignment_test.py`

### Issue: "GUI hangs or freezes"
**Solution**:
1. Use non-hanging version: `python3 non_hanging_gui.py`
2. Check system tray integration issues
3. Try headless mode: set `HEADLESS=true` in `.env`

### Issue: "Dependencies installation fails"
**Solution**:
1. Upgrade pip: `pip install --upgrade pip`
2. Use specific Python version: `python3.8 -m pip install ...`
3. Check system dependencies (especially on Linux)

---

**Made with ❤️ by [Hacker0458](https://github.com/Hacker0458)**

**⭐ If this project helps you, please give it a star!**