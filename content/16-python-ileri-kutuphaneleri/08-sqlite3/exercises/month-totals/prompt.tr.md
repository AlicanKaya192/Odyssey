`month_totals(orders, year)` fonksiyonunu yaz: `orders` `[ISO tarih,
tutar]` çiftleri. Bellekte `orders (day TEXT, total REAL)` tablosuna eklesin;
yalnızca `year` yılındaki siparişleri ay ay toplayıp `{"01": 15.5, ...}`
sözlüğünü döndürsün (aylar sıralı). Ayı ve yılı SQL'de `strftime` alsın.

**Beklenen çıktı:**

```
{'01': 15.5, '03': 20.0}
```
