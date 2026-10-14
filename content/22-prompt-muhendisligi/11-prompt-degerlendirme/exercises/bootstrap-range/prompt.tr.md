`bootstrap(ok1, ok2, rounds, seed)` dersteki yeniden örneklemeyi yapsın:
`rng = random.Random(seed)`; her turda `n = len(ok1)` indeksi
`rng.randrange(n)` ile çek ve `(ok2 - ok1)` toplamını `n`'e böl. Farkları
sırala; alt uç `diffs[rounds // 20]`, üst uç
`diffs[rounds - rounds // 20 - 1]`. Döndür: `[gerçek fark, alt uç, üst
uç]`, her biri 3 basamağa yuvarlanmış.

**Beklenen çıktı:**

```
[0.125, 0.0, 0.25]
```
