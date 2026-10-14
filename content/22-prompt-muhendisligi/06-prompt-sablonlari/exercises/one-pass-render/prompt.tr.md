`render(template, values)` önce eksik ve kullanılmayan değişkenleri
bulsun; biri bile varsa metin olarak `missing [...], unused [...]`
döndürsün (iki liste abece sırasıyla, dersteki biçimde). Yoksa şablonu
**tek geçişte** doldursun: `SLOT.sub` ile her yer tutucunun yerine
değerinin `str` hâli. Yerleşen değerin içindeki işaretler doldurulmaz.

**Beklenen çıktı:**

```
Ada wrote: Is {{name}} ok?
missing ['message'], unused []
```
