#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import os
import random
import json
import re

import feedparser
import requests

TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TG_TOKEN or TG_CHAT_ID is not defined")

# ---------------- FILE PATHS ----------------
QURAN_STATE_FILE = Path.home() / ".morning_brief_quran_state"
BOOK_STATE_FILE = Path.home() / ".morning_brief_book_state"
POEM_STATE_FILE = Path.home() / ".morning_brief_poem_state"
AI_LIMIT_FILE = Path.home() / ".morning_brief_ai_usage"

QURAN_API_BASE = "https://api.alquran.cloud/v1"
QURAN_EDITIONS = [
    "en.asad",
    "en.pickthall",
    "en.yusufali",
]
TOTAL_AYAHS = 6236

# ---------------- HELPERS ----------------
def safe_openai_text_response(response_json):
    try:
        return response_json["output"][0]["content"][0]["text"].strip()
    except Exception:
        return None

def load_json_file(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default

def save_json_file(path: Path, data):
    try:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def can_use_ai():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        if AI_LIMIT_FILE.exists():
            date_str, count_str = AI_LIMIT_FILE.read_text(encoding="utf-8").split("|")
            if date_str == today:
                return int(count_str) < 2
    except Exception:
        pass
    return True

def register_ai_call():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        count = 1
        if AI_LIMIT_FILE.exists():
            date_str, count_str = AI_LIMIT_FILE.read_text(encoding="utf-8").split("|")
            if date_str == today:
                count = int(count_str) + 1
        AI_LIMIT_FILE.write_text(f"{today}|{count}", encoding="utf-8")
    except Exception:
        pass

def ask_openai(prompt: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not can_use_ai():
        return None

    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-5.4-mini",
                "input": prompt,
            },
            timeout=20,
        )

        if response.status_code != 200:
            return None

        data = response.json()
        out = safe_openai_text_response(data)
        if out:
            register_ai_call()
            return out
        return None
    except Exception:
        return None

# ---------------- SMART FALLBACKS ----------------
def build_smart_aein_fallback(news):
    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", []) + news.get("cloud_platform", [])
    full_text = " ".join(headlines).lower()

    revenue = 5
    execution = 7
    strategic = 5
    urgency = 5

    revenue_keywords = ["ipo", "valuation", "investment", "revenue", "market", "growth", "business", "deal"]
    strategic_keywords = ["ai", "cloud", "chip", "data", "automation", "platform", "technology", "kubernetes", "openshift", "telco"]
    urgent_keywords = ["war", "strike", "attack", "fires", "warning", "crisis", "iran", "tehran", "military"]
    difficulty_keywords = ["tariff", "sanction", "regulation", "warning", "crisis", "conflict", "pharmaceutical"]

    for k in revenue_keywords:
        if k in full_text:
            revenue += 1
    for k in strategic_keywords:
        if k in full_text:
            strategic += 1
    for k in urgent_keywords:
        if k in full_text:
            urgency += 1
    for k in difficulty_keywords:
        if k in full_text:
            execution -= 1

    revenue = max(4, min(revenue, 9))
    execution = max(3, min(execution, 9))
    strategic = max(4, min(strategic, 10))
    urgency = max(4, min(urgency, 10))

    if urgency >= 8:
        theme = "Geopolitical pressure and technology-market dynamics must be managed at the same time."
        risk = "The risk of distraction and reactive decision-making is increasing."
    elif strategic >= 8:
        theme = "Technology-led developments are creating a strong strategic positioning moment."
        risk = "Poor prioritization could waste a valuable opportunity window."
    else:
        theme = "Macro pressure and business priorities should be read together."
        risk = "A fragmented agenda can create loss of focus."

    if strategic >= 8 and revenue >= 7:
        opportunity = "AI, cloud, and platform trends are creating both strategic and commercial opportunity."
    elif revenue >= 7:
        opportunity = "Market movement may open new revenue and offer opportunities."
    else:
        opportunity = "Operational efficiency and focused execution can create advantage."

    if urgency >= 8:
        recommendation = "Simplify the day with a risk and priority filter instead of tracking every headline."
        decision = "Choose one critical decision area and place all other topics second."
    elif strategic >= 8:
        recommendation = "Map AI and cloud developments directly to high-impact business outcomes."
        decision = "Turn one high strategic-fit topic into concrete action today."
    else:
        recommendation = "Narrow the agenda using revenue, delivery, and strategic-fit filters."
        decision = "Advance the one topic with the highest business impact today."

    return (
        f"Theme: {theme}\n"
        f"Risk: {risk}\n"
        f"Opportunity: {opportunity}\n\n"
        f"Score:\n"
        f"- Revenue Impact: {revenue}/10\n"
        f"- Execution Ease: {execution}/10\n"
        f"- Strategic Fit: {strategic}/10\n"
        f"- Urgency: {urgency}/10\n\n"
        f"Recommendation: {recommendation}\n"
        f"Decision: {decision}"
    )

