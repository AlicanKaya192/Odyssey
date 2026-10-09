## Kurallar ve indeksler

- Şekil: seviye seviye, soldan sağa boşluksuz dolu ikili ağaç.
- Sıra (min-heap): ebeveyn ≤ çocuk. En küçük `heap[0]`'da.
- `i`'nin çocukları `2i + 1`, `2i + 2`; ebeveyni `(i - 1) // 2`.

## `heapq` fonksiyonları

| Fonksiyon | Ne yapar | Süre |
|---|---|---|
| `heappush(h, x)` | ekle | `O(log n)` |
| `heappop(h)` | en küçüğü al | `O(log n)` |
| `h[0]` | en küçüğe bak (almadan) | `O(1)` |
| `heapify(liste)` | listeyi yerinde heap yap | `O(n)` |
| `heapreplace(h, x)` | önce al, sonra ekle | `O(log n)` |
| `heappushpop(h, x)` | önce ekle, sonra al | `O(log n)` |
| `nlargest(k, it)` / `nsmallest(k, it)` | en büyük / en küçük `k` | `O(n log k)` |
| `merge(*sıralılar)` | sıralı listeleri tembelce birleştir | toplam `O(n log k)` |
| `heapify_max`, `heappush_max`, `heappop_max` | max-heap (Python 3.14) | aynı |

## Hangisi ne zaman?

| İhtiyaç | Seç |
|---|---|
| Hep en küçüğü/en büyüğü al, arada ekle | heap |
| Bir kez sırala, sonra oku | `sorted` |
| En büyük/küçük birkaç tane (`k` küçük) | `nlargest` / `nsmallest` ya da boyu `k` heap |
| Tek en büyük/küçük | `max` / `min` |
| Ortadan silme, aralık sorgusu | BST ya da sıralı liste + `bisect` |

## Sık hatalar

- **Heap listesini sıralı sanmak:** `heap[1]` ikinci en küçük **olmayabilir**
  (`[1, 3, 2, ...]`'te ikinci en küçük `2`, `heap[2]`'de).
- **Listeyi elle değiştirmek:** `heap.append(x)` ya da `heap[3] = 0` kuralı
  bozar; yalnızca `heapq` fonksiyonlarıyla değiştir.
- **`heapify` yapmadan `heappop`:** sıradan bir listeden `heappop` yanlış
  eleman verir.
- **Demet eşitliği:** `(öncelik, değer)`'de öncelikler eşitse değerler
  karşılaştırılır; karşılaştırılamıyorsa `TypeError`. `(öncelik, sayaç,
  değer)` yaz.
- **Max-heap için eksiyi unutmak:** `-x` ile koyduysan alırken de `-` ile
  geri çevir.
