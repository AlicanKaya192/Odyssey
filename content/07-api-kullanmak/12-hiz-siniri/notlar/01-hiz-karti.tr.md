Hız sınırıyla çalışmanın özeti.

## Başlıklar

| Başlık | Anlam | Örnek |
|---|---|---|
| `X-RateLimit-Limit` | Penceredeki toplam hak | `3` |
| `X-RateLimit-Remaining` | Kalan hak | `0` |
| `X-RateLimit-Reset` | Hakkın yenileneceği an (saniye ya da zaman damgası) | `1712000000` |
| `Retry-After` | `429`/`503` sonrası beklenecek saniye | `1` |

Başlıklar metin gelir: `int(r.headers["Retry-After"])`.

## Aralığı hesaplamak

| Sınır | İstekler arası en az |
|---|---|
| Saniyede 3 | 0,34 sn |
| Dakikada 60 | 1 sn |
| Dakikada 30 | 2 sn |
| Saatte 1000 | 3,6 sn |

Formül: `aralık = pencere_saniye / izin_verilen_istek` ve biraz pay.

## Kalıp: ayar + güvenlik ağı

```python
import time

def get_paced(url, gap=0.4, attempts=5):
    for _ in range(attempts):
        r = requests.get(url, timeout=5)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 1)))
            continue
        time.sleep(gap)
        return r
    return None
```

## 429 ile diğer 4xx'lerin farkı

| | `429` | `400`, `401`, `404`... |
|---|---|---|
| İstek doğru mu? | Evet | Hayır |
| Ne yapılır? | Bekle, aynısını gönder | İsteği düzelt |
