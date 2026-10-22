# ResumeForge — AI Resume Analyzer

An end-to-end resume analyzer: Django backend + SQLite database, signup/login
auth, a landing page, and a Python ML pipeline (scikit-learn TF‑IDF matching
+ rule-based skill/section extraction) that scores an uploaded resume
against an optional job description.

## Features

- **Landing page** — marketing page explaining the product.
- **Sign up / Log in / Log out** — Django's built-in auth system, extended
  with a custom sign-up form (email, first/last name).
- **Dashboard** — stats (total analyses, average score, best score) and a
  table of recent resume analyses.
- **Resume upload & analysis** — upload a PDF / DOCX / TXT resume, optionally
  paste a job description, and get:
  - An overall score (0–100)
  - Keyword-match score (TF‑IDF cosine similarity vs. the job description)
  - Structure score (Education / Experience / Skills / Projects /
    Certifications / Contact info sections detected)
  - Contact-info score (email & phone detected)
  - Readability score (resume length + action-verb usage)
  - Skills detected, grouped by category (140+ keyword skills DB)
  - Matched vs. missing skills against the job description
  - Ranked, actionable suggestions
- **History** — view or delete past analyses.
- **Database** — Django ORM on SQLite (`db.sqlite3`, zero external setup).

## Tech stack

| Layer      | Tech                                             |
|------------|---------------------------------------------------|
| Backend    | Django 5                                          |
| Database   | SQLite (Django's default DB backend)              |
| ML / NLP   | scikit-learn (TF‑IDF + cosine similarity), regex-based rule engine |
| File parsing | pdfplumber / pypdf (PDF), python-docx (DOCX)    |
| Frontend   | Django templates, vanilla CSS (no build step)     |

## Project structure

```
resume_analyzer_project/
├── manage.py
├── requirements.txt
├── db.sqlite3                # created after migrate
├── resume_analyzer/          # Django project (settings, urls)
├── core/                     # landing page, signup, login, dashboard
│   ├── templates/
│   │   ├── base.html
│   │   ├── core/ (landing.html, dashboard.html)
│   │   └── registration/ (login.html, signup.html)
│   └── static/core/css/style.css
├── analyzer/                 # resume upload + ML analysis app
│   ├── models.py             # Resume model
│   ├── forms.py
│   ├── views.py
│   ├── ml/
│   │   ├── extractor.py      # PDF/DOCX/TXT text extraction
│   │   ├── skills_data.py    # skills keyword database
│   │   └── analyzer.py       # scoring engine (TF-IDF + heuristics)
│   └── templates/analyzer/ (upload.html, result.html, history.html)
└── .vscode/                  # VS Code run/debug config
```

## Setup — Run in VS Code

### 1. Open the project

Unzip the project, then in VS Code: **File → Open Folder...** and select the
`resume_analyzer_project` folder (this is your workspace root).

### 2. Create a virtual environment

Open a terminal in VS Code (`` Ctrl+` `` / `` Cmd+` ``) at the project root:

```bash
python3 -m venv venv

# Activate it:
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```

VS Code should prompt you to select this interpreter — click **Yes**, or
select it manually via **Python: Select Interpreter** (`Ctrl+Shift+P`) →
choose `./venv/bin/python`.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates `db.sqlite3` with all tables (users, sessions, resumes, etc.).

### 5. Create an admin account (optional, for `/admin/`)

```bash
python manage.py createsuperuser
```

### 6. Run the server

Either:

```bash
python manage.py runserver
```

…or in VS Code press **F5** (uses the included `.vscode/launch.json` "Django:
Run Server" configuration — requires the **Python** + **Python Debugger**
extensions, listed in `.vscode/extensions.json`).

Then open **http://127.0.0.1:8000/** in your browser.

### 7. Try it out

1. Go to the landing page → **Sign up free**.
2. Create an account.
3. Click **Analyze** → upload a resume (PDF/DOCX/TXT) → optionally paste a
   job description → **Run analysis**.
4. View your score breakdown, matched/missing skills, and suggestions.
5. Check **Dashboard** / **History** for past analyses.
6. Visit `/admin/` and log in with your superuser to browse raw data.

## Notes

- `DEBUG = True` and the `SECRET_KEY` in `resume_analyzer/settings.py` are
  set for local development only — **change both before deploying**.
- Uploaded resumes are stored under `media/resumes/user_<id>/`.
- Max upload size is 5MB (enforced in `analyzer/forms.py`).
- The skills database is in `analyzer/ml/skills_data.py` — extend the
  category lists there to recognize more keywords.
