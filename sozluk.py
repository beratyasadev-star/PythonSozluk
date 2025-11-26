# sozluk.py

import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import json
from pathlib import Path

# Veri dosyası
DATA_FILE = Path(__file__).with_name('sozluk_data.json')

# Sözlük Veri Yapısı: Uygulamanın temel kelime ve tanım deposu
sozluk = {
    "python": "Yüksek seviyeli, yorumlamalı ve genel amaçlı bir programlama dilidir.",
    "flask": "Python ile yazılmış hafif bir web çatısı (framework).",
    "venv": "Python projeleri için bağımlılıkları izole eden sanal ortamdır."
}


def save_sozluk():
    """Mevcut `sozluk` sözlüğünü `sozluk_data.json` dosyasına kaydeder."""
    try:
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(sozluk, f, ensure_ascii=False, indent=2)
        print(f"💾 Sözlük kaydedildi -> {DATA_FILE}")
    except Exception as e:
        print(f"⚠️ Kaydetme hatası: {e}")


def load_sozluk():
    """Varsa `sozluk_data.json` dosyasından verileri yükler ve mevcut `sozluk` ile birleştirir."""
    if not DATA_FILE.exists():
        return
    try:
        with DATA_FILE.open('r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, dict):
            # Yeni anahtarları ekle, mevcutları bozmadan
            for k, v in data.items():
                if k not in sozluk:
                    sozluk[k] = v
        print(f"📂 Sözlük dosyasından yüklendi: {DATA_FILE}")
    except Exception as e:
        print(f"⚠️ Yükleme hatası: {e}")

# Başlangıçta varsa kayıtlı veriyi yükle
load_sozluk()


def bulk_load_from_source(source, kelime_sayisi=1000):
    """Verilen `source` bir URL veya yerel dosya yolu olabilir.
    İçinden satır bazlı kelime listesi okur ve ilk `kelime_sayisi` kelimeyi yüklemeye çalışır.
    """
    # Kaynaktan satırları al
    words = []
    try:
        if source.startswith('http://') or source.startswith('https://'):
            r = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            r.raise_for_status()
            text = r.text
            # Frekans listelerini (word count format) destek et
            words = []
            for line in text.splitlines():
                line = line.strip()
                if line:
                    # İlk sütunu (kelimeyi) al, kalanını (sayı) yoksay
                    parts = line.split()
                    if parts:
                        words.append(parts[0])
        else:
            p = Path(source)
            if not p.exists():
                print(f"⚠️ Kaynak dosya bulunamadı: {source}")
                return
            with p.open('r', encoding='utf-8') as f:
                words = []
                for line in f.readlines():
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if parts:
                            words.append(parts[0])
    except Exception as e:
        print(f"⚠️ Kaynak okuma hatası: {e}")
        return

    if not words:
        print("⚠️ Kaynakta kelime bulunamadı.")
        return

    hedef = words[:kelime_sayisi]
    print(f"\n🔁 Toplu yükleme başlıyor: kaynak={source} hedef_kelime_sayisi={len(hedef)}")
    eklenen = 0
    for w in hedef:
        k = w.lower().strip()
        if not k or k in sozluk:
            continue
        # dene: wiktionary then nisanyan
        tanim = wiktionary_kelime_cek(k)
        kaynak = 'Wiktionary'
        if not tanim:
            tanim = nisanyan_kelime_cek(k)
            kaynak = 'Nisanyan'
        if tanim:
            sozluk[k] = tanim
            eklenen += 1
            if eklenen % 50 == 0:
                print(f"{eklenen} kelime eklendi...")
        # küçük bekleme
        time.sleep(0.15)

    print(f"\n✨ Toplu yükleme tamamlandı. Eklenen: {eklenen}")
    if eklenen:
        save_sozluk()
    return eklenen


def nisanyan_kelime_cek(kelime):
    """Nisanyan Sözlüğü'nden belirli bir kelimeyi çeker."""
    try:
        url = f"https://nisanyan.org/?k={kelime}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Nisanyan'ın sayfa yapısına göre tanımları bul
        anlamlar_div = soup.find('div', class_='anlamlar')
        
        if anlamlar_div:
            ilk_anlam = anlamlar_div.find('span')
            if ilk_anlam:
                tanim = ilk_anlam.get_text(strip=True)
                if tanim:
                    return tanim[:200]  # İlk 200 karakteri al
        
        return None
        
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None


def wiktionary_kelime_cek(kelime):
    """Wiktionary (Türkçe) sayfasından bir kelimenin tanımını çekmeye çalışır."""
    try:
        base = "https://tr.wiktionary.org/wiki/"
        url = base + urllib.parse.quote(kelime)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=8)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')

        # Wiktionary'de "Türkçe" başlığı bulunur (span id="Türkçe").
        span = soup.find('span', id='Türkçe')
        if not span:
            # bazen başlık farklı olabilir veya dil bölümü yoktur
            # fallback: sayfadaki ilk anlam listesi
            ol = soup.find('ol')
            if ol:
                li = ol.find('li')
                if li:
                    return li.get_text(" ", strip=True)[:300]
            return None

        # Türkçe bölümünü bulup takip eden kardeş elemanlarda ilk <ol> içindeki <li>'yi al
        parent = span.parent
        for sib in parent.find_next_siblings():
            if sib.name == 'ol':
                li = sib.find('li')
                if li:
                    return li.get_text(" ", strip=True)[:300]
            # bazı sayfalarda tanımlar <ul> veya <p> içinde olabilir
            if sib.name in ('p', 'ul'):
                text = sib.get_text(" ", strip=True)
                if text:
                    return text[:300]

        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


