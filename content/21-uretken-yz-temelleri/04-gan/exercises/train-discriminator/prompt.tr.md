Başlangıç kodunda üretici yok: sahte örnekler hep tek bir kümeden
(`CENTRES[0]` çevresinden) geliyor. `train_discriminator(steps)` döngüsünde
ayırt edicinin adımı eksik. Gerçek grubun türevi
`backward(acts_r, (p_r - 1) / 128, disc)`, sahte grubunki
`backward(acts_f, p_f / 128, disc)`; ikisinin katman katman toplamıyla
`opt.step(disc, ...)` çağır. Fonksiyon eğitimden sonra ayırt edicinin
gerçek ve sahte örneklere verdiği ortalama olasılığı döndürüyor. Ağ
parçaları salt okunur `gan_model.py`'de.

**Beklenen çıktı:**

```
[0.87, 0.11]
```
