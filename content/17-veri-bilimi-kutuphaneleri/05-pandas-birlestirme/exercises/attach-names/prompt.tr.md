`attach_names(orders, customers)` siparişlere (`[order, customer, amount]`)
müşteri adlarını (`[customer, name]`) eklesin ve adları sipariş sırasıyla
liste olarak döndürsün. Müşterisi bulunmayan siparişin adı `"?"` olsun
(`fillna("?")`). Başlangıç kodu varsayılan `inner` ile birleştiriyor; bir
sipariş kayboluyor.

**Beklenen çıktı:**

```
['Ada', 'Can', 'Ada', '?']
```
