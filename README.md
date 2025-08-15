# 6sense Full Automation with Persona Extraction

This script (`6sense_full_persona_automation.py`) automates the extraction of company and persona (people) data from the 6sense platform, including intent and location insights. It outputs a CSV file with all relevant company and persona information.

## Features
- Fetches all companies matching your filters from 6sense.
- For each company, extracts:
  - Company name, location, website, size, LinkedIn URL
  - Intent and intent location
- For each company, fetches up to 5 personas (people):
  - First name, last name, LinkedIn URL (employee), role/title
  - E-mail address is always set to "skipped"
- Outputs one row per persona per company (or a row with persona columns as '-' if no personas found).

## Requirements
- Python 3.8+
- `requests`, `pandas`

Install requirements:
```
pip install -r requirements.txt
```

## Authentication Setup
This script requires valid 6sense session cookies and CSRF token. You must update these values in the script before running:

1. **Log in to 6sense in your browser.**
2. **Open DevTools → Network tab.**
3. **Find a request to the company list API** (e.g., `/charcoal-sales/.../filterset/live_query/objects/account/`).
4. **Copy these values:**
   - `cf_clearance` (from cookies)
   - `__Secure-6sisession` (from cookies)
   - `x-csrftoken` (from request headers)
5. **Paste them into the script** in the `self.cookies` and `self.headers` sections in the `__init__` method.

> **Note:** Tokens must be from the same session/tab as the company list, not the persona tab.

## Usage
Run the script from the command line:
```
python 6sense_full_persona_automation.py
```

The script will fetch all available companies and personas, and save the results to a timestamped CSV file (e.g., `6sense_full_persona_api_data_20250703_153000.csv`).

## Output
The CSV will contain columns:
- First name
- Last name
- LinkedIn URL (Employee)
- E-mail address
- Role/Title
- Company name
- Company location
- Company website URL
- Company LinkedIn URL
- Company size
- Intent
- Intent location

## Troubleshooting
- **401 Unauthorized / No data found:**
  - Double-check your cookies and CSRF token are correct and not expired.
  - Make sure you are logged in and copying from the correct tab/session.
  - If you get logged out, repeat the authentication steps above.
- **No personas for some companies:**
  - Some companies may not have any personas available in 6sense.

## Customization
- To limit the number of companies for testing, edit the `run_automation` method and set `max_pages`.
- To change filters, edit the payload in `get_company_finder_payload`.

---

For any issues or improvements, please contact your automation maintainer. 
