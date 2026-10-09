`min_max(train, test)` fonksiyonunu yaz: her sütunu eğitim verisinin
**en küçüğü 0, en büyüğü 1** olacak şekilde ölçekle ve test verisine uygula:
`(x − min) / (max − min)`. Eğitimde bir sütun sabitse (`max == min`) o sütunun
sonucu 0 olsun. `.round(3).tolist()` döndür.

Test değerleri 0–1 dışına çıkabilir; bu doğru, kırpma.

**Beklenen çıktı:**

```
[[0.25, 0.0], [1.5, 0.0], [-0.25, 0.0]]
```
