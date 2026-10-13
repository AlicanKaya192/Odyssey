`span_scores(found, gold)` kuralın bulduklarını (`found`) doğru cevaplarla
(`gold`) karşılaştırıp `[kesinlik, duyarlılık]` döndürsün (3 basamak).
Tekrarlar sayılır: aynı tutar iki kez varsa iki kez bulunmalı. `found` boşsa
kesinlik, `gold` boşsa duyarlılık `0.0`.

**Beklenen çıktı:**

```
[0.667, 0.667]
[0.0, 0.0]
```
