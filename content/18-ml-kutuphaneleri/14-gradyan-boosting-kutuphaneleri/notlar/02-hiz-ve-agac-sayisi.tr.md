Boosting'in iki ana ayarı birbirine bağlıdır: **öğrenme hızı** her ağacın
düzeltmesinin ne kadarının alındığı, **ağaç sayısı** kaç düzeltme
yapıldığı. Küçük adımlar daha çok adım ister.

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=20000, n_features=20, n_informative=8,
                           flip_y=0.05, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
for rate, trees in [(0.3, 100), (0.1, 100), (0.03, 100), (0.03, 600)]:
    model = HistGradientBoostingClassifier(learning_rate=rate, max_iter=trees,
                                           early_stopping=False, random_state=0)
    print(rate, trees, round(model.fit(X_train, y_train).score(X_test, y_test), 3))
```

```text
0.3 100 0.954
0.1 100 0.955
0.03 100 0.948
0.03 600 0.957
```

## Ne görüyoruz

- 100 ağaçla 0,3 ve 0,1 hemen hemen aynı (0,954, 0,955). 0,03 ise 100
  ağaçta yetişemiyor: 0,948, model henüz yolun başında.
- Aynı küçük hız 600 ağaçla en iyi sonucu verdi: 0,957. Küçük adımlar,
  yeterince adım atılırsa genellikle biraz daha iyi bir yere varır.
- Bedeli süre: 600 ağaç, 100 ağacın 6 katı iş.

## Kural

- Hızı küçültünce ağaç sayısını büyüt; ikisini ayrı ayrı aramak yerine
  hızı sabitle (0,05–0,1) ve ağaç sayısını erken durdurmaya bırak.
- Fark küçük (0,955 ile 0,957); önce veri ve özelliklerle uğraşmak çoğu
  zaman daha çok kazandırır.
