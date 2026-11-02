`both_p(a, b)` "b, a'dan büyük mü" sorusu için iki p döndürsün: Welch
t-testi (`ttest_ind(b, a, equal_var=False)`) ve Mann–Whitney
(`mannwhitneyu(b, a)`), 4 basamak. Başlangıç kodu t'nin p'sini iki kez
döndürüyor. Örnekteki dev değerin iki teste etkisine bak.

**Beklenen çıktı:**

```text
[0.2506, 0.0002]
```
