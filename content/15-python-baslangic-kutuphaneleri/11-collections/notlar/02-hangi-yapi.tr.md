## Aynı sayım, üç yol

```python
from collections import Counter, defaultdict

text = "to be or not to be that is the question to be"
words = text.split()

counts1 = {}
for w in words:
    counts1[w] = counts1.get(w, 0) + 1
counts2 = defaultdict(int)
for w in words:
    counts2[w] += 1
counts3 = Counter(words)
print(counts1 == dict(counts2) == dict(counts3))
print(counts3.most_common(3))
by_length = defaultdict(list)
for w in sorted(set(words)):
    by_length[len(w)].append(w)
print(dict(by_length))
```

```text
True
[('to', 3), ('be', 3), ('or', 1)]
{2: ['be', 'is', 'or', 'to'], 3: ['not', 'the'], 8: ['question'], 4: ['that']}
```

Üç yol da aynı sonucu verdi. Fark okunaklılıkta: `Counter(words)` niyeti
tek kelimeyle söylüyor ve `most_common` hazır geliyor. Sayma dışında bir şey
biriktiriyorsan (liste, küme) `defaultdict`; burada kelimeler uzunluklarına
göre gruplandı. Düz sözlük ve `get` her yerde çalışır, ama en çok yazı onda.

## Hangi yapı?

| İhtiyaç | Yapı |
|---|---|
| Sırayla tutmak, sona eklemek | `list` |
| Anahtarla bulmak | `dict` |
| Tekrarsız, "içinde var mı?" | `set` |
| Değişmeyen küçük kayıt | `tuple` / `namedtuple` |
| Saymak, en sıklar | `Counter` |
| Anahtara göre gruplamak | `defaultdict(list)` |
| İki uçtan ekleme/çıkarma, kuyruk | `deque` |
| Son N öğe | `deque(maxlen=N)` |
| Ayar katmanları | `ChainMap` |
| Alanları değişen, metotlu kayıt | `dataclass` (İleri Python) |

## Neden önemli?

Doğru yapı kodu hem kısaltır hem hızlandırır. Bu bilgisayarda 100 000
elemanı baştan çıkarmak listede yaklaşık 0,9 saniye, `deque`'de 0,005
saniye sürdü:

```python
import time
from collections import deque

items = list(range(100_000))
start = time.perf_counter()
while items:
    items.pop(0)
print("list", round(time.perf_counter() - start, 3))
items = deque(range(100_000))
start = time.perf_counter()
while items:
    items.popleft()
print("deque", round(time.perf_counter() - start, 4))
```

Liste her `pop(0)`'da arkadaki bütün elemanları bir adım kaydırıyor; eleman
sayısı iki katına çıkınca iş dört katına çıkıyor. `deque` her çıkarmada
aynı küçük işi yapıyor. Süreler bilgisayara göre değişir, aradaki büyük fark
değişmez.
