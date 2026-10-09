En çok kullanacağın iskeletler, tek yerde.

## İki işaretçi (sıralı liste)

```python
lo, hi = 0, len(items) - 1
while lo < hi:
    total = items[lo] + items[hi]
    if total == target:
        break
    if total < target:
        lo += 1
    else:
        hi -= 1
```

## Kayan pencere

```python
window = sum(values[:k])                  # sabit pencere
best = window
for i in range(k, len(values)):
    window += values[i] - values[i - k]   # giren eklenir, çıkan çıkarılır
    best = max(best, window)
```

```python
left = 0                                  # değişken pencere
for right, x in enumerate(items):
    # x'i pencereye ekle
    while SART_BOZULDU:
        # items[left]'i pencereden çıkar
        left += 1
    # right - left + 1 pencere boyu
```

## Önek toplamı

```python
prefix = [0]
for x in values:
    prefix.append(prefix[-1] + x)
# values[lo:hi] toplamı: prefix[hi] - prefix[lo]
```

## Sözlükle sayma ve gruplama

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1

groups = {}
for word in words:
    groups.setdefault("".join(sorted(word)), []).append(word)
```

## Yığın ve kuyruk

```python
stack = []                  # LIFO
stack.append(x); top = stack.pop()

from collections import deque
queue = deque([start])      # FIFO
while queue:
    node = queue.popleft()
```

## Ağaçta özyineleme

```python
def solve(node):
    if node is None:
        return BOS_CEVAP
    return BIRLESTIR(node.value, solve(node.left), solve(node.right))
```

## Heap

```python
import heapq
heapq.heappush(h, (priority, number, item))
priority, number, item = heapq.heappop(h)
heapq.nlargest(k, values)   # en büyük k, O(n log k)
```

## Python işlemlerinin maliyeti

| İşlem | Maliyet |
|---|---|
| `lst[i]`, `lst.append(x)`, `lst.pop()` | `O(1)` |
| `x in lst`, `lst.index(x)`, `lst.count(x)`, `lst.remove(x)` | `O(n)` |
| `lst.insert(0, x)`, `lst.pop(0)` | `O(n)` |
| `x in s`, `s.add(x)`, `d[k]`, `d[k] = v` | ortalama `O(1)` |
| `dq.appendleft(x)`, `dq.popleft()` | `O(1)` |
| `sorted(lst)`, `lst.sort()` | `O(n log n)` |
| `bisect.bisect_left(lst, x)` | `O(log n)` |
| `bisect.insort(lst, x)` | `O(n)` |
| `heapq.heappush`, `heapq.heappop` | `O(log n)` |
| `heapq.heapify(lst)` | `O(n)` |
| `min(lst)`, `max(lst)`, `sum(lst)` | `O(n)` |
| `lst[a:b]` (dilim) | `O(b - a)` |
