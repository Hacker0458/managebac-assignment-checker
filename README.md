# ManageBac Assignment Checker

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![iOS](https://img.shields.io/badge/iOS-18.0+-blue.svg)
![Swift](https://img.shields.io/badge/swift-6.1+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-iOS%20%7C%20macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)

A powerful cross-platform tool to help students track their ManageBac assignments with intelligent analysis and notifications.

[English](README.md) | [中文](README.zh.md)

</div>

## ✨ Features

### 🖥️ Multi-Platform Support
- **iOS Native App**: Built with SwiftUI for iOS 18+
- **Desktop App**: Cross-platform GUI for Windows, macOS, and Linux
- **Command Line**: Flexible CLI interface for automation

### 🤖 Smart Analysis
- Automatic assignment deadline tracking
- Priority-based assignment sorting
- AI-powered study suggestions (OpenAI integration)
- Comprehensive statistics and visualizations

### 🔔 Intelligent Notifications
- Real-time desktop notifications
- Email alerts for upcoming deadlines
- Background task scheduling (iOS)
- Customizable notification intervals

### 📊 Rich Reporting
- Multiple export formats (HTML, JSON, Markdown)
- Interactive dashboards
- Assignment timeline visualization
- Progress tracking and statistics

## 🚀 Quick Start

### iOS App

#### Requirements
- iOS 18.0 or later
- Xcode 16+ (for development)

#### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/managebac-assignment-checker.git
cd managebac-assignment-checker
```

2. Open in Xcode:
```bash
open ManageBacChecker.xcodeproj
```

3. Build and run on your iOS device or simulator

### Python Desktop App

#### Requirements
- Python 3.8 or later
- pip package manager

#### One-Click Installation
```bash
# Linux/macOS
bash install.sh

# Windows
install.bat
```

#### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the GUI
python intelligent_launcher.py
```

## 📁 Project Structure

```
managebac-assignment-checker/
├── ManageBacChecker/              # iOS App Source
│   ├── ManageBacCheckerApp.swift  # App entry point
│   ├── ContentView.swift          # Main view
│   ├── AssignmentListView.swift   # Assignment list
│   ├── StatisticsView.swift       # Statistics dashboard
│   ├── SettingsView.swift         # Settings screen
│   └── AssignmentManager.swift    # Core business logic
├── ManageBacChecker.xcodeproj/    # Xcode project
├── Config/                        # iOS configuration
│   ├── Shared.xcconfig            # Shared build settings
│   └── ManageBacChecker.entitlements
├── managebac_checker/             # Python package
│   ├── checker.py                 # Main checker logic
│   ├── analyzer.py                # Analysis engine
│   ├── reporter.py                # Report generation
│   ├── notifier.py                # Notification system
│   └── gui.py                     # Desktop GUI
├── tests/                         # Test suite
├── scripts/                       # Helper scripts
├── docs/                          # Documentation
└── archive/                       # Historical versions

```

## 🎯 Usage

### iOS App

1. **Login**: Enter your ManageBac credentials on first launch
2. **View Assignments**: Browse your assignments sorted by priority
3. **Check Statistics**: View comprehensive statistics and charts
4. **Configure Notifications**: Customize alert preferences in Settings
5. **Background Sync**: Enable background refresh for automatic updates

### Desktop App

#### GUI Mode (Recommended)
```bash
python intelligent_launcher.py
```

#### Command Line Mode
```bash
# Check assignments
python main.py

# With custom configuration
python main.py --config my_config.env

# Generate specific report format
python main.py --format html
```

## 🔧 Configuration

### iOS App
- Configure settings within the app's Settings screen
- Credentials stored securely using iOS Keychain
- Notification preferences sync via UserDefaults

### Python App

Create a `config.env` file (or copy from `config.example.env`):

```env
# ManageBac Credentials
MANAGEBAC_EMAIL=your-email@example.com
MANAGEBAC_PASSWORD=your-password
MANAGEBAC_SCHOOL=your-school-name

# Notification Settings
ENABLE_EMAIL_NOTIFICATIONS=true
EMAIL_ADDRESS=your-email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-smtp-username
SMTP_PASSWORD=your-app-password

# AI Features (Optional)
OPENAI_API_KEY=your-openai-key
ENABLE_AI_ANALYSIS=true

# Report Settings
DEFAULT_REPORT_FORMAT=html
OUTPUT_DIRECTORY=./reports
```

## 🏗️ Architecture

### iOS App (Swift + SwiftUI)
- **Architecture**: MVVM pattern with SwiftUI
- **UI Framework**: SwiftUI with iOS 18+ features
- **Data Management**: @ObservableObject + UserDefaults
- **Background Tasks**: BGTaskScheduler
- **Notifications**: UNUserNotificationCenter
- **Web Integration**: WKWebView for ManageBac scraping

### Python Desktop App
- **Core**: Python 3.8+ with async/await
- **Web Scraping**: Playwright + BeautifulSoup4
- **GUI Framework**: tkinter with modern theming
- **AI Integration**: OpenAI GPT API
- **Testing**: pytest with factory pattern
- **Notifications**: Cross-platform notification system

## 🧪 Testing

### iOS App
```bash
# Run unit tests
xcodebuild test -scheme ManageBacChecker -destination 'platform=iOS Simulator,name=iPhone 15'

# Run UI tests
xcodebuild test -scheme ManageBacChecker -destination 'platform=iOS Simulator,name=iPhone 15' -only-testing:ManageBacCheckerUITests
```

### Python App
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=managebac_checker --cov-report=html

# Run specific test file
pytest tests/test_checker.py
```

## 📖 Documentation

- [iOS Project Overview](docs/iOS_PROJECT_FINAL_STATUS.md)
- [Installation Guide](docs/INSTALLATION_TROUBLESHOOTING.md)
- [Tutorial (中文)](docs/详细使用教程.md)
- [API Documentation](docs/API.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

### Development Setup

#### iOS Development
1. Install Xcode 16+
2. Clone the repository
3. Open `ManageBacChecker.xcodeproj`
4. Build and run

#### Python Development
1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes
5. Run tests:
   ```bash
   pytest
   ```
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**方籽杰 (Fang Zijie)**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- ManageBac platform for providing the assignment management system
- OpenAI for AI-powered analysis capabilities
- The open-source community for excellent libraries and tools

## 📊 Project Status

- ✅ Python Desktop App: **Production Ready**
- ✅ iOS Native App: **95% Complete** (App Store submission pending)
- 🔄 Android App: **Planned**
- 🔄 Web Dashboard: **Planned**

## 🐛 Bug Reports & Feature Requests

Please use [GitHub Issues](https://github.com/yourusername/managebac-assignment-checker/issues) to report bugs or request features.

## 📈 Roadmap

### Version 2.0 (Q4 2025)
- [ ] Android native app
- [ ] Web dashboard
- [ ] Multi-user support
- [ ] Advanced AI features
- [ ] Custom report templates

### Version 1.5 (Q3 2025)
- [x] iOS native app
- [x] Background task scheduling
- [x] Enhanced notifications
- [ ] iCloud sync
- [ ] Widget support

---

<div align="center">

**Made with ❤️ for students using ManageBac**

⭐ Star this repository if you find it helpful!

</div>
