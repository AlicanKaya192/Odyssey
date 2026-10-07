`minispark` ile bir RDD kur, bölümlerine bak ve bir hesap yap.

**Yapman gerekenler:**

1. `SparkSession` ve `sc` başlangıç kodunda hazır.
2. `nums = sc.parallelize(range(1, 21), 4)`.
3. Bölüm sayısını yazdır.
4. Her bölümdeki öğe sayısını liste olarak yazdır (`glom()` ve `map(len)`).
5. Çift sayıların karelerinin toplamını yazdır: `filter`, `map`, `sum`.

**Beklenen çıktı:**

```
4
[5, 5, 5, 5]
1540
```
