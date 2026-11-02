`skew_of_means(values, n, reps, seed)` `values` listesinden `reps` tane `n`
kişilik iadeli örneklem çeksin
(`np.random.default_rng(seed).choice(values, size=(reps, n))`), satır
ortalamalarını alsın ve **ortalamaların** çarpıklığını
(`scipy.stats.skew`) 2 basamakla döndürsün. Başlangıç kodu verinin kendi
çarpıklığını döndürüyor.

**Beklenen çıktı:**

```text
1.7
0.39
```
