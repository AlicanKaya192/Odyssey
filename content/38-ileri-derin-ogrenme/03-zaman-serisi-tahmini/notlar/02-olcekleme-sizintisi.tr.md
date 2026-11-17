Derste ölçeklemenin ortalamasını yalnızca ilk 630 günden aldık. Eğilimli bir
seride bunun neden önemli olduğunu sayılarla görelim.

```python
import numpy as np
from dl_data import make_series

series = make_series(730)
split = 630
print(round(float(series[:split].mean())))
print(round(float(series.mean())))
print(round(float(series[split:].mean())))
```

```text
58
57
54
```

- Eğitim döneminin ortalaması 58, bütün serininki
  57, test döneminin 54: yıllık mevsim test
  döneminde seriyi aşağı çekiyor. Bütün seriden ölçekleseydik, model
  eğitim sırasında test döneminin seviyesini dolaylı olarak "bilirdi".
- Gerçek kullanımda gelecek elde olmaz; ölçüm de öyle yapılmalı. Kural
  tablo verisindekinin aynısı: **her istatistik yalnızca eğitimden**.

## Eğilimle başa çıkmak

Ölçeklenmiş seri yükselmeye devam ettiği için test dönemi eğitimin hiç
görmediği değerlere çıkabilir. Ağlar gördükleri aralığın dışında kötü
tahmin eder. İki yaygın çare:

| Çare | Nasıl | Geri dönüş |
|---|---|---|
| Fark almak | Hedef `y[t] - y[t-1]`: değişimi tahmin et | Tahmini son gerçek değere ekle |
| Pencere başına ölçek | Her pencereyi kendi ortalamasıyla merkezle | Tahmine o ortalamayı geri ekle |

İkisi de Zaman Serileri patikasındaki durağanlık fikrinin derin öğrenmedeki
karşılığı: modele seviyeyi değil, deseni öğret.
