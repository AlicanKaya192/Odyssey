| Ölçü | İngilizcesi | pandas | NumPy | Aykırıya |
|---|---|---|---|---|
| Ortalama | mean | `x.mean()` | `np.mean(x)` | duyarlı |
| Medyan | median | `x.median()` | `np.median(x)` | dayanıklı |
| Tepe değer | mode | `x.mode()[0]` | — | — |
| Varyans | variance | `x.var()` | `np.var(x, ddof=1)` | duyarlı |
| Standart sapma | standard deviation | `x.std()` | `np.std(x, ddof=1)` | duyarlı |
| Yüzdelik | percentile | `x.quantile(0.95)` | `np.percentile(x, 95)` | dayanıklı |
| IQR | interquartile range | `x.quantile(0.75) - x.quantile(0.25)` | `scipy.stats.iqr(x)` | dayanıklı |
| Hepsi birden | — | `x.describe()` | `scipy.stats.describe(x)` | — |

## ddof tuzağı

- pandas `var()` ve `std()`: varsayılan `ddof=1` ($n-1$'e böler).
- NumPy `var()` ve `std()`: varsayılan `ddof=0` ($n$'e böler).
- Örneklemden evrenin sapmasını tahmin ediyorsan `ddof=1`.

## Formüller

$$\bar{x} = \dfrac{1}{n}\sum_{i=1}^{n} x_i \qquad s^2 = \dfrac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 \qquad z = \dfrac{x - \bar{x}}{s}$$

## Aykırı değer kuralları

- Çan biçimli veride: $\lvert z \rvert > 3$.
- Çarpık veride: $Q_3 + 1{,}5 \cdot IQR$'nin üstü ya da $Q_1 - 1{,}5 \cdot IQR$'nin altı.
- Aykırıyı silmeden önce nedenine bak; ne yaptığını raporda yaz.
