Dönüşümlerin hiçbir şey hesaplamadığını, eylemin her şeyi çalıştırdığını
sayaçla göster.

**Yapman gerekenler:**

1. `nums = sc.parallelize(range(100), 5)`.
2. Üç dönüşüm zincirle: `map(lambda x: x * 3)`, `filter(lambda x: x % 2 == 0)`,
   `map(lambda x: x + 1)`; sonucu `result` adıyla tut.
3. `sc.stats.jobs` ve `sc.stats.partitions_computed` değerlerini aynı satıra
   yazdır.
4. `result.count()` sonucunu yazdır.
5. Aynı iki sayacı yeniden aynı satıra yazdır.

**Beklenen çıktı:**

```
0 0
50
1 20
```

Eylemden önce sıfır iş; sonra bir iş ve dört adımın beşer bölümü.
