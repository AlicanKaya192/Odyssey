`has_duplicate(items)` fonksiyonunu iç içe döngülerle yaz: her ikiliyi
(`i < j`) karşılaştırsın ve `(bulundu_mu, karşılaştırma)` demetini döndürsün.

- İlk eşit ikiliyi bulunca **hemen** `(True, karşılaştırma)` döndür.
- Hiç eşit ikili yoksa `(False, karşılaştırma)` döndür.

**Beklenen çıktı:**

```
(True, 1)
(True, 5)
(False, 4950)
```

Tekrar yoksa (en kötü durum) 100 elemanda 4950 karşılaştırma: her ikili.
Tekrar baştaysa tek karşılaştırma yetti.
