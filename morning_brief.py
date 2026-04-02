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
POEM_STATE_FILE = Path.home() / ".morning_brief_poem_state"

QURAN_API_BASE = "https://api.alquran.cloud/v1"
QURAN_EDITIONS = [
    "tr.diyanet",
    "tr.transliteration",
    "en.asad",
]
TOTAL_AYAHS = 6236


# ---------------- YARDIMCI ----------------

AI_LIMIT_FILE = Path.home() / ".morning_brief_ai_usage"

def can_use_ai():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        if AI_LIMIT_FILE.exists():
            data = AI_LIMIT_FILE.read_text().split("|")
            if len(data) == 2:
                date, count = data
                if date == today:
                    return int(count) < 2
    except:
        pass

    return True

def register_ai_call():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        if AI_LIMIT_FILE.exists():
            data = AI_LIMIT_FILE.read_text().split("|")
            if len(data) == 2 and data[0] == today:
                count = int(data[1]) + 1
            else:
                count = 1
        else:
            count = 1

        AI_LIMIT_FILE.write_text(f"{today}|{count}")
    except:
        pass

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



def build_smart_exec_fallback(news):
    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])
    full = " ".join(headlines).lower()

    if any(k in full for k in ["war", "iran", "attack", "strike", "crisis"]):
        theme = "Jeopolitik riskler teknoloji ve piyasaları doğrudan etkiliyor."
        risk = "Reaktif karar alma ve enerji maliyetleri."
        opp = "Belirsizlik dönemlerinde doğru pozisyon avantaj yaratır."
    elif any(k in full for k in ["ai", "cloud", "chip", "data"]):
        theme = "AI ve cloud yatırımları rekabetin merkezinde."
        risk = "Yanlış yatırım dağılımı."
        opp = "Verimlilik ve ölçeklenebilirlik avantajı."
    else:
        theme = "Makro ve teknoloji dengesi birlikte ilerliyor."
        risk = "Odak kaybı."
        opp = "Operasyonel verimlilik."

    return (
        f"Ana tema: {theme}\n"
        f"Risk: {risk}\n"
        f"Fırsat: {opp}\n"
        f"Ali için bugün:\n"
        f"- Yap: Gündemi sadeleştir ve 1 ana hedef seç.\n"
        f"- Dikkat et: Gereksiz işlere dağılma.\n"
        f"- İzle: AI + cloud + piyasa kesişimi."
    )

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
        if not api_key or not can_use_ai():
            return build_smart_exec_fallback(news)

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
        register_ai_call()
        return text if text else fallback

    except Exception:
        return fallback



def build_smart_aein_fallback(news):
    headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])
    full_text = " ".join(headlines).lower()

    revenue = 5
    execution = 7
    strategic = 5
    urgency = 5

    revenue_keywords = ["ipo", "valuation", "investment", "revenue", "market", "growth", "business", "deal"]
    strategic_keywords = ["ai", "cloud", "chip", "data", "automation", "platform", "technology"]
    urgent_keywords = ["war", "strike", "attack", "fires", "warning", "live updates", "crisis", "iran", "tehran"]
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
        theme = "Jeopolitik baskı ile teknoloji ve piyasa gündemi aynı anda yönetiliyor."
        risk = "Dikkatin dağılması ve reaktif karar alma riski artıyor."
    elif strategic >= 8:
        theme = "Teknoloji eksenli gündem stratejik pozisyon almayı öne çıkarıyor."
        risk = "Yanlış önceliklendirme yüzünden fırsat penceresi kaçabilir."
    else:
        theme = "Makro baskılar ve iş gündemi birlikte okunmalı."
        risk = "Parçalı gündem odak kaybı yaratabilir."

    if strategic >= 8 and revenue >= 7:
        opp = "AI, cloud ve platform alanında ticari ve stratejik fırsat birlikte oluşuyor."
    elif revenue >= 7:
        opp = "Piyasa hareketliliği yeni gelir ve teklif fırsatları yaratabilir."
    else:
        opp = "Operasyon verimliliği ve odaklı execution ile avantaj yaratılabilir."

    if urgency >= 8:
        advice = "Bugün haberleri izlemek yerine risk ve öncelik filtresiyle sadeleştir."
        decision = "Tek kritik karar alanını seç, diğer tüm konuları ikinci plana al."
    elif strategic >= 8:
        advice = "AI ve cloud başlıklarını doğrudan iş sonucu üreten alanlarla eşleştir."
        decision = "Bugün stratejik uyumu yüksek tek bir başlığı somut aksiyona çevir."
    else:
        advice = "Gelir, delivery ve stratejik uyum filtresiyle gündemi daralt."
        decision = "Bugün en yüksek iş etkisi olan tek konuyu ilerlet."

    return (
        f"Ana tema: {theme}\n"
        f"Risk: {risk}\n"
        f"Fırsat: {opp}\n"
        f"\nScore:\n"
        f"- Revenue Impact: {revenue}/10\n"
        f"- Execution Ease: {execution}/10\n"
        f"- Strategic Fit: {strategic}/10\n"
        f"- Urgency: {urgency}/10\n"
        f"\nÖneri: {advice}\n"
        f"Karar: {decision}"
    )


