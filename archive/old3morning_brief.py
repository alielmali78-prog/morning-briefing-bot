#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import os
import random
import feedparser
import requests

TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TG_TOKEN veya TG_CHAT_ID tanımlı değil")


# ---------------- AI ----------------
def generate_ai_insight(news):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "AI insight üretilemedi"

        headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])

        prompt = f"""
Aşağıdaki haber başlıklarına göre kısa bir executive analiz yap:

{headlines}

Format:
- Günün ana teması
- Risk
- Fırsat
- 1 cümlelik öneri

Kısa, net yaz.
"""

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=20
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI hata: {e}"


# ---------------- HAVA ----------------
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        data = requests.get(url, timeout=10).json()
        temp = data["current_weather"]["temperature"]
        return f"İstanbul: {temp}°C"
    except:
        return "İstanbul: veri alınamadı"


# ---------------- AYET ----------------
QURAN_STATE_FILE = Path.home() / ".morning_brief_quran_state"
QURAN_API_BASE = "https://api.alquran.cloud/v1"
TOTAL_AYAHS = 6236


def read_quran_index():
    try:
        if QURAN_STATE_FILE.exists():
            return int(QURAN_STATE_FILE.read_text().strip())
    except:
        pass
    return 1


def write_quran_index(idx):
    QURAN_STATE_FILE.write_text(str(idx))


def fetch_ayah(idx):
    try:
        url = f"{QURAN_API_BASE}/ayah/{idx}/tr.diyanet"
        data = requests.get(url, timeout=10).json()["data"]

        surah = data["surah"]["englishName"]
        no = data["numberInSurah"]
        text = data["text"]

        return (f"{surah} {no}", text)
    except:
        return ("Ayet", "Ayet alınamadı")


def get_daily_ayah():
    idx = read_quran_index()
    ref, text = fetch_ayah(idx)

    next_idx = idx + 1 if idx < TOTAL_AYAHS else 1
    write_quran_index(next_idx)

    return (ref, text)


# ---------------- DATA ----------------
PHRASALS = [
    ("carry out", "uygulamak"),
    ("figure out", "anlamak"),
    ("set up", "kurmak"),
    ("take over", "devralmak"),
]

BOOKS = [
    "Sapiens – Yuval Noah Harari",
    "Atomic Habits – James Clear",
    "Thinking, Fast and Slow – Daniel Kahneman",
]

POEMS = [
    "Yaşamak bir ağaç gibi tek ve hür – Nazım Hikmet",
    "Ben sana mecburum – Attila İlhan",
]


# ---------------- HABER ----------------
def get_news(url, n=3):
    feed = feedparser.parse(url)
    return [e.title for e in feed.entries[:n] if e.title]


def collect_news():
    return {
        "global": get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3),
        "technology": get_news("https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en", 2),
        "business": get_news("https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en", 2),
    }


def bullets(items):
    return "\n".join([f"- {i}" for i in items]) if items else "- veri yok"


# ---------------- MAIN ----------------
def build_sabah_rutini(news, weather):

    global_news = news["global"]
    tech_news = news["technology"]
    biz_news = news["business"]

    p1, p2 = random.sample(PHRASALS, 2)
    ayet = get_daily_ayah()
    kitap = random.choice(BOOKS)

    msg = []

    msg.append("📌 *Sabah Haber Rutini*")
    msg.append(f"🕔 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    msg.append("")
    msg.append(f"🌤 {weather}")
    msg.append("")

    msg.append("*1) Global*")
    msg.append(bullets(global_news))
    msg.append("")

    msg.append("*2) Piyasa*")
    msg.append(bullets(biz_news))
    msg.append("")

    msg.append("*3) Tech*")
    msg.append(bullets(tech_news))
    msg.append("")

    msg.append("*4) English*")
    msg.append(f"- {p1[0]}: {p1[1]}")
    msg.append(f"- {p2[0]}: {p2[1]}")
    msg.append("")

    msg.append("*5) Ayet*")
    msg.append(f"{ayet[1]} ({ayet[0]})")
    msg.append("")

    msg.append("*6) Kitap*")
    msg.append(kitap)

    if random.random() > 0.5:
        msg.append("")
        msg.append(random.choice(POEMS))

    # 🔥 AI BURADA
    ai_text = generate_ai_insight(news)
    msg.append("")
    msg.append("*🧠 Executive Insight*")
    msg.append(ai_text)

    return "\n".join(msg)


def send(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
    )
    r.raise_for_status()


# ---------------- RUN ----------------
if __name__ == "__main__":
    news = collect_news()
    weather = get_weather()
    msg = build_sabah_rutini(news, weather)
    send(msg)
