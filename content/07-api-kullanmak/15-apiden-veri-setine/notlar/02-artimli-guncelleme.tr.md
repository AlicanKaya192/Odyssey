Veri setini her gün sıfırdan çekmek yerine yalnızca değişenleri almak.

## Fikir

1. Elindeki kayıtları **kimliğe göre** bir sözlükte tut: `{id: kayıt}`.
2. Son güncelleme tarihini bir dosyada sakla (`last_sync.txt`).
3. API'ye "bu tarihten beri değişenleri ver" diye sor.
4. Gelenleri sözlüğe yaz: aynı kimlik varsa güncellenir, yoksa eklenir.
5. Yeni tarihi kaydet.

## Kod

```python
import json
import os

import requests

BASE = "http://api.odyssey.test"


def read_state():
    if os.path.exists("last_sync.txt"):
        with open("last_sync.txt", encoding="utf-8") as handle:
            return handle.read().strip()
    return "2000-01-01"


def merge(known, changed):
    for book in changed:
        known[book["id"]] = book
    return known


since = read_state()
r = requests.get(BASE + "/changes", params={"since": since}, timeout=10)
changed = r.json()["data"]
with open("books_by_id.json", encoding="utf-8") as handle:
    known = {int(k): v for k, v in json.load(handle).items()}
known = merge(known, changed)
```

JSON anahtarları metin olduğu için (Bölüm 04) dosyadan okurken `int(k)` ile
sayıya çeviriyoruz.

## Silinen kayıtlar

"Değişenleri ver" uç noktaları silinen kayıtları çoğu zaman göstermez. Bunun
için API'ler ya ayrı bir "silinenler" uç noktası sunar ya da kayda bir
`deleted: true` alanı ekler. Hiçbiri yoksa ara sıra tam çekim yapıp
karşılaştırmak gerekir.

## Tarih biçimi

Tarihleri ISO 8601 metin olarak sakla (`2024-03-05`): hem okunur hem metin
olarak sıralandığında doğru sıraya girer, karşılaştırma `>=` ile yapılabilir.
