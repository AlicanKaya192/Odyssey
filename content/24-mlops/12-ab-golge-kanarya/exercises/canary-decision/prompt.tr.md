Bir kanarya aşamasının kararını veren `canary_decision(n, min_n, canary_score, control_score, tolerance)` fonksiyonunu yaz:

- Kanaryada `min_n`'den az müşteri varsa `"wait"` (karar için erken).
- Kanaryanın skoru `control_score - tolerance`'tan küçükse `"rollback"`.
- Yoksa `"advance"`.

Kontroller bu sırayla yapılır.

**Beklenen çıktı:**

```
wait
rollback
advance
```
