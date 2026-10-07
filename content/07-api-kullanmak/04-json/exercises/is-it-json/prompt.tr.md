Elinde beş metin var. Bazıları geçerli JSON, bazıları Python sözlüğüne
benzediği için JSON sanılmış.

**Yapman gerekenler:**

1. `is_valid(text)` fonksiyonunu yaz: `json.loads` metni okuyabiliyorsa
   `True`, `json.JSONDecodeError` veriyorsa `False` döndürsün. `try` /
   `except` kullan.
2. `samples` listesindeki her metin için `valid` ya da `invalid` yaz,
   ardından metnin kendisini yaz.

**Beklenen çıktı:**

```
valid   {"city": "Izmir"}
invalid {'city': 'Izmir'}
invalid {"ok": True}
invalid [1, 2,]
valid   null
```

`null` tek başına da geçerli bir JSON: değeri `None`.
