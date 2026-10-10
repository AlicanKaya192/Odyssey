`copy_effect(spread)` veriye alanın gürültülü bir kopyasını eklesin
(`area_copy = area + np.random.default_rng(1).normal(0, spread, len(X))`),
ormanı yeniden eğitsin ve test verisinde `[alanın_önemi, kopyanın_önemi]`
döndürsün (`n_repeats=5`, `random_state=0`, 3 basamak; kopya son sütun).
Başlangıç kodu kopyayı eklemiyor.

**Beklenen çıktı:**

```
[0.457, 0.282]
```
