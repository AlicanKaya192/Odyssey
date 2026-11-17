`channel_stats(batch)` `(N, C, H, W)` sırasındaki bir yığının her kanalı için
ortalamayı ve standart sapmayı (PyTorch'un `std`'si, varsayılan ayarla)
3 basamakla iki liste olarak döndürsün: `means, stds`.

**Beklenen çıktı:**

```
[0.75, 0.5]
[0.5, 0.0]
```
