# JobTrace
Privacy-first, manual AI-assisted desktop tool to track job applications using screen context and Google Gemini Vision.
=======

JobTrace helps you keep a clean, structured record of your job search activities (applications, recruiter messages, job views, interviews, etc.) by turning your screen work into organized rows in Google Sheets — but **only when you tell it to analyze**.

You stay in full control. Nothing runs automatically in the background.

## Why people need something like this

Job searching usually happens across 5–10 different places:

- LinkedIn  
- Company career portals  
- Email threads with recruiters  
- WhatsApp / Telegram recruiter chats  
- Personal notes / Notion / Excel  

After 2–3 weeks most people can no longer remember:

- Which jobs they already applied to  
- When and through which link/channel  
- Who the recruiter was  
- What stage each application is in  

JobTrace solves exactly this problem — without spying on you, without running 24/7, and without trying to “guess” what you’re doing.

## What JobTrace is (and is not)

**It is**
- A small desktop program you start manually  
- Controlled completely by you (start/stop/analyze)  
- Uses Google Gemini AI only when **you** press Analyze  
- Saves clean tabular data → your own Google Sheet  
- Deletes screenshots immediately after analysis  

**It is not**
- An always-running background tool  
- A screen recorder or video maker  
- A keylogger  
- An auto-applier or job scraper  
- A replacement for GitHub Copilot / Claude / ChatGPT  

## How it works (simple flow)

1. You click “New Session” when you start job-search work  
2. While the session is active → occasional screenshots are taken  
3. When you finish the task → you click “Analyze” (or press Ctrl+Shift+Enter)  
4. Gemini AI looks at the screenshots and understands what you did  
5. It creates structured rows (company, role, action, date, etc.)  
6. Rows are added to your Google Sheet  
7. Screenshots are deleted right away  

→ You decide **when** and **what** gets analyzed.

## Main features you control

- Small icon lives in system tray (bottom-right corner on Windows)  
- Click it → small control window appears  
- Buttons:  
  • New Session  
  • Pause / Resume capture  
  • Analyze now  
- Keyboard shortcut: **Ctrl + Shift + Enter** = Analyze current session  

## Privacy & safety (very important)

| What                  | What actually happens                              |
|-----------------------|-----------------------------------------------------|
| Screen capture        | Only while you have an **active session**           |
| AI analysis           | Only when **you** click Analyze or use shortcut     |
| Screenshots           | Automatically deleted after analysis                |
| Video or audio        | Never recorded — not even an option                 |
| Data sent to Google   | Only clean structured text (JSON → Sheets)          |
| Always-on monitoring  | Does **not** exist                                  |

## Folder structure (for developers)

```
JobTrace/
├── engine/         # Controls when the app starts/stops/analyzes
├── capture/        # Takes and temporarily holds screenshots
├── llm/            # Talks to Google Gemini + cleans the output
├── sheets/         # Pushes data to your Google Sheet
├── ui/             # Tray icon + small control window (uses PySide6)
├── core/           # Keyboard shortcuts & app state
├── utils/          # Logging and small helpers
└── main.py         # Starts the whole program
```

## What gets saved in Google Sheets

Example columns:

| Timestamp           | Company       | Role                     | Recruiter     | Action          | Channel    | Confidence | Notes                             |
|---------------------|---------------|--------------------------|---------------|-----------------|------------|------------|-----------------------------------|
| 2025-04-12 14:35    | Stripe        | Senior Backend Engineer  | Sarah K.      | Application     | Website    | 0.92       | Used referral link from John      |
| 2025-04-12 15:10    | Razorpay      | Product Manager          | Priya M.      | Cold email sent | Email      | 0.95       | Replied to LinkedIn DM            |

## Setup Guide – step-by-step (especially for first-timers)

This part looks long — but most steps are one-time only and I explain everything.

### You need (minimum)

- Windows computer (macOS/Linux versions planned later)  
- Python 3.10 or newer installed  
- Internet connection  
- A Google account (Gmail is fine)  

### Step 1: Get the code

