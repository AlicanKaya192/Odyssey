`flatten_shapes(n, size)` `make_shapes(n, size=size)` ile görüntüleri
üretiyor. Görüntüleri tensöre çevirip ilk boyutu koruyarak düzleştir; düz
tensörün şeklini ve kaç görüntünün daire (etiket 0) olduğunu tek listede
döndür: `[satır, sütun, daire sayısı]`.

**Beklenen çıktı:**

```
[50, 256, 15]
[20, 64, 7]
```
