`day_store_table(days, stores, sales, day_order, store_order)` gün × mağaza
**ortalama** satış tablosunu `pivot_table` ile kursun, satırları `day_order`,
sütunları `store_order` sırasına koysun ve `sns.heatmap(..., annot=True,
fmt=".0f")` ile çizsin. `heat.png` olarak kaydedip şekli kapatsın ve şunu
döndürsün:

- `"shape"`: tablonun şekli `[satır, sütun]`
- `"first_row"`: ilk satırın hücre yazıları (`ax.texts`'ten, sırayla)

**Beklenen çıktı:**

```
[2, 2]
['100', '80']
```
