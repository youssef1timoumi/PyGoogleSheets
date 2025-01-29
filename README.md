## Overview

This project consists of Python scripts that integrate with the Google Sheets API to automate client management and revenue tracking. The scripts allow for seamless data sharing between team members using a Google Spreadsheet as a lightweight remote database, eliminating the need for traditional cloud storage.

## Features

- **Google Sheets Integration**: Uses Google Sheets API to read and write data.
- **Client Management**: Handles solo clients, teams, and groups with automatic balance calculations.
- **Automated Email Notifications**: Sends notifications when clients are added or registered with a referral code.
- **Revenue Tracking**: Calculates total revenue and marketing commissions.

---

## Installation

### Prerequisites

- Python 3.x installed
- Install dependencies:

  ```bash
  pip install gspread pandas oauth2client
  ```

### Google Service Account Credentials

1. Go to **Google Cloud Console**.
2. Enable **Google Sheets API** & **Google Drive API**.
3. Generate a service account key (JSON file).  
   **DO NOT SHARE THIS FILE.**
4. Store the credentials securely and set up an environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
   ```

---

## Configuration

### Google Sheets Setup

- Update `SPREADSHEET_NAME` in `main.py` with the name of your Google Spreadsheet.
- Ensure your spreadsheet has the following sheet names:
  - `soloclient`
  - `clientteams`
  - `clientgrps`

### Email Notifications

- Update `from_email` and `password` in `services.py` (use an App Password if using Gmail with 2FA).
- Update recipient emails in `notify_client_saved` and `notify_registration_with_code`.

---

## Usage

### Run the main script to access the menu:

```bash
python main.py
```

### Available Options:

1. **Add Solo Client**  
2. **Add Team** (Requires at least 3 members, 10% discount per member)  
3. **Add Group** (Requires at least 4 members, 15% discount per member)  
4. **Calculate Marketing Revenue**  
5. **Calculate Total Revenue**  
6. **Calculate Payment for Specific User**  
7. **Exit**  

---

## Security Best Practices

- **DO NOT** expose your credentials (e.g., `credentials.json`).
- Use environment variables for sensitive data.
- Restrict access to the Google Spreadsheet to trusted accounts.

---

## Future Enhancements

- Implement a GUI for easier client management.
- Enhance logging and error handling.
- Integrate with additional APIs for extended functionality.

---

## Authors

- **Youssef Timoumi**