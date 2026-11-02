| Soru | Sınıf | Çağrı |
|---|---|---|
| İki ortalama, kaç kişi? | `TTestIndPower` | `solve_power(effect_size=d, power=0.8, alpha=0.05)` |
| İki oran, kaç kişi? | `NormalIndPower` | `solve_power(effect_size=h, power=0.8, alpha=0.05)` |
| Oranları h'ye çevir | — | `proportion_effectsize(p_b, p_a)` |
| Bu n ile güç ne? | ikisi de | `power(effect_size=..., nobs1=n, alpha=0.05)` |
| Bu n ile MDE ne? | ikisi de | `solve_power(nobs1=n, power=0.8, alpha=0.05)` |

`nobs1` birinci grubun büyüklüğü; ikinci grup varsayılan olarak aynı
(`ratio=1`). Sonuç her zaman **yukarı** yuvarlanır.

## Güç, α ve tek yön

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

solver = TTestIndPower()
settings = [(0.05, 0.8, "two-sided"), (0.05, 0.9, "two-sided"),
            (0.01, 0.8, "two-sided"), (0.05, 0.8, "larger")]
for alpha, power, side in settings:
    n = solver.solve_power(effect_size=0.2, power=power, alpha=alpha,
                           alternative=side)
    print(alpha, power, side, int(np.ceil(n)))
```

```text
0.05 0.8 two-sided 394
0.05 0.9 two-sided 527
0.01 0.8 two-sided 586
0.05 0.8 larger 310
```

- Gücü 0,8'den 0,9'a çıkarmak ya da α'yı 0,01'e indirmek daha çok kişi
  ister.
- Tek yönlü test daha az kişi ister; ama yön testten **önce** seçilmelidir.

## Akılda kalacaklar

- n, etkinin karesiyle ters orantılı: etki yarıya inerse n dört katına
  çıkar.
- Etki büyüklüğü olarak "umduğun" değil, "kaçırmak istemediğin en küçük"
  etkiyi yaz.
- Hesap şüpheliyse benzetimle doğrula: aynı büyüklükte binlerce test,
  anlamlı çıkanların oranı.
