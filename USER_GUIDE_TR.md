# PulseAI Kullanım Kılavuzu

Bu doküman PulseAI'nin nasıl kurulacağını, yapılandırılacağını ve çalıştırılacağını adım adım açıklar.

PulseAI, bilgiyi aşağıdakilere dönüştüren günlük bir karar sistemidir:

- İçgörü
- Öncelik
- Aksiyon
- Fırsat

Çıktı Telegram üzerinden yapılandırılmış bir briefing olarak gönderilir.

--------------------------------------------------

# 1. Sistem Gereksinimleri

PulseAI Linux üzerinde en stabil çalışır.

Önerilen sistemler:

- Fedora
- Red Hat Enterprise Linux (RHEL)
- Rocky Linux / AlmaLinux
- Ubuntu / Debian

Gerekenler:

- Python 3.10+
- İnternet erişimi
- Telegram bot token
- Telegram chat id

Opsiyonel:

- OpenAI API anahtarı

--------------------------------------------------

# 2. Dil Desteği

PulseAI iki dil destekler:

TR  
EN  

config.json içinde ayarlanır:

{
  "language": "TR"
}

TR = Türkçe briefing  
EN = İngilizce briefing  

--------------------------------------------------

# 3. Windows Kullanıcıları

PulseAI Linux için tasarlanmıştır.

Windows için önerilen çözüm:

WSL kullanmaktır.

WSL = Windows içinde Linux çalıştırma.

Kurulum:

wsl --install

Windows yeniden başlatılır.

Ubuntu kurulur.

WSL içinde Python kurulur:

sudo apt update
sudo apt install python3 python3-pip

Proje normal şekilde çalıştırılır.

Bu en stabil yöntemdir.

--------------------------------------------------

# 4. Proje Yapısı

Ana dosyalar:

morning_brief.py     → ana script  
config.json          → konfigürasyon  
README.md            → İngilizce doküman  
README_TR.md         → Türkçe doküman  
USER_GUIDE.md        → İngilizce kullanım kılavuzu  
USER_GUIDE_TR.md     → Türkçe kullanım kılavuzu  
archive/             → yedekler  

--------------------------------------------------

# 5. Kurulum

Gerekli Python paketlerini yüklemek için:

pip install -r requirements.txt

veya

pip3 install -r requirements.txt

requirements.txt dosyası proje için gerekli paketleri içerir:

- requests → API çağrıları için  
- feedparser → RSS haberlerini okumak için  

--------------------------------------------------

# 6. Telegram Ayarı

Telegram değişkenlerini ayarla:

export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TG_CHAT_ID="YOUR_CHAT_ID"

Kalıcı yapmak için:

echo 'export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"' >> ~/.bashrc
echo 'export TG_CHAT_ID="YOUR_CHAT_ID"' >> ~/.bashrc

source ~/.bashrc

--------------------------------------------------

# 7. OpenAI Ayarı (Opsiyonel)

PulseAI iki modda çalışır:

AI Mode  
Fallback Mode  

AI aktif etmek için:

export OPENAI_API_KEY="YOUR_API_KEY"

API anahtarı yoksa sistem fallback modda çalışır.

--------------------------------------------------

# 8. Konfigürasyon Dosyası

config.json düzenlenir.

Örnek:

{
  "city": "Istanbul",
  "language": "TR"
}

--------------------------------------------------

# 9. Briefing Yapısı

PulseAI 14 bölüm üretir:

1 Günün Özeti  
2 Global Manşetler  
3 Piyasa Özeti  
4 Cloud / Platform Radarı  
5 Fikir Sinyalleri  
6 AI / Teknoloji Radarı  
7 Speaking Practice  
8 Kitap Önerisi  
9 Günlük Yansıma  
10 Günün Sözü  
11 Karar İçgörüsü  
12 En Yüksek Öncelik  
13 Aksiyon Planı  
14 Yönetici İçgörüsü  

--------------------------------------------------

# 10. Çalıştırma

python3 morning_brief.py

--------------------------------------------------

# 11. Script Kontrol

python3 -m py_compile morning_brief.py

--------------------------------------------------

# 12. Cron Otomasyonu

crontab -e

Örnek:

0 8 * * * /usr/bin/python3 /home/USER/morning-briefing-bot/morning_brief.py

--------------------------------------------------

# 13. Cron Wrapper Script

run_briefing.sh oluştur:

#!/bin/bash
export TG_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TG_CHAT_ID="YOUR_CHAT_ID"
export OPENAI_API_KEY="YOUR_API_KEY"
/usr/bin/python3 /home/USER/morning-briefing-bot/morning_brief.py

Çalıştırılabilir yap:

chmod +x run_briefing.sh

--------------------------------------------------

# 14. Yedekleme Politikası

Aktif dosya:

morning_brief.py

Yedekler:

archive/

Sadece local (GitHub'a push edilmez):

brain.md

--------------------------------------------------

# 15. Önerilen Akış

1 config düzenle  
2 compile kontrol  
3 manuel çalıştır  
4 telegram kontrol  
5 cron ekle  

--------------------------------------------------

# 16. Notlar

PulseAI fallback modda da çalışır.

AI yoksa sistem durmaz.

Telegram gönderimi zorunludur.

Linux önerilir.

Windows için WSL önerilir.

--------------------------------------------------

# 17. Amaç

PulseAI şu amaçlarla tasarlanmıştır:

- gündemi sadeleştirmek
- öncelik belirlemek
- aksiyon üretmek
- gereksiz bilgiyi filtrelemek
- karar almayı hızlandırmak

