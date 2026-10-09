## Counter

| Yazım | Ne yapar |
|---|---|
| `Counter(öğeler)` | sayar |
| `c[x]` | sayısı (yoksa 0) |
| `c.most_common(n)` | en sık n, `(öğe, sayı)` |
| `c.update(öğeler)` / `c.subtract(öğeler)` | ekle / çıkar |
| `c.total()` | sayıların toplamı |
| `a + b`, `a - b`, `a & b`, <code>a &#124; b</code> | topla, çıkar, küçüğü, büyüğü |

## defaultdict

| Yazım | Varsayılan |
|---|---|
| `defaultdict(list)` | `[]`: gruplamak |
| `defaultdict(int)` | `0`: saymak |
| `defaultdict(set)` | `set()`: tekrarsız gruplamak |

Okumak da anahtarı oluşturur; var mı diye `in` ile bak.

## namedtuple

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p[0], p._replace(x=1), p._asdict()
```

## deque

| Yazım | Ne yapar |
|---|---|
| `append(x)` / `appendleft(x)` | sağa / sola ekle |
| `pop()` / `popleft()` | sağdan / soldan çıkar |
| `deque(maxlen=n)` | en fazla n öğe, eskisi düşer |
| `rotate(k)` | sağa döndür |
| `d[0]`, `d[-1]` | uçlara bakmak |

## ChainMap

`ChainMap(ilk, ikinci, ...)`: anahtarı sırayla arar; yazma ilk sözlüğe gider.
