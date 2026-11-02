## Formüller

| Tahmin | Standart hata | Gereken örneklem |
|---|---|---|
| Ortalama $\bar{x}$ | $\dfrac{s}{\sqrt{n}}$ | $n = \left(\dfrac{s}{SE}\right)^2$ |
| Oran $\hat{p}$ | $\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n}}$ | $n = \dfrac{\hat{p}(1-\hat{p})}{SE^2}$ |

## Kodda

```python
import numpy as np
from scipy import stats

x = np.array([4.1, 5.0, 5.6, 6.2, 6.9, 7.4, 8.0, 9.3, 11.2, 12.5])
print(round(x.std(ddof=1) / np.sqrt(len(x)), 4))
print(round(float(stats.sem(x)), 4))
```

```text
0.8532
0.8532
```

- `scipy.stats.sem` ortalamanın standart hatasını verir; varsayılan olarak
  `ddof=1` kullanır.
- Elle hesaplarken NumPy'de `ddof=1` yazmayı unutma.

## Okuma kuralı

- Standart hata **ortalamanın** ne kadar oynadığıdır; tek tek değerlerin
  yayılımı standart sapmadır.
- Raporda "ortalama ± standart hata" yazıyorsan hangisi olduğunu belirt;
  "± sapma" ile karıştırılır.
- Kabaca: gerçek ortalama çoğu zaman tahminin 2 standart hata yakınındadır.
  Bunun tam hâli bir sonraki bölümdeki güven aralığı.

## Karekök kuralı

| Örneklem | Standart hata |
|---|---|
| $n$ | $SE$ |
| $4n$ | $SE / 2$ |
| $16n$ | $SE / 4$ |
| $100n$ | $SE / 10$ |
