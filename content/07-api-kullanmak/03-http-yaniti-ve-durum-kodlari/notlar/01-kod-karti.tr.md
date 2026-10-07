Durum kodlarını hızlıca hatırlamak için.

## Sınıflar

| Sınıf | Anlam | Kimin işi |
|---|---|---|
| `1xx` | Bilgi: "devam et" | Nadiren görürsün |
| `2xx` | Başarı | Gövdeyi kullan |
| `3xx` | Yönlendirme: başka yere bak | Kütüphane kendisi takip eder |
| `4xx` | İstemci hatası | **Senin**: isteği düzelt |
| `5xx` | Sunucu hatası | **Onların**: bekle, yeniden dene |

## Gündelik on kod

- `200` tamam · `201` oluşturuldu · `204` tamam ama gövde yok
- `400` bozuk istek · `401` tanınmıyorsun · `403` iznin yok · `404` yok
- `429` yavaşla · `500` sunucu hatası · `503` şu an hizmet yok

## Bir cümleyle karar

> 4 ile başlıyorsa isteğine bak, 5 ile başlıyorsa bekle.

İstisna `429`: dört ile başlıyor ama istek doğru; yalnızca çok sık
gönderiliyor. `Retry-After` kadar bekleyip aynı isteği gönderirsin.

## Python

```python
from http import HTTPStatus

HTTPStatus(404).phrase     # 'Not Found'
404 // 100                 # 4 -> sınıf
200 <= code < 300          # başarılı mı?
```
