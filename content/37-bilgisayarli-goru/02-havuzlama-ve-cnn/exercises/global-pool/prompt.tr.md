`global_pool(fmap)` `(C, H, W)` sırasındaki bir özellik haritasının her kanalı
için küresel ortalamayı ve küresel en büyüğü (`F.adaptive_avg_pool2d`,
`F.adaptive_max_pool2d`, çıkış boyu 1) 3 basamakla iki liste olarak
döndürsün.

**Beklenen çıktı:**

```
[2.5, 2.0]
[4.0, 8.0]
```
