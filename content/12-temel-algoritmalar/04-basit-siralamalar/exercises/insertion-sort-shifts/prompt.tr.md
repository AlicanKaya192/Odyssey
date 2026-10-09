`insertion_sort(items)` fonksiyonunu yaz: listenin sıralı bir kopyasını ve
yapılan **kaydırma** sayısını bir demet olarak döndürsün:
`(sıralı_liste, kaydırma)`.

Bir kaydırma = `items[j + 1] = items[j]` satırının bir kez çalışması. Bu
sayı listenin **ters sayımına** (yanlış sıradaki ikili sayısına) eşittir:
sıralı listede 0, ters sıralı listede `n(n−1)/2`.

`sorted` ve `.sort()` kullanma.

**Beklenen çıktı:**

```
([5, 6, 11, 12, 13], 7)
([1, 2, 3, 4], 0)
([1, 2, 3, 4], 6)
```
