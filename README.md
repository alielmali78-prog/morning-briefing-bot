# Morning Briefing Bot

Telegram için Türkçe yönetici brifingi üreten otomatik briefing bot.

## Özellikler

- 14 bölümlü sabit briefing yapısı
- Türkçe haber kaynakları
- Cloud / AI radar
- Fikir sinyalleri üretimi
- Executive karar içgörüsü
- Günlük ayet (TR)
- Günün sözü (TR)
- Speaking practice
- Kitap önerisi
- Spam haber filtreleme
- Bölümler arası tekrar engelleme
- Telegram markdown output

## Bölümler

1. Günün Özeti  
2. Global Manşetler  
3. Piyasa Özeti  
4. Bulut / Platform Radarı  
5. Fikir Sinyalleri  
6. AI / Teknoloji Radarı  
7. Speaking Practice  
8. Kitap Önerisi  
9. Günlük Yansıma (Ayet)  
10. Günün Sözü  
11. Karar İçgörüsü  
12. En Yüksek Öncelik  
13. Aksiyon Planı  
14. Yönetici İçgörüsü  

## Kaynaklar

### Haber
- AA
- TRT Haber
- BBC Türkçe

### Teknoloji
- Webrazzi
- Donanım Haber
- CIO Türkiye

### Ekonomi
- BloombergHT
- Ekonomim

## Filtreler

Sistem otomatik olarak şunları filtreler:

- ihale
- hizmeti alınacaktır
- satın alma
- ilan
- duyuru
- teklif

## Deduplicate

Cloud ve AI bölümleri arasında tekrar eden haberler otomatik kaldırılır.

## Çalıştırma

```bash
python3 morning_brief.py
