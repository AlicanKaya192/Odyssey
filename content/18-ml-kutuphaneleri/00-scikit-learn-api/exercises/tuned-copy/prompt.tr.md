`tuned_copy(c)` `LogisticRegression(C=1.0)` kurup başlangıç kodundaki veriyle
eğitsin. Sonra `sklearn.base.clone` ile bir kopya alıp kopyanın `C`'sini
`set_params(C=c)` ile değiştirsin. `[asıl_C, kopya_C, kopya_eğitilmiş_mi]`
döndürsün; eğitilmiş mi = `hasattr(kopya, "coef_")`.

**Beklenen çıktı:**

```
[1.0, 5.0, False]
```
