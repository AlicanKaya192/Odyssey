`restock(cities, stock, amount)` stoğu 0 olan satırların stoğunu `amount`
yapsın ve stok listesini döndürsün. Başlangıç kodu zincirli atama yapıyor
(`df[...]["stock"] = ...`); pandas 3'te bu asıl tabloyu **değiştirmez**. Tek
adımda `df.loc[koşul, "stock"] = amount` yaz.

**Beklenen çıktı:**

```
[5, 10, 10]
```
