# Contributing to ManageBac Assignment Checker

Thank you for your interest in contributing to ManageBac Assignment Checker! This document provides guidelines and instructions for contributing to the project.

## 🌟 Ways to Contribute

- 🐛 **Report Bugs**: Help us identify and fix issues
- 💡 **Suggest Features**: Share ideas for new features or improvements
- 📝 **Improve Documentation**: Help make our docs clearer and more comprehensive
- 🔧 **Submit Code**: Fix bugs or implement new features
- 🌍 **Translate**: Help make the app available in more languages
- 🎨 **Design**: Contribute UI/UX improvements

## 🚀 Getting Started

### Prerequisites

#### For Python Development
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

#### For iOS Development
- macOS with Xcode 16+
- iOS 18.0+ SDK
- Swift 6.1+

### Setting Up Development Environment

#### Python Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/managebac-assignment-checker.git
cd managebac-assignment-checker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### iOS Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/managebac-assignment-checker.git
cd managebac-assignment-checker

# Open in Xcode
open ManageBacChecker.xcodeproj

# Build and run (Cmd+R)
```

## 📋 Development Workflow

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/yourusername/managebac-assignment-checker.git
   ```

### 2. Create a Branch

Create a feature branch for your changes:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 3. Make Your Changes

#### Code Style

**Python:**
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

**Swift:**
- Follow Swift API Design Guidelines
- Use SwiftUI best practices
- Follow MVVM architecture pattern
- Use async/await for asynchronous operations

#### Testing

**Python:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=managebac_checker --cov-report=html

# Run specific test file
pytest tests/test_checker.py
```

**iOS:**
```bash
# Run tests in Xcode
xcodebuild test -scheme ManageBacChecker -destination 'platform=iOS Simulator,name=iPhone 15'
```

#### Code Quality

**Python:**
```bash
# Format code
black managebac_checker/

# Lint code
flake8 managebac_checker/

# Type checking
mypy managebac_checker/
```

### 4. Commit Your Changes

Write clear, descriptive commit messages:
```bash
git add .
git commit -m "feat: add new assignment filtering feature"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

Pull Request Guidelines:
- Provide a clear title and description
- Link related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation if needed

## 🧪 Testing Guidelines

### Writing Tests

**Python:**
```python
import pytest
from managebac_checker import Checker

def test_assignment_detection():
    """Test that assignments are correctly detected."""
    checker = Checker()
    assignments = checker.get_assignments()
    assert len(assignments) > 0
    assert all(hasattr(a, 'title') for a in assignments)
```

**Swift:**
```swift
import Testing
@testable import ManageBacChecker

@Test func testAssignmentSorting() {
    let manager = AssignmentManager()
    let assignments = [/* test data */]
    let sorted = manager.sortByPriority(assignments)
    #expect(sorted.first?.priority == .high)
}
```

### Test Coverage

- Aim for at least 80% code coverage
- Write tests for edge cases
- Test error handling
- Test async operations

## 📝 Documentation Guidelines

### Code Documentation

**Python:**
```python
def fetch_assignments(email: str, password: str) -> List[Assignment]:
    """
    Fetch assignments from ManageBac.
    
    Args:
        email: User's ManageBac email
        password: User's ManageBac password
        
    Returns:
        List of Assignment objects
        
    Raises:
        AuthenticationError: If credentials are invalid
        NetworkError: If connection fails
    """
    pass
```

**Swift:**
```swift
/// Fetches assignments from ManageBac server.
///
/// - Parameters:
///   - forceRefresh: Whether to bypass cache and force a fresh fetch
/// - Returns: Array of assignments sorted by due date
/// - Throws: NetworkError if request fails
func fetchAssignments(forceRefresh: Bool = false) async throws -> [Assignment] {
    // Implementation
}
```

### User Documentation

When updating user-facing features:
- Update README.md
- Add entries to CHANGELOG.md
- Update relevant documentation in `docs/`
- Include screenshots for UI changes

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Gather relevant information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., iOS 18.0, macOS 14.0, Windows 11]
- App version: [e.g., 2.1.0]
- Python version: [if applicable]

**Additional context**
Any other relevant information.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context, screenshots, or examples.
```

## 🎨 UI/UX Contributions

When contributing UI changes:
- Follow iOS Human Interface Guidelines
- Maintain consistency with existing design
- Ensure accessibility compliance
- Test on multiple screen sizes
- Include before/after screenshots

## 🌍 Translation Contributions

To add or improve translations:
1. Check existing language files
2. Follow the existing format
3. Test the translation in context
4. Ensure proper encoding (UTF-8)

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community

**Unacceptable behavior includes:**
- Trolling, insulting comments, or personal attacks
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 📞 Getting Help

- 📧 Email: your.email@example.com
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/managebac-assignment-checker/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/managebac-assignment-checker/issues)

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Project README
- Release notes

Thank you for contributing to ManageBac Assignment Checker! 🎉

---

<div align="center">

**Questions?** Feel free to ask in [GitHub Discussions](https://github.com/yourusername/managebac-assignment-checker/discussions)

</div>

