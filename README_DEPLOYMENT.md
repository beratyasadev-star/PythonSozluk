# PythonSozluk - Deployment Rehberi

## Canlı Uygulamaya Erişim

### Frontend (GitHub Pages)
Frontend statik siteye yayınlandı:  
**https://beratyasadev-star.github.io/PythonSozluk/**

### Backend API - Deployment Seçenekleri

#### Seçenek 1: Render.com (Önerilen - Easiest)

1. [Render.com](https://render.com) sitesine git ve ücretsiz hesap oluştur.
2. GitHub hesabınızla bağlan ("Connect GitHub").
3. "New +" → "Web Service" seç.
4. GitHub repo seç: `PythonSozluk`.
5. Ayarlar:
   - **Branch**: `main`
   - **Root Directory**: `/` (boş bırak)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Deploy → birkaç dakika sonra live API URL alacaksın (örn: `https://pythonsozluk-xxxxx.onrender.com`).

#### Seçenek 2: Fly.io

1. [Fly.io](https://fly.io) sitesine git, hesap oluştur.
2. Makinene `flyctl` yükle: `brew install flyctl` (macOS).
3. `fly auth login` ile oturum aç.
4. Repository köküne zaten `fly.toml` hazırlı.
5. Terminalde:
   ```bash
   cd /Users/beratyasa/Documents/PythonSozluk
   fly deploy
   ```
6. Canlı URL alacaksın (örn: `https://pythonsozluk.fly.dev`).

#### Seçenek 3: Yerel Test (Development)

Backend'i yerelde çalıştır:
```bash
cd /Users/beratyasa/Documents/PythonSozluk
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Backend `http://localhost:8000` adresinde çalışacak.

---

## Frontend + Backend Entegrasyonu

Backend deploy edildikten sonra frontend'i güncelle:

1. Backend canlı URL'sini al (örn: `https://pythonsozluk-xxxxx.onrender.com`).
2. Frontend'i prod API ile rebuild et:
   ```bash
   cd /Users/beratyasa/Documents/PythonSozluk/frontend
   export VITE_API_BASE="https://pythonsozluk-xxxxx.onrender.com"
   npm run build
   ```
3. Çıktı `frontend/dist/` içine yazılacak.
4. Dist içeriğini `gh-pages` dalına push et:
   ```bash
   rm -rf /tmp/ps-gh-pages || true
   mkdir -p /tmp/ps-gh-pages
   cp -R frontend/dist/* /tmp/ps-gh-pages/
   cd /tmp/ps-gh-pages
   git init
   git remote add origin https://github.com/beratyasadev-star/PythonSozluk.git
   git checkout -b gh-pages
   git add .
   git commit -m "chore: update frontend with prod API"
   git push -f origin gh-pages
   ```
5. Frontend Pages URL'sine git ve API'nin canlı olup olmadığını kontrol et.

---

## Hızlı E2E Test

Backend canlı olduktan sonra curl ile test et:
```bash
# Sağlığını kontrol et
curl https://pythonsozluk-xxxxx.onrender.com/health

# Kelime ara
curl "https://pythonsozluk-xxxxx.onrender.com/lookup?word=python"

# Kelime ekle
curl -X POST https://pythonsozluk-xxxxx.onrender.com/add \
  -H "Content-Type: application/json" \
  -d '{"word":"test","definition":"A test word"}'
```

---

## Notes

- Render free tier limit'ı: 750 compute hours/month (24/7 çalışırsa 31 günü kaplar).
- Fly.io benzer free tier'a sahip.
- GitHub Pages static site için unlimited (ücretsiz).
- Backend URL ve Frontend URL'yi bir kere güncelle, sonra her çalışacak.

Sorularında bana sor!
