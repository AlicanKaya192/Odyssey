Gerçek veride sık görülen bir durum: iki sütun neredeyse aynı bilgiyi
taşır (metrekare ve brüt metrekare, Celsius ve Fahrenheit, toplam ve
ortalama). Üç seçim yöntemi bu durumda **üç farklı** şey yapar.

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(9)
signal = rng.normal(size=400)
other = rng.normal(size=400)
X = np.column_stack([signal, signal + rng.normal(0, 0.05, 400), other,
                     rng.normal(size=(400, 3))])
y = (signal + 0.5 * other + rng.normal(0, 0.5, 400) > 0).astype(int)
print(round(float(np.corrcoef(X[:, 0], X[:, 1])[0, 1]), 3))
print(SelectKBest(f_classif, k=2).fit(X, y).get_support(indices=True).tolist())
l1 = LogisticRegression(penalty="l1", C=0.05, solver="liblinear").fit(X, y)
print(l1.coef_.round(2).tolist()[0])
forest = RandomForestClassifier(n_estimators=200, random_state=9).fit(X, y)
print(forest.feature_importances_.round(2).tolist())
```

```text
0.999
[0, 1]
[0.0, 1.73, 0.63, 0.0, 0.0, 0.0]
[0.31, 0.32, 0.16, 0.08, 0.06, 0.07]
```

## Üç yöntem, üç davranış

- Sütun 0 ve 1 birbirinin kopyası (korelasyon 0,999). Sütun 2 de hedefle
  ilgili ama daha zayıf; 3–5 gürültü.
- **Filtre** (`SelectKBest`, k=2) iki kopyayı birden seçti: her biri tek
  başına güçlü görünüyor. Gerçekten yeni bilgi taşıyan sütun 2 dışarıda
  kaldı.
- **L1** kopyalardan birini sıfırladı (sütun 0'a 0, sütun 1'e 1,73) ve sütun
  2'yi tuttu: aynı bilgiyi iki kez ödemiyor. Hangi kopyanın seçildiği
  rastlantıya bağlı olabilir.
- **Orman** önemi kopyalar arasında **bölüştürdü** (0,31 ve 0,32). Tek başına
  bakan biri "ikisi de orta düzeyde önemli" diye düşünür; aslında aynı
  özelliğin yarısı.

## Ne yapmalı?

- Seçmeden önce yüksek korelasyonlu çiftlere bak (`df.corr()`, ısı haritası);
  anlamı aynıysa birini elle at.
- Önem puanlarını yorumlarken kopyaları birlikte düşün: bir grup olarak
  önemlidirler (Modeli Açıklamak bölümü).
- L1'in hangi kopyayı seçtiğine anlam yükleme; iki kopyanın yeri değişse
  sonuç da değişebilir.
