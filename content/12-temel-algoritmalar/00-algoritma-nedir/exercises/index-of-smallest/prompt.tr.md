`index_of_smallest(numbers)` fonksiyonunu yaz: listedeki en küçük sayının
**sırasını (indeksini)** döndürsün.

**Kurallar:**

- En küçük birden fazla kez geçiyorsa **ilkinin** indeksini döndür.
- Liste boşsa `-1` döndür.
- `min()` ve `.index()` kullanma.

**Yapman gerekenler:**

1. Boş listeyi en başta ele al.
2. En küçüğün **değerini değil, indeksini** aklında tut: `best = 0`.
3. `for i in range(1, len(numbers)):` ile gez; `numbers[i]` daha küçükse
   `best = i`.

**Beklenen çıktı:**

```
1
-1
```
