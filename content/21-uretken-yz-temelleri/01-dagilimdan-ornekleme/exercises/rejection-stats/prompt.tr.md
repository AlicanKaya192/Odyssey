`rejection_stats(n, seed)` $[0, 1]$ aralığında $f(x) = 6x(1-x)$ yoğunluğundan
reddetme yöntemiyle örnek çeksin. Aynı üreteçten (`np.random.default_rng(seed)`)
önce `n` tane `x`, sonra `n` tane yükseklik (`random(n) * 1.5`) üret; yüksekliği
`6 * x * (1 - x)`'ten küçük olanları tut. `[kabul oranı, tutulanların
ortalaması]` döndür, ikisi de 3 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[0.664, 0.502]
[0.73, 0.482]
```
