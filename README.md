# ManageBac Assignment Checker

A Playwright-powered tool to log into ManageBac and generate rich assignment reports (Pending/Submitted/Overdue), with HTML/Markdown/JSON outputs.

> Educational use only. You must comply with your school and ManageBac terms of use.

## Features

- Automated login to ManageBac (Playwright, Chromium)
- Scrapes all assignments (Pending/Submitted/Overdue)
- Generates reports in HTML / Markdown / JSON (with visual KPIs)
- Optional detail enrichment (open assignment pages to collect description/attachments)
- Environment-based configuration (no credentials in code)

## Quickstart

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
   # MANAGEBAC_EMAIL=...
   # MANAGEBAC_PASSWORD=...
   # (optional) REPORT_FORMAT=html,markdown,json
   ```

4. Install browser engines for Playwright (first time only):
   ```bash
   playwright install chromium
   ```

5. Run the script:
   ```bash
   python main.py
   ```

### One-liners

- Generate HTML only
  ```bash
  REPORT_FORMAT=html python main.py
  ```
- Generate all formats + enrich details (open some assignment pages)
  ```bash
  FETCH_DETAILS=true DETAILS_LIMIT=8 REPORT_FORMAT=html,markdown,json python main.py
  ```

## Configuration

Set the following environment variables in your `.env` file:

- `MANAGEBAC_EMAIL`: Your ManageBac email
- `MANAGEBAC_PASSWORD`: Your ManageBac password
- `MANAGEBAC_URL`: The ManageBac URL (default: https://shtcs.managebac.cn)
- `REPORT_FORMAT`: Comma-separated formats: `console`, `html`, `markdown`, `json`
- `FETCH_DETAILS`: `true|false` open assignment pages to collect more fields
- `DETAILS_LIMIT`: Max detail pages to open (default 8)
- `OUTPUT_DIR`: Reports output dir (default `./reports`)
- `HEADLESS`: `true|false` browser headless mode
- `DEBUG`: `true|false` verbose scraping logs

## Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the assignment checker
python main.py

# Open the latest HTML report (macOS)
open $(ls -t reports/*.html | head -n 1)
```

## Notes

- This tool relies on your current ManageBac UI structure. Minor UI changes may require selector updates.
- Do not commit `.env` with credentials (already git-ignored).

## License

MIT — see LICENSE.

- Credentials are stored in `.env` file (not committed to git)
- Uses secure environment variable loading
- Browser runs in headless mode by default