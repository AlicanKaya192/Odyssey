Bölüm 12'deki kelime saymayı Spark yazımıyla yap.

**Yapman gerekenler:**

1. Satırlar başlangıç kodunda; `lines = sc.parallelize(text, 2)`.
2. `flatMap` ile kelimelere böl, `map` ile `(kelime, 1)` yap,
   `reduceByKey` ile topla.
3. Sonucu sayıya göre büyükten küçüğe, eşitlikte kelimeye göre sırala:
   `sortBy(lambda kv: (-kv[1], kv[0]))`.
4. İlk dört öğeyi (`take(4)`) her satıra kelime ve sayı olarak yazdır.
5. Kaç farklı kelime olduğunu yazdır (`count()`).

**Beklenen çıktı:**

```
data 3
spark 3
in 2
memory 2
13
```
