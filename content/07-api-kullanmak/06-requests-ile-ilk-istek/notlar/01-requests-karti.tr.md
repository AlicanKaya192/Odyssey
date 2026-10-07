requests ile bir isteğin ve yanıtın en sık kullanılan parçaları.

## İstek göndermek

```python
import requests

r = requests.get(url)                    # getir
r = requests.post(url, json=veri)        # oluştur (Bölüm 09)
r = requests.put(url, json=veri)         # tamamen değiştir
r = requests.patch(url, json=veri)       # kısmen değiştir
r = requests.delete(url)                 # sil
```

Hepsi aynı ek bilgileri alabilir: `params=` (sorgu, Bölüm 07), `headers=`
(Bölüm 08), `timeout=` (Bölüm 11).

## Yanıtın parçaları

| İfade | Ne verir | Örnek |
|---|---|---|
| `r.status_code` | Durum kodu (int) | `200` |
| `r.ok` | Kod 400'den küçük mü | `True` |
| `r.headers["Content-Type"]` | Bir başlık (ad harf duyarsız) | `application/json; charset=utf-8` |
| `r.text` | Gövde, metin olarak | `'{"id": 1, ...}'` |
| `r.json()` | Gövde, Python nesnesi olarak | `{'id': 1, ...}` |
| `r.url` | İsteğin son adresi | `http://api.odyssey.test/books/1` |
| `r.request.method` | Gönderilen yöntem | `GET` |
| `r.raise_for_status()` | 4xx/5xx ise `HTTPError` fırlatır | |

## Güvenli okuma kalıbı

```python
r = requests.get(url)
if r.status_code == 200:
    data = r.json()
else:
    print("error", r.status_code, r.text)
```

ya da:

```python
r = requests.get(url)
r.raise_for_status()      # hata varsa burada durur
data = r.json()
```

## Hatalar

| Hata | Ne zaman |
|---|---|
| `requests.exceptions.MissingSchema` | Adres `http://` ile başlamıyor |
| `requests.JSONDecodeError` | Gövde JSON değilken `json()` çağrıldı |
| `requests.HTTPError` | `raise_for_status()` 4xx/5xx gördü |
| `requests.ConnectionError` | Sunucuya hiç ulaşılamadı (Bölüm 11) |
| `requests.Timeout` | Yanıt zamanında gelmedi (Bölüm 11) |
