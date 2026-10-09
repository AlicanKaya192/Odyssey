## Temel

| Yazım | Ne yapar |
|---|---|
| `pickle.dumps(nesne)` | nesne → `bytes` |
| `pickle.loads(baytlar)` | `bytes` → nesne |
| `pickle.dump(nesne, dosya)` | dosyaya yaz (`"wb"`) |
| `pickle.load(dosya)` | dosyadan oku (`"rb"`) |
| `pickle.HIGHEST_PROTOCOL` | en yeni biçim |

## Kendi sınıfın

| Yazım | Ne zaman |
|---|---|
| `__getstate__(self)` | saklanacak durumu döndür (kilidi, bağlantıyı çıkar) |
| `__setstate__(self, state)` | yüklerken durumu geri koy, çıkarılanı yeniden kur |
| `__reduce__(self)` | nesne nasıl kurulur: `(fonksiyon, argümanlar)` |

## Hatalar

| Hata | Sebep |
|---|---|
| `TypeError: write() argument must be str, not bytes` | dosya `"w"` ile açıldı, `"wb"` olmalı |
| `TypeError: cannot pickle '_thread.lock' object` | saklanamayan bir parça var |
| `PicklingError: Can't pickle <function <lambda> ...>` | lambda ya da iç içe fonksiyon adıyla bulunamıyor |
| `AttributeError: module '__main__' has no attribute 'Point'` | yüklerken sınıf yok |
| `UnpicklingError: invalid load key` | dosya pickle değil ya da bozuk |

## shelve

```python
import shelve

with shelve.open("cache") as db:
    db["key"] = {"a": 1}       # yaz
    value = db.get("key", {})  # oku
    value["a"] = 2
    db["key"] = value          # değişikliği geri ata
    del db["key"]              # sil
```

## Kurallar

- **Güvenilmeyen kaynaktan pickle yükleme**; dış dünya için JSON.
- Uzun süre saklanacak veri için de JSON ya da CSV: sınıf adı değişince
  pickle dosyası açılmaz.
- pickle uygun yerler: Python içi geçici önbellek, süreçler arası taşıma.
