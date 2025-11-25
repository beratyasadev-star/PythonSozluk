# 1. Sözlük Veri Yapısını Oluşturma
# Python'da Dictionary (sözlük) {anahtar: değer} yapısıyla tanımlanır.
sozluk = {
    "python": "Yüksek seviyeli, yorumlamalı ve genel amaçlı bir programlama dilidir.",
    "flask": "Python ile yazılmış hafif bir web çatısı (framework).",
    "venv": "Python projeleri için bağımlılıkları izole eden sanal ortamdır."
}

def kelime_ara():
    """Kullanıcıdan kelime alır ve sözlükte arama yapar."""
    print("-" * 40)
    print("Python Konsol Sözlük Uygulamasına Hoş Geldiniz!")
    print(f"Aranabilir kelimeler: {', '.join(sozluk.keys())}")
    print("-" * 40)

    # Kullanıcıdan giriş alma
    aranan_kelime = input("Aramak istediğiniz kelimeyi girin: ").lower().strip()

    # 2. Sözlükte arama ve çıktı verme
    if aranan_kelime in sozluk:
        tanim = sozluk[aranan_kelime]
        print(f"\n✅ Kelime: {aranan_kelime.capitalize()}")
        print(f"Tanım: {tanim}")
    else:
        print(f"\n❌ Üzgünüm, '{aranan_kelime}' kelimesi sözlükte bulunamadı.")

# Programın başlangıç noktası
if __name__ == "__main__":
    kelime_ara()