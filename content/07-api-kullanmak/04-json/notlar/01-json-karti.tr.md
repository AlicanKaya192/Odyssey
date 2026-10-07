JSON ile Python arasında gidip gelmek için gereken her şey.

## Dört fonksiyon

| Fonksiyon | Yön | Neyle |
|---|---|---|
| `json.loads(text)` | JSON → Python | Metin |
| `json.dumps(obj)` | Python → JSON | Metin |
| `json.load(handle)` | JSON → Python | Dosya |
| `json.dump(obj, handle)` | Python → JSON | Dosya |

Hatırlama yolu: **`s` = string** (metin).

## Tür karşılıkları

| JSON | Python |
|---|---|
| `{"a": 1}` nesne | `dict` |
| `[1, 2]` dizi | `list` |
| `"metin"` | `str` |
| `3`, `3.5` | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## `dumps` ayarları

```python
json.dumps(obj, indent=2)            # okunur, girintili
json.dumps(obj, ensure_ascii=False)  # Türkçe harfler olduğu gibi
json.dumps(obj, sort_keys=True)      # anahtarlar abece sırasıyla
```

## JSON olmayanlar

| Python | Ne yapılır |
|---|---|
| `tuple` | Kendiliğinden listeye döner |
| `set` | Hata verir → `sorted(s)` |
| tarih | Hata verir → `"2024-03-01"` metni |
| `{1: "a"}` | Anahtar `"1"` olur |

## Geçerli mi?

```text
{"city": "Izmir"}      geçerli
{'city': 'Izmir'}      tek tırnak → geçersiz
{"ok": True}           büyük harf True → geçersiz (true olmalı)
{"a": 1,}              son virgül → geçersiz
{"note": None}         None → geçersiz (null olmalı)
```
