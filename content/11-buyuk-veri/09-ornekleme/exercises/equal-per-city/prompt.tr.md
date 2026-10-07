Basit ve katmanlı örneklemle Trabzon'un ortalama fiyatını tahmin et.

**Yapman gerekenler:**

1. `orders = make_orders(200_000)`; Trabzon'un gerçek ortalama
   `unit_price`'ını hesapla.
2. `random_state` 0'dan 49'a 50 kez tekrarla:
   - basit örneklem: `orders.sample(n=800, random_state=i)`,
   - katmanlı örneklem: her şehirden 100 sipariş,
     `orders.groupby("city", group_keys=False).sample(n=100, random_state=i)`,
   - her birinde Trabzon ortalama tahmininin gerçek değerden mutlak farkını
     kendi listesine ekle.
3. Her yöntem için bir satıra adını (`simple` / `stratified`) ve 50 farkın
   ortalamasını (bir ondalık) yazdır.

**Beklenen çıktı:**

```
simple 100.8
stratified 57.5
```

Tek bir örneklemde katmanlı yöntem şans eseri kötü de çıkabilir; ortalamada
Trabzon'un hatası küçülüyor.