def build_smart_exec_fallback(news):
    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", []) + news.get("cloud_platform", [])
    full = " ".join(headlines).lower()

    if any(k in full for k in ["war", "iran", "attack", "strike", "crisis", "military"]):
        theme = "Geopolitical risks are directly affecting technology and markets."
        risk = "Reactive decision-making and energy-cost pressure."
        opportunity = "The right positioning creates advantage during uncertainty."
    elif any(k in full for k in ["ai", "cloud", "chip", "data", "platform"]):
        theme = "AI and cloud investments are at the center of competition."
        risk = "Misallocation of investment."
        opportunity = "Efficiency and scalability advantage."
    else:
        theme = "Macro conditions and technology dynamics are moving together."
        risk = "Loss of focus."
        opportunity = "Operational efficiency."

    return (
        f"Theme: {theme}\n"
        f"Risk: {risk}\n"
        f"Opportunity: {opportunity}\n"
        f"Today's Recommendation:\n"
        f"- Do: Simplify the agenda and choose one main objective.\n"
        f"- Watch: Avoid spreading attention across low-value tasks.\n"
        f"- Track: The intersection of AI, cloud, and market dynamics."
    )

def build_smart_english(news):
    headlines = " ".join(news.get("global", []) + news.get("technology", []) + news.get("cloud_platform", [])).lower()

    if "ai" in headlines or "cloud" in headlines:
        return (
            "Phrasal verb: scale up - to expand at scale\n"
            "Idiom: stay ahead of the curve - to stay ahead of trends\n"
            "Business expression: digital transformation - digital transformation\n"
            "Example: Companies must scale up AI capabilities to stay ahead of the curve."
        )
    elif "war" in headlines or "crisis" in headlines or "iran" in headlines:
        return (
            "Phrasal verb: brace for - to prepare for\n"
            "Idiom: in troubled waters - in a difficult situation\n"
            "Business expression: risk management - risk management\n"
            "Example: Firms must brace for uncertainty when they are in troubled waters."
        )
    else:
        return (
            "Phrasal verb: move forward - to continue progressing\n"
            "Idiom: keep the momentum - to maintain momentum\n"
            "Business expression: operational efficiency - operational efficiency\n"
            "Example: Teams must move forward while keeping the momentum."
        )

# ---------------- AI OUTPUTS ----------------
def generate_ai_insight(news):
    fallback = build_smart_exec_fallback(news)

    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", []) + news.get("cloud_platform", [])
    prompt = (
        "You are a strategic executive advisor.\n\n"
        f"Headlines:\n{headlines}\n\n"
        "Write in English.\n"
        "Output exactly in this format:\n"
        "Theme:\n"
        "Risk:\n"
        "Opportunity:\n"
        "Today's Recommendation:\n"
        "- Do:\n"
        "- Watch:\n"
        "- Track:\n"
        "Keep it concise and executive-level.\n"
    )

    out = ask_openai(prompt)
    return out if out else fallback

def generate_aein_decision(news):
    fallback = build_smart_aein_fallback(news)

    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", []) + news.get("cloud_platform", [])
    prompt = (
        "You are an executive decision engine.\n\n"
        "Decision filters:\n"
        "- Does it create revenue?\n"
        "- Does it improve delivery capability?\n"
        "- Does it contribute to a scalable model?\n"
        "- Does it strengthen strategic position?\n"
        "- Is it worth the time, energy, and cost?\n\n"
        f"Evaluate these headlines:\n{headlines}\n\n"
        "Write in English.\n"
        "Output format:\n"
        "Theme:\n"
        "Risk:\n"
        "Opportunity:\n\n"
        "Score:\n"
        "- Revenue Impact: X/10\n"
        "- Execution Ease: X/10\n"
        "- Strategic Fit: X/10\n"
        "- Urgency: X/10\n\n"
        "Recommendation:\n"
        "Decision:\n"
        "Do not repeat the headlines.\n"
    )

    out = ask_openai(prompt)
    return out if out else fallback

