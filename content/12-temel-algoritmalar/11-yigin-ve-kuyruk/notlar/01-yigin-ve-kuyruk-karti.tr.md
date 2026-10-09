## İşlemler

| İş | Yığın (`list`) | Kuyruk (`collections.deque`) |
|---|---|---|
| Ekle | `stack.append(x)` `O(1)` | `queue.append(x)` `O(1)` |
| Al | `stack.pop()` `O(1)` | `queue.popleft()` `O(1)` |
| Almadan bak | `stack[-1]` | `queue[0]` |
| Boş mu? | `if not stack:` | `if not queue:` |
| Boyut | `len(stack)` | `len(queue)` |

## Sık hatalar

- **Boş yapıdan almak:** `[].pop()` ve `deque().popleft()` `IndexError` verir.
  Almadan önce `if stack:` diye bak.
- **Kuyruğu listeyle yapmak:** `items.pop(0)` her seferinde bütün listeyi
  kaydırır: kuyruk uzadıkça `O(n²)`'ye gider.
- **Postfix'te sıra:** önce çıkan **sağdaki** işlenen: `right = pop()`, sonra
  `left = pop()`. Toplama ve çarpmada fark etmez, çıkarma ve bölmede eder.

## Hangisi ne zaman?

| Soru | Yapı |
|---|---|
| "En son açılan/eklenen ilk kapanmalı" | yığın |
| "Geri al" / "bir adım geri git" | yığın |
| "Önce gelen önce işlensin" | kuyruk |
| "Yakından uzağa, katman katman" (BFS) | kuyruk |
| "Derine dal, sonra geri dön" (DFS) | yığın (ya da özyineleme) |
| "Sıradaki büyük/küçük eleman" | monoton yığın |
| "Her an en küçüğü/en büyüğü ver" | öncelik kuyruğu (`heapq`, bu modülün 15. bölümü) |

## İş parçacıkları arasında

Birden fazla iş parçacığı (thread) aynı kuyruğa yazıp okuyacaksa
`queue.Queue` (FIFO) ve `queue.LifoQueue` (yığın) kullanılır: kilitleme
kendiliğinden yapılır. Tek iş parçacığında `deque` daha hızlı ve yeterli.
