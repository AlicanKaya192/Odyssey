`pca_error(k)` eğitim resimlerinden PCA yönlerini bulsun (önce ortalamayı
çıkar, sonra `np.linalg.svd(..., full_matrices=False)`), test resimlerini ilk
`k` yöne yansıtıp geri kursun ve ortalama kare hatayı 4 basamağa
yuvarlanmış `float` olarak döndürsün.

**Beklenen çıktı:**

```
2 0.0539
8 0.0245
16 0.0115
```
