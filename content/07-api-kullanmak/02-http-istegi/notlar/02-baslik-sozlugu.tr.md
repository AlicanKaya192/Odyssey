İsteklerde en sık göreceğin başlıklar ve tipik değerleri.

| Başlık | Örnek değer | Anlamı |
|---|---|---|
| `Host` | `api.example.com` | İsteğin gittiği ana makine |
| `Accept` | `application/json` | "Yanıtı JSON olarak istiyorum" |
| `Content-Type` | `application/json` | "Gönderdiğim gövde JSON" |
| `Content-Length` | `37` | Gövde 37 bayt |
| `Authorization` | `Bearer abc123` | Kimlik jetonu (Bölüm 08) |
| `User-Agent` | `python-requests/2.32` | İsteği gönderen program |
| `Accept-Language` | `tr-TR` | Yanıtın tercih edilen dili |

## İçerik türleri (Content-Type / Accept)

| Değer | Ne |
|---|---|
| `application/json` | JSON veri |
| `text/html` | Web sayfası |
| `text/plain` | Düz metin |
| `text/csv` | CSV tablo |
| `application/x-www-form-urlencoded` | Form verisi (`ad=değer&...`) |
| `multipart/form-data` | Dosya yükleme |

## Okurken iki kural

1. **Adlarda büyük/küçük harf fark etmez.** Programda adları küçük harfe
   çevirip sakla: `headers[name.lower()] = value`.
2. **Yalnızca ilk iki noktadan böl.** `Host: localhost:8000` satırında
   değer `localhost:8000`. `line.split(": ", 1)`.

## Gövdenin bayt sayısı

```python
body = '{"city": "Izmir"}'
print(len(body))                  # 17 harf
print(len(body.encode("utf-8")))  # 17 bayt

body = '{"city": "Kadıköy"}'
print(len(body))                  # 19 harf
print(len(body.encode("utf-8")))  # 21 bayt: ı ve ö ikişer bayt
```

`Content-Length` her zaman **bayt** sayısıdır.
