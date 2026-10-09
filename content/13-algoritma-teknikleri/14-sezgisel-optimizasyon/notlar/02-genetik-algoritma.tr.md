**Genetik algoritma** çözümleri bir **nüfus** olarak tutar ve evrimi taklit
eder: her nesilde iyiler hayatta kalır, ikisinin parçaları birleşip
(**çaprazlama**, crossover) çocuk olur ve küçük rastgele değişiklikler
(**mutasyon**) çeşitliliği korur. Bir çözüm bir **gen dizisidir**; burada 20
eşyalık bir sırt çantasında hangi eşyanın alındığını gösteren 0/1 dizisi.

```python
import random

rng = random.Random(0)
weights = [rng.randint(1, 30) for _ in range(20)]
values = [rng.randint(1, 50) for _ in range(20)]
CAP = 100


def fitness(genes):
    w = sum(wi for wi, g in zip(weights, genes) if g)
    v = sum(vi for vi, g in zip(values, genes) if g)
    return v if w <= CAP else 0


def best_by_dp():
    dp = [0] * (CAP + 1)
    for w, v in zip(weights, values):
        for c in range(CAP, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[CAP]


def genetic(generations, size=40):
    pop = [[rng.randint(0, 1) for _ in range(20)] for _ in range(size)]
    for gen in range(generations + 1):
        pop.sort(key=fitness, reverse=True)
        if gen in (0, 10, 50, 200):
            print(gen, fitness(pop[0]))
        parents = pop[:size // 2]                  # en iyi yarı yaşar
        children = []
        while len(children) < size - len(parents):
            a, b = rng.sample(parents, 2)
            cut = rng.randint(1, 19)
            child = a[:cut] + b[cut:]              # çaprazlama
            if rng.random() < 0.3:
                i = rng.randrange(20)
                child[i] = 1 - child[i]            # mutasyon
            children.append(child)
        pop = parents + children


print(best_by_dp())
genetic(200)
```

```text
304
0 157
10 218
50 304
200 304
```

İlk satır dinamik programlamanın (DP 2) bulduğu kesin en iyi: 304. Rastgele
nüfusun en iyisi 157 idi; 50 nesilde 304'e ulaştı. Bu tohumda şanslıydık: aynı
kodu başka üç tohumla denediğimizde kesin en iyinin %81–97'sinde takıldı.
Nüfus birbirine benzeyince (çeşitlilik kaybı) çaprazlama yeni bir şey
üretemiyor.

Sırt çantası için DP kesin ve hızlı; genetik algoritmayı burada yalnızca
cevabı bildiğimiz için seçtik. Gerçek kullanımı, DP'nin ya da başka kesin
yöntemin olmadığı problemler: devre ve anten tasarımı, ders/vardiya
çizelgeleme, sinir ağı mimarisi araması.
