`order_total(order_id)` salt okunur `shop_data.py`'deki `ORDERS`'tan
siparişi bulsun ve `{"order_id": ..., "total": ...}` döndürsün: toplam,
siparişteki her `[ürün, birim fiyat, adet]` için fiyat × adet toplamı, 2
basamağa yuvarlanmış. Sipariş yoksa `{"error": "no order <numara>"}`.

**Beklenen çıktı:**

```
{'order_id': 'ORD-10077', 'total': 214.9}
{'order_id': 'ORD-61890', 'total': 78.5}
{'error': 'no order ORD-00000'}
```
