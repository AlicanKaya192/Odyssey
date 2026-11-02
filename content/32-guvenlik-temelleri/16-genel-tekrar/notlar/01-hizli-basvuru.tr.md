## Formüller

| Ne | Hesap |
|---|---|
| Erişilebilirlik | çalışılan süre / toplam süre × 100 |
| Nitel risk | olasılık (1–5) × etki (1–5); 1–4 düşük, 5–9 orta, 10–16 yüksek, 17–25 kritik |
| Tek kayıp beklentisi | SLE = varlık değeri (AV) × etki oranı (EF) |
| Yıllık kayıp beklentisi | ALE = SLE × yıllık olay sayısı (ARO) |
| Önlem değer mi? | önceki ALE − sonraki ALE − önlemin yıllık maliyeti > 0 |
| Parola entropisi | uzunluk × log₂(alfabe boyutu) bit |

## CVSS düzeyleri

0,1–3,9 düşük · 4,0–6,9 orta · 7,0–8,9 yüksek · 9,0–10,0 kritik.

## STRIDE

| Harf | Tehdit | Bozduğu |
|---|---|---|
| S | Kimlik taklidi (spoofing) | Kimlik doğruluğu |
| T | Kurcalama (tampering) | Bütünlük |
| R | İnkâr (repudiation) | İnkâr edilemezlik |
| I | Bilgi ifşası (information disclosure) | Gizlilik |
| D | Hizmet engelleme (denial of service) | Erişilebilirlik |
| E | Yetki yükseltme (elevation of privilege) | Yetkilendirme |

## Python araçları

| İş | Araç |
|---|---|
| Özet | `hashlib.sha256(veri).hexdigest()` |
| Parola özeti | `hashlib.pbkdf2_hmac("sha256", parola, tuz, tekrar)` |
| Anahtarlı özet | `hmac.new(anahtar, mesaj, hashlib.sha256)` |
| Sabit süreli karşılaştırma | `hmac.compare_digest(a, b)` |
| Güvenli rastgele | `secrets.token_hex(16)`, `secrets.choice(...)` |
| Adresin gerçek sahibi | `urllib.parse.urlsplit(url).hostname` |

## Erişim modelleri

DAC sahibi karar verir · MAC kuralı sistem koyar · RBAC rol · ABAC özellik.
Bell-LaPadula: yukarı okuma yok, aşağı yazma yok (gizlilik). Biba: aşağı
okuma yok, yukarı yazma yok (bütünlük).

## Kontrol listeleri

- **Yeni hesap:** rolün yetkileri, çok faktör, sahibi kayıtlı.
- **Ayrılan:** bütün hesaplar kapalı, ortak sırlar değişti, jetonlar iptal.
- **Jeton:** biçim → imza → `iss` → `aud` → `exp` → `nbf`.
- **Şüpheli e-posta:** gönderen alan adı, bağlantının gerçek sahibi,
  telaş, parola ya da ödeme isteği → bildir, başka kanaldan doğrula.
- **Yedek:** 3 kopya, 2 ortam, 1 başka yerde, 1 bağlantısız; denenmiş.
