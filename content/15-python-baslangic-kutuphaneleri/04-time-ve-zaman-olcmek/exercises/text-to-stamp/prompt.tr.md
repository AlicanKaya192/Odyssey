`text_to_stamp(text)` fonksiyonunu yaz: `"2026-03-15 14:30"` biçimindeki
**UTC** zamanı zaman damgasına çevirip **tam sayı** olarak döndürsün.
Adımlar: `strptime`, `replace(tzinfo=timezone.utc)`, `timestamp()`, `int`.

**Beklenen çıktı:**

```
1773585000
86400
```
