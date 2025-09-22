# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based web automation tool that uses Playwright to log into ManageBac (a school management system) and check for unsubmitted assignments. It's a single-file application with a focus on web scraping and credential management.

## Common Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Setup environment configuration
cp .env.example .env
# Then edit .env with actual credentials
```

### Running the Application
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run the main script
python main.py

# Run in non-headless mode for debugging (set HEADLESS=false in .env)
# Or override environment variable
HEADLESS=false python main.py
```

### Development and Testing
```bash
# Check Python syntax
python -m py_compile main.py

# Install development tools (not in requirements.txt)
pip install pylint black flake8

# Code formatting
black main.py

# Linting
pylint main.py
flake8 main.py
```

## Architecture and Code Structure

### Single-File Design
This project follows a single-file architecture pattern (`main.py`) which contains:

- **ManageBacChecker Class**: The main application class that encapsulates all functionality
- **Configuration Management**: Environment variable loading and validation using python-dotenv
- **Browser Automation**: Playwright-based web automation for ManageBac interaction
- **Error Handling**: Comprehensive exception handling for web scraping resilience

### Key Components

**Environment Configuration**:
- Uses `.env` file for secure credential storage
- Supports configurable timeouts, headless mode, and target URLs
- Validates required credentials at startup

**Login System** (`login` method):
- Robust selector-based form filling
- Multiple fallback strategies for login button detection
- URL-based success/failure detection
- Error message extraction for debugging

**Assignment Detection** (`get_unsubmitted_assignments` method):
- Multi-strategy approach using various CSS selectors
- Fallback to content parsing when specific elements aren't found
- Status-based filtering (looks for keywords like "not submitted", "unsubmitted", "pending", "overdue")
- Structured data extraction with timestamps

### Web Scraping Strategy

The application uses a defensive programming approach for web scraping:

1. **Multiple Selector Strategy**: Tries various CSS selectors for the same element types
2. **Graceful Degradation**: Falls back to content parsing if structured elements aren't found
3. **Timeout Configuration**: Configurable timeouts for different operations
4. **Error Isolation**: Individual element extraction errors don't crash the entire process

### Security Considerations

- Credentials stored only in `.env` file (git-ignored)
- No credential logging or exposure in output
- Environment variable validation at startup
- Secure browser automation practices (no credential caching)

### Browser Automation Configuration

- Uses Chromium as the browser engine
- Headless mode by default for CI/server environments
- Custom viewport size for consistent rendering
- Sandbox disabled for compatibility in restricted environments

## Development Notes

### Adding New Features

When extending this application:

1. **New Selectors**: Add CSS selectors to the existing arrays in login/assignment detection methods
2. **New Assignment Sources**: Add new selector strategies to `get_unsubmitted_assignments`
3. **Configuration Options**: Add new environment variables with defaults and update `__init__`
4. **Error Handling**: Maintain the existing pattern of try/catch with informative error messages

### Debugging Web Scraping Issues

- Set `HEADLESS=false` in `.env` to see browser automation visually
- Increase `TIMEOUT` value for slower networks
- Check browser console and network tabs for JavaScript errors or failed requests
- ManageBac's UI may change over time, requiring selector updates

### Testing Considerations

This project currently has no automated tests. When adding tests, consider:

- Mock Playwright browser interactions for unit tests
- Use test credentials or mock ManageBac responses
- Test different assignment status scenarios
- Test error conditions (wrong credentials, network failures)