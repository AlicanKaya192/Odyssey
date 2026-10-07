Kütüphanenin web sitesi (`https://library.example.com`) API'yi
tarayıcıdan çağıracak.

**Yapman gereken:** `CORSMiddleware` ile yalnızca bu siteye, yalnızca `GET`
için izin ver (başlıkların hepsi serbest).

- `GET /books`, `Origin: https://library.example.com` → cevapta `access-control-allow-origin: https://library.example.com`
- `OPTIONS /books` ön sorusu, başka bir siteden → `400`
