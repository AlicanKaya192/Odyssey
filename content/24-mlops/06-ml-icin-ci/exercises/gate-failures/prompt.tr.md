`gate_failures(metrics, rules)` fonksiyonunu yaz ve düşen kuralların listesini döndür:

- Doğruluk `rules["min_accuracy"]`'den küçükse `"accuracy"`.
- Doğruluk `metrics["baseline"] + rules["min_lift"]`'ten küçükse `"lift"`.
- `metrics["slices"]` içindeki her dilim için, **adlarının abece sırasıyla**: değeri `rules["min_slice"]`'tan küçükse `"slice:<ad>"`.

Hiçbir kural düşmediyse boş liste.

**Beklenen çıktı:**

```
[]
accuracy
lift
slice:basic
slice:pro
```
