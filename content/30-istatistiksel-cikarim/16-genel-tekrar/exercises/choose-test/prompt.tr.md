`choose_test(outcome, groups, paired, skewed)` doğru testin adını döndürsün.
`outcome` `"mean"` ya da `"rate"`. Oranlarda iki grup `"z-test"`, daha
çoğu `"chi-square"`. Ortalamalarda: ikiden çok grup `"anova"` (çarpıksa
`"kruskal"`); eşli iki grup `"paired-t"` (çarpıksa `"wilcoxon"`); bağımsız
iki grup `"welch"` (çarpıksa `"mann-whitney"`). Başlangıç kodu hep
`"welch"` diyor.

**Beklenen çıktı:**

```text
welch
wilcoxon
chi-square
```
