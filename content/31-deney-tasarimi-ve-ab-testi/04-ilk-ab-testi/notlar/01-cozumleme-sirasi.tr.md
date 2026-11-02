| Adım | Soru | Düşerse |
|---|---|---|
| 1. SRM | Grup büyüklükleri tasarıma uyuyor mu? | Dur, nedeni bul |
| 2. Denge | Önceki özellikler eşit mi? | Atamayı incele |
| 3. Süre | Plan kadar mı sürdü, tam haftalar mı? | Erken bakma uyarısı |
| 4. Birincil metrik | Fark, aralık, p | — |
| 5. İkincil metrikler | Neden böyle? | Yorumda dikkat |
| 6. Koruma metrikleri | Bir şey bozuldu mu? | Dur |
| 7. Karar | Plandaki kurala göre | — |

## Tek fonksiyonda birincil metrik

```python
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportions_ztest)


def primary(k_a, n_a, k_b, n_b):
    p = proportions_ztest([k_b, k_a], [n_b, n_a])[1]
    low, high = confint_proportions_2indep(k_b, n_b, k_a, n_a)
    return [round(k_b / n_b - k_a / n_a, 4), round(float(low), 4),
            round(float(high), 4), round(float(p), 4)]


print(primary(1766, 15041, 1940, 14959))
```

```text
[0.0123, 0.0048, 0.0197, 0.0012]
```

Sıra: fark, aralığın alt ve üst ucu, p.

## Karar tablosu

| Aralık | Karar |
|---|---|
| Alt uç pratik eşiğin üstünde | uygula |
| Sıfırın üstünde ama eşiğin altına iniyor | belirsiz: maliyete göre ya da daha çok veri |
| Sıfırı içine alıyor | kanıt yok |
| Tamamen sıfırın altında | geri al, nedeni incele |
