Mağazanın haftalık mevsimselliğini ölç. Bu dosyada her günün adı
hazır bir sütunda: `weekday` (`Mon`, `Tue`, ..., `Sun`).

**Yapman gerekenler:**

1. `store_sales_days.csv` dosyasını oku.
2. Haftanın gününe göre grupla ve satış ortalamasını al; sonucu küçükten
   büyüğe sırala (`sort_values()`).
3. En yüksek günü ve ortalamasını (bir ondalık) yazdır.
4. En düşük günü ve ortalamasını (bir ondalık) yazdır.
5. En yüksek ortalamanın en düşüğe oranını iki ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
Sat 336.1
Mon 217.6
1.54
```

Bu oran, hiç model kurmadan elindeki ilk tahmin aracı: "gelecek cumartesi,
bir pazartesinin yaklaşık bir buçuk katı satar."
