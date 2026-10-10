`daily_totals(days, amounts)` günleri indeks yapan bir seri kursun
(`pd.Series(amounts, index=days)`). Aynı gün birden fazla kez geçebilir;
tekrarları `groupby(level=0).sum()` ile birleştirip `{gün: toplam}`
sözlüğü döndürsün. **Döngü yazma**; `to_dict()` yeter.

**Beklenen çıktı:**

```
{'mon': 40, 'tue': 21, 'wed': 5}
```
