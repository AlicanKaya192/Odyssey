`pick_counts(probs, n, seed)` olasılık listesinden `n` kez kategori seçsin ve
her kategorinin kaç kez seçildiğini liste olarak döndürsün. Birikimli toplamı
`np.cumsum`, seçimi `np.searchsorted(cum, u, side="right")` ile yap; düzgün
sayılar `np.random.default_rng(seed).random(n)`. Sayıları
`np.bincount(..., minlength=len(probs))` ile bul ve `tolist()` ile döndür.

**Beklenen çıktı:**

```
[471, 313, 216]
[44, 6]
```
