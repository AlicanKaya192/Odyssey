`share_interval(k, n)` `n` kişiden `k`'sının alışveriş yaptığı bir örneklem
için %95 **Wilson** aralığını `[alt, üst]` olarak 4 basamakla döndürsün
(`proportion_confint(..., method="wilson")`). Başlangıç kodu Wald
(`"normal"`) kullanıyor: `k = 0` olunca aralık tek bir noktaya çöküyor.

**Beklenen çıktı:**

```text
[0.1027, 0.1692]
[0.0, 0.1611]
```
