Uzun biçimde düz `shift(1)` bir mağazanın satırına başka bir mağazanın
değerini getiriyor. Yanlışı ve doğruyu yan yana gör.

**Yapman gerekenler:**

1. `stores.csv` dosyasını oku (`parse_dates=["date"]`).
2. İki sütun ekle: `lag_wrong = long["sales"].shift(1)` ve
   `lag1 = long.groupby("store")["sales"].shift(1)`.
3. 2 Ocak 2024'ün B mağazası satırı için `sales`, `lag_wrong` ve `lag1`
   değerlerini liste olarak yazdır.
4. B mağazasının 1 Ocak 2024 satışını yazdır (doğru cevabın bu olduğunu
   görmek için).
5. `sales` ile `lag_wrong` ve `sales` ile `lag1` korelasyonlarını üç
   ondalığa yuvarlayıp aynı satıra yazdır.
6. `lag1` sütunundaki `NaN` sayısını yazdır.

**Beklenen çıktı:**

```
[190, 288.0, 180.0]
180
-0.33 0.866
4
```

Yanlış gecikme, B'nin dünü yerine A'nın aynı günkü satışını getirdi.
Korelasyonu eksi: sütun dolu, sayılar makul ve tamamen anlamsız. Son satırda
dört `NaN` var: her mağazanın ilk gününün dünü yok.
