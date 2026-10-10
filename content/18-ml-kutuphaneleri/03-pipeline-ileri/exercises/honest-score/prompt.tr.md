`honest_score(seed)` tamamen rastgele bir veri üretiyor (60 satır, 2000 sütun,
rastgele hedef). Başlangıç kodu en iyi 10 sütunu **bütün veriden** seçip sonra
çapraz doğruluyor: sahte yüksek skor. Seçimi (`SelectKBest(f_classif, k=10)`)
modelle birlikte bir pipeline'a koy ve `cross_val_score(..., cv=5)`
ortalamasını 2 basamağa yuvarlı döndür.

**Beklenen çıktı:**

```
0.45
```
