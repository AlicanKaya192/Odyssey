`shrink(qtys, prices)` iki sütunlu bir tablo kursun (`qty`, `price`). `qty`'yi
`pd.to_numeric(..., downcast="unsigned")` ile, `price`'ı `astype("float32")`
ile küçültsün. Şunu döndürsün:

- `"dtypes"`: yeni türler, metin listesi (`dtypes.astype(str).tolist()`)
- `"smaller"`: yeni tablonun belleği eskisinden az mı (`bool`)

Belleği `memory_usage(deep=True).sum()` ile ölç.

**Beklenen çıktı:**

```
['uint8', 'float32']
True
```
