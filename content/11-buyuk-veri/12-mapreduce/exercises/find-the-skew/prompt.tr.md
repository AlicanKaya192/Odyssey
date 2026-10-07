Şehre göre üç reduce makinesine dağıtılan siparişlerde yük ne kadar
dengesiz?

**Yapman gerekenler:**

1. `partition(key, reducers)` fonksiyonunu `zlib.crc32` ile yaz.
2. `orders = make_orders(200_000)`; her siparişin şehrini
   `partition(city, 3)` ile bir makineye ata.
3. Her makinenin aldığı sipariş sayısını makine numarasına göre sıralı bir
   liste olarak yazdır.
4. Her makinenin payını yüzde olarak (bir ondalık) liste hâlinde yazdır.
5. En çok iş alan makinenin en az iş alana oranını (bir ondalık) yazdır.

**Beklenen çıktı:**

```
[132175, 57962, 9863]
[66.1, 29.0, 4.9]
13.4
```

Bir makine öbürünün on katından fazla iş alıyor: iş en yavaş makine bitince
bitecek.
