Model müşterinin mesajından sayıları JSON olarak çıkardı:
`{"items": [{"price": ..., "count": ...}, ...], "discount": ...}`.
`total_from_json(text)` JSON'u okusun ve doğrulasın; geçerliyse tutarı
(ara toplam × (1 − indirim), 2 basamak) döndürsün, değilse `None`.
Geçerli sayılır: `items` boş olmayan liste; her `price` 0'dan büyük sayı;
her `count` 1 ya da daha büyük `int`; `discount` 0 ile 0.5 arasında
sayı.

**Beklenen çıktı:**

```
193.41
None
None
```
