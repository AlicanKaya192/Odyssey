Dersteki `run_month`'un karar kısmını yazan `decide_month(live, base, drift, invalid, candidate)` fonksiyonunu yaz. Eşikler başlangıç kodunda hazır. Sırayla:

- `live` en az `base - MAX_DROP` ve `drift` en fazla `MAX_DRIFT` ise `"keep"`.
- `invalid` (geçersiz satır payı) `MAX_INVALID`'den büyükse `"data rejected"`.
- `candidate` (adayın skoru) `live + MIN_GAIN`'den küçükse `"kept out"`.
- Yoksa `"promoted"`.

**Beklenen çıktı:**

```
keep
promoted
kept out
data rejected
```
