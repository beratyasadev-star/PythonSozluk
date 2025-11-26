PythonSozluk
=============

Kısa: Konsol tabanlı küçük bir Türkçe sözlük uygulaması. Wiktionary ve Nisanyan'dan tanım çekme, lokal JSON kalıcılığı ve toplu yükleme desteği içerir.

Hazırlayan: Proje otomatik güncellemeler ile geliştirildi.

Gereksinimler
------------
- Python 3.8+
- Sanal ortam (önerilir)
- Python paketleri: `requests`, `beautifulsoup4`

Kurulum
-------
1. Sanal ortam oluşturun ve aktifleştirin (örnek):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
# veya
pip install requests beautifulsoup4
```

Kullanım
--------
- Normal interaktif menüyü çalıştırmak için:

```bash
python sozluk.py
```

- Toplu 1000 kelime yüklemek için (yerel dosya veya uzak URL kullanabilirsiniz):

```bash
# Yerel dosyadan (her satır bir kelime):
python -c "from sozluk import bulk_load_from_source; bulk_load_from_source('words.txt', 1000)"

# Uzak URL'den (ham metin içinde satır satır kelimeler):
python -c "from sozluk import bulk_load_from_source; bulk_load_from_source('https://example.com/turkish-words.txt', 1000)"
```

Notlar
-----
- Toplu yükleme önce Wiktionary, sonra Nisanyan (fallback) deneyecek.
- Çekilen tanımlar `sozluk_data.json` dosyasına kaydedilir.
- Nisanyan doğrudan scraping şu an her zaman çalışmayabilir (site değişiklikleri veya placeholder sayfalar olabilir).
- Lütfen telif ve kullanım koşullarına dikkat edin; otomatik çekim yapmadan önce hedef sitenin robots.txt ve kullanım koşullarını inceleyin.

İpuçları
-------
- Eğer proje kökünde hazır bir `words.txt` dosyanız varsa, yukarıdaki komutla doğrudan 1000 kelimeyi çekebilirsiniz.
- Büyük toplu yüklemeler yaparken sunuculara aşırı istek göndermemeye dikkat edin (fonksiyonda küçük beklemeler eklenmiştir).

Daha fazla yardım için: dosyayı açın ve `sozluk.py` içindeki fonksiyonları inceleyin.
