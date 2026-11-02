`decide(values, mu0, alpha)` tek örneklem t-testini (`stats.ttest_1samp`)
yapıp `[karar, p]` döndürsün: `p < alpha` ise karar `"reject"`, değilse
`"keep"`; p 4 basamak. Başlangıç kodunda karşılaştırma ters.

**Beklenen çıktı:**

```text
['reject', 0.008]
['keep', 1.0]
```
