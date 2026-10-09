## Formüller ve NumPy karşılıkları

| Ölçü | Formül | NumPy |
|---|---|---|
| Ortalama | `Σx / n` | `x.mean()` |
| Varyans | `Σ(x − ort)² / n` | `x.var()` (`ddof=1` ile `n − 1`) |
| Standart sapma | `√varyans` | `x.std()` |
| Yüzdelik | sıralı listede `(n − 1)·q/100`, arada doğrusal | `np.percentile(x, q)` |
| Medyan | 50. yüzdelik | `np.median(x)` |
| Kovaryans | `Σ(x − ort_x)(y − ort_y) / n` | `np.cov(x, y, ddof=0)` |
| Pearson | kovaryans / (ss_x · ss_y) | `np.corrcoef(x, y)[0, 1]` |
| Histogram | eşit kutulara say | `np.histogram(x, bins, range)` |

## Sayısal sağlamlık

- `E[x²] − (E[x])²` yerine önce ortalamayı çıkar (iki geçiş) ya da Welford.
- Çok sayıda küçük sayıyı toplarken Python'un `math.fsum`'ı yuvarlama hatasını
  biriktirmez; NumPy'nin `sum`'ı ikili (pairwise) toplama yapar.
- Sabit bir sütunun standart sapması 0: ona bölmek `inf` ya da `nan` üretir.

## Sık hatalar

- `int()` sıfıra doğru keser: `int(-0.3)` 0 verir, `math.floor(-0.3)` −1.
  Kutu numarası hesaplarken aralık dışı negatif değerler bu yüzden yanlış
  kutuya girebilir; önce aralığı denetle.
- `np.cov` varsayılan olarak `n − 1`'e böler, `np.var` `n`'e.
- Korelasyonu nedensellik sanmak; korelasyon 0 diye ilişkiyi yok saymak.
