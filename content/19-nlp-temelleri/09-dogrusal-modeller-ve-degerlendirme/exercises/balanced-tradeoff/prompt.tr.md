`neutral_scores(class_weight)` verilen `class_weight` (`None` ya da
`"balanced"`) ile bir lojistik regresyon eğitsin ve test verisinde **nötr**
sınıfın `[kesinlik, duyarlılık]` değerlerini 3 basamakla döndürsün.
Kesinlik ve duyarlılığı kendin hesapla (`sklearn.metrics` kullanmadan).

**Beklenen çıktı:**

```
plain [0.778, 0.681]
balanced [0.652, 0.806]
```
