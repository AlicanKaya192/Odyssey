Harcama (`spend`) ortalamaları hangi büyüklükte çana döner? `n` = 30 ve
`n` = 2000 için (aynı `rng`, önce 30) 2000'er örneklem ortalaması çek:
`rng.choice(y, size=(2000, n)).mean(axis=1)`. `se = sigma / np.sqrt(n)`.
Her satıra `n`, `mu - 1.96 * se`'nin **altına** düşenlerin payını ve
`mu + 1.96 * se`'nin **üstüne** çıkanların payını (3 basamak) yaz. Çan
biçiminde ikisi de 0.025'e yakın olur.

**Beklenen çıktı:**

```text
30 0.0 0.046
2000 0.02 0.029
```
