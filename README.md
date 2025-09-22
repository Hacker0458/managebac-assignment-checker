# ManageBac Assignment Checker

An automated tool to check for unsubmitted assignments on ManageBac.

## Features

- Automated login to ManageBac
- Lists unsubmitted assignments
- Secure credential management using environment variables

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. Create a `.env` file (copy from `.env.example`) and add your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. Run the script:
   ```bash
   python main.py
   ```

## Configuration

Set the following environment variables in your `.env` file:

- `MANAGEBAC_EMAIL`: Your ManageBac email
- `MANAGEBAC_PASSWORD`: Your ManageBac password
- `MANAGEBAC_URL`: The ManageBac URL (default: https://shtcs.managebac.cn)

## Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the assignment checker
python main.py
```

## Security

- Credentials are stored in `.env` file (not committed to git)
- Uses secure environment variable loading
- Browser runs in headless mode by default