from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
import wikipediaapi
import re
import json
import requests
from duckduckgo_search import DDGS
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hallucination_detector_secret_key_2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

GROQ_API_KEY = "your api key"
NEWS_API_KEY = "your api key"
client = Groq(api_key=GROQ_API_KEY)

# ── Database Models ──────────────────────────────────────────────────
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    detections = db.relationship("Detection", backref="user", lazy=True)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    hallucination_detected = db.Column(db.Boolean, nullable=False)
    severity = db.Column(db.Float, nullable=False)
    summary = db.Column(db.Text)
    sentences = db.Column(db.Text)
    hallucinated_words = db.Column(db.Text)
    hallucinated_claims = db.Column(db.Text)
    highlighted_response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── Sources ──────────────────────────────────────────────────────────
def get_wikipedia_context(query, max_chars=800):
    try:
        wiki = wikipediaapi.Wikipedia(user_agent="HallucinationDetector/1.0", language="en")
        stopwords = {"what","is","are","the","a","an","of","in","on","at","to","for","how","why","who","when","where","was","were","did","do","does","tell","me","about","explain","describe"}
        words = [w for w in re.findall(r'\b\w+\b', query.lower()) if w not in stopwords]
        candidates = [" ".join(words)]
        for i in range(len(words)):
            for j in range(i+1, len(words)+1):
                candidates.append(" ".join(words[i:j]))
        for q in candidates:
            if len(q) < 3:
                continue
            page = wiki.page(q.title())
            if page.exists():
                return f"[Wikipedia: {page.title}]\n{page.summary[:max_chars]}"
    except Exception as e:
        print(f"Wikipedia error: {e}")
    return None

def get_duckduckgo_context(query, max_results=3):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"• {r['title']}: {r['body']}")
        if results:
            return "[DuckDuckGo Web Search]\n" + "\n".join(results)
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
    return None

def get_news_context(query, max_chars=800):
    try:
        url = "https://newsapi.org/v2/everything"
        params = {"q": query, "apiKey": NEWS_API_KEY, "pageSize": 3, "sortBy": "relevancy", "language": "en"}
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get("articles"):
            articles = []
            for a in data["articles"][:3]:
                title = a.get("title", "")
                desc = a.get("description", "")
                if title and desc:
                    articles.append(f"• {title}: {desc}")
            if articles:
                return "[Recent News]\n" + "\n".join(articles)
    except Exception as e:
        print(f"NewsAPI error: {e}")
    return None

def get_wikidata_context(query):
    try:
        search_url = "https://www.wikidata.org/w/api.php"
        params = {"action": "wbsearchentities", "search": query, "language": "en", "format": "json", "limit": 1}
        res = requests.get(search_url, params=params, timeout=5)
        data = res.json()
        if not data.get("search"):
            return None
        entity_id = data["search"][0]["id"]
        entity_url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
        entity_res = requests.get(entity_url, timeout=5)
        entity_data = entity_res.json()
        entity = entity_data["entities"][entity_id]
        description = entity.get("descriptions", {}).get("en", {}).get("value", "")
        label = entity.get("labels", {}).get("en", {}).get("value", "")
        if label or description:
            return f"[Wikidata Facts]\n{label}: {description}"
    except Exception as e:
        print(f"Wikidata error: {e}")
    return None

def get_openlibrary_context(query):
    try:
        url = "https://openlibrary.org/search.json"
        params = {"q": query, "limit": 2, "fields": "title,author_name,first_publish_year"}
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        if data.get("docs"):
            results = []
            for doc in data["docs"][:2]:
                title = doc.get("title", "")
                authors = ", ".join(doc.get("author_name", [])[:2])
                year = doc.get("first_publish_year", "")
                if title:
                    results.append(f"• '{title}' by {authors} ({year})")
            if results:
                return "[Open Library]\n" + "\n".join(results)
    except Exception as e:
        print(f"Open Library error: {e}")
    return None

def get_all_context(prompt):
    sources = []
    for fn in [get_wikipedia_context, get_duckduckgo_context, get_news_context, get_wikidata_context, get_openlibrary_context]:
        result = fn(prompt)
        if result:
            sources.append(result)
    return "\n\n".join(sources) if sources else "No context found."

def highlight_words(text, hallucinated_words):
    if not hallucinated_words:
        return text
    result = text
    for word in sorted(hallucinated_words, key=len, reverse=True):
        word = word.strip()
        if not word:
            continue
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        result = pattern.sub(
            f'<mark style="background:#ff4444;color:white;padding:1px 4px;border-radius:3px;">{word}</mark>',
            result
        )
    return result

def detect_hallucinations(prompt, context, response):
    system_prompt = """You are an expert hallucination detection system.
Return ONLY a valid JSON object with this exact structure, no markdown, no extra text:
{
    "hallucination_detected": true or false,
    "severity": 0.0 to 1.0,
    "sentences": [{"text": "sentence", "hallucinated": true or false, "reason": "why"}],
    "hallucinated_words": ["word1", "word2"],
    "hallucinated_claims": ["claim1", "claim2"],
    "summary": "brief summary"
}"""
    chat = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Prompt: {prompt}\n\nContext:\n{context}\n\nAI Response: {response}\n\nReturn JSON only."}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1
    )
    raw = chat.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

# ── Auth Routes ──────────────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "error")
            return redirect(url_for("register"))
        hashed = generate_password_hash(password)
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid username or password!", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))

# ── Main Route ───────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    result = None
    prompt = ""
    response = ""
    context_mode = "auto"
    manual_context_text = ""
    highlighted_response = None
    error = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        response = request.form["response"]
        context_mode = request.form.get("context_mode", "auto")
        manual_context_text = request.form.get("manual_context_text", "")
        context_used = manual_context_text if context_mode == "manual" else get_all_context(prompt)

        try:
            result = detect_hallucinations(prompt, context_used, response)
            highlighted_response = highlight_words(response, result.get("hallucinated_words", []))

            # Save to database
            detection = Detection(
                user_id=current_user.id,
                prompt=prompt,
                response=response,
                hallucination_detected=result["hallucination_detected"],
                severity=result["severity"],
                summary=result.get("summary", ""),
                sentences=json.dumps(result.get("sentences", [])),
                hallucinated_words=json.dumps(result.get("hallucinated_words", [])),
                hallucinated_claims=json.dumps(result.get("hallucinated_claims", [])),
                highlighted_response=highlighted_response
            )
            db.session.add(detection)
            db.session.commit()

        except Exception as e:
            error = f"Error during detection: {str(e)}"

    return render_template("index.html",
        result=result,
        prompt=prompt,
        response=response,
        context_mode=context_mode,
        manual_context_text=manual_context_text,
        highlighted_response=highlighted_response,
        error=error
    )

# ── History Route ────────────────────────────────────────────────────
@app.route("/history")
@login_required
def history():
    detections = Detection.query.filter_by(user_id=current_user.id).order_by(Detection.timestamp.desc()).all()
    parsed = []
    for d in detections:
        parsed.append({
            "id": d.id,
            "prompt": d.prompt,
            "response": d.response,
            "hallucination_detected": d.hallucination_detected,
            "severity": d.severity,
            "summary": d.summary,
            "sentences": json.loads(d.sentences or "[]"),
            "hallucinated_words": json.loads(d.hallucinated_words or "[]"),
            "hallucinated_claims": json.loads(d.hallucinated_claims or "[]"),
            "highlighted_response": d.highlighted_response,
            "timestamp": d.timestamp.strftime("%d %b %Y, %I:%M %p")
        })
    return render_template("history.html", detections=parsed)

@app.route("/history/delete/<int:detection_id>")
@login_required
def delete_detection(detection_id):
    detection = Detection.query.get_or_404(detection_id)
    if detection.user_id != current_user.id:
        return redirect(url_for("history"))
    db.session.delete(detection)
    db.session.commit()
    return redirect(url_for("history"))

@app.route("/landing")
def landing():
    return render_template("landing.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)