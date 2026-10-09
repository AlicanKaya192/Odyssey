## Sıralama

| Yazım | Ne yapar |
|---|---|
| `sorted(x)` | yeni liste, aslı aynı |
| `x.sort()` | yerinde, `None` döner |
| `sorted(x, reverse=True)` | büyükten küçüğe |
| `sorted(x, key=str.casefold)` | harf büyüklüğüne bakmadan |
| `sorted(x, key=len)` | uzunluğa göre |
| `sorted(d.items(), key=itemgetter(1))` | sözlüğü değere göre |
| `sorted(x, key=lambda r: (r["a"], -r["b"]))` | a artan, b azalan |

## operator

| Yazım | Eşdeğeri |
|---|---|
| `itemgetter(1)` | `lambda r: r[1]` |
| `itemgetter("age")` | `lambda r: r["age"]` |
| `itemgetter(1, 2)` | `lambda r: (r[1], r[2])` |
| `attrgetter("price")` | `lambda o: o.price` |
| `methodcaller("lower")` | `lambda s: s.lower()` |
| `operator.add`, `mul`, `neg` | `+`, `*`, tek eksi |

## heapq ve bisect

| Yazım | Ne verir |
|---|---|
| `heapq.nlargest(n, x, key=...)` | en büyük n |
| `heapq.nsmallest(n, x, key=...)` | en küçük n |
| `bisect.bisect(sıralı, v)` | v'nin gireceği yer (eşitlerin sağı) |
| `bisect.bisect_left(sıralı, v)` | eşitlerin solu |
| `bisect.insort(sıralı, v)` | sırayı bozmadan ekle |

## Hatırla

- Python'un sıralaması kararlıdır: eşitler geliş sırasını korur.
- Karışık türler (`3` ve `"a"`) sıralanamaz.
- `None`'ları sona atmak: `key=lambda v: (v is None, v)`.
