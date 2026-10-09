Sayılar bir akıştan tek tek geliyor ve her yeni sayıdan sonra **o ana kadarki
medyan** isteniyor (bir sensörün anlık medyanı, bir sitenin yanıt sürelerinin
ortası). Her seferinde sıralamak `O(n log n)`; iki heap ile her adım
`O(log n)`.

## Fikir

Sayıları ikiye böl:

- `low`: küçük yarı, **max-heap** (kökü küçük yarının en büyüğü).
- `high`: büyük yarı, **min-heap** (kökü büyük yarının en küçüğü).

İki kural tut: `low`'daki her sayı `high`'dakilerden küçük ya da eşit ve
`low` en fazla bir eleman fazla. O zaman medyan köklerden okunur: tek sayıda
`low`'un kökü, çift sayıda iki kökün ortalaması.

```python
import heapq

def running_median(stream):
    low, high = [], []         # low: eksiyle max-heap, high: min-heap
    out = []
    for x in stream:
        heapq.heappush(low, -x)
        heapq.heappush(high, -heapq.heappop(low))   # low'un en büyüğü high'a
        if len(high) > len(low):                    # boyları dengele
            heapq.heappush(low, -heapq.heappop(high))
        if len(low) > len(high):
            out.append(-low[0])
        else:
            out.append((-low[0] + high[0]) / 2)
    return out

print(running_median([5, 15, 1, 3, 8]))
```

```text
[5, 10.0, 5, 4.0, 5]
```

Kontrol: `[5, 15]` → `10.0`, `[1, 3, 5, 15]` → `(3 + 5) / 2 = 4.0`,
`[1, 3, 5, 8, 15]` → `5`.

Her yeni sayı önce `low`'a girip oradan en büyüğü `high`'a geçtiği için
birinci kural kendiliğinden korunur; ikinci adım yalnızca boyları dengeler.
Bellek `O(n)`, ama her adım `O(log n)`.
