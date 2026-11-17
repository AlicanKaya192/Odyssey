`Residual.forward` yalnızca katmanın çıktısını veriyor. Artık bağlantıyı yaz:
girdi + ReLU(katmanın çıktısı). `apply_block` ağırlıkları 0,25 ve sabiti 0 yapıp
sonucu döndürüyor.

**Beklenen çıktı:**

```
[1.0, -3.0]
[3.0, 3.0]
```
