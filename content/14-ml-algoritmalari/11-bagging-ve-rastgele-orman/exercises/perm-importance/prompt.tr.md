`perm_importance(X, y, seed)` fonksiyonunu yaz: hazır `model_predict`'in
doğruluğu temel; `rng = np.random.default_rng(seed)`, her sütun `j` için (sırayla)
kopyada o sütunu `rng.permutation` ile karıştır ve doğruluk düşüşünü
hesapla. Düşüşleri `round(..., 3)` liste olarak döndürsün.

**Beklenen çıktı:**

```
[0.0, 0.527, 0.0]
```
