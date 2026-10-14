`gan_losses(p_real, p_fake)` ayırt edicinin gerçek ve sahte örneklere
verdiği olasılık listelerini alsın ve üç ortalama döndürsün:
`[ayırt edici kaybı, üretici kaybı, eski üretici kaybı]`. Ayırt edici
kaybı `-(log(p_real) + log(1 - p_fake))` (iki listenin ortalamalarının
toplamı), üretici kaybı `-log(p_fake)`, eski biçim `log(1 - p_fake)`. Her
sayı 4 basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[0.3953, 1.7533, -0.231]
[1.3863, 0.6931, -0.6931]
```
