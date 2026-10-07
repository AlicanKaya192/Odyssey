Hattın ilk adımı: 200 000 satırlık CSV'nin belleğini küçük bir örnekten
tahmin et ve tahmini gerçekle karşılaştır.

**Yapman gerekenler:**

1. `write_orders_csv("orders.csv", 200_000)` hazır. Dosyanın diskteki
   boyutunu MB olarak (bir ondalık) yazdır.
2. İlk 5000 satırı türlerle (`DTYPES` hazır) oku; satır başına belleği
   (`memory_usage(deep=True)`) 200 000 ile çarpıp MB olarak (bir ondalık)
   yazdır.
3. Dosyanın tamamını aynı türlerle oku ve gerçek belleği MB olarak (bir
   ondalık) yazdır.
4. Tahminin gerçekten farkı %2'den küçük mü, yazdır.

**Beklenen çıktı:**

```
12.0
9.0
9.0
True
```
