Hata yönetiminin tek sayfalık özeti.

## İstisnalar

| İstisna | Ne zaman | Yeniden dene? |
|---|---|---|
| `requests.Timeout` | Yanıt `timeout` süresinde gelmedi | Evet |
| `requests.ConnectionError` | Sunucuya ulaşılamadı | Evet |
| `requests.HTTPError` | `raise_for_status()` 4xx/5xx gördü | 5xx evet, 4xx hayır |
| `requests.RequestException` | Hepsinin atası | Duruma göre |

## Yakalama sırası

```python
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
except requests.Timeout:
    ...
except requests.ConnectionError:
    ...
except requests.HTTPError:
    ...
except requests.RequestException:
    ...
```

Özelden genele. `RequestException` en sonda.

## Yeniden deneme şablonu

```python
import time

def get_with_retry(url, attempts=4):
    delay = 1
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                return r
        except (requests.Timeout, requests.ConnectionError):
            pass
        if attempt < attempts - 1:
            time.sleep(delay)
            delay *= 2
    return None
```

## Kurallar

1. Her isteğe `timeout=`.
2. Yalnızca geçici hataları yeniden dene: zaman aşımı, bağlantı, `5xx`, `429`.
3. Yalnızca tekrarlanabilir istekleri yeniden dene: `GET`, `PUT`, `DELETE`.
4. Üst sınır koy; beklemeyi her denemede katla (1, 2, 4...).
5. `429` ve `503`'te `Retry-After` varsa ona uy.
6. Vazgeçtiğinde ne olduğunu açıkça yaz.
