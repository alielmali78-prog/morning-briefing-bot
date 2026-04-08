# PulseAI Kullanım Kılavuzu

Bu doküman PulseAI'nin nasıl kurulacağını ve çalıştırılacağını adım adım açıklar.

PulseAI, bilgiyi aşağıdakilere dönüştüren günlük karar sistemidir:

- İçgörü
- Öncelik
- Aksiyon
- Fırsat

Çıktı Telegram üzerinden gönderilir.

--------------------------------------------------

# 1. Sistem Gereksinimleri

PulseAI Linux üzerinde en stabil çalışır.

Önerilen sistemler:

- Fedora
- Red Hat
- Rocky Linux
- Ubuntu
- Debian

Gerekenler:

- Python 3.10+
- internet erişimi
- Telegram bot token
- Telegram chat id

Opsiyonel:

- OpenAI API key

--------------------------------------------------

# 2. Dil Desteği

PulseAI iki dil destekler:

TR  
EN  

config.json içinde ayarlanır:

"language": "TR"

TR = Türkçe briefing  
EN = İngilizce briefing  

--------------------------------------------------

# 3. Windows Kullanıcıları

PulseAI Linux için tasarlanmıştır.

Windows için önerilen çözüm:

WSL kullanmak.

WSL = Windows içinde Linux çalıştırma.

Kurulum:

wsl --install

Restart

Ubuntu aç

Python kur:

sudo apt update
sudo apt install python3 python3-pip

Projeyi çalıştır.

Bu en stabil yöntemdir.

Native Windows mümkündür fakat önerilmez.

--------------------------------------------------

# 4. Proje Yapısı

morning_brief.py → ana script  
config.json → konfigürasyon  
README.md → İngilizce doküman  
README_TR.md → Türkçe doküman  
USER_GUIDE.md → İngilizce kullanım  
USER_GUIDE_TR.md → Türkçe kullanım  
archive/ → yedekler  

--------------------------------------------------


--------------------------------------------------

# 6. Telegram Ayarı

export TG_TOKEN="TOKEN"
export TG_CHAT_ID="CHAT_ID"

kalıcı yapmak için:

echo 'export TG_TOKEN="TOKEN"' >> ~/.bashrc
echo 'export TG_CHAT_ID="CHAT_ID"' >> ~/.bashrc

source ~/.bashrc

--------------------------------------------------

# 7. OpenAI (Opsiyonel)

İki mod vardır:

AI mode  
Fallback mode  

Aktif etmek:

export OPENAI_API_KEY="KEY"

Anahtar yoksa sistem fallback ile çalışır.

--------------------------------------------------

# 8. config.json

Örnek:

{
 "city":"Istanbul",
 "language":"TR"
}

--------------------------------------------------

# 9. Bölümler

1 Günün Özeti  
2 Global Manşetler  
3 Piyasa Özeti  
4 Cloud Radar  
5 Fikir Sinyalleri  
6 AI Radar  
7 Speaking  
8 Kitap  
9 Ayet  
10 Söz  
11 Karar İçgörüsü  
12 Öncelik  
13 Aksiyon  
14 Yönetici İçgörüsü  

--------------------------------------------------

# 10. Çalıştırma

python3 morning_brief.py

--------------------------------------------------

# 11. Compile kontrol

python3 -m py_compile morning_brief.py

--------------------------------------------------

# 12. Cron

crontab -e

0 8 * * * python3 /path/morning_brief.py

--------------------------------------------------


# 13. Backup

Aktif dosya:

morning_brief.py

Yedekler:

archive/

Local-only dosya (GitHub'a push edilmez):

brain.md



- requests → API çağrıları için
- feedparser → RSS haberlerini okumak için


# 5. Kurulum

Gerekli Python kütüphanelerini yüklemek için:

pip install -r requirements.txt

Bu dosya proje için gerekli paketleri içerir:

- requests → API çağrıları için
- feedparser → RSS haberlerini okumak için