def nisanyan_sozlugu_yukle(kelime_sayisi=20):
    """Nisanyan Sözlüğü'nden toplu kelime çeker."""
    print("\n🔄 Nisanyan Sözlüğü'nden kelimeler yükleniyor...")
    
    # Yaygın Türkçe kelimeleri
    populer_kelimeler = [
        "aşk", "bilim", "dostluk", "eğitim", "felsefe", "gülümseme", 
        "hayat", "iyilik", "jandarma", "kültür", "liman", "matematik",
        "nesne", "osmanlı", "paşa", "rehber", "sanat", "teknoloji",
        "uyarı", "vatan", "yazı", "zaman", "anlam", "barış", "cemet",
        "dakika", "ek", "forma", "güzel", "hukuk", "insan"
    ]
    
    eklenen = 0
    for i, kelime in enumerate(populer_kelimeler[:kelime_sayisi]):
        if kelime not in sozluk:
            # Önce Wiktionary deneyelim, sonra Nisanyan'a fallback yap
            tanim = wiktionary_kelime_cek(kelime)
            kaynak = "Wiktionary"
            if not tanim:
                tanim = nisanyan_kelime_cek(kelime)
                kaynak = "Nisanyan"

            if tanim:
                sozluk[kelime] = tanim
                eklenen += 1
                print(f"✅ {kelime}: eklendi ({eklenen}/{kelime_sayisi}) - kaynak: {kaynak}")
            else:
                print(f"⏭️ {kelime}: atlandı (kaynak bulunamadı)")
            
            # Sunucuya aşırı yük bindirme
            time.sleep(0.5)
        
        if eklenen >= kelime_sayisi:
            break
    
    print(f"\n✨ Toplam {eklenen} kelime eklendi!\n")
    if eklenen > 0:
        save_sozluk()


def kelime_ara():
    """Kullanıcıdan kelime alır ve sözlükte arama yapar."""
    print("\n--- Kelime Arama Ekranı ---")
    
    aranan_kelime = input("Aramak istediğiniz kelimeyi girin: ").lower().strip()
    
    if aranan_kelime in sozluk:
        tanim = sozluk[aranan_kelime]
        print(f"\n✅ Kelime: {aranan_kelime.capitalize()}")
        print(f"Tanım: {tanim}")
        print("Tebrikler! 🎉")
    else:
        print(f"\n❌ Üzgünüm, '{aranan_kelime}' kelimesi sözlükte bulunamadı.")


def kelime_ekle():
    """Kullanıcıdan yeni kelime ve tanım alarak sözlüğe ekler."""
    print("\n--- Yeni Kelime Ekleme Ekranı ---")
    
    yeni_kelime = input("Eklemek istediğiniz kelimeyi girin: ").lower().strip()
    
    if yeni_kelime in sozluk:
        print(f"⚠️ '{yeni_kelime}' zaten sözlükte mevcut. Tanımı: {sozluk[yeni_kelime]}")
        return

    yeni_tanim = input(f"'{yeni_kelime}' kelimesinin tanımını girin: ").strip()
    
    sozluk[yeni_kelime] = yeni_tanim
    print(f"\n✅ '{yeni_kelime}' sözlüğe başarıyla eklendi.")
    # Değişiklikleri kaydet
    save_sozluk()


def tum_kelimeler_goruntule():
    """Sözlükteki tüm kelimeleri listeler."""
    print("\n--- Mevcut Kelimeler ---")
    if sozluk:
        for i, (kelime, tanim) in enumerate(sozluk.items(), 1):
            print(f"{i}. {kelime}: {tanim[:80]}...")
    else:
        print("Sözlükte henüz kelime yok.")


def ana_menu():
    """Uygulamanın ana menüsünü ve döngüsünü yönetir."""
    print("-" * 50)
    print("🤖 Python Konsol Sözlük Uygulaması")
    print(f"Mevcut kelime sayısı: {len(sozluk)}")
    print("-" * 50)

    while True:
        print("\nNe yapmak istersiniz?")
        print("1: Kelime Ara")
        print("2: Kelime Ekle") 
        print("3: Nisanyan'dan Kelime Yükle")
        print("4: Tüm Kelimeleri Görüntüle")
        print("5: Çıkış")
        
        secim = input("\nSeçiminiz (1-5): ").strip()

        if secim == '1':
            kelime_ara()
        elif secim == '2':
            kelime_ekle()
        elif secim == '3':
            try:
                miktar = input("Kaç kelime yüklemek istersiniz? (default: 20): ").strip()
                miktar = int(miktar) if miktar.isdigit() else 20
                nisanyan_sozlugu_yukle(kelime_sayisi=miktar)
            except ValueError:
                print("❌ Geçersiz sayı girdiniz.")
        elif secim == '4':
            tum_kelimeler_goruntule()
        elif secim == '5':
            print("\nUygulamadan çıkılıyor. Güle güle! 👋")
            # Çıkmadan önce kaydet
            save_sozluk()
            break
        else:
            print("❌ Geçersiz seçim. Lütfen 1-5 arasında bir sayı girin.")


# Programın başlangıç noktası
if __name__ == "__main__":
    ana_menu()
