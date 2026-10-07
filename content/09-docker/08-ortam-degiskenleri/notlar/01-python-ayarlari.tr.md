Ortam değişkenlerini Python'da düzenli okumanın yolu: bütün ayarlar tek
yerde, varsayılanları ve türleriyle.

## Tek bir ayar modülü

```python
# settings.py
import os

APP_ENV = os.environ.get("APP_ENV", "development")
PORT = int(os.environ.get("PORT", "8000"))
DEBUG = os.environ.get("DEBUG", "false").lower() in ("1", "true", "yes")
DB_URL = os.environ.get("DB_URL", "sqlite:///local.db")
```

Programın geri kalanı `from settings import PORT` diyor; `os.environ`'u her
yerde ayrı ayrı okumuyor.

## Türlere dikkat

Ortam değişkeni **her zaman metin**:

| Okunan | Yanlış | Doğru |
|---|---|---|
| `PORT=8000` | `PORT + 1` → hata (metin + sayı) | `int(PORT) + 1` |
| `DEBUG=false` | `if DEBUG:` → **True** (boş olmayan metin doğru sayılır) | `DEBUG.lower() == "true"` |
| `RATE=0.5` | `RATE * 2` → `"0.50.5"` (metin iki kez yazılır) | `float(RATE)` |

`if os.environ.get("DEBUG"):` en sık hata: `"false"` metni de doğru sayılıyor.

## Zorunlu ayarlar

Bazı ayarların varsayılanı olmamalı (ör. gerçek veritabanının şifresi).
Eksikse program hemen ve açık bir mesajla durmalı:

```python
import os
import sys

password = os.environ.get("DB_PASSWORD")
if not password:
    sys.exit("DB_PASSWORD is not set")
```

`sys.exit("mesaj")` mesajı yazıp 1 koduyla çıkıyor; `docker logs` sebebi
gösteriyor.

## `.env` dosyası

Geliştirirken ayarları bir `.env` dosyasında tutmak yaygın:

```text
APP_ENV=development
DB_PASSWORD=local-only-password
```

- `docker run --env-file .env app` ile veriliyor.
- **`.gitignore` ve `.dockerignore`'a yazılır.** Depoya giden `.env.example`
  yalnızca adları ve sahte değerleri taşır.
