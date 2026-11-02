## Teorem tek satırda

Bağımsız seçilmiş $n$ değerin ortalaması, $n$ büyüdükçe yaklaşık normal
dağılır:

$$\bar{X} \approx N\!\left(\mu,\ \dfrac{\sigma}{\sqrt{n}}\right)$$

## Standart hatalar

| Ne | Standart hata |
|---|---|
| Ortalama | $\dfrac{\sigma}{\sqrt{n}}$ |
| Oran | $\sqrt{\dfrac{p(1-p)}{n}}$ |

## Söylediği ve söylemediği

| Söyler | Söylemez |
|---|---|
| Ortalamaların dağılımı çana yaklaşır | Verinin kendisi normal olur |
| Ortalamaların merkezi $\mu$ | Tek bir örneklemin ortalaması $\mu$'ye eşit |
| Genişlik $\sqrt{n}$ ile daralır | Belirli bir $n$ her veride yeter |

## Ne zaman çabuk, ne zaman yavaş?

- Simetrik veride birkaç on kişi yeter.
- Orta çarpık veride (oturum süresi) onlarca kişide çan belirgin.
- Çok çarpık veride (harcama: çoğu sıfır, birkaç çok büyük) binlerce kişi
  gerekebilir.
- Kontrol: benzetimle örneklem ortalamalarını çiz, iki kuyruğa ayrı bak.

## Kod kalıbı

```python
import numpy as np

rng = np.random.default_rng(0)
values = rng.exponential(scale=10, size=50_000)
means = rng.choice(values, size=(5000, 40)).mean(axis=1)
se_formula = values.std() / np.sqrt(40)
print(round(means.std(), 3), round(se_formula, 3))
```

```text
1.577 1.589
```

İki sayı aynı şeyi ölçüyor: biri benzetimden, biri formülden.
