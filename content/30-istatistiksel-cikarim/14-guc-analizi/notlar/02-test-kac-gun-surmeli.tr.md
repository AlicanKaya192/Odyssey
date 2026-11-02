Güç analizi grup başına kişi sayısını verir. Asıl soru çoğu zaman
"bu test kaç gün sürecek?" sorusudur.

## Kişiden güne

Toplam kişi (iki grup) günlük ziyaretçiye bölünür:

```python
import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def days_needed(p_a, p_b, daily_visitors):
    h = proportion_effectsize(p_b, p_a)
    n = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
    return int(np.ceil(2 * np.ceil(n) / daily_visitors))


print(days_needed(0.114, 0.130, 1500))
print(days_needed(0.114, 0.122, 1500))
```

```text
9
35
```

Yarı büyüklükteki bir farkı (%11,4'ten %12,2'ye) yakalamak yaklaşık dört kat
uzun sürüyor. Süre kabul edilemezse üç yol var: daha büyük bir etkiyi
hedeflemek, daha çok trafik ayırmak ya da daha az gürültülü bir metrik
seçmek.

## Süreyi belirlerken

- **En az bir tam hafta.** Kullanıcılar hafta içi ve hafta sonu farklı
  davranır; üç günlük test haftanın bir kısmını temsil eder.
- **Süre önceden yazılır.** "Anlamlı çıkınca durdururuz" yaklaşımı yanlış
  alarm oranını şişirir; bunu deney tasarımı modülünde göreceğiz.
- **Taban oranı geçmiş veriden alınır**, tahminle değil. Yanlış taban oranı
  bütün hesabı kaydırır.
- **Trafiğin hepsi teste girmeyebilir.** Yalnızca ödeme sayfasına gelenler
  sayılıyorsa günlük ziyaretçi o sayfanınkidir.
