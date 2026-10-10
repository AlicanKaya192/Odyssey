`l1_counts(c)` ölçeklenmiş şarap verisinde (`Xs`) L1 cezalı lojistik regresyon
eğitsin (`l1_ratio=1`, `solver="saga"`, `C=c`, `max_iter=5000`) ve her sınıfın
sıfır olmayan katsayı sayısını liste olarak döndürsün. `penalty=` eskidi,
kullanma. Başlangıç kodu varsayılan (L2) cezayı kullanıyor.

**Beklenen çıktı:**

```
[3, 8, 4]
[4, 4, 4]
```
