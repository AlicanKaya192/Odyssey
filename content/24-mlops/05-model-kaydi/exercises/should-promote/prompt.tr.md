Kapının kararını veren `should_promote(candidate, current, min_gain)` fonksiyonunu yaz. `candidate` ve `current` ölçüm sözlükleri (`{"accuracy": 0.82}` gibi); `current` canlıda hiç sürüm yoksa `None`.

Sırayla:

- Adayın ölçümlerinde `"accuracy"` yoksa `"keep"` (ölçülmemiş sürüm canlıya geçmez).
- `current` `None` ise `"promote"` (ilk sürüm).
- Adayın doğruluğu canlıdakinden en az `min_gain` fazlaysa `"promote"`.
- Değilse `"keep"`.

**Beklenen çıktı:**

```
promote
keep
promote
keep
```
