Gerçek sorularda çözüm her değeri alamaz: oranlar 0 ile 1 arasında kalır,
paylar toplamı 1 olur, bütçe aşılamaz. `minimize` bunları iki yolla alır:
**sınırlar** (`bounds`, her değişkene ayrı alt-üst sınır) ve **kısıtlar**
(`constraints`, değişkenler arasındaki eşitlik ya da eşitsizlik).

Örnek: üç yatırım arasında parayı bölüştürüp riski (varyansı) en küçük yapmak.

```python
import numpy as np
from scipy import optimize

cov = np.array([[0.04, 0.006, 0.002],
                [0.006, 0.09, 0.01],
                [0.002, 0.01, 0.0225]])


def risk(w):
    return float(w @ cov @ w)


sum_to_one = {"type": "eq", "fun": lambda w: w.sum() - 1}
res = optimize.minimize(risk, x0=np.full(3, 1 / 3), bounds=[(0, 1)] * 3,
                        constraints=[sum_to_one])
print(res.success, res.x.round(3).tolist(), round(float(res.x.sum()), 6))
print(round(risk(np.full(3, 1 / 3)), 5), round(res.fun, 5))
free = optimize.minimize(risk, x0=np.full(3, 1 / 3))
print(float(np.abs(free.x).max()) < 1e-4)
```

```text
True [0.329, 0.076, 0.595] 1.0
0.02094 0.0148
True
```

## Ne oldu?

- `bounds=[(0, 1)] * 3`: her pay 0 ile 1 arasında (açığa satış yok).
- `{"type": "eq", "fun": ...}`: `fun` **sıfır** olmalı, yani paylar toplamı
  1. Eşitsizlik için `"type": "ineq"`: `fun` **sıfır ya da büyük** olmalı.
- Sonuç: en az riskli üçüncü yatırıma %59,5, en riskli ikinciye %7,6.
  Eşit bölüşüme (0,02094) göre risk 0,0148'e indi.
- Kısıt kaldırılınca çözücü "hiç yatırma" cevabını buldu: bütün paylar 0,
  risk 0. Matematiksel olarak doğru, anlamsız. **Kısıtı unutmak** en
  iyilemede en sık hatadır: çözücü sorulanı değil, yazılanı çözer.

## Yöntem

Kısıt verilince `minimize` kendiliğinden kısıtları bilen bir yönteme
(SLSQP) geçer. Kısıt ve sınırlar ne kadar açık yazılırsa çözüm o kadar
güvenilir; sonucun kısıtları gerçekten sağladığını (`res.x.sum()`) yine de
kontrol et.
