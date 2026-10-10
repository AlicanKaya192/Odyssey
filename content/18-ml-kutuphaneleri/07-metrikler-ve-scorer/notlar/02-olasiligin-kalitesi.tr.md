AUC olasılıkların **sırasına** bakar, değerlerine bakmaz. "%30 risk"
diyen bir modelin gerçekten 100 vakadan 30'unda haklı çıkıp çıkmadığını
**Brier skoru** ölçer: olasılık ile gerçek sonuç (0 ya da 1) arasındaki
farkın karesinin ortalaması. Küçük daha iyi.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=2000, n_features=8, n_informative=4,
                           weights=[0.95], flip_y=0.02, random_state=7)
print(round(y.mean() * (1 - y.mean()), 4))
for model in [LogisticRegression(), DecisionTreeClassifier(random_state=0)]:
    auc = cross_val_score(model, X, y, cv=5, scoring="roc_auc").mean()
    brier = -cross_val_score(model, X, y, cv=5, scoring="neg_brier_score").mean()
    print(type(model).__name__, round(auc, 3), round(brier, 4))
brier_scorer = make_scorer(brier_score_loss, greater_is_better=False,
                           response_method="predict_proba")
scores = cross_val_score(LogisticRegression(), X, y, cv=5, scoring=brier_scorer)
print(round(-scores.mean(), 4))
```

```text
0.0564
LogisticRegression 0.849 0.0376
DecisionTreeClassifier 0.747 0.0585
0.0376
```

## Ne görüyoruz

- İlk satır taban çizgi: herkese aynı olasılığı (pozitif oranı) veren model
  0,0564 alır.
- Lojistik regresyon 0,0376: olasılıkları anlamlı.
- Derinliği sınırsız ağaç her yaprakta 0 ya da 1 olasılık veriyor; Brier
  0,0585, yani **taban çizgiden kötü**. Yanıldığında tam güvenle yanılıyor.
  AUC'si de düşük (0,747).
- Kendi scorer'ında olasılık gerekiyorsa `response_method="predict_proba"`:
  `brier_scorer` hazır `"neg_brier_score"` ile aynı sayıyı verdi.

## Ne zaman önemli

- Olasılık bir karara doğrudan giriyorsa (risk, fiyat, beklenen maliyet).
- Eşik seçilecekse: eşik olasılığın üstünde kurulur, olasılık kötüyse eşik de
  kötü olur.
