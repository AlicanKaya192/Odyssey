Beş ürünün fiyatı, adlarıyla birlikte bir seride duruyor. Pahalı olanları
ayıracaksın.

**Yapman gerekenler:**

1. `prices` serisi başlangıç kodunda hazır.
2. Fiyatı **100 ve üstünde** olanları `expensive` adlı seride topla.
3. Sırayla yazdır: `expensive`, kaç ürün olduğu, ve ortalama fiyat
   (bir basamağa yuvarlanmış).

**Beklenen çıktı:**

```
kalem    120
canta    240
kitap    175
dtype: int64
3
178.3
```

**Dikkat et:** NumPy'da filtrelediğinde geriye yalnızca sayılar kalıyordu.
Burada **ürün adları da geliyor** — hangi fiyatın hangi ürüne ait olduğunu
kaybetmiyorsun. Serinin index'i tam olarak bunun için var.
