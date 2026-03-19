# Morning Briefing Bot

Telegram üzerinden her sabah otomatik briefing gönderen kişisel asistan sistemi.

## Özellikler

- Global haber başlıkları
- 7 parçalı sabah haber rutini
- İstanbul hava durumu
- AI / Cloud / teknoloji başlıkları
- English booster
- Günün ayeti
- Kitap önerisi
- Opsiyonel şiir dizesi

## Kullanılan Teknolojiler

- Python 3
- Telegram Bot API
- Google News RSS
- Open-Meteo API
- Cron
- GitHub

## Nasıl Çalışır?

Sistem şu akışla çalışır:

1. Cron her sabah belirlenen saatte script'i çalıştırır
2. Script haber başlıklarını RSS üzerinden çeker
3. Hava durumu verisini Open-Meteo API’den alır
4. İçeriği sabah briefing formatında birleştirir
5. Telegram bot üzerinden kullanıcıya gönderir

## Kurulum

### Gereksinimler

```bash
pip install requests feedparser
