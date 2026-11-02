`false_alarm_rate(values, n, reps, seed, alpha)` I. tür hatayı benzetimle
ölçsün: `np.random.default_rng(seed)` ile `values`'tan `reps` tane `n`'lik
iadeli örneklem çek; her birinde gerçek ortalamaya (`values`'ın
ortalaması, yani H₀ **doğru**) karşı `ttest_1samp` uygula (`axis=1`) ve
`p < alpha` olanların payını 3 basamakla döndür. Başlangıç kodu ters
olanları sayıyor.

**Beklenen çıktı:**

```text
0.053
0.014
```
