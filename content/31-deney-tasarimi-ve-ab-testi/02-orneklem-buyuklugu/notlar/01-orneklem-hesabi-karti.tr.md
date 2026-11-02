## Dört adım

1. Birincil metriğin geçmiş verideki ortalaması ve sapması.
2. En küçük anlamlı etki: göreli (%5) ya da mutlak (0,5 puan).
3. Grup başına n: `TTestIndPower().solve_power(effect_size=d, power=0.8,
   alpha=0.05)`; oranlarda `NormalIndPower` + `proportion_effectsize`.
4. Süre: $2n$ / (günlük kullanıcı × deneye giren pay), tam haftaya yukarı.

## Hızlı tahmin

```python
import math


def rule_of_16(sd, delta):
    return math.ceil(16 * sd**2 / delta**2)


print(rule_of_16(0.32, 0.006))
print(rule_of_16(0.32, 0.012))
```

```text
45512
11378
```

Fark iki katına çıkınca kişi dörtte birine iner.

## Kontrol listesi

- Sayılan birim kullanıcı mı? Ziyaret sayısıyla hesap yapılmaz.
- Taban oranı ve sapma **geçmiş veriden** mi?
- MDE, ekibin umduğu etkiden küçük mü?
- Eşit olmayan bölmede `ratio` hesaba girdi mi?
- Süre en az bir tam hafta mı?
- Aynı trafikte başka deney var mı?
