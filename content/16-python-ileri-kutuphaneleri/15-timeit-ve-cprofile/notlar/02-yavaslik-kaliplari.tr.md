Profil çıktısında en tepede çoğu zaman aynı birkaç kalıp çıkar. İkisi
aşağıda ölçüldü; her birinde önce sonucun aynı olduğu, sonra hızın en az 10
kat arttığı denetleniyor.

```python
import timeit

customers = [{"id": i, "name": f"c{i}"} for i in range(3_000)]
orders = [{"id": n, "customer": (n * 7) % 3_000} for n in range(3_000)]


def match_nested():
    result = []
    for order in orders:
        for customer in customers:
            if customer["id"] == order["customer"]:
                result.append((order["id"], customer["name"]))
    return result


def match_dict():
    by_id = {c["id"]: c["name"] for c in customers}
    return [(order["id"], by_id[order["customer"]]) for order in orders]


scores = list(range(2_000, 0, -1))


def best_each_time():
    return [sorted(scores)[0] for _ in range(200)]


def best_once():
    best = min(scores)
    return [best for _ in range(200)]


for slow, fast in [(match_nested, match_dict), (best_each_time, best_once)]:
    same = slow() == fast()
    slow_time = min(timeit.repeat(slow, number=1, repeat=3))
    fast_time = min(timeit.repeat(fast, number=1, repeat=3))
    print(slow.__name__, same, slow_time / fast_time > 10)
```

```text
match_nested True True
best_each_time True True
```

Bu bilgisayarda ilki yaklaşık 600, ikincisi yaklaşık 100 kat hızlandı.

## Kalıplar

| Yavaş | Hızlı | Neden |
|---|---|---|
| İç içe döngüyle eşleştirmek | önce sözlük (indeks) kur, sonra ara | 3000 × 3000 karşılaştırma yerine 3000 + 3000 adım |
| Döngüde her seferinde `sorted(...)` | bir kez `min` / `sorted` | aynı işi 200 kez yapmamak |
| Listede `in` | kümede `in` | küme adresi doğrudan hesaplıyor |
| `x not in liste` ile tekrar atmak | `dict.fromkeys` / `set` | tek geçiş |
| `liste.count(k)` her anahtar için | `Counter` | tek geçiş |
| Listenin başına `insert(0, x)` | `collections.deque.appendleft` | kaydırma yok |
| pandas'ta satır satır `iterrows` | sütun işlemi (vektörel) | döngü C'de |

Ortak fikir: **aynı işi tekrar tekrar yapma** ve **doğru veri yapısını seç**.
Hangi kalıbın senin programında önemli olduğunu yine profil söyler.
