`top_k(stream, k)` fonksiyonunu **boyu en fazla `k` olan bir min-heap** ile
yaz: en büyük `k` değeri **büyükten küçüğe** döndürsün.

- Heap'te `k`'dan az eleman varsa yeni sayıyı ekle.
- Doluysa ve yeni sayı kökten (`heap[0]`) büyükse `heapq.heapreplace` ile kökün
  yerine koy.
- Sonunda heap'i `heappop` ile boşaltınca küçükten büyüğe gelir; ters çevir.

`sorted`, `sort`, `nlargest` yok. `k <= 0` için `[]`.

**Beklenen çıktı:**

```
[9, 8, 7]
[5, 5]
```
