## Bu modülde en çok kullanılanlar

| İş | NumPy |
|---|---|
| Tohumlu üreteç | `rng = np.random.default_rng(0)` |
| Normal / düzgün dağılım | `rng.normal(ort, ss, size)`, `rng.uniform(a, b, size)` |
| Boyut | `X.shape`, `X.ndim`, `len(X)` |
| Sütun başına | `X.mean(axis=0)`, `X.std(axis=0)`, `X.sum(axis=0)` |
| Satır başına | `X.sum(axis=1)` |
| Matris çarpımı | `X @ w`, `X.T @ X` |
| Koşulla seçmek | `X[y == 1]`, `np.where(k, a, b)` |
| En büyüğün yeri | `np.argmax(v)`, `np.argsort(v)` |
| Sayma | `np.bincount(y)`, `np.unique(y, return_counts=True)` |
| Karşılaştırma | `np.allclose(a, b)`, `(a == b).all()` |
| Yuvarlama, listeye | `a.round(3)`, `a.tolist()` |

## Yayın (broadcasting) kuralı

İki dizinin boyutları **sondan başa** karşılaştırılır; her boyut ya eşit ya
da 1 olmalı. `(200, 2) - (2,)` olur (vektör her satıra), `(200, 2) - (200,)`
olmaz; satır başına çıkarmak için `(200, 1)` gerekir: `v[:, None]` ya da
`v.reshape(-1, 1)`.

## Sık hatalar

- `axis` karıştırmak: `axis=0` sütun başına sonuç verir (boy = özellik
  sayısı), `axis=1` satır başına (boy = örnek sayısı).
- `ddof`: NumPy ve scikit-learn varsayılan olarak `n`'e böler (`ddof=0`);
  pandas'ın `std()`'si `n − 1`'e (`ddof=1`).
- Kayan noktalı sayıları `==` ile karşılaştırmak: `np.allclose` kullan.
- Tohumsuz üreteç: her çalıştırmada başka sonuç; deney tekrarlanamaz.
