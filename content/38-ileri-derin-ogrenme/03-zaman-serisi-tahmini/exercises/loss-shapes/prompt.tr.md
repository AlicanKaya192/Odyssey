Başlangıç kodunda `(batch, 1)` şekilli bir tahmin ve `(batch,)` şekilli bir
hedef var. `loss_shapes(batch)` iki şekli liste olarak döndürsün: `pred -
target` farkının şekli ve `pred.squeeze(-1) - target` farkının şekli.

**Beklenen çıktı:**

```
[[4, 4], [4]]
[[1, 1], [1]]
```
