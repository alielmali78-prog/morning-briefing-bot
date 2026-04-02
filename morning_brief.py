#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import os
import random
import json
import feedparser
import requests

TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("TG_TOKEN veya TG_CHAT_ID tanımlı değil")


# ---------------- DOSYA YOLLARI ----------------
QURAN_STATE_FILE = Path.home() / ".morning_brief_quran_state"
BOOK_STATE_FILE = Path.home() / ".morning_brief_book_state"

QURAN_API_BASE = "https://api.alquran.cloud/v1"
QURAN_EDITIONS = [
    "tr.diyanet",
    "tr.transliteration",
    "en.asad",
]
TOTAL_AYAHS = 6236


# ---------------- YARDIMCI ----------------
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

        if response.status_code != 200:
            return fallback

        data = response.json()
        text = safe_openai_text_response(data)
        return text if text else fallback

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
        "example": "Before we roll out the platform, all teams must be on the same page."
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

        if response.status_code != 200:
            return fallback_text

        data = response.json()
        text = safe_openai_text_response(data)
        return text if text else fallback_text

    except Exception:
        return fallback_text


# ---------------- AI SPEAKING PROMPT ----------------
SPEAKING_FALLBACKS = [
    "In 2–3 sentences, explain how energy costs impact cloud strategy.",
    "Describe how AI investments should be prioritized in uncertain markets.",
    "How should a telecom company adapt to AI transformation?",
    "Explain how a cloud leader should balance innovation and cost pressure.",
]


def generate_speaking_prompt(news):
    fallback = random.choice(SPEAKING_FALLBACKS)

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback

        headlines = news.get("global", []) + news.get("technology", [])

        prompt = f"""
Create 1 executive speaking practice question for Ali.

Context:
{headlines}

Rules:
- 1 sentence only
- Business English
- Executive level
- Should require a 2-3 sentence answer
- Focus on cloud, AI, telecom, strategy or risk
- Make it practical, not academic
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

        if response.status_code != 200:
            return fallback

        data = response.json()
        text = safe_openai_text_response(data)
        return text if text else fallback

    except Exception:
        return fallback


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
BOOK_FALLBACKS = {
    "ai_strategy": [
        "Co-Intelligence – Ethan Mollick",
        "The Coming Wave – Mustafa Suleyman",
        "Empire of AI – Karen Hao",
    ],
    "leadership": [
        "Lead Bigger – Anne Chow",
        "Working Backwards – Colin Bryar and Bill Carr",
    ],
    "execution": [
        "Reshuffle – Sangeet Paul Choudary",
        "Competing in the Age of AI – Marco Iansiti & Karim R. Lakhani",
    ],
}

BOOK_REASON_FALLBACKS = {
    "Co-Intelligence – Ethan Mollick": "Neden bugün: AI’yi günlük iş akışına pratik şekilde entegre etme bakışı sunuyor.",
    "The Coming Wave – Mustafa Suleyman": "Neden bugün: AI, regülasyon ve stratejik risk dengesini güçlü biçimde düşündürüyor.",
    "Empire of AI – Karen Hao": "Neden bugün: AI ekosistemindeki güç dengelerini ve rekabeti daha net görmeni sağlar.",
    "Lead Bigger – Anne Chow": "Neden bugün: dönüşüm dönemlerinde liderlik etkisini daha sistemli kurmaya yardım eder.",
    "Working Backwards – Colin Bryar and Bill Carr": "Neden bugün: müşteri odaklı ve disiplinli execution kültürünü anlatır.",
    "Reshuffle – Sangeet Paul Choudary": "Neden bugün: platform, iş modeli ve değişen rekabet yapısını daha iyi okumana yardım eder.",
    "Competing in the Age of AI – Marco Iansiti & Karim R. Lakhani": "Neden bugün: AI çağında işletme modeli ve organizasyon etkisini netleştirir.",
}


def flatten_book_pool():
    books = []
    for group in BOOK_FALLBACKS.values():
        books.extend(group)
    return books


def choose_book_category(news):
    global_text = " ".join(news.get("global", [])).lower()
    tech_text = " ".join(news.get("technology", [])).lower()
    business_text = " ".join(news.get("business", [])).lower()
    full_text = f"{global_text} {tech_text} {business_text}"

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
    if isinstance(recent, list):
        return recent
    return []


def save_recent_book(book_title):
    recent = get_recent_books()
    updated = [book_title] + [b for b in recent if b != book_title]
    updated = updated[:7]
    save_json_file(BOOK_STATE_FILE, {"recent": updated})


def choose_fallback_book(news):
    category = choose_book_category(news)
    candidate_pool = BOOK_FALLBACKS.get(category, [])[:]

    if not candidate_pool:
        candidate_pool = flatten_book_pool()

    recent = set(get_recent_books())
    filtered = [book for book in candidate_pool if book not in recent]

    if not filtered:
        all_books = flatten_book_pool()
        filtered = [book for book in all_books if book not in recent]

    if not filtered:
        filtered = flatten_book_pool()

    chosen = random.choice(filtered)
    reason = BOOK_REASON_FALLBACKS.get(chosen, "Neden bugün: gündemin ana ekseniyle bağlantılı güçlü bir okuma önerisi.")
    save_recent_book(chosen)
    return chosen, reason


def generate_book_recommendation(news):
    fallback_book, fallback_reason = choose_fallback_book(news)

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return fallback_book, fallback_reason

        recent_books = get_recent_books()
        headlines = news.get("global", []) + news.get("technology", []) + news.get("business", [])

        prompt = f"""
Ali için profesyonel bir kitap öner.

Context:
{headlines}

Son günlerde önerilmiş kitaplar:
{recent_books}

Kurallar:
- 1 kitap öner
- AI / leadership / strategy / execution odaklı olsun
- Son önerilenleri tekrar etme
- Çıktı tam olarak iki satır olsun
- 1. satır: Kitap: <kitap adı> – <yazar>
- 2. satır: Neden bugün: <tek cümle Türkçe gerekçe>
- Ek açıklama yazma
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

        if response.status_code != 200:
            return fallback_book, fallback_reason

        data = response.json()
        text = safe_openai_text_response(data)

        if not text:
            return fallback_book, fallback_reason

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) < 2:
            return fallback_book, fallback_reason

        raw_book_line = lines[0]
        raw_reason_line = lines[1]

        if ":" in raw_book_line:
            book_title = raw_book_line.split(":", 1)[1].strip()
        else:
            book_title = raw_book_line.strip()

        reason = raw_reason_line if raw_reason_line.startswith("Neden bugün:") else f"Neden bugün: {raw_reason_line}"

        if not book_title:
            return fallback_book, fallback_reason

        save_recent_book(book_title)
        return book_title, reason

    except Exception:
        return fallback_book, fallback_reason


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
    book_title, book_reason = generate_book_recommendation(news)
    ai_text = generate_ai_insight(news)
    english_text = generate_english_booster(news)
    speaking = generate_speaking_prompt(news)

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

    msg.append("*🎤 Speaking Practice*")
    msg.append("Aşağıdaki soruya İngilizce 2-3 cümleyle cevap ver:")
    msg.append(speaking)
    msg.append("")

    msg.append("*6) Günün Ayeti*")
    msg.append(f"{ayet[1]} ({ayet[0]})")
    msg.append("")

    msg.append("*7) Kitap Önerisi*")
    msg.append(book_title)
    msg.append(book_reason)

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
