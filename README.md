# HALLUCINATION-DETECTION-IN-LLM
Used for detecting hallucination in any LLM comparing by 5 real-time sources
# FACTRA — AI Hallucination Detection System

> **Fact-checking & Automated Cross-reference Tool for Response Analysis**

FACTRA is a web-based AI hallucination detection system. Paste any response from ChatGPT, Gemini, Claude, Llama, or any other AI — FACTRA cross-checks it against **5 real-time trusted sources** and highlights exactly which words and sentences are hallucinated, with a severity score. Results in **2–5 seconds**.

---

> Dark and light theme supported. Toggle in the navbar.

---

## ✨ Features

- 🔍 **Word-level hallucination highlighting** — specific words marked in red
- 📋 **Sentence-by-sentence analysis** — each sentence rated individually
- 📊 **Severity score** — 0–100% rating of how hallucinated the response is
- 🌐 **5 real-time context sources** — Wikipedia, DuckDuckGo, NewsAPI, Wikidata, Open Library
- ⚡ **Results in 2–5 seconds** — powered by Groq's ultra-fast LLM inference
- 🔐 **User accounts** — register, login, and view your own detection history
- 📜 **Detection history** — every check saved with full details per user
- 🌗 **Dark & Light theme** — toggle in navbar, saved in browser
- 🏠 **Landing page** — professional SaaS-style landing page

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS (custom dark/light theme), JavaScript |
| Backend | Python, Flask |
| Authentication | Flask-Login, Werkzeug (password hashing) |
| Database | SQLite via Flask-SQLAlchemy |
| LLM Inference | Groq API (llama-3.3-70b-versatile) |
| Context Sources | Wikipedia API, DuckDuckGo Search, NewsAPI, Wikidata, Open Library |

---

## 📁 Project Structure

```
factra/
│
├── fast_app.py               # Main Flask app — all routes, logic, API calls
│
├── static/
│   ├── style.css             # Styles for login, register, detect, history pages
│   ├── landing.css           # Styles for landing page
│   └── theme.js              # Dark/light theme toggle logic + localStorage
│
├── templates/
│   ├── landing.html          # Public landing page
│   ├── login.html            # Login page
│   ├── register.html         # Register page
│   ├── index.html            # Main detection page (requires login)
│   └── history.html          # Detection history page (requires login)
│
├── database.db               # SQLite database (auto-created on first run)
├── requirements.txt          # All Python dependencies
└── README.md                 # This file
```

---

## ⚙️ Prerequisites

Before you start, make sure you have:

