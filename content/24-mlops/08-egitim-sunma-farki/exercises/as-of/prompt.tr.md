Bir özelliğin geçmişi tarihe göre sıralı bir liste: her eleman `[tarih, değer]`, tarihler `"YYYY-MM-DD"` biçiminde. `as_of(history, day)` fonksiyonunu yaz: `day` tarihinde ya da öncesinde bilinen **son** değeri döndür.

- Tarihi `day`'den sonra olan değerler yok sayılır.
- `day`'den önce hiç değer yoksa (ya da liste boşsa) `None`.

**Beklenen çıktı:**

```
1
4
None
None
```
