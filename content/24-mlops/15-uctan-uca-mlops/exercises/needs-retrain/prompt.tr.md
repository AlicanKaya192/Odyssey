Hattın tetiğini yazan `needs_retrain(live, base, drift, max_drop, max_drift)` fonksiyonunu yaz. Şu iki durumdan biri varsa `True`, yoksa `False` döndür:

- `live`, `base - max_drop`'tan küçük (doğruluk düştü).
- `drift`, `max_drift`'ten büyük (kayma büyük).

**Beklenen çıktı:**

```
False
True
True
```
