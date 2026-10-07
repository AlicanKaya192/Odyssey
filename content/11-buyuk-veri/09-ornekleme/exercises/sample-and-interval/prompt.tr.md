Bir örneklemle ortalama fiyatı tahmin et ve güven aralığını kur.

**Yapman gerekenler:**

1. `orders = make_orders(200_000)`; gerçek ortalama `unit_price`'ı iki
   ondalığa yuvarlayıp yazdır.
2. `orders.sample(n=5_000, random_state=1)` ile örneklem al; örneklem
   ortalamasını iki ondalığa yuvarlayıp yazdır.
3. Standart hatayı (`std() / np.sqrt(n)`) iki ondalığa yuvarlayıp yazdır.
4. %95 güven aralığının alt ve üst sınırını (± 1,96 standart hata) iki
   ondalığa yuvarlayıp aynı satıra yazdır.
5. Gerçek ortalamanın aralığın içinde olup olmadığını yazdır.

**Beklenen çıktı:**

```
739.31
748.36
12.16
724.54 772.19
True
```
