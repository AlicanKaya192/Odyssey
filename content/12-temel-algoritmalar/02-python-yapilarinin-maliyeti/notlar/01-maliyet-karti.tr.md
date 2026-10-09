Python'un yerleşik yapılarında sık kullanılan işlemlerin ortalama
maliyeti. `n` yapının eleman sayısı, `k` işlemin dokunduğu parça.

## Liste (`list`)

| İşlem | Maliyet |
|---|---|
| `items[i]`, `items[i] = x` | `O(1)` |
| `len(items)` | `O(1)` |
| `items.append(x)` | `O(1)` amortize |
| `items.pop()` (sondan) | `O(1)` |
| `items.insert(0, x)`, `items.pop(0)` | `O(n)` |
| `x in items`, `items.index(x)`, `items.count(x)` | `O(n)` |
| `items.remove(x)` | `O(n)` |
| `items[a:b]` (dilim) | `O(k)` |
| `min`, `max`, `sum` | `O(n)` |
| `items.sort()`, `sorted(items)` | `O(n log n)` |
| `items.reverse()` | `O(n)` |

## Sözlük (`dict`) ve küme (`set`)

| İşlem | Maliyet |
|---|---|
| `d[key]`, `d[key] = v`, `del d[key]` | `O(1)` ortalama |
| `key in d`, `x in s` | `O(1)` ortalama |
| `s.add(x)`, `s.discard(x)` | `O(1)` ortalama |
| `d.get(key, varsayılan)` | `O(1)` ortalama |
| `set(items)`, `dict(...)` kurmak | `O(n)` |
| <code>a &amp; b</code>, <code>a &#124; b</code> (kesişim, birleşim) | `O(len(a) + len(b))` kabaca |
| Bütün elemanları gezmek | `O(n)` |

"Ortalama" kelimesi önemli: çok kötü dağılmış hash'lerde en kötü durum
`O(n)` olabilir, ama Python'un yerleşik türlerinde pratikte buna
rastlanmaz.

## `collections.deque`

| İşlem | Maliyet |
|---|---|
| `append`, `appendleft` | `O(1)` |
| `pop`, `popleft` | `O(1)` |
| `items[i]` (ortada) | `O(n)` |
| `deque(maxlen=k)` ile son `k` eleman | eklerken `O(1)`, eskisi kendiliğinden düşer |

## Metin (`str`)

| İşlem | Maliyet |
|---|---|
| `s[i]`, `len(s)` | `O(1)` |
| `sub in s`, `s.find(sub)` | en kötü `O(len(s) × len(sub))` |
| `s + t` | `O(len(s) + len(t))`: yeni metin kurulur |
| `"".join(parts)` | toplam uzunlukta `O` |
| `s.split()`, `s.replace(...)` | `O(len(s))` |

## Akılda tutulacak üç cümle

1. "İçinde var mı?" diye çok soracaksan küme ya da sözlük kur.
2. Baştan çıkaracaksan `deque` kullan.
3. Döngünün içindeki her tek satırlık çağrının maliyetini döngünün tur
   sayısıyla çarp.