- **Python 3.9+** → [Download here](https://python.org)
- **VS Code** (recommended) → [Download here](https://code.visualstudio.com)
- **Git** (optional, for cloning) → [Download here](https://git-scm.com)

---

## 🔑 API Keys Required

FACTRA needs **2 free API keys**:

### 1. Groq API Key (for LLM inference)
1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for free
3. Click **API Keys → Create API Key**
4. Copy the key (starts with `gsk_...`)

### 2. NewsAPI Key (for news context)
1. Go to [https://newsapi.org](https://newsapi.org)
2. Click **Get API Key** and sign up free
3. Copy your API key
4. Free tier: **100 requests/day** (resets every 24 hours)

---

## 🚀 Installation & Setup

### Step 1 — Clone or Download the Project

**Option A — Clone with Git:**
```bash
git clone https://github.com/yourusername/factra.git
cd factra
```

**Option B — Download ZIP:**
- Click **Code → Download ZIP** on GitHub
- Extract the folder
- Open it in VS Code

---

### Step 2 — Open in VS Code

```
File → Open Folder → Select the factra folder → Open
```

---

### Step 3 — Open VS Code Terminal

Press **Ctrl + `** (backtick) to open the terminal inside VS Code.

---

### Step 4 — Create Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

Windows:
```bash
# If you get a security error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line. ✅

---

### Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 6 — Add Your API Keys

Open `fast_app.py` and find these two lines near the top:

```python
GROQ_API_KEY = "your api key"
NEWS_API_KEY = "your api key"
```

Replace with your actual keys:

```python
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NEWS_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Save the file with **Ctrl + S**.

---

### Step 7 — Run the App

```bash
python fast_app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
* Debugger is active!
```

---

### Step 8 — Open in Browser

Go to:
```
http://127.0.0.1:5001/landing
```

You'll see the FACTRA landing page. Click **Get started free** to register and start detecting! 🎉

---

## 🖱️ One-Click Launch (Windows only)

Create a file called `start.bat` in the project folder:

```bat
@echo off
cd /d C:\path\to\your\factra
call venv\Scripts\activate
start chrome http://127.0.0.1:5001/landing
python fast_app.py
pause
```

Replace `C:\path\to\your\factra` with your actual folder path.

Now just **double-click `start.bat`** to launch the app anytime — no terminal needed!

---

## 📖 How to Use

1. **Register** — create a free account at `/register`
2. **Login** — sign in at `/login`
3. **Detect** — on the main page:
   - Paste your **prompt** (the question you asked the AI)
   - Paste the **AI response** you want to check
   - Choose **Auto-fetch** (recommended) or provide your own context
   - Click **Detect Hallucinations**
4. **View Results** — see highlighted words, sentence analysis, severity score
5. **History** — click **History** in the navbar to see all past detections

---

## 🌐 Context Sources

FACTRA automatically fetches context from these 5 sources:

| Source | Type | API Key Needed |
|---|---|---|
| Wikipedia | Encyclopedic knowledge | ❌ No |
| DuckDuckGo | Live web search | ❌ No |
| NewsAPI | Recent news articles | ✅ Yes (free) |
| Wikidata | Structured facts & entities | ❌ No |
| Open Library | Books & literature | ❌ No |

---

## 📊 Understanding Results

| Result | Meaning |
|---|---|
| 🚨 Hallucination Detected | The AI made something up |
| ✅ No Hallucinations | Response looks accurate |
| Severity % | 0% = clean · 100% = heavily hallucinated |
| Red highlighted words | Specific hallucinated words/phrases |
| ❌ Sentence | That sentence is hallucinated |
| ✅ Sentence | That sentence looks accurate |
| 💡 Reason | Why the sentence is flagged |

---

## 🗄️ Database Schema

FACTRA uses SQLite with two tables:

**User table:**
```
id          INTEGER  PRIMARY KEY
username    TEXT     UNIQUE
password    TEXT     (hashed with Werkzeug)
```

**Detection table:**
```
id                      INTEGER  PRIMARY KEY
user_id                 INTEGER  FOREIGN KEY → user.id
prompt                  TEXT
response                TEXT
hallucination_detected  BOOLEAN
severity                FLOAT
summary                 TEXT
sentences               TEXT     (JSON)
hallucinated_words      TEXT     (JSON)
hallucinated_claims     TEXT     (JSON)
highlighted_response    TEXT
timestamp               DATETIME
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `venv\Scripts\activate` fails | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first |
| `ModuleNotFoundError` | Make sure `(venv)` is showing and run `pip install -r requirements.txt` |
| `Site can't be reached` | Wait for terminal to show `Running on http://127.0.0.1:5001` first |
| No results / loading forever | Check your Groq API key is correct in `fast_app.py` |
| `database.db` not created | Run `python fast_app.py` at least once — it auto-creates on startup |
| NewsAPI returns nothing | You may have hit the 100/day free limit — resets at midnight |
| DuckDuckGo fails | Temporary rate limit — wait a few minutes and try again |

---

## 📦 Dependencies

All dependencies are in `requirements.txt`. Key packages:

```
flask
flask-login
flask-sqlalchemy
werkzeug
groq
wikipedia-api
duckduckgo-search
requests
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🔒 Security Notes

- Passwords are **hashed** using Werkzeug's `generate_password_hash` — never stored in plain text
- Each user can only see **their own** detection history
- API keys are stored in `fast_app.py` — **do not commit your API keys to GitHub**
- Add this to your `.gitignore` before pushing:

```gitignore
venv/
database.db
__pycache__/
*.pyc
.env
```

---

## 🚧 Known Limitations

- Requires **active internet connection** for context fetching
- NewsAPI limited to **100 requests/day** on free tier
- Works best with **English** prompts and responses
- Very recent events (last 24–48 hours) may not be in Wikipedia/Wikidata yet
- The LLM judge can itself make mistakes on highly niche topics

---

## 🔮 Future Scope

- [ ] Chrome Extension — detect hallucinations directly on any webpage
- [ ] Multi-language support (Hindi, Spanish, French etc.)
- [ ] Compare mode — check same prompt across multiple AIs side by side
- [ ] PDF export of hallucination reports
- [ ] Public FACTRA API for developers
- [ ] Domain-specific models (medical, legal, finance)
- [ ] Accuracy benchmarking against HaluEval / TruthfulQA datasets

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👤 Author

**Shreshth**
- 3rd Year B.Tech AI Engineering Student
- Built with Flask, Groq API, and 5 real-time sources

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — ultra-fast LLM inference
- [Wikipedia API](https://pypi.org/project/Wikipedia-API/) — encyclopedic context
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) — web search context
- [NewsAPI](https://newsapi.org) — news context
- [Wikidata](https://wikidata.org) — structured facts
- [Open Library](https://openlibrary.org) — book data
- [HDM-2](https://github.com/aimonlabs/hallucination-detection-model) — original inspiration for this project

---

<div align="center">
  <strong>FACT<span style="color:#00e676">RA</span></strong> — Stop trusting AI blindly.
</div>
