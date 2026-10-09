A **genetic algorithm** keeps solutions as a **population** and imitates
evolution: in each generation the good ones survive, pieces of two of them
combine into a child (**crossover**), and small random changes (**mutation**)
keep the variety. A solution is a **gene string**; here a 0/1 string showing
which item is taken in a knapsack of 20 items.

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
        parents = pop[:size // 2]                  # the best half survives
        children = []
        while len(children) < size - len(parents):
            a, b = rng.sample(parents, 2)
            cut = rng.randint(1, 19)
            child = a[:cut] + b[cut:]              # crossover
            if rng.random() < 0.3:
                i = rng.randrange(20)
                child[i] = 1 - child[i]            # mutation
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

The first line is the exact best found by dynamic programming (DP 2): 304. The
best of the random population was 157; it reached 304 in 50 generations. We
were lucky with this seed: trying the same code with three other seeds, it got
stuck at 81–97% of the exact best. When the population becomes alike (loss of
variety), crossover cannot produce anything new.

For the knapsack, DP is exact and fast; we chose the genetic algorithm here
only because we know the answer. Its real use is problems with no DP or other
exact method: circuit and antenna design, class/shift scheduling, neural
network architecture search.
