# PulseAI User Guide

This document explains how to install, configure, and run PulseAI step by step.

PulseAI is a daily executive briefing system that collects information and converts it into:

- Insight
- Priority
- Action
- Opportunity

The output is delivered as a structured Telegram briefing.

--------------------------------------------------

# 1. System Requirements

PulseAI works best on Linux.

Recommended environments:

- Fedora
- Red Hat Enterprise Linux (RHEL)
- Rocky Linux / AlmaLinux
- Ubuntu / Debian

Required:

- Python 3.10+
- Internet access
- Telegram bot token
- Telegram chat ID

Optional:

- OpenAI API key

--------------------------------------------------

# 2. Language Support

PulseAI supports two language modes:

TR  
EN  

Set language in config.json:

{
  "language": "TR"
}

TR = Turkish briefing  
EN = English briefing  

--------------------------------------------------

# 3. Windows Users

PulseAI is designed for Linux.

If you use Windows, the recommended solution is WSL.

WSL = Windows Subsystem for Linux

This allows running Linux inside Windows.

Recommended steps:

Install WSL:

wsl --install

Reboot Windows

Install Ubuntu inside WSL

Open Ubuntu terminal

Install Python:

sudo apt update
sudo apt install python3 python3-pip

Clone project and run normally.

This is the most stable Windows setup.

Native Windows is possible but not recommended.

Issues may include:

environment variables  
cron scheduling  
shell differences  
path handling  

WSL solves these.

--------------------------------------------------

# 4. Project Structure

Main files:

morning_brief.py     → main script  
config.json          → configuration  
README.md            → English product doc  
README_TR.md         → Turkish product doc  
USER_GUIDE.md        → English guide  
USER_GUIDE_TR.md     → Turkish guide  
archive/             → backups  

--------------------------------------------------

# 5. Install Dependencies

Install Python packages:

pip install -r requirements.txt

or

pip3 install -r requirements.txt

--------------------------------------------------

# 6. Configure Telegram

Set Telegram variables:

export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TG_CHAT_ID="YOUR_CHAT_ID"

Persist variables:

echo 'export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"' >> ~/.bashrc
echo 'export TG_CHAT_ID="YOUR_CHAT_ID"' >> ~/.bashrc

source ~/.bashrc

--------------------------------------------------

# 7. OpenAI Configuration (Optional)

PulseAI works in two modes:

AI Mode  
Fallback Mode  

Enable AI mode:

export OPENAI_API_KEY="YOUR_API_KEY"

Without API key PulseAI still works.

--------------------------------------------------

# 8. Configuration File

Edit config.json

Example:

{
  "city": "Istanbul",
  "language": "TR",
  "sections": {
    "weather": true,
    "summary": true,
    "global_headlines": true,
    "market_snapshot": true,
    "cloud_platform_radar": true,
    "idea_signals": true,
    "ai_tech_radar": true,
    "speaking_practice": true,
    "book_recommendation": true,
    "decision_insight": true
  }
}

--------------------------------------------------

# 9. Briefing Structure

PulseAI generates 14 sections:

1 Summary  
2 Global Headlines  
3 Market Snapshot  
4 Cloud / Platform Radar  
5 Idea Signals  
6 AI / Technology Radar  
7 Speaking Practice  
8 Book Recommendation  
9 Daily Reflection  
10 Daily Quote  
11 Decision Insight  
12 Top Priority  
13 Action Plan  
14 Executive Insight  

--------------------------------------------------

# 10. Run PulseAI

Manual run:

python3 morning_brief.py

Expected:

news collected  
briefing generated  
telegram sent  

--------------------------------------------------

# 11. Validate Script

python3 -m py_compile morning_brief.py

If no output → OK

--------------------------------------------------

# 12. Cron Automation

Open cron:

crontab -e

Run every day 08:00:

0 8 * * * /usr/bin/python3 /home/USER/morning-briefing-bot/morning_brief.py

Example 06:30:

30 6 * * * /usr/bin/python3 /home/USER/morning-briefing-bot/morning_brief.py

--------------------------------------------------

# 13. Cron Wrapper Script (Recommended)

Create run_briefing.sh

#!/bin/bash
export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TG_CHAT_ID="YOUR_CHAT_ID"
export OPENAI_API_KEY="YOUR_API_KEY"
/usr/bin/python3 /home/USER/morning-briefing-bot/morning_brief.py

Make executable:

chmod +x run_briefing.sh

Cron:

0 8 * * * /home/USER/morning-briefing-bot/run_briefing.sh

--------------------------------------------------

# 14. Troubleshooting

No Telegram message:

check token  
check chat id  
check internet  
check bot started  

AI not working:

check OPENAI_API_KEY  
check quota  

Cron not working:

use wrapper script  

Windows problems:

use WSL  

--------------------------------------------------

# 15. Backup Policy

Active file:

morning_brief.py

Backups:

archive/

Local only:

brain.md

--------------------------------------------------

# 16. Recommended Workflow

1 edit config  
2 compile check  
3 run manually  
4 confirm telegram  
5 add cron  

Example:

python3 -m py_compile morning_brief.py
python3 morning_brief.py
crontab -e

--------------------------------------------------

# 17. Purpose

PulseAI is designed to:

simplify information  
identify priority  
produce action  
reduce noise  
accelerate decision making  

