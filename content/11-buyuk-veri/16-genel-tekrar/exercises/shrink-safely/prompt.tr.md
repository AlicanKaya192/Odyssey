Sipariş tablosunu türlerle küçült ve hiçbir değerin bozulmadığını kanıtla.

**Yapman gerekenler:**

1. `orders` (200 000 satır) varsayılan türlerle okunmuş hâlde hazır.
   Belleğini MB olarak (bir ondalık) yazdır.
2. `small` adında bir kopya kur: `order_id`, `customer_id`, `quantity`
   sütunlarını `pd.to_numeric(..., downcast="integer")` ile küçült; `city`,
   `category`, `payment` sütunlarını `category` yap.
3. `small`'un belleğini MB olarak (bir ondalık) yazdır.
4. `quantity` ve `customer_id` sütunlarının yeni türlerini aynı satıra
   yazdır.
5. İki tablodaki ciro toplamları (`quantity * unit_price`) birebir aynı mı,
   yazdır.

**Beklenen çıktı:**

```
19.2
9.0
int8 int32
True
```
