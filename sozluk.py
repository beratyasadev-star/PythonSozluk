# sozluk.py

# Sözlük Veri Yapısı: Uygulamanın temel kelime ve tanım deposu
# Program her çalıştığında bu verilerle başlar.
sozluk = {
    "python": "Yüksek seviyeli, yorumlamalı ve genel amaçlı bir programlama dilidir.",
    "flask": "Python ile yazılmış hafif bir web çatısı (framework).",
    "venv": "Python projeleri için bağımlılıkları izole eden sanal ortamdır."
}

def kelime_ara():
    """Kullanıcıdan kelime alır ve sözlükte arama yapar."""
    print("\n--- Kelime Arama Ekranı ---")
    
    # Kullanıcıdan giriş alma
    aranan_kelime = input("Aramak istediğiniz kelimeyi girin: ").lower().strip()
    
    # Sözlükte arama
    if aranan_kelime in sozluk:
        tanim = sozluk[aranan_kelime]
        print(f"\n✅ Kelime: {aranan_kelime.capitalize()}")
        print(f"Tanım: {tanim}")
    else:
        print(f"\n❌ Üzgünüm, '{aranan_kelime}' kelimesi sözlükte bulunamadı.")


def kelime_ekle():
    """Kullanıcıdan yeni kelime ve tanım alarak sözlüğe ekler."""
    print("\n--- Yeni Kelime Ekleme Ekranı ---")
    
    # Yeni kelimeyi al
    yeni_kelime = input("Eklemek istediğiniz kelimeyi girin: ").lower().strip()
    
    # Eğer kelime zaten varsa uyarı ver
    if yeni_kelime in sozluk:
        print(f"⚠️ '{yeni_kelime}' zaten sözlükte mevcut. Tanımı: {sozluk[yeni_kelime]}")
        return

    # Yeni tanımı al
    yeni_tanim = input(f"'{yeni_kelime}' kelimesinin tanımını girin: ").strip()
    
    # Sözlüğe ekle (Python'da sözlüğe eklemek bu kadar basittir)
    sozluk[yeni_kelime] = yeni_tanim
    
    print(f"\n✅ '{yeni_kelime}' sözlüğe başarıyla eklendi.")


def ana_menu():
    """Uygulamanın ana menüsünü ve döngüsünü yönetir."""
    print("-" * 40)
    print("🤖 Python Konsol Sözlük Uygulaması")
    print(f"Mevcut kelime sayısı: {len(sozluk)}")
    print(f"Aranabilir kelimeler: {', '.join(sozluk.keys())}")
    print("-" * 40)

    while True:
        print("\nNe yapmak istersiniz?")
        secim = input("1: Kelime Ara, 2: Kelime Ekle, 3: Çıkış (1/2/3): ").strip()

        if secim == '1':
            kelime_ara()
        elif secim == '2':
            kelime_ekle()
        elif secim == '3':
            print("Uygulamadan çıkılıyor. Güle güle!")
            break
        else:
            print("Geçersiz seçim. Lütfen 1, 2 veya 3 girin.")

# Programın başlangıç noktası
if __name__ == "__main__":
    ana_menu()