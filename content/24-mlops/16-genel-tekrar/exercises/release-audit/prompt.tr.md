Dersteki denetçiyi kısa kodlarla yazan `audit_codes(release, min_gain)` fonksiyonunu yaz. Sırayla şu kodları ekle:

- `"seed"`: `release["seed"]` `None`.
- `"digest"`: `release["data_digest"]` boş.
- `"gate"`: `gate_month` `trained_month`'tan küçük.
- `"gain"`: `gain` `min_gain`'den küçük.
- `"threshold"`: `threshold` tam `0.5`.
- `"fallback"`: `fallback` `None`.
- `"drift"` ve `"calibration"`: `monitors` listesinde yoksa (bu sırayla).

**Beklenen çıktı:**

```
seed
digest
gate
gain
threshold
fallback
drift
calibration
[]
```
