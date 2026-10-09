`k_smallest(values, k)` fonksiyonunu yaz: listenin en küçük `k` elemanını
**küçükten büyüğe** bir liste olarak döndürsün. `k` eleman sayısından büyükse
hepsini döndürsün.

Yol: listenin **kopyasını** `heapq.heapify` ile heap yap, sonra `k` kez
`heapq.heappop`. Asıl liste değişmesin. `sorted`, `sort`, `nsmallest` yok.

**Beklenen çıktı:**

```
[1, 2, 4]
[1, 2, 4, 7, 8, 9]
[7, 2, 9, 4, 1, 8]
```
