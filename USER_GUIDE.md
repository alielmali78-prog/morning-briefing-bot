# PulseAI — Quick Start Guide

Get started in 5 minutes.

---

## 🚀 What is PulseAI?

PulseAI is a daily decision system.

It transforms global information into:
- Insight
- Priority
- Action

Instead of reading news, you get **what to focus on today**.

---

## ⚙️ 1. Requirements

- Python 3
- Internet connection
- Telegram account

Optional:
- OpenAI API key (for richer insights)

---

## 📦 2. Installation

```bash
git clone https://github.com/alielmali78-prog/morning-briefing-bot.git
cd morning-briefing-bot
pip install requests feedparser
##
3. Setup Environment

Set your Telegram credentials:
export TG_TOKEN="YOUR_BOT_TOKEN"
export TG_CHAT_ID="YOUR_CHAT_ID"


4. Create Telegram Bot
Open Telegram
Search for BotFather
Create a new bot
Copy the token
Send a message to your bot
▶️ 5. Run PulseAI
python3 morning_brief.py

You will receive a daily briefing message in Telegram.

🧠 6. How to Use

Focus on these sections:

🔥 Top Priority

Your most important focus today

⚡ Action Plan

What you should do today

🧠 Decision Insight

Context and reasoning

📈 7. Example Daily Flow

Morning:

Read Top Priority
Pick 1 action

During the day:

Execute that action
🔄 8. Automation (Optional)

Run automatically every morning using cron:

30 5 * * * python3 /path/to/morning_brief.py
❗ Troubleshooting
No Telegram message
Check TG_TOKEN
Check TG_CHAT_ID
AI not working
Check OPENAI_API_KEY
API quota may be exceeded
Script runs but content is basic
System is running in fallback mode (normal)
🧠 Final Advice

Do not read everything.

Focus → Decide → Act

EOF




---

## 🔐 OpenAI API Key

PulseAI can optionally use OpenAI for richer insights.

Each user must provide their own API key.

### Set your API key

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
What happens without an API key?

If no API key is provided, PulseAI will still run.

In that case, it works in fallback mode:

no advanced AI generation
built-in smart logic is used instead
the system remains usable and stable
Important
Do not hardcode your API key into the script
Do not commit your API key to GitHub
Do not share your API key with others