# ---------------- AI ENGLISH BOOSTER ----------------
ENGLISH_FALLBACKS = [
    {
        "phrasal": ("scale up", "to expand at scale"),
        "idiom": ("move the needle", "to make a meaningful impact"),
        "business": ("cost discipline", "cost discipline"),
        "example": "We need to scale up carefully if we want to move the needle without losing cost discipline."
    },
    {
        "phrasal": ("roll out", "to launch or deploy"),
        "idiom": ("on the same page", "to be aligned"),
        "business": ("operational efficiency", "operational efficiency"),
        "example": "Before we roll out the platform, all teams must be on the same page."
    },
    {
        "phrasal": ("cut back", "to reduce or cut back"),
        "idiom": ("brace for impact", "to prepare for impact"),
        "business": ("risk exposure", "risk exposure"),
        "example": "Firms may cut back investment and brace for impact when risk exposure rises."
    },
    {
        "phrasal": ("phase out", "to remove gradually"),
        "idiom": ("in the driver's seat", "to be in control"),
        "business": ("strategic alignment", "strategic alignment"),
        "example": "A company stays in the driver's seat when it phases out legacy systems with strong strategic alignment."
    },
]

def generate_english_booster(news):
    fallback_item = random.choice(ENGLISH_FALLBACKS)
    fallback_text = (
        f"Phrasal verb: {fallback_item['phrasal'][0]} - {fallback_item['phrasal'][1]}\n"
        f"Idiom: {fallback_item['idiom'][0]} - {fallback_item['idiom'][1]}\n"
        f"Business expression: {fallback_item['business'][0]} - {fallback_item['business'][1]}\n"
        f"Example: {fallback_item['example']}"
    )

    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", []) + news.get("cloud_platform", [])
    prompt = (
        "You are a professional business English coach.\n\n"
        f"Generate English learning content that matches these headlines:\n{headlines}\n\n"
        "Write exactly in this format:\n"
        "Phrasal verb: <expression> - <meaning in English>\n"
        "Idiom: <expression> - <meaning in English>\n"
        "Business expression: <expression> - <meaning in English>\n"
        "Example: <English example sentence>\n"
        "Keep it concise.\n"
    )

    out = ask_openai(prompt)
    return out if out else build_smart_english(news)

# ---------------- AI SPEAKING PROMPT ----------------
SPEAKING_FALLBACKS = [
    "In 2-3 English sentences, explain how energy costs affect cloud strategy.",
    "Describe how AI investments should be prioritized in uncertain markets.",
    "How should a telecom company adapt to AI transformation?",
    "Explain how a cloud leader should balance innovation and cost pressure.",
]

def generate_speaking_prompt(news):
    fallback = random.choice(SPEAKING_FALLBACKS)

    headlines = news.get("global", []) + news.get("technology", []) + news.get("cloud_platform", [])
    prompt = (
        "Create one executive speaking practice question.\n\n"
        f"Context:\n{headlines}\n\n"
        "Rules:\n"
        "- one sentence only\n"
        "- business English\n"
        "- executive level\n"
        "- should require a 2-3 sentence answer\n"
        "- focus on cloud, AI, telecom, strategy, or risk\n"
        "- practical, not academic\n"
    )

    out = ask_openai(prompt)
    return out if out else fallback

# ---------------- WEATHER ----------------
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        data = requests.get(url, timeout=10).json()
        temp = data["current_weather"]["temperature"]
        return f"Istanbul: {temp}C"
    except Exception:
        return "Istanbul: data unavailable"

