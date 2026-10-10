p değeri iki şeyin karışımıdır: farkın **büyüklüğü** ve örneklemin
**büyüklüğü**. Örneklem yeterince büyükse önemsiz bir fark bile "çok
anlamlı" çıkar; küçükse önemli bir fark kaçar. Bu yüzden p'nin yanına her zaman
farkın kendi büyüklüğü yazılır.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(12)
a = rng.normal(100.0, 10, 200_000)
b = rng.normal(100.3, 10, 200_000)
res = stats.ttest_ind(b, a)
d = (b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
print(f"{res.pvalue:.1e}", round(float(b.mean() - a.mean()), 2), round(float(d), 3))
small_a = a[:20]
small_b = b[:20] + 5
res2 = stats.ttest_ind(small_b, small_a)
pooled = np.sqrt((small_a.var(ddof=1) + small_b.var(ddof=1)) / 2)
d2 = (small_b.mean() - small_a.mean()) / pooled
print(round(float(res2.pvalue), 3), round(float(d2), 2))
```

```text
7.9e-19 0.28 0.028
0.339 0.31
```

## İki uç

- **Dev örneklem, küçücük fark.** 200 000'er kişi, fark 0,28 puan (100
  üzerinden). p = 7,9e-19: istatistiksel olarak "kesin". Ama etki büyüklüğü
  d = 0,028; iki grup neredeyse tamamen üst üste. Bu farkın pratikte bir
  anlamı yok.
- **Küçük örneklem, gerçek fark.** 20'şer kişi, ikinci gruba 5 puan eklendi.
  p = 0,339: "anlamlı değil". Oysa d = 0,31, küçük-orta bir etki; sadece
  bu kadar az kişiyle görünmüyor.

## Etki büyüklüğü (Cohen's d)

`d = (ortalamaların farkı) / (ortak standart sapma)`: fark kaç **sapma**
büyüklüğünde? Kaba bir okuma: 0,2 küçük, 0,5 orta, 0,8 büyük. Birimden
bağımsızdır; farklı ölçüleri karşılaştırmayı sağlar.

## Raporda ne yazılır?

1. Farkın kendisi ve birimi ("ortalama 4,3 puan yüksek").
2. Güven aralığı ("%95 GA: −0,01 ile 8,66").
3. Etki büyüklüğü (d).
4. p değeri: en sonda, tek başına değil.

"p < 0,05" yazıp bırakmak, okuyana farkın ne kadar olduğunu ve ne kadar emin
olunduğunu söylemez.