# ---------------- AEIN DECISION ENGINE ----------------
def generate_aein_decision(news):
    fallback = build_smart_aein_fallback(news)

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or not can_use_ai():
            return fallback

        headlines = news.get("global", []) + news.get("business", []) + news.get("technology", [])

        prompt = f"""
Sen AEIN v21 mantığıyla çalışan bir executive decision engine'sin.

Ali'nin karar filtresi:
- gelir getiriyor mu?
- delivery gücünü artırıyor mu?
- ölçeklenebilir modele katkı sağlıyor mu?
- stratejik pozisyonu güçlendiriyor mu?
- zaman / enerji / para maliyetine değiyor mu?

Aşağıdaki haber başlıklarını bu mantıkla değerlendir:

{headlines}

Türkçe yaz.

Çıktı formatı:

Ana tema:
Risk:
Fırsat:

Score:
- Revenue Impact: X/10
- Execution Ease: X/10
- Strategic Fit: X/10
- Urgency: X/10

Öneri:
Karar:

Kurallar:
- kısa ve net yaz
- sayılar gerçekçi olsun
- karar cümlesi somut ve aksiyon içersin
- haber başlıklarını tekrar etme
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
        register_ai_call()
        return text if text else fallback

    except Exception:
        return fallback



def build_smart_english(news):
    headlines = " ".join(news.get("global", []) + news.get("technology", [])).lower()

    if "ai" in headlines or "cloud" in headlines:
        return (
            "Phrasal verb: scale up — ölçek büyütmek\n"
            "Idiom: stay ahead of the curve — trendin önünde olmak\n"
            "Business expression: digital transformation — dijital dönüşüm\n"
            "Example: Companies must scale up AI capabilities to stay ahead of the curve."
        )
    elif "war" in headlines or "crisis" in headlines:
        return (
            "Phrasal verb: brace for — hazırlanmak\n"
            "Idiom: in troubled waters — zor durumda\n"
            "Business expression: risk management — risk yönetimi\n"
            "Example: Firms must brace for uncertainty in troubled waters."
        )
    else:
        return (
            "Phrasal verb: move forward — ilerlemek\n"
            "Idiom: keep the momentum — ivmeyi korumak\n"
            "Business expression: operational efficiency — operasyonel verimlilik\n"
            "Example: Teams must move forward while keeping the momentum."
        )

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
        if not api_key or not can_use_ai():
            return build_smart_english(news)

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
        register_ai_call()
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
        if not api_key or not can_use_ai():
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
        register_ai_call()
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
        if not api_key or not can_use_ai():
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


# ---------------- GÜNÜN DİZESİ ----------------
POEM_FALLBACKS = [
    "“Yaşamak bir ağaç gibi tek ve hür ve bir orman gibi kardeşçesine” – Nazım Hikmet",
    "“Ben sana mecburum bilemezsin” – Attila İlhan",
    "“Ne içindeyim zamanın, ne de büsbütün dışında” – Ahmet Hamdi Tanpınar",
    "“Göğe bakalım” – Turgut Uyar",
    "“İnsan yaşadığı yere benzer” – Edip Cansever",
    "“Bir umuttur yaşatan insanı” – Nazım Hikmet",
    "“Aldırma gönül aldırma” – Sabahattin Ali",
    "“En uzak mesafe ne Afrika’dır ne Çin” – Cemal Süreya",
    "“Sevmek, kimi zaman rezilce korkudur” – Attila İlhan",
    "“Her şey sende gizli” – Sıtkı Erinç",
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

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or not can_use_ai():
            return fallback

        recent_poems = get_recent_poems()
        headlines = news.get("global", []) + news.get("technology", []) + news.get("business", [])

        prompt = f"""