# ---------------- VERSE ----------------
def read_quran_index():
    try:
        if QURAN_STATE_FILE.exists():
            return int(QURAN_STATE_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        pass
    return 1

def write_quran_index(idx: int):
    QURAN_STATE_FILE.write_text(str(idx), encoding="utf-8")

def fetch_ayah_from_api(global_ayah_number: int):
    for edition in QURAN_EDITIONS:
        try:
            url = f"{QURAN_API_BASE}/ayah/{global_ayah_number}/{edition}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()["data"]

            surah_name = data["surah"]["englishName"]
            number_in_surah = data["numberInSurah"]
            verse_text = data["text"]

            return (f"{surah_name} {number_in_surah}", verse_text)
        except Exception:
            continue

    return ("Verse unavailable", "Verse data is unavailable today.")

def get_daily_ayah():
    idx = read_quran_index()
    ref, text = fetch_ayah_from_api(idx)
    next_idx = idx + 1
    if next_idx > TOTAL_AYAHS:
        next_idx = 1
    write_quran_index(next_idx)
    return (ref, text)

# ---------------- BOOKS ----------------
BOOK_FALLBACKS = {
    "ai_strategy": [
        "Co-Intelligence - Ethan Mollick",
        "The Coming Wave - Mustafa Suleyman",
        "Empire of AI - Karen Hao",
    ],
    "leadership": [
        "Lead Bigger - Anne Chow",
        "Working Backwards - Colin Bryar and Bill Carr",
    ],
    "execution": [
        "Reshuffle - Sangeet Paul Choudary",
        "Competing in the Age of AI - Marco Iansiti and Karim R. Lakhani",
    ],
}

BOOK_REASON_FALLBACKS = {
    "Co-Intelligence - Ethan Mollick": "Why today: It offers a practical perspective on integrating AI into everyday workflows.",
    "The Coming Wave - Mustafa Suleyman": "Why today: It helps frame the balance between AI, regulation, and strategic risk.",
    "Empire of AI - Karen Hao": "Why today: It gives a clearer view of power dynamics and competition in the AI ecosystem.",
    "Lead Bigger - Anne Chow": "Why today: It helps build leadership impact more systematically during transformation periods.",
    "Working Backwards - Colin Bryar and Bill Carr": "Why today: It explains a customer-centric and disciplined execution culture.",
    "Reshuffle - Sangeet Paul Choudary": "Why today: It helps you better understand platforms, business models, and changing competitive dynamics.",
    "Competing in the Age of AI - Marco Iansiti and Karim R. Lakhani": "Why today: It clarifies business-model and organizational impact in the age of AI.",
}

def flatten_book_pool():
    books = []
    for group in BOOK_FALLBACKS.values():
        books.extend(group)
    return books

def choose_book_category(news):
    full_text = " ".join(
        news.get("global", []) + news.get("technology", []) + news.get("business", []) + news.get("cloud_platform", [])
    ).lower()

    ai_keywords = ["ai", "artificial intelligence", "model", "chip", "cloud", "data", "automation"]
    leadership_keywords = ["leadership", "manager", "ceo", "strategy", "board", "organization", "talent"]
    execution_keywords = ["market", "platform", "operations", "execution", "supply", "cost", "efficiency"]

    ai_score = sum(1 for k in ai_keywords if k in full_text)
    leadership_score = sum(1 for k in leadership_keywords if k in full_text)
    execution_score = sum(1 for k in execution_keywords if k in full_text)

    scores = {
        "ai_strategy": ai_score,
        "leadership": leadership_score,
        "execution": execution_score,
    }
    return max(scores, key=scores.get)

def get_recent_books():
    state = load_json_file(BOOK_STATE_FILE, {"recent": []})
    recent = state.get("recent", [])
    return recent if isinstance(recent, list) else []

def save_recent_book(book_title):
    recent = get_recent_books()
    updated = [book_title] + [b for b in recent if b != book_title]
    updated = updated[:7]
    save_json_file(BOOK_STATE_FILE, {"recent": updated})

def choose_fallback_book(news):
    category = choose_book_category(news)
    pool = BOOK_FALLBACKS.get(category, [])[:]
    if not pool:
        pool = flatten_book_pool()

    recent = set(get_recent_books())
    filtered = [book for book in pool if book not in recent]
    if not filtered:
        filtered = [book for book in flatten_book_pool() if book not in recent]
    if not filtered:
        filtered = flatten_book_pool()

    chosen = random.choice(filtered)
    reason = BOOK_REASON_FALLBACKS.get(chosen, "Why today: It is a strong reading recommendation aligned with the day's main theme.")
    save_recent_book(chosen)
    return chosen, reason

def generate_book_recommendation(news):
    fallback_book, fallback_reason = choose_fallback_book(news)

    headlines = news.get("global", []) + news.get("technology", []) + news.get("business", []) + news.get("cloud_platform", [])
    recent_books = get_recent_books()
    prompt = (
        "Recommend one professional book.\n\n"
        f"Context:\n{headlines}\n\n"
        f"Recently suggested books:\n{recent_books}\n\n"
        "Rules:\n"
        "- Suggest one book\n"
        "- Focus on AI, leadership, strategy, or execution\n"
        "- Do not repeat recent suggestions\n"
        "- Output exactly two lines\n"
        "- Line 1: Book: <title> - <author>\n"
        "- Line 2: Why today: <one-sentence reason in English>\n"
    )

    out = ask_openai(prompt)
    if not out:
        return fallback_book, fallback_reason

    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if len(lines) < 2:
        return fallback_book, fallback_reason

    raw_book_line = lines[0]
    raw_reason_line = lines[1]

    if ":" in raw_book_line:
        book_title = raw_book_line.split(":", 1)[1].strip()
    else:
        book_title = raw_book_line.strip()

    reason = raw_reason_line if raw_reason_line.startswith("Why today:") else f"Why today: {raw_reason_line}"

    if not book_title:
        return fallback_book, fallback_reason

    save_recent_book(book_title)
    return book_title, reason

# ---------------- QUOTES ----------------
POEM_FALLBACKS = [
    "To live free and alone like a tree, and brotherly like a forest. - Nazim Hikmet",
    "Hope is what keeps a person alive. - Nazim Hikmet",
    "Let us look at the sky. - Turgut Uyar",
    "You do not know how bound I am to you. - Attila Ilhan",
    "I am neither within time, nor entirely outside it. - Ahmet Hamdi Tanpinar",
    "A person resembles the place they live in. - Edip Cansever",
    "Do not mind it, my heart, do not mind it. - Sabahattin Ali",
    "The longest distance is neither Africa nor China. - Cemal Sureya",
    "To love is, at times, a humiliating fear. - Attila Ilhan",
    "Everything is hidden within you. - Sitki Erinc",
]

def get_recent_poems():
    state = load_json_file(POEM_STATE_FILE, {"recent": []})
    recent = state.get("recent", [])
    return recent if isinstance(recent, list) else []

def save_recent_poem(poem_text):
    recent = get_recent_poems()
    updated = [poem_text] + [p for p in recent if p != poem_text]
    updated = updated[:10]
    save_json_file(POEM_STATE_FILE, {"recent": updated})

def choose_fallback_poem():
    recent = set(get_recent_poems())
    filtered = [p for p in POEM_FALLBACKS if p not in recent]
    if not filtered:
        filtered = POEM_FALLBACKS[:]
    chosen = random.choice(filtered)
    save_recent_poem(chosen)
    return chosen

def generate_poem_line(news):
    fallback = choose_fallback_poem()

    headlines = news.get("global", []) + news.get("technology", []) + news.get("business", []) + news.get("cloud_platform", [])
    recent_poems = get_recent_poems()
    prompt = (
        "Suggest one short and strong daily quote.\n\n"
        f"Context:\n{headlines}\n\n"
        f"Recently used quotes:\n{recent_poems}\n\n"
        "Rules:\n"
        "- English only\n"
        "- One line only\n"
        "- Keep it sharp and reflective\n"
        "- Avoid repeating recent quotes\n"
        "- Format: <quote> - <author>\n"
    )

    out = ask_openai(prompt)
    if not out:
        return fallback

    poem = out.strip()
    save_recent_poem(poem)
    return poem

# ---------------- CLOUD / PLATFORM RADAR ----------------
CLOUD_PLATFORM_KEYWORDS = [
    "cloud", "iaas", "paas", "saas", "kubernetes", "openshift",
    "devops", "platform", "datacenter", "data center", "server",
    "infrastructure", "infra", "virtualization", "vmware",
    "container", "docker", "edge", "telco", "network cloud",
    "observability", "sre", "ci/cd", "automation", "ansible"
]

def filter_cloud_platform_news(items, limit=3):
    scored = []
    for item in items:
        lower = item.lower()
        score = sum(1 for k in CLOUD_PLATFORM_KEYWORDS if k in lower)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [item for _, item in scored[:limit]]

def collect_cloud_platform_news():
    sources = [
        "https://news.google.com/rss/search?q=cloud+OR+IaaS+OR+PaaS+OR+SaaS+OR+Kubernetes+OR+OpenShift+OR+DevOps+OR+datacenter&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=telco+cloud+OR+platform+engineering+OR+virtualization+OR+infrastructure&hl=en-US&gl=US&ceid=US:en",
    ]

    combined = []
    seen = set()

    for src in sources:
        for title in get_news(src, 8):
            if title not in seen:
                combined.append(title)
                seen.add(title)

    filtered = filter_cloud_platform_news(combined, limit=3)
    return filtered if filtered else combined[:3]

def build_idea_engine(cloud_news):
    ideas = []

    for item in cloud_news:
        lower = item.lower()

        if "cost" in lower or "optimization" in lower:
            ideas.append("Cost optimization trend -> Build a FinOps / cost visibility solution")
        elif "kubernetes" in lower or "openshift" in lower:
            ideas.append("Kubernetes adoption is rising -> Opportunity for a managed Kubernetes / platform service")
        elif "edge" in lower:
            ideas.append("Edge investment is increasing -> Opportunity for edge Kubernetes / telco edge platforms")
        elif "telco" in lower or "network" in lower:
            ideas.append("Telco cloud is growing -> Opportunity for a telco-specific PaaS / platform solution")
        elif "cloud" in lower:
            ideas.append("Cloud adoption is increasing -> Opportunity for migration / modernization services")

    if not ideas:
        ideas.append("Cloud trends -> Evaluate general platform and managed service opportunities")

    unique = []
    for idea in ideas:
        if idea not in unique:
            unique.append(idea)
    return unique[:3]

# ---------------- PRIORITY / ACTION ----------------
def map_priority_level(score):
    if score < 10:
        return "Low"
    if score < 15:
        return "Medium"
    if score < 20:
        return "Medium-High"
    if score < 25:
        return "High"
    return "Critical"

def build_top_priority_from_scores(aein_text):
    scores = {
        "revenue": 5,
        "execution": 5,
        "strategic": 5,
        "urgency": 5,
    }

    patterns = {
        "revenue": r"Revenue Impact:\s*(\d+)/10",
        "execution": r"Execution Ease:\s*(\d+)/10",
        "strategic": r"Strategic Fit:\s*(\d+)/10",
        "urgency": r"Urgency:\s*(\d+)/10",
    }

    for key, pattern in patterns.items():
        m = re.search(pattern, aein_text, flags=re.I)
        if m:
            scores[key] = int(m.group(1))

    score = scores["revenue"] + scores["strategic"] + scores["urgency"] - (10 - scores["execution"])
    level = map_priority_level(score)

    if scores["urgency"] >= 8:
        focus = "Focus on simplifying risk and priorities; elevate the single most critical item."
    elif scores["strategic"] >= 8 and scores["revenue"] >= 7:
        focus = "Turn the one AI/cloud topic with high strategic fit and revenue impact into concrete action."
    elif scores["revenue"] >= 8:
        focus = "Prioritize high revenue-impact opportunities while protecting delivery capacity."
    elif scores["execution"] >= 8:
        focus = "Complete one easy-to-execute quick win today."
    else:
        focus = "Stay focused on the one topic with the highest strategic fit."

    return f"Priority Score: {score}\nPriority Level: {level}\nFocus: {focus}"

def build_action_engine(aein_text, top_priority):
    lower = (aein_text + "\n" + top_priority).lower()

    if "risk" in lower and "urgency" in lower:
        return (
            "- Clarify 1 critical risk\n"
            "- Close 1 urgent decision today\n"
            "- Eliminate or postpone 1 distraction"
        )

    if "ai" in lower or "cloud" in lower or "strategic fit" in lower:
        return (
            "- Select 1 AI/cloud opportunity\n"
            "- Define 1 concrete use case or action\n"
            "- Remove 1 unnecessary agenda item today"
        )

    if "revenue" in lower:
        return (
            "- Prioritize 1 high revenue-impact opportunity\n"
            "- Move forward 1 customer / proposal / output item\n"
            "- Postpone 1 low-return task"
        )

    return (
        "- Select 1 main focus\n"
        "- Complete 1 concrete action today\n"
        "- Postpone 1 distracting task"
    )

# ---------------- NEWS ----------------
def get_news(url, n=3):
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:n] if getattr(entry, "title", "").strip()]

