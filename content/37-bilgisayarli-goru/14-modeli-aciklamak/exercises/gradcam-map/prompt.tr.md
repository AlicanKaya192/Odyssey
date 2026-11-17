`gradcam_map(maps, grads)` `(C, H, W)` biçiminde iki liste alsın: son evrişim
haritaları ve sınıf puanının onlara göre gradyanı. Grad-CAM haritasını
(kanal ağırlığı = gradyanın ortalaması; haritaların ağırlıklı toplamı; ReLU)
3 basamakla liste listesi olarak döndürsün.

**Beklenen çıktı:**

```
[[1.0, 0.0], [0.0, 0.0]]
[[0.5, 0.0], [0.0, 1.0]]
```
