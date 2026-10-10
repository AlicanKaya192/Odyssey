Rastgele ormanın gücü ağaçların **birbirinden farklı** olmasından gelir.
Farkı iki ayar belirler: her bölünmede kaç sütuna bakıldığı
(`max_features`) ve kesim noktasının aranıp aranmadığı (ExtraTrees'te
rastgele seçilir). Torba dışı skorla, ayrı bir doğrulama kurmadan
karşılaştırılabilir:

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
for features in ["sqrt", 0.5, None]:
    rf = RandomForestClassifier(n_estimators=200, max_features=features,
                                oob_score=True, random_state=0)
    print(features, round(rf.fit(X_train, y_train).oob_score_, 3))
extra = ExtraTreesClassifier(n_estimators=300, bootstrap=True, oob_score=True,
                             random_state=0).fit(X_train, y_train)
print(round(extra.oob_score_, 3), round(extra.score(X_test, y_test), 3))
```

```text
sqrt 0.916
0.5 0.904
None 0.907
0.918 0.893
```

## Ne görüyoruz

- `max_features="sqrt"` (10 sütunda 3) en iyisi. `None` her bölünmede bütün
  sütunlara bakıyor; ağaçlar birbirine benziyor ve oylamanın kazancı
  azalıyor. Bu, torbalamanın (bagging) kendisi.
- ExtraTrees kesim noktalarını da rastgele seçiyor: torba dışı skoru
  ormanınkine yakın (0,918), test skoru biraz düşük (0,893). Bu veride
  ormandan iyi değil; hangisinin iyi olduğu veriye göre değişir.
- ExtraTrees varsayılan olarak önyükleme yapmaz; torba dışı skor için
  `bootstrap=True` gerekir.

## Ne zaman

- Orman ile ExtraTrees aynı doğrulamada karşılaştırılır; biri her zaman
  kazanmaz.
- `max_features` ormanın en etkili ayarlarından biri; aramaya `"sqrt"`,
  `"log2"` ve 0,3–0,7 arası oranlar konur.