1. Go to GitHub → https://github.com/your-username/jobtrace  
2. Click green **Code** button → **Download ZIP**  
   (or if you know git: `git clone https://github.com/your-username/jobtrace.git`)  
3. Extract the ZIP file to any folder (example: `C:\Users\YourName\jobtrace`)  
4. Open that folder

### Step 2: Install Python (skip if already installed)

- Not sure if you have Python? → Open Command Prompt and type `python --version`  
- If it says “command not found” → download from https://www.python.org/downloads/  
- During install: **very important** → check “Add Python to PATH” box

### Step 3: Create virtual environment & install packages

1. Open Command Prompt (cmd)  
2. Go to your project folder:
   ```
   cd C:\Users\YourName\jobtrace
   ```
3. Create virtual environment:
   ```
   python -m venv .venv
   ```
4. Activate it:
   ```
   .venv\Scripts\activate
   ```
   (You should now see `(.venv)` at the beginning of the line)

5. Install all required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 4: Get Google Gemini API key (AI part)

1. Open browser → https://aistudio.google.com/app/apikey  
2. Sign in with Google  
3. Click **Create API key**  
4. Copy the long key that appears (looks like `AIz...`)

### Step 5: Connect to Google Sheets (storage part) – most important setup

This part gives JobTrace permission to write to **your own** Google Sheet.

1. Go to https://console.cloud.google.com  
2. Click project dropdown (top) → **New Project** → name it “jobtrace” → Create  
3. In the search bar type “Sheets API” → select **Google Sheets API** → **Enable**  
4. Search again → “Drive API” → **Google Drive API** → **Enable**  
5. Left menu → **APIs & Services** → **Credentials**  
6. Click **+ Create Credentials** → **Service account**  
7. Name: “jobtrace-sheets” → Create and Continue → skip roles → Done  
8. You’ll see the new service account → click it  
9. Go to **Keys** tab → **Add Key** → **Create new key** → **JSON** → Download  
10. Rename the downloaded file to exactly: `service_account.json`  
11. Move it into your `jobtrace` folder (same place as `main.py`)

12. Create your Google Sheet:  
    - Go to https://sheets.google.com  
    - Click **Blank** → new spreadsheet  
    - Look at URL: `https://docs.google.com/spreadsheets/d/ABC123xyz.../edit`  
    - Copy only the middle part → `ABC123xyz...` → this is your **SHEET ID**

13. Share the sheet:  
    - In Google Sheets → click **Share** (top right)  
    - Paste the service account email (you see it in service_account.json — looks like `jobtrace-sheets@jobtrace-123456.iam.gserviceaccount.com`)  
    - Give it **Editor** access → Send

### Step 6: Create .env file (last configuration)

In the `jobtrace` folder create new text file called `.env` (yes — with the dot)

Paste this and replace the values:

```env
GOOGLE_API_KEY=AIz...your-real-gemini-key-here...
GOOGLE_SHEETS_ID=ABC123xyz...your-sheet-id-here...
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
```

Save it.

### Step 7: Run JobTrace

In the same Command Prompt (make sure `.venv` is active):

```bash
python main.py
```

→ You should see a small icon appear in the system tray (bottom right)

→ Right-click icon → open control panel → click **New Session** to start

## Quick start after setup

1. Right-click tray icon → open panel  
2. Click **New Session**  
3. Do your job applications, emails, LinkedIn browsing normally  
4. When finished → click **Analyze** or press **Ctrl + Shift + Enter**  
5. Wait 10–40 seconds → open your Google Sheet → new rows should appear  

## Common first-time questions

- “Nothing happens after python main.py” → check tray (sometimes hidden — click ^ arrow)  
- “I don’t see the Analyze button working” → make sure session is active (green indicator)  
- “Gemini gives weird results” → try clearer windows, bigger text, fewer tabs open  

## License

MIT License — see [LICENSE](LICENSE) file

## Questions or problems?

Open an issue on GitHub — even if you’re just confused.  
We especially welcome feedback from first-time users.

Happy (organized) job hunting! 🚀
