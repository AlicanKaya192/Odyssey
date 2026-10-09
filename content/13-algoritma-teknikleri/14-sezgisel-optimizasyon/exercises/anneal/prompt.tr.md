`anneal(x, seed)` fonksiyonunu yaz: `f`'in en küçük olduğu yeri tavlama
benzetimiyle arasın ve bulunan en iyi `x`'i `round(..., 2)` ile döndürsün.
`rng = random.Random(seed)`, `temp = 20.0`, 3000 adım. Her adımda **bu sırayla**:

- `cand = x + rng.uniform(-3, 3)`, `delta = f(cand) - f(x)`
- `delta < 0` ise kabul; değilse `rng.random() < math.exp(-delta / temp)` ise kabul
- `f(x) < f(best)` ise `best = x`; sonra `temp *= 0.998`

**Beklenen çıktı:**

```
0 -1.54
1 -1.54
2 -1.54
3 -1.54
```
