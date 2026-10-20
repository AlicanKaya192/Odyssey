Tahmin kaydına yazılacak satırı kuran `log_entry(row, probability, version, month)` fonksiyonunu yaz:

- Olasılık 0 ile 1 arasında değilse (iki uç dahil) `None` döndür: bozuk bir tahmin kayda girmesin.
- Değilse `{"id": ..., "month": ..., "model_version": ..., "churn_probability": ...}` sözlüğünü döndür; olasılık üç basamağa yuvarlanmış, kimlik `row["id"]`.

**Beklenen çıktı:**

```
id C7
month 2026-05
model_version 3
churn_probability 0.901
None
```
