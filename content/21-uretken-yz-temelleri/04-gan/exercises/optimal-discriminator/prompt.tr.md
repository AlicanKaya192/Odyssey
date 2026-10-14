Gerçek veri standart normal, üretici ise ortalaması `mu_g`, standart sapması
`sd_g` olan bir normal dağılım olsun. `optimal_d(xs, mu_g, sd_g)` her `x` için
en iyi ayırt edicinin değerini döndürsün:
`p_data(x) / (p_data(x) + p_g(x))`. Normal yoğunluk:
`exp(-(x - m) ** 2 / (2 * s ** 2)) / (s * sqrt(2 * pi))`. Sonuç 3 basamağa
yuvarlanmış `float` listesi.

**Beklenen çıktı:**

```
[0.5, 0.5, 0.5]
[0.881, 0.5, 0.119]
```
