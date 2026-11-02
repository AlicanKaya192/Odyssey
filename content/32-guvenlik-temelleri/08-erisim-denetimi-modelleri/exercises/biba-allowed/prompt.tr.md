Biba modeli bütünlüğü korur. Düzeyler küçükten büyüğe
`LEVELS = ["low", "medium", "high"]`.

`biba_allowed(subject, obj, action)` şunu döndürsün:

- `"read"`: öznenin düzeyi nesnenin düzeyine **eşit ya da küçükse** `True`
  (aşağı okuma yok),
- `"write"`: öznenin düzeyi nesnenin düzeyine **eşit ya da büyükse** `True`
  (yukarı yazma yok),
- başka her eylem: `False`.

Başlangıç kodu Bell-LaPadula'yı yazıyor; Biba onun tersi.

**Beklenen çıktı:**

```
medium low False True
medium high True False
high high True True
False
```
