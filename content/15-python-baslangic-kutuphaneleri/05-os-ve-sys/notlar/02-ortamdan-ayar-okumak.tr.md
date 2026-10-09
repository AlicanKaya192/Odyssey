Gerçek projelerde port, veritabanı adresi, hata ayıklama kipi, API anahtarı
gibi ayarlar koda yazılmaz; **ortam değişkenlerinden** okunur. Aynı kod
senin bilgisayarında, bir test sunucusunda ve gerçek sunucuda farklı
ayarlarla çalışır.

## Varsayılanlı ve türü çevrilmiş okuma

```python
import os


def load_settings():
    return {
        "mode": os.environ.get("APP_MODE", "production"),
        "port": int(os.environ.get("APP_PORT", "8000")),
        "debug": os.environ.get("APP_DEBUG", "0") in ("1", "true", "yes"),
    }


print(load_settings())
os.environ["APP_PORT"] = "9090"
os.environ["APP_DEBUG"] = "true"
print(load_settings())
print(bool("0"), bool("false"), bool(""))
```

```text
{'mode': 'production', 'port': 8000, 'debug': False}
{'mode': 'production', 'port': 9090, 'debug': True}
True True False
```

- Her ayarın bir **varsayılanı** var; değişken tanımlı değilse program yine
  çalışıyor.
- Sayı `int(...)` ile çevriliyor; değerler hep metin.
- Evet/hayır ayarı `bool(...)` ile çevrilmez: **boş olmayan her metin
  `True`**, `"0"` ve `"false"` bile. Kabul edilen değerleri açıkça yaz.

## Ortam değişkenini vermek

Programı başlatmadan önce terminalde:

| Kabuk | Yazım |
|---|---|
| PowerShell (Windows) | `$env:APP_PORT = "9090"` |
| Komut İstemi (cmd) | `set APP_PORT=9090` |
| Linux / macOS | `export APP_PORT=9090` |

Bu yalnızca o terminal penceresinde geçerlidir; pencere kapanınca biter.

## Gizli bilgiler koda yazılmaz

API anahtarı ve parola gibi değerler kodun içine yazılırsa kodla birlikte
GitHub'a gider ve herkes görür. Ortam değişkeninden okunur:

```python
import os

api_key = os.environ.get("WEATHER_API_KEY")
if api_key is None:
    print("WEATHER_API_KEY is not set")
```

Projelerde bu değerler çoğu zaman `.env` adlı bir dosyada tutulur ve dosya
`.gitignore` ile depodan dışarıda bırakılır.

## sys.argv ile basit argüman

`python resize.py photo.jpg 800` yazıldığında `sys.argv` `['resize.py',
'photo.jpg', '800']` olur. İki üç argümanlık küçük betiklerde yeterlidir;
seçenekli, yardım metinli araçlar için İleri Python modülündeki `argparse`
kullanılır.
