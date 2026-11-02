`alarm_rates(n1, sd1, n2, sd2, reps, seed)` gerçek farkın sıfır olduğu bir
dünyada iki testi ölçsün: `np.random.default_rng(seed)` ile ortalaması 10,
sapması `sd1` olan `reps` × `n1` ve sapması `sd2` olan `reps` × `n2`
normal değer üret (önce birinci grup). Satır satır Student (`ttest_ind`,
varsayılan) ve Welch (`equal_var=False`) uygula; `p < 0.05` paylarını
`[student, welch]` olarak 3 basamakla döndür.

**Beklenen çıktı:**

```text
[0.259, 0.053]
[0.051, 0.05]
```
