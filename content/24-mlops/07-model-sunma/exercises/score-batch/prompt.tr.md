`scorer.py`'de sabit ağırlıklı bir model var: `churn_probability(row)` ve `VERSION`. Toplu puanlama yapan `score_batch(rows)` fonksiyonunu yaz:

- Her müşteri için `[id, olasılık, sürüm]` listesi üret; olasılık üç basamağa yuvarlanmış, sürüm `VERSION`.
- Müşterilerin sırası korunsun.

**Beklenen çıktı:**

```
['C1', 1.0, 3]
['C2', 0.01, 3]
['C3', 0.618, 3]
```
