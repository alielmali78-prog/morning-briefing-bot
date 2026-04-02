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


# ---------------- AI INSIGHT ----------------
def generate_ai_insight(news):
    fallback = (
        "Ana tema: Enerji, makro baskı ve teknoloji yatırımları birlikte fiyatlanıyor.\n"
        "Risk: Jeopolitik belirsizlik ve maliyet baskısı.\n"
        "Fırsat: Verimlilik odaklı AI ve cloud optimizasyonu.\n"
        "Ali için bugün:\n"
        "- Yap: AI işlerini doğrudan verimlilik ve maliyet KPI'larına bağla.\n"
        "- Dikkat et: Enerji ve altyapı kapasite planlamasını hafife alma.\n"
        "- İzle: Telco + cloud + AI birleşiminden çıkan yeni iş modelleri."
    )

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback

        headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])

        prompt = f"""
Sen Ali'nin kişisel stratejik sabah danışmanısın.

Ali:
- Telekom, bulut ve platform teknolojilerinde deneyimli bir yönetici
- Kısa, net ve aksiyon odaklı çıktı ister
- Gürültü değil, anlamlı yön ve öncelik görmek ister

Aşağıdaki haber başlıklarını değerlendir:

{headlines}

Türkçe yaz.
Çıktı tam olarak şu başlıklarla gelsin:

Ana tema:
Risk:
Fırsat:
Ali için bugün:
- Yap:
- Dikkat et:
- İzle:

Kurallar:
- En fazla 8 kısa satır
- Yönetici dili kullan
- Haberleri tek tek tekrar etme
- Ali için somut öneri ver
"""

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4.1-mini",
                "input": prompt,
            },
            timeout=20,
        )

        data = response.json()

        if response.status_code != 200:
            return fallback

        return data["output"][0]["content"][0]["text"]

    except Exception:
        return fallback


# ---------------- AI ENGLISH BOOSTER ----------------
ENGLISH_FALLBACKS = [
    {
        "phrasal": ("scale up", "ölçek büyütmek"),
        "idiom": ("move the needle", "anlamlı fark yaratmak"),
        "business": ("cost discipline", "maliyet disiplini"),
        "example": "We need to scale up carefully if we want to move the needle without losing cost discipline."
    },
    {
        "phrasal": ("roll out", "devreye almak"),
        "idiom": ("on the same page", "aynı fikirde olmak"),
        "business": ("operational efficiency", "operasyonel verimlilik"),
        "example": "Before we roll out the new platform, all teams must be on the same page about operational efficiency goals."
    },
    {
        "phrasal": ("cut back", "azaltmak, kısmak"),
        "idiom": ("brace for impact", "sert etkiye hazırlanmak"),
        "business": ("risk exposure", "risk maruziyeti"),
        "example": "Firms may cut back investment and brace for impact when risk exposure rises."
    },
    {
        "phrasal": ("phase out", "kademeli kaldırmak"),
        "idiom": ("in the driver's seat", "kontrolde olmak"),
        "business": ("strategic alignment", "stratejik uyum"),
        "example": "A company stays in the driver's seat when it phases out legacy systems with strong strategic alignment."
    },
]


def generate_english_booster(news):
    fallback_item = random.choice(ENGLISH_FALLBACKS)
    fallback_text = (
        f"Phrasal verb: {fallback_item['phrasal'][0]} — {fallback_item['phrasal'][1]}\n"
        f"Idiom: {fallback_item['idiom'][0]} — {fallback_item['idiom'][1]}\n"
        f"Business expression: {fallback_item['business'][0]} — {fallback_item['business'][1]}\n"
        f"Example: {fallback_item['example']}"
    )

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback_text

        headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])

        prompt = f"""
Sen Ali için çalışan profesyonel bir iş İngilizcesi koçusun.

Aşağıdaki haber başlıklarının temasına uygun İngilizce öğrenme içeriği üret:

{headlines}

Türkçe açıklamalı ve tam olarak şu formatta yaz:

Phrasal verb: <ifade> — <Türkçe anlamı>
Idiom: <ifade> — <Türkçe anlamı>
Business expression: <ifade> — <Türkçe anlamı>
Example: <İngilizce örnek cümle>

Kurallar:
- Profesyonel ve iş hayatına uygun ifadeler seç
- Günün haber temasıyla uyumlu olsun
- Kısa ve net yaz
- Ek açıklama ekleme
"""

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4.1-mini",
                "input": prompt,
            },
            timeout=20,
        )

        data = response.json()

        if response.status_code != 200:
            return fallback_text

        return data["output"][0]["content"][0]["text"]

    except Exception:
        return fallback_text


# ---------------- HAVA DURUMU ----------------
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        data = requests.get(url, timeout=10).json()
        temp = data["current_weather"]["temperature"]
        return f"İstanbul: {temp}°C"
    except Exception:
        return "İstanbul: veri alınamadı"


# ---------------- AYET (API + tekrarsız sıra) ----------------
QURAN_STATE_FILE = Path.home() / ".morning_brief_quran_state"
QURAN_API_BASE = "https://api.alquran.cloud/v1"

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


# ---------------- KİTAP ----------------
BOOKS = [
    "Sapiens – Yuval Noah Harari",
    "Atomic Habits – James Clear",
    "Thinking, Fast and Slow – Daniel Kahneman",
]


# ---------------- ŞİİR ----------------
POEMS = [
    "“Yaşamak bir ağaç gibi tek ve hür ve bir orman gibi kardeşçesine” – Nazım Hikmet",
    "“Ben sana mecburum bilemezsin” – Attila İlhan",
]


# ---------------- HABER ----------------
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


# ---------------- ANA İÇERİK ----------------
def build_sabah_rutini(news, weather):
    global_news = news.get("global", [])[:3]
    tech_news = news.get("technology", [])[:2]
    business_news = news.get("business", [])[:2]

    ayet = get_daily_ayah()
    kitap = random.choice(BOOKS)
    ai_text = generate_ai_insight(news)
    english_text = generate_english_booster(news)

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
    msg.append(english_text)
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

    msg.append("")
    msg.append("*🧠 Executive Insight*")
    msg.append(ai_text)

    return "\n".join(msg)


# ---------------- GÖNDERİM ----------------
def send(text):
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
        timeout=10
    )
    response.raise_for_status()


# ---------------- ÇALIŞTIR ----------------
if __name__ == "__main__":
    news = collect_news()
    weather = get_weather()
    message = build_sabah_rutini(news, weather)
    send(message)

