**1005** numaralı siparişin kalemlerini göster: sipariş numarası, müşteri
adı, ürün adı ve adet.

Sütunlar: `order_id`, `customer`, `product`, `quantity`. Ürün adına göre
sırala.

```
order_id  customer      product  quantity
--------  ------------  -------  --------
1005      Helix Studio  Desktop  1       
...
```

Sonuç üç satır olmalı — o siparişte üç kalem var.

Dört tabloya birden ihtiyacın var:

- `orders` — siparişin kendisi
- `customers` — müşteri adı
- `order_items` — siparişin kalemleri
- `products` — ürün adı

Her `JOIN` bir öncekinin sonucuna ekleniyor. Bağlantılar:
`orders.customer_id = customers.id`, `orders.id = order_items.order_id`,
`order_items.product_id = products.id`.

Müşteri adının her satırda tekrar ettiğine dikkat et: birleştirme sipariş
bilgisini her kalem için çoğaltıyor.
