`reversed_copy(items)` fonksiyonunu yaz: listenin **ters sıradaki bir
kopyasını** döndürsün; asıl liste değişmesin.

Akla ilk gelen yol her elemanı yeni listenin başına eklemek
(`insert(0, x)`), ama bu her eklemede bütün listeyi kaydırır: `O(n²)`.
Bunun yerine listeyi **sondan başa** gez ve `append` ile ekle: `O(n)`.

**Kurallar:** `insert`, `reverse`, `reversed` ve `[::-1]` kullanma.

**Beklenen çıktı:**

```
[4, 3, 2, 1]
[1, 2, 3, 4]
[]
```
