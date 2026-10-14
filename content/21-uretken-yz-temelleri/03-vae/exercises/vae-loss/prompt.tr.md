`vae_loss(x, out, mu, logvar, beta)` bir grup örneğin kaybını hesaplasın.
`x` ve `out` piksel listeleri, `mu` ve `logvar` kod listeleri (her satır
bir örnek). Örnek başına geri kurma terimi ikili çapraz entropinin
pikseller üzerinden toplamı:
`-(x * log(out) + (1 - x) * log(1 - out))`; KL terimi de boyutlar
üzerinden toplam. Döndür: `[geri kurma ortalaması, KL ortalaması,
geri kurma + beta * KL]`, ortalamalar örnekler üzerinden, her sayı 4
basamağa yuvarlanmış `float`.

**Beklenen çıktı:**

```
[0.7623, 1.4417, 2.2039]
[0.7623, 1.4417, 1.4831]
```
