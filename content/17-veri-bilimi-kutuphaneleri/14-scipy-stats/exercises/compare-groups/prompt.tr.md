`compare_groups(a, b)` iki bağımsız grubu **Welch** t-testiyle karşılaştırsın
(`stats.ttest_ind(b, a, equal_var=False)`: sapmalar ve grup boyları farklı).
`[fark, p, anlamlı_mı]` döndürsün: fark `b`'nin ortalaması eksi `a`'nınki (2
basamak), p 4 basamak, anlamlı `p < 0.05` (`bool`). Başlangıç kodu sapmaların
eşit olduğunu varsayıyor.

**Beklenen çıktı:**

```
[11.89, 0.0302, True]
```
