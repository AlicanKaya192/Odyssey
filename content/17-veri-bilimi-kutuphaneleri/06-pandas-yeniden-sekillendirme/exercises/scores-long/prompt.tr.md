`scores_long(table)` `{"id": [...], "score_2024": [...], ...}` biçiminde bir
sözlük alıyor; yıl sütun adının içinde. `pd.wide_to_long` ile
(`stubnames="score"`, `i="id"`, `j="year"`, `sep="_"`) uzun biçime
çevirsin, `reset_index()` yapsın, `["id", "year"]`'a göre sıralasın ve
satırları `[id, yıl, puan]` listesi olarak döndürsün. **Döngü yazma.**

**Beklenen çıktı:**

```
[1, 2024, 60]
[1, 2025, 70]
[2, 2024, 75]
[2, 2025, 80]
```
