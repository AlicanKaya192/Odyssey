`last_real_steps(out, lengths)`: `out` `(B, T, H)` boyutlu her adımın
çıktısı, `lengths` her dizinin gerçek uzunluğu. Her dizinin son gerçek
adımının çıktısını `(B, H)` liste olarak döndürsün. Döngü yerine iki dizinli
seçim kullanabilirsin.

**Beklenen çıktı:**

```
[[3, 3], [5, 5]]
[[1, 1], [4, 4]]
```
