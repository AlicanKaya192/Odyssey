Karıştırarak bölünce skor `random_state`'e bağlı olur. Aynı model, aynı
veri, yalnızca tohum değişince:

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (RepeatedStratifiedKFold, StratifiedKFold,
                                     cross_val_score)

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
model = LogisticRegression()
for seed in range(3):
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    print(seed, round(cross_val_score(model, X, y, cv=cv).mean(), 3))
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=0)
scores = cross_val_score(model, X, y, cv=cv)
print(len(scores), round(scores.mean(), 3), round(scores.std(), 3))
```

```text
0 0.825
1 0.817
2 0.827
50 0.825 0.027
```

## Ne görüyoruz

- Üç tohumda ortalama 0,817 ile 0,827 arasında oynuyor. İki model arasında
  0,01'lik fark görürsen bu oynamadan büyük olup olmadığına bak.
- `RepeatedStratifiedKFold` 5 katlı bölmeyi 10 kez, her seferinde başka
  karıştırmayla yapıyor: 50 skor. Ortalama 0,825, katlar arası sapma 0,027.
- Tekrar etmek modeli iyileştirmez; yalnızca ortalamayı tek bir şanslı ya da
  şanssız bölmeden kurtarır. Bedeli 10 kat eğitim.

## Ne zaman

- Veri küçükse (birkaç yüz satır) ve modeller birbirine yakınsa.
- Raporda tek sayı yerine "ortalama ± sapma" yazılacaksa.
- Veri büyükse tek bir 5 katlı bölme çoğu zaman yeter.
