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


# --- HAVA DURUMU ---
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        data = requests.get(url, timeout=10).json()
        temp = data["current_weather"]["temperature"]
        return f"İstanbul: {temp}°C"
    except Exception:
        return "İstanbul: veri alınamadı"


# --- AYET ---
# --- AYET (API + tekrarsız sıra) ---
QURAN_STATE_FILE = Path.home() / ".morning_brief_quran_state"
QURAN_API_BASE = "https://api.alquran.cloud/v1"

# Türkçe çeviri edition'ı. AlQuran Cloud birden fazla edition destekler.
# Bu edition çalışmazsa aşağıdaki fallback devreye girecek.
QURAN_EDITIONS = [
    "tr.diyanet",
    "tr.transliteration",
    "en.asad",
]

TOTAL_AYAHS = 6236


def read_quran_index():
    try:
        if QURAN_STATE_FILE.exists():
            return int(QURAN_STATE_FILE.read_text().strip())
    except Exception:
        pass
    return 1


def write_quran_index(idx: int):
    QURAN_STATE_FILE.write_text(str(idx))


def fetch_ayah_from_api(global_ayah_number: int):
    """
    Global ayet numarasına göre ayeti API'den çekmeye çalışır.
    """
    for edition in QURAN_EDITIONS:
        try:
            url = f"{QURAN_API_BASE}/ayah/{global_ayah_number}/{edition}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()["data"]

            surah_name = data["surah"]["englishName"]
            number_in_surah = data["numberInSurah"]
            text = data["text"]

            return (f"{surah_name} {number_in_surah}", text)
        except Exception:
            continue

    return ("Ayet alınamadı", "Bugün için ayet verisi alınamadı.")


def get_daily_ayah():
    idx = read_quran_index()
    ref, text = fetch_ayah_from_api(idx)

    next_idx = idx + 1
    if next_idx > TOTAL_AYAHS:
        next_idx = 1

    write_quran_index(next_idx)
    return (ref, text)

# --- PHRASAL VERB ---
PHRASALS = [
    ("carry out", "uygulamak, yerine getirmek"),
    ("figure out", "anlamak, çözmek"),
    ("set up", "kurmak"),
    ("take over", "devralmak"),
]


# --- KİTAP ---
BOOKS = [
    "Sapiens – Yuval Noah Harari",
    "Atomic Habits – James Clear",
    "Thinking, Fast and Slow – Daniel Kahneman",
]


# --- ŞİİR ---
POEMS = [
    "“Yaşamak bir ağaç gibi tek ve hür ve bir orman gibi kardeşçesine” – Nazım Hikmet",
    "“Ben sana mecburum bilemezsin” – Attila İlhan",
]


# --- HABER ---
def get_news(url, n=3):
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:n] if getattr(entry, "title", "").strip()]


def collect_news():
    return {
        "global": get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3),
        "technology": get_news("https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en", 2),
        "business": get_news("https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en", 2),
    }


def bullets(items):
    if not items:
        return "- Veri alınamadı"
    return "\n".join([f"- {item}" for item in items])


def build_sabah_rutini(news, weather):
    global_news = news.get("global", [])[:3]
    tech_news = news.get("technology", [])[:2]
    business_news = news.get("business", [])[:2]

    p1, p2 = random.sample(PHRASALS, 2)
    #ayet = random.choice(AYETLER)
    ayet = get_daily_ayah()
    kitap = random.choice(BOOKS)

    msg = []
    msg.append("📌 *Sabah Haber Rutini*")
    msg.append(f"🕔 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    msg.append("")
    msg.append(f"🌤 *Hava Durumu:* {weather}")
    msg.append("")

    msg.append("*1) Günün Özeti*")
    msg.append("Küresel akışta ana tema; makro gelişmeler, teknoloji yatırımları ve jeopolitik risklerin birlikte yön belirlemesi. Manşetleri tek tek değil, genel eğilim üzerinden okumak daha anlamlı.")
    msg.append("")

    msg.append("*2) Global Manşetler*")
    msg.append(bullets(global_news))
    msg.append("")

    msg.append("*3) Piyasa Snapshot*")
    msg.append(bullets(business_news))
    msg.append("")

    msg.append("*4) AI / Cloud Radar*")
    msg.append(bullets(tech_news))
    msg.append("")

    msg.append("*5) English Booster*")
    msg.append(f"- {p1[0]} – {p1[1]}")
    msg.append(f"- {p2[0]} – {p2[1]}")
    msg.append("")

    msg.append("*6) Günün Ayeti*")
    msg.append(f"{ayet[1]} ({ayet[0]})")
    msg.append("")

    msg.append("*7) Kitap Önerisi*")
    msg.append(kitap)

    if random.random() > 0.5:
        msg.append("")
        msg.append("*Ek: Günün Dizesi*")
        msg.append(random.choice(POEMS))

    return "\n".join(msg)


def send(text):
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
        timeout=10
    )
    response.raise_for_status()


if __name__ == "__main__":
    news = collect_news()
    weather = get_weather()
    message = build_sabah_rutini(news, weather)
    send(message)
