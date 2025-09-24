#!/bin/bash

# ========================================
# 🔧 ManageBac Assignment Checker - 快速修复脚本
# Quick Installation Fix Script
# ========================================

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo -e "${BLUE}"
echo "========================================"
echo "🔧 ManageBac Assignment Checker"
echo "   Quick Installation Fix"
echo "========================================"
echo -e "${NC}"

# Function to detect Python
detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        print_error "Python 3 not found! Please install Python 3.9+"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_success "Found Python: $PYTHON_VERSION"
}

# Fix 1: Create requirements.txt if missing
fix_requirements() {
    print_info "Fixing requirements.txt issue..."

    if [ ! -f "requirements.txt" ] || [ ! -s "requirements.txt" ]; then
        print_warning "Creating fallback requirements.txt..."
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
        print_success "Fallback requirements.txt created"
    else
        print_success "requirements.txt already exists and is valid"
    fi
}

# Fix 2: Install dependencies one by one
fix_dependencies() {
    print_info "Installing dependencies with error recovery..."

    # Upgrade pip first
    $PIP_CMD install --upgrade pip

    # Core packages that must succeed
    CORE_PACKAGES=(
        "playwright>=1.45.0"
        "python-dotenv>=1.0.0"
    )

    for package in "${CORE_PACKAGES[@]}"; do
        print_info "Installing core package: $package"
        if $PIP_CMD install "$package"; then
            print_success "✓ $package"
        else
            print_error "Failed to install $package - this is required!"
            exit 1
        fi
    done

    # Optional packages
    OPTIONAL_PACKAGES=(
        "jinja2>=3.1.4"
        "openai>=1.0.0"
        "pystray>=0.19.0"
        "pillow>=10.0.0"
    )

    for package in "${OPTIONAL_PACKAGES[@]}"; do
        print_info "Installing optional package: $package"
        if $PIP_CMD install "$package"; then
            print_success "✓ $package"
        else
            print_warning "⚠️ Failed to install $package (optional)"
        fi
    done

    print_success "Dependency installation completed"
}

# Fix 3: Setup Playwright browsers
fix_playwright() {
    print_info "Setting up Playwright browsers..."

    if $PYTHON_CMD -m playwright install chromium; then
        print_success "Playwright browsers installed"
    else
        print_warning "Playwright browser installation failed"
        print_info "You can try manually later: python3 -m playwright install chromium"
    fi
}

# Fix 4: Create project structure
fix_structure() {
    print_info "Creating project structure..."

    # Create directories
    mkdir -p logs cache reports managebac_checker

    # Create basic config if missing
    if [ ! -f ".env" ]; then
        if [ -f "config.example.env" ]; then
            cp config.example.env .env
            print_success "Environment config created from example"
        else
            cat > .env << 'EOF'
# ManageBac Configuration
MANAGEBAC_EMAIL=your_email@school.edu
MANAGEBAC_PASSWORD=your_password
MANAGEBAC_URL=https://your_school.managebac.com
HEADLESS=true
DEBUG=false
REPORT_FORMAT=console,json
OUTPUT_DIR=./reports
ENABLE_NOTIFICATIONS=false
EOF
            print_success "Basic environment config created"
        fi
    fi

    print_success "Project structure verified"
}

# Fix 5: Test installation
test_installation() {
    print_info "Testing installation..."

    # Test Python imports
    if $PYTHON_CMD -c "import playwright; print('Playwright OK')" 2>/dev/null; then
        print_success "Playwright import successful"
    else
        print_error "Playwright import failed"
        return 1
    fi

    if $PYTHON_CMD -c "import dotenv; print('python-dotenv OK')" 2>/dev/null; then
        print_success "python-dotenv import successful"
    else
        print_warning "python-dotenv import failed"
    fi

    print_success "Installation test completed"
}

# Main execution
main() {
    detect_python

    print_info "Starting installation fixes..."

    fix_requirements
    fix_dependencies
    fix_playwright
    fix_structure
    test_installation

    echo -e "${GREEN}"
    echo "========================================"
    echo "✅ Installation Fix Completed!"
    echo "========================================"
    echo -e "${NC}"

    print_info "Next steps:"
    echo "1. Edit .env file with your ManageBac credentials"
    echo "2. Run: python3 gui_launcher.py (if available)"
    echo "3. Or run: python3 main_new.py (if available)"
    echo ""
    print_success "Your installation should now work correctly!"
}

# Run main function
main "$@"