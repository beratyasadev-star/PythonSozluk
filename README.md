# PythonSozluk 📚

Modern, web tabanlı bir Türkçe sözlük uygulaması. Kelimelerin anlamlarını Wiktionary ve Nisanyan gibi kaynaklardan çekip kaydeder, dilediğiniz zaman erişmenizi sağlar.

## 🌐 Canlı Demo

**Frontend (Kullanıcı Arayüzü):** https://beratyasadev-star.github.io/PythonSozluk/  

## 🎯 Proje Nedir?

Bu proje iki ana bölümden oluşuyor:

### 1. **Backend (Arka Plan Servisi)**
Python ile yazılmış bir web servisi. Kelimelerin anlamlarını internetten bulup kaydeder ve istediğinizde size sunar.

**Kullanılan Teknolojiler:**
- **Python + FastAPI:** Hızlı ve modern bir web framework
- **BeautifulSoup4:** Web sayfalarından bilgi çekmek için
- **JSON:** Kelimeleri saklamak için basit dosya sistemi

**Ne Yapar:**
- Kelime araması yaparsınız → Wiktionary ve Nisanyan'dan anlam bulur
- Bulunan anlamları kaydeder → Tekrar arama yapmanıza gerek kalmaz
- API üzerinden kelime ekleme, listeleme, silme işlemleri yapar

### 2. **Frontend (Kullanıcı Arayüzü)**
React ile yapılmış modern ve kullanıcı dostu bir web arayüzü.

**Kullanılan Teknolojiler:**
- **React 18:** Modern kullanıcı arayüzü için
- **Vite:** Hızlı geliştirme ve derleme aracı
- **CSS:** Temiz ve responsive tasarım

**Ne Yapar:**
- Kelime arama kutucuğu
- Sonuçları anında gösterir
- Tüm kelimeleri listeleyebilirsiniz
- Yeni kelime ekleyebilirsiniz

## 🚀 Nasıl Çalışıyor?

1. **Kelime Arıyorsunuz:** Web arayüzünde bir kelime yazıyorsunuz
2. **Backend Çalışıyor:** Sunucu önce kendi veritabanına bakıyor
3. **Bulamazsa İnternetten Çekiyor:** Wiktionary veya Nisanyan'dan anlam buluyor
4. **Kaydediyor:** Bulduğu anlamı JSON dosyasına kaydediyor
5. **Size Gösteriyor:** Sonucu anında ekranınıza getiriyor

## 🏗️ Deployment (Yayınlama)

Projeyi internete açmak için iki farklı platform kullandık:

### **Frontend → GitHub Pages**
- **Nedir:** GitHub'ın sunduğu ücretsiz web hosting servisi
- **Neden:** Statik (HTML/CSS/JS) dosyalar için ideal, hızlı ve güvenilir
- **Nasıl:** Vite ile derlenmiş dosyalar `gh-pages` branch'ine yüklendi

### **Backend → Render**
- **Nedir:** Python uygulamalarını ücretsiz host edebilen bulut platformu
- **Neden:** Sürekli çalışan API servisleri için uygun, kolay kurulum
- **Nasıl:** `render.yaml` config dosyası ile otomatik deployment

## 💻 Yerel Geliştirme (Kendi Bilgisayarınızda Çalıştırma)

### Gereksinimler
- Python 3.8+
- Node.js 16+
- npm veya yarn

### Backend'i Çalıştırma

```bash
# 1. Sanal ortam oluştur
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

# 2. Paketleri yükle
pip install -r requirements.txt

# 3. Servisi başlat
python -m uvicorn app:app --reload --port 8000
```

Backend şimdi `http://localhost:8000` adresinde çalışıyor.

### Frontend'i Çalıştırma

```bash
# 1. Frontend klasörüne git
cd frontend

# 2. Paketleri yükle
npm install

# 3. Geliştirme sunucusunu başlat
npm run dev
```

Frontend şimdi `http://localhost:5173` adresinde çalışıyor.

## 📖 Konsol Uygulaması

Eski, terminal tabanlı versiyonu da hala çalışıyor:

```bash
python sozluk.py
```

Menüden kelime arama, ekleme, listeleme yapabilirsiniz.

## 📁 Proje Yapısı

```
PythonSozluk/
├── app.py                  # FastAPI backend servisi
├── sozluk.py              # Konsol uygulaması (eski versiyon)
├── sozluk_data.json       # Kelime veritabanı (JSON)
├── requirements.txt       # Python bağımlılıkları
├── render.yaml            # Render deployment ayarları
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Ana React bileşeni
│   │   ├── main.jsx       # React entry point
│   │   └── styles.css     # Stil dosyası
│   ├── index.html         # HTML template
│   └── package.json       # Frontend bağımlılıkları
└── README.md              # Bu dosya
```

## 🛠️ Teknik Detaylar

### API Endpoints (Backend)

- `GET /health` - Servis sağlık kontrolü
- `GET /lookup?word={kelime}` - Kelime ara
- `GET /words` - Tüm kelimeleri listele
- `POST /add` - Yeni kelime ekle
- `POST /bulk` - Toplu kelime yükle

### CORS (Cross-Origin Resource Sharing)

Backend, frontend'den gelen istekleri kabul edebilmek için CORS ayarlandı:
- GitHub Pages: `https://beratyasadev-star.github.io`
- Local development: `http://localhost:5173` ve `http://127.0.0.1:5173`

### Environment Variables

**Frontend için:**
- `VITE_API_BASE` - Backend API adresi (build time'da ayarlanır)

## 🔄 Deployment Süreci

### Frontend Deployment
```bash
cd frontend
VITE_API_BASE="https://pythonsozluk.onrender.com" npm run build -- --base /PythonSozluk/
# Ardından dist/ klasörü gh-pages branch'ine push edilir
```

### Backend Deployment
Render'a push yaptığınızda `render.yaml` otomatik olarak:
1. Python bağımlılıklarını yükler (`pip install -r requirements.txt`)
2. Uvicorn ile FastAPI uygulamasını başlatır
3. $PORT environment variable üzerinden çalışır

## 🌟 Özellikler

- ✅ Web tabanlı modern arayüz
- ✅ Gerçek zamanlı kelime arama
- ✅ Otomatik tanım çekme (Wiktionary & Nisanyan)
- ✅ Yerel veritabanı (JSON)
- ✅ Toplu kelime yükleme
- ✅ Responsive tasarım
- ✅ Ücretsiz hosting (GitHub Pages + Render)

## 📝 Gelecek Geliştirmeler

- [ ] Kullanıcı hesapları ve favoriler
- [ ] Kelime geçmişi
- [ ] Örnek cümleler
- [ ] Sesli telaffuz
- [ ] Dark mode

## 🤝 Katkıda Bulunma

Projeyi fork'layıp pull request gönderebilirsiniz. Her türlü katkı ve öneri değerlidir!



---

**Geliştirici:** beratyasa  
**Tarih:** Kasım 2025  
**Teknolojiler:** Python, FastAPI, React, Vite, GitHub Pages, Render
