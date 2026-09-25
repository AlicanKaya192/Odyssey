"""Deponun GitHub yıldız sayısı.

Alt şeridin solunda duruyor; tıklayan depoya gidip isterse yıldız veriyor.
Güncelleme denetimiyle aynı kurallar:

- yalnızca **GET**, hiçbir şey göndermiyor;
- ayarlardaki güncelleme denetimi kapalıysa **hiç ağa çıkmıyor** (o ayarın
  anlamı "program ağa çıkmasın");
- başarısız olunca sessiz kalıyor, son bilinen sayı gösterilmeye devam
  ediyor.

Sayı `settings` tablosunda saklanıyor: açılışta ağ cevabını beklemeden
bir önceki sayı görünüyor.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .updates import USER_AGENT

REPO_API = "https://api.github.com/repos/AlicanKaya192/Odyssey"
REPO_PAGE = "https://github.com/AlicanKaya192/Odyssey"

TIMEOUT_SEC = 6
MAX_RESPONSE_BYTES = 256 * 1024

# İki sorgu arasındaki en kısa süre. GitHub kimliksiz isteklerde aynı IP'ye
# saatte 60 istek veriyor ve güncelleme denetimi de o paydan yiyor; pencereye
# her dönüldüğünde sormak yerine en fazla iki dakikada bir soruluyor.
MIN_INTERVAL_SEC = 120
# Açık kalan oturumda kendiliğinden tazeleme aralığı.
REFRESH_SEC = 10 * 60

CACHE_KEY = "github_stars"


def cached(store) -> int | None:
    """Son bilinen yıldız sayısı; hiç alınmadıysa `None`."""
    deger = store.setting(CACHE_KEY, "")
    return int(deger) if deger.isdigit() else None


def remember(store, count: int) -> None:
    store.set_setting(CACHE_KEY, str(count))


def fetch_stars(url: str = "", timeout: int = TIMEOUT_SEC) -> int | None:
    """Deponun yıldız sayısı. **Hiçbir zaman hata fırlatmaz**; olmazsa `None`."""
    istek = urllib.request.Request(
        url or REPO_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(istek, timeout=timeout) as cevap:
            ham = cevap.read(MAX_RESPONSE_BYTES)
        veri = json.loads(ham)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, UnicodeDecodeError):
        return None
    sayi = veri.get("stargazers_count") if isinstance(veri, dict) else None
    return sayi if isinstance(sayi, int) and sayi >= 0 else None
