`mean_cost(fn_cost, weight)` yanlış pozitifin 1, yanlış negatifin `fn_cost`
tuttuğu maliyeti `make_scorer` ile scorer yapıp
`LogisticRegression(class_weight=weight)` için 5 katlı ortalama maliyeti
**artı** sayı olarak, 1 basamakla döndürsün. Başlangıç kodunda scorer
maliyetin küçük olması gerektiğini bilmiyor.

**Beklenen çıktı:**

```
26.4
21.6
```
