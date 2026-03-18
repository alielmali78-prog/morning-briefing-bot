#!/usr/bin/env python3
from datetime import datetime
import os
import random
import feedparser
import requests

TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TG_TOKEN veya TG_CHAT_ID tanımlı değil")
# --- HAVA DURUMU (Open-Meteo - API key yok) ---
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        data = requests.get(url, timeout=10).json()
        temp = data["current_weather"]["temperature"]
        return f"🌤 İstanbul: {temp}°C"
    except:
        return "🌤 İstanbul: veri alınamadı"

# --- AYET ---
AYETLER = [
    ("İnşirah 6", "Şüphesiz zorlukla beraber bir kolaylık vardır."),
    ("Bakara 286", "Allah kimseye gücünün yeteceğinden fazlasını yüklemez."),
    ("Âl-i İmran 139", "Gevşemeyin, üzülmeyin; eğer inanıyorsanız en üstün sizsiniz."),
]

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
    return [entry.title for entry in feed.entries[:n]]

def build():
    now = datetime.now().strftime("%d.%m %H:%M")

    global_news = get_news("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3)

    msg = []
    msg.append(f"📌 *Sabah Rutini v3*")
    msg.append(f"🕔 {now}")
    msg.append(get_weather())
    msg.append("")

    msg.append("*🌍 Global Headlines*")
    for i, n in enumerate(global_news, 1):
        msg.append(f"{i}. {n}")

    msg.append("")
    msg.append("*🧠 Executive Summary*")
    msg.append("Bugün teknoloji ve makro gelişmeler birlikte yön belirliyor. Kararları tek başlıkla değil trend ile değerlendir.")

    msg.append("")
    msg.append("*📡 AI / Cloud Radar*")
    msg.append("- AI yatırımları hız kesmeden devam ediyor")
    msg.append("- Cloud maliyet optimizasyonu öne çıkıyor")

    msg.append("")
    msg.append("*🗣 English Booster*")
    p1, p2 = random.sample(PHRASALS, 2)
    msg.append(f"{p1[0]} – {p1[1]}")
    msg.append(f"{p2[0]} – {p2[1]}")

    msg.append("")
    ayet = random.choice(AYETLER)
    msg.append("*📖 Günün Ayeti*")
    msg.append(f"{ayet[1]} ({ayet[0]})")

    msg.append("")
    msg.append("*📚 Kitap Önerisi*")
    msg.append(random.choice(BOOKS))

    # Şiir 50% ihtimal
    if random.random() > 0.5:
        msg.append("")
        msg.append("*✍️ Günün Dizesi*")
        msg.append(random.choice(POEMS))

    return "\n".join(msg)

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
        timeout=10
    )

if __name__ == "__main__":
    send(build())
