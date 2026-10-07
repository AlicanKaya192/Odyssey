MapReduce'un klasik örneğini kendin kur: kelime sayma.

**Yapman gerekenler:**

1. `mapper(line)` yaz: satırdaki her kelime için `(kelime, 1)` üretsin
   (`yield`).
2. Shuffle: `defaultdict(list)` ile her kelimenin değerlerini topla.
3. `reducer(key, values)` yaz: `(kelime, toplam)` döndürsün.
4. En az iki kez geçen kelimeleri, önce sayıya göre büyükten küçüğe, eşit
   sayıda kelimeye göre abece sırasıyla, her satıra kelime ve sayı olarak
   yazdır.

**Beklenen çıktı:**

```
shuffle 3
data 2
machines 2
many 2
needs 2
reduce 2
the 2
then 2
```
