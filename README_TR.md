# Morning Briefing Bot (TR)

Telegram üzerinden günlük yönetici brifingi üreten, Türkçe kaynaklarla çalışan ve yapılandırılabilir briefing bot.

## Genel Amaç

Bu proje, her gün tek mesajda şu alanları özetleyen bir briefing üretir:

- gündemin genel görünümü
- piyasa ve ekonomi gelişmeleri
- bulut / platform trendleri
- yapay zeka / teknoloji sinyalleri
- yönetici içgörüleri
- aksiyon önerileri
- speaking practice
- kitap önerisi
- günlük yansıma ve günün sözü

## Öne Çıkan Özellikler

- 14 bölümlü sabit briefing yapısı
- Türkçe haber kaynakları
- Cloud / Platform ve AI / Teknoloji ayrımı
- tekrar eden haberleri azaltma mantığı
- spam / ihale tarzı içerikleri filtreleme
- Türkçe ayet ve Türkçe söz
- yönetici odaklı karar içgörüsü
- Telegram gönderimi
- config.json ile kontrol edilebilir yapı

## Bölüm Yapısı

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

## Yapılandırma

`config.json` üzerinden aşağıdaki alanlar yönetilir:

- şehir
- dil
- açık / kapalı bölümler
- reflection ayarları

## Çalıştırma

```bash
python3 morning_brief.py

## Notlar

- Ana çalışma dosyası: `morning_brief.py`
- Yedekler: `archive/`
- İngilizce ana dokümantasyon: `README.md`
- Türkçe dokümantasyon: `README_TR.md`
- `brain.md` sadece local kullanım içindir, repo’ya push edilmez

## Hedef

Bu proje, sabah hızlı okunabilir, aksiyon odaklı ve yönetici seviyesinde bir briefing üretmek için tasarlanmıştır.
