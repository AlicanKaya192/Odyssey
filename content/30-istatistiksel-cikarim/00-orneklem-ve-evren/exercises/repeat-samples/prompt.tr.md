Tek örneklem şanslı mıydı, bilemeyiz. 500 örneklem çek: `seed` 0'dan 499'a,
her biri `users["minutes"].sample(n=50, random_state=seed)`. Ortalamaları
topla ve üç sayı yazdır: en küçük ortalama, en büyük ortalama (2 basamak)
ve gerçek ortalamaya **1 dakika ya da daha yakın** olanların payı (3
basamak).

**Beklenen çıktı:**

```text
6.84
11.98
0.75
```
