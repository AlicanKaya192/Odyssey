`decide(srm_p, guard_ok, low, threshold)` sırayla: SRM p'si 0,001'den
küçükse `"stop: SRM"`, koruma bozuksa (`guard_ok` False) `"stop:
guardrail"`, alt uç eşikten büyük ya da eşitse `"ship"`, sıfırdan büyükse
`"unclear"`, yoksa `"no evidence"`. Başlangıç kodu güven kontrollerini
atlıyor.

**Beklenen çıktı:**

```text
ship
stop: SRM
```
