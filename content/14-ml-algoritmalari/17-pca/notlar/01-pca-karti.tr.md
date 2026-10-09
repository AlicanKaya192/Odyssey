## Adımlar

| Adım | Kod |
|---|---|
| Ortala | `Xc = X - X.mean(axis=0)` |
| Kovaryans | `C = Xc.T @ Xc / (n - 1)` |
| Özvektörler | `vals, vecs = np.linalg.eigh(C)`, büyükten küçüğe sırala |
| Ya da SVD | `U, S, Vt = np.linalg.svd(Xc, full_matrices=False)`, varyans `S**2 / (n - 1)` |
| İzdüşüm | `Z = Xc @ vecs[:, :k]` |
| Geri kurma | `X ≈ Z @ vecs[:, :k].T + ortalama` |

## scikit-learn

| Ad | Anlamı |
|---|---|
| `PCA(k)` | `k` bileşen; `PCA(0.95)` varyansın %95'ini tutan en küçük `k` |
| `components_` | bileşenler (satır satır) |
| `explained_variance_` | her bileşenin varyansı (özdeğer) |
| `explained_variance_ratio_` | toplam varyanstaki payı |
| `transform` / `inverse_transform` | izdüşür / geri kur |

## Ne zaman?

- Çok sayıda ilişkili özellik: boyut indirgeme, gürültü azaltma.
- Görselleştirme: 2 ya da 3 bileşene indirip çizmek.
- Modelden önce: daha az özellik, daha hızlı eğitim (doğruluk biraz düşebilir).

## Sık hatalar

- Ölçeklememek: birimi büyük özellik birinci bileşeni ele geçirir.
- PCA'yı bütün veriye uyup sonra bölmek: test bilgisi sızar; `Pipeline` içinde
  yalnızca eğitim verisine uy.
- Bileşenin işaretine anlam yüklemek: `v` ile `−v` aynı eksen.
- Doğrusal olmayan yapıları beklemek: PCA yalnızca doğrusal yönleri bulur.
- Yüksek varyansı "önemli" sanmak: hedefle ilgisiz bir yön de çok yayılmış
  olabilir.
