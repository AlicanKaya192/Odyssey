## math

| Fonksiyon | Ne yapar | Örnek |
|---|---|---|
| `isclose(a, b)` | ondalıkları toleransla karşılaştırır | `isclose(0.1 + 0.2, 0.3)` → `True` |
| `fsum(xs)` | hatasız ondalık toplam | `fsum([0.1] * 10)` → `1.0` |
| `floor`, `ceil`, `trunc` | aşağı, yukarı, sıfıra doğru | `floor(-2.5)` → `-3` |
| `prod(xs)` | çarpım | `prod([1, 2, 3, 4])` → `24` |
| `factorial(n)` | n! | `factorial(5)` → `120` |
| `comb(n, k)`, `perm(n, k)` | seçim, sıralı diziliş | `comb(10, 3)` → `120` |
| `gcd`, `lcm` | ortak bölen, ortak kat | `gcd(24, 36)` → `12` |
| `isqrt(n)` | tam sayı karekökü | `isqrt(17)` → `4` |
| `log(x, b)`, `log2`, `log10`, `exp` | logaritma ve üs | `log2(1024)` → `10.0` |
| `hypot`, `dist` | hipotenüs, uzaklık | `dist((0, 0), (3, 4))` → `5.0` |
| `pi`, `e`, `inf`, `nan`, `isnan` | sabitler | `nan == nan` → `False` |

## statistics

| Fonksiyon | Ne yapar |
|---|---|
| `mean`, `fmean` | ortalama (`fmean` her zaman float ve daha hızlı) |
| `median`, `median_low`, `median_high` | medyan; çift sayıda değerde alt/üst ortanca |
| `mode`, `multimode` | en sık değer(ler) |
| `stdev`, `variance` | örneklem (`n − 1`) |
| `pstdev`, `pvariance` | kitle (`n`) |
| `quantiles(xs, n=4)` | kesim noktaları (çeyrekler) |
| `correlation(x, y)` | Pearson korelasyonu |
| `linear_regression(x, y)` | eğim ve kesişim |
| `NormalDist(mu, sigma)` | `cdf`, `inv_cdf`, `pdf`, `mean`, `stdev` |

## Ne zaman NumPy?

`statistics` saf Python'dur: birkaç bin değere kadar rahat, milyonlarca
değerde yavaş. Büyük dizilerde ve tablolarda NumPy ve pandas kullanılır
(Veri Bilimi Kütüphaneleri modülü).
