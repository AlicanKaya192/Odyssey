`choose_k(ks)` her `k` için `make_pipeline(SelectKBest(f_classif, k=k),
LogisticRegression())` kurup `cross_val_score(..., cv=5)` ortalamasını
hesaplasın. Şunu döndürsün:

- `"scores"`: skorlar, `ks` sırasıyla liste (3 basamak)
- `"best"`: en yüksek skorlu `k` (eşitlikte küçük olan)

Seçim pipeline'ın içinde olmalı.

**Beklenen çıktı:**

```
[0.868, 0.87, 0.852]
4
```
