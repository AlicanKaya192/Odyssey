Kesikli dağılımda `cdf(k)` "$k$ dahil ve altı", `sf(k)` "$k$ **hariç**
üstü" demek. Cümledeki kelime hangi çağrıyı yazacağını belirler:

| Cümle | Matematik | scipy |
|---|---|---|
| en fazla 3 | $X \le 3$ | `cdf(3)` |
| 3'ten az | $X \le 2$ | `cdf(2)` |
| en az 3 | $X \ge 3$ | `sf(2)` |
| 3'ten fazla | $X \ge 4$ | `sf(3)` |
| tam 3 | $X = 3$ | `pmf(3)` |
| 2 ile 5 arası (ikisi dahil) | $2 \le X \le 5$ | `cdf(5) - cdf(1)` |

## Ölçerek doğrula

```python
from scipy import stats

buyers = stats.binom(n=20, p=0.114)
print(round(float(buyers.sf(2)), 4))
print(round(float(1 - buyers.cdf(2)), 4))
print(round(float(sum(buyers.pmf(k) for k in range(3, 21))), 4))
```

```text
0.403
0.403
0.403
```

Üçü de aynı soruyu ("en az 3") soruyor: `sf(2)`, `1 - cdf(2)` ve 3'ten 20'ye
kadar tek tek olasılıkların toplamı.

## Sürekli dağılımda sınır fark etmez

Normal dağılımda $X < 1000$ ile $X \le 1000$ aynı olasılığı verir, çünkü tek
bir noktanın olasılığı sıfırdır. Tuzak yalnızca kesikli dağılımlarda (binom,
Poisson) var.

## Bir kontrol alışkanlığı

Şüphedeysen sınırdaki değeri ayrıca hesapla: `pmf(k)` küçük değilse, onu dahil
edip etmemen sonucu belirgin değiştirir.
