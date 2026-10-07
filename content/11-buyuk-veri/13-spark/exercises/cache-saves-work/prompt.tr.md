Aynı RDD'yi iki eylemde kullan; önbellekli ve önbelleksiz hesaplanan
bölüm sayısını karşılaştır.

**Yapman gerekenler:**

1. `nums = sc.parallelize(range(1_000), 4)`.
2. Önbelleksiz: `plain = nums.map(lambda x: x * 2)`. Sayacı bir değişkene
   al, `plain.count()` ve `plain.sum()` çağır, sayaçtaki artışı yazdır.
3. Önbellekli: `cached = nums.map(lambda x: x * 2).cache()`. Aynısını yap
   ve artışı yazdır.
4. İki `sum` sonucunun aynı olup olmadığını yazdır.

**Beklenen çıktı:**

```
16
8
True
```