def collect_news():
    return {
        "global": get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3),
        "technology": get_news("https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en", 2),
        "business": get_news("https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en", 2),
        "cloud_platform": collect_cloud_platform_news(),
    }

def bullets(items):
    if not items:
        return "- Data unavailable"
    return "\n".join([f"- {item}" for item in items])

# ---------------- MAIN CONTENT ----------------
def build_daily_briefing(news, weather):
    global_news = news.get("global", [])[:3]
    business_news = news.get("business", [])[:2]
    tech_news = news.get("technology", [])[:2]
    cloud_platform_news = news.get("cloud_platform", [])[:3]
    ideas = build_idea_engine(cloud_platform_news)

    verse_ref, verse_text = get_daily_ayah()
    book_title, book_reason = generate_book_recommendation(news)
    quote_text = generate_poem_line(news)
    decision_text = generate_aein_decision(news)
    top_priority = build_top_priority_from_scores(decision_text)
    action_plan = build_action_engine(decision_text, top_priority)
    exec_text = generate_ai_insight(news)
    english_text = generate_english_booster(news)
    speaking = generate_speaking_prompt(news)

    msg = []
    msg.append("📌 *Daily Briefing*")
    msg.append(f"🕔 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    msg.append("")
    msg.append(f"🌤 *Weather:* {weather}")
    msg.append("")

    msg.append("*1) Summary*")
    msg.append("The main global pattern today is the combined effect of macro developments, technology investments, and geopolitical risk. It is more useful to read the broader direction than individual headlines.")
    msg.append("")

    msg.append("*2) Global Headlines*")
    msg.append(bullets(global_news))
    msg.append("")

    msg.append("*3) Market Snapshot*")
    msg.append(bullets(business_news))
    msg.append("")

    msg.append("*4) ☁️ Cloud / Platform Radar*")
    msg.append(bullets(cloud_platform_news))
    msg.append("")

    msg.append("*💡 Idea Signals*")
    msg.append(bullets(ideas))
    msg.append("")

    msg.append("*5) AI / Tech Radar*")
    msg.append(bullets(tech_news))
    msg.append("")

    msg.append("*6) English Booster*")
    msg.append(english_text)
    msg.append("")

    msg.append("*🎤 Speaking Practice*")
    msg.append("Answer the following question in 2-3 English sentences:")
    msg.append(speaking)
    msg.append("")

    msg.append("*7) Daily Reflection (Verse)*")
    msg.append(f"{verse_text} ({verse_ref})")
    msg.append("")

    msg.append("*8) Book Recommendation*")
    msg.append(book_title)
    msg.append(book_reason)
    msg.append("")

    msg.append("*9) Daily Quote*")
    msg.append(quote_text)
    msg.append("")

    msg.append("*🧠 Decision Insight*")
    msg.append(decision_text)
    msg.append("")

    msg.append("*🔥 Top Priority*")
    msg.append(top_priority)
    msg.append("")

    msg.append("*⚡ Action Plan*")
    msg.append(action_plan)
    msg.append("")

    msg.append("*🧠 Executive Insight*")
    msg.append(exec_text)

    return "\n".join(msg)

# ---------------- SEND ----------------
def send(text):
    last_error = None
    for timeout_value in (15, 30):
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
                timeout=timeout_value
            )
            response.raise_for_status()
            return
        except requests.exceptions.RequestException as e:
            last_error = e
    raise last_error

# ---------------- RUN ----------------
if __name__ == "__main__":
    news = collect_news()
    weather = get_weather()
    message = build_daily_briefing(news, weather)
    send(message)
