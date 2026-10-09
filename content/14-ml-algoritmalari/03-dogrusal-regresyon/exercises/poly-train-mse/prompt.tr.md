`poly_train_mse(x, y, degree)` fonksiyonunu yaz: özellikler
`x, x², …, x^degree` (ve başta 1 sütunu); ağırlıkları `np.linalg.lstsq` ile
bul ve **eğitim** MSE'sini `round(..., 4)` ile döndürsün.

Eğitim hatası derece arttıkça hep düşer; bu, modelin daha iyi olduğu anlamına
gelmez.

**Beklenen çıktı:**

```
1 6.2347
2 0.0125
4 0.0007
```
