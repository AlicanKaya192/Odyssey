Kimlik göndermenin yolları, tek tabloda.

| Yöntem | Nasıl gönderilir | requests | Not |
|---|---|---|---|
| API anahtarı (başlık) | `X-API-Key: abc123` | `headers={"X-API-Key": key}` | Başlık adı API'ye göre değişir |
| API anahtarı (sorgu) | `?api_key=abc123` | `params={"api_key": key}` | Adres kayıtlara düşer; mecbursa |
| Bearer jeton | `Authorization: Bearer abc123` | `headers={"Authorization": "Bearer " + token}` | `Bearer ` önekini unutma |
| Basic | `Authorization: Basic <base64>` | `auth=(user, password)` | Yalnızca `https` |

## Kodlara göre ne yapılır

| Kod | Anlam | Yapılacak |
|---|---|---|
| `401` | Tanınmıyorsun | Anahtar/jeton gönderildi mi? Doğru başlıkta mı? Süresi doldu mu? |
| `403` | İznin yok | Başka bir yetki ya da anahtar gerekiyor; tekrar denemek işe yaramaz |

## Oturum kalıbı

```python
import os
import requests

BASE = "http://api.odyssey.test"
token = os.environ.get("LIBRARY_TOKEN", "letmein")

session = requests.Session()
session.headers.update({"Authorization": "Bearer " + token})

me = session.get(BASE + "/me")
me.raise_for_status()
print(me.json())
```

## Güvenlik listesi

- Anahtar ve jeton koda yazılmaz; ortam değişkeninden ya da `.env`
  dosyasından okunur.
- `.env` dosyası `.gitignore`'a eklenir.
- Sızan anahtar hemen API'nin panelinden iptal edilip yenisi alınır;
  geçmişten silmek yetmez.
- Ekran görüntüsü ve hata kaydı paylaşırken başlıkları gizle.
- Anahtara yalnızca gereken yetkiyi ver (yalnızca okuma gibi).