Ali için kısa ve güçlü bir günün dizesi öner.

Bağlam:
{headlines}

Son günlerde kullanılan dizeler:
{recent_poems}

Kurallar:
- Türkçe yaz
- Tek satır olsun
- Şair adıyla birlikte ver
- Kısa, güçlü, sabah rutini tonuna uygun olsun
- Fazla melankolik olmasın
- Son kullanılanları tekrar etme
- Format:
“<dize>” – <şair>
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

        if not text:
            return fallback

        poem = text.strip()
        save_recent_poem(poem)
        return poem

    except Exception:
        return fallback


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



def build_top_priority_from_scores(aein_text):
    import re

    lower = aein_text.lower()

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

    priority_score = scores["revenue"] + scores["strategic"] + scores["urgency"] - (10 - scores["execution"])

    if scores["urgency"] >= 8:
        focus = "Risk ve öncelik sadeleştirmesine odaklan; tek kritik işi öne al."
    elif scores["strategic"] >= 8 and scores["revenue"] >= 7:
        focus = "Stratejik uyumu ve gelir etkisi yüksek tek AI/cloud başlığını somut aksiyona çevir."
    elif scores["revenue"] >= 8:
        focus = "Gelir etkisi yüksek fırsatları öne al; delivery gücünü zorlamadan ilerle."
    elif scores["execution"] >= 8:
        focus = "Hızlı kazanım sağlayacak, uygulanması kolay tek işi bugün tamamla."
    else:
        focus = "Dağılmadan, stratejik uyumu en yüksek tek konuya odaklan."

    return f"Priority Score: {priority_score}/30\n🔥 Top Priority: {focus}"



def build_action_engine(aein_text, top_priority):
    lower = (aein_text + "\n" + top_priority).lower()

    if "risk" in lower and "urgency" in lower:
        return (
            "- 1 kritik riski netleştir\n"
            "- 1 acil kararı bugün kapat\n"
            "- 1 dikkat dağıtan konuyu ertele"
        )

    if "ai" in lower or "cloud" in lower or "strategic fit" in lower:
        return (
            "- 1 AI/cloud fırsatını seç\n"
            "- 1 somut use-case veya aksiyon tanımla\n"
            "- 1 gereksiz gündemi bugünden çıkar"
        )

    if "revenue" in lower:
        return (
            "- 1 gelir etkisi yüksek fırsatı öne al\n"
            "- 1 müşteri / teklif / çıktı başlığını ilerlet\n"
            "- 1 düşük getirili işi ertele"
        )

    return (
        "- 1 ana odağı seç\n"
        "- 1 somut aksiyonu bugün tamamla\n"
        "- 1 dikkat dağıtan işi ertele"
    )


# ---------------- ANA İÇERİK ----------------
def build_sabah_rutini(news, weather):
    global_news = news.get("global", [])[:3]
    tech_news = news.get("technology", [])[:2]
    business_news = news.get("business", [])[:2]

    ayet = get_daily_ayah()
    book_title, book_reason = generate_book_recommendation(news)
    poem_text = generate_poem_line(news)
    ai_text = generate_ai_insight(news)
    aein_text = generate_aein_decision(news)
    top_priority = build_top_priority_from_scores(aein_text)
    action_engine = build_action_engine(aein_text, top_priority)
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
    msg.append("")

    msg.append("*8) Günün Dizesi*")
    msg.append(poem_text)

    msg.append("")
    msg.append("*🧠 AEIN Decision Engine*")
    msg.append(aein_text)

    msg.append("")
    msg.append("*🔥 Top Priority*")
    msg.append(top_priority)

    msg.append("")
    msg.append("*⚡ Action Engine*")
    msg.append(action_engine)

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
