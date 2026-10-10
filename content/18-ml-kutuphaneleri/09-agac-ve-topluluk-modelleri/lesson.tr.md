# Ağaç ve Topluluk Modelleri

Karar ağacının nasıl bölündüğünü, rastgele ormanı, torba dışı (OOB)
doğrulamayı ve boosting fikrini Makine Öğrenmesi patikasında ve ML
Algoritmaları modülünde gördün. Bu bölüm scikit-learn'de ağaçlarla
çalışırken işe yarayan araçlara bakıyor: ağacı **budamak**, eksik değerle
doğrudan eğitmek, `feature_importances_`'ın neden yanıltabildiği ve birkaç
modeli birleştiren `VotingClassifier` / `StackingClassifier`.

## Budama: ccp_alpha

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
full = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
print(full.get_n_leaves(), full.get_depth(), round(full.score(X_test, y_test), 3))
path = full.cost_complexity_pruning_path(X_train, y_train)
print(len(path.ccp_alphas))
search = GridSearchCV(DecisionTreeClassifier(random_state=0),
                      {"ccp_alpha": path.ccp_alphas}, cv=5).fit(X_train, y_train)
pruned = search.best_estimator_
print(round(search.best_params_["ccp_alpha"], 4), pruned.get_n_leaves(),
      pruned.get_depth(), round(pruned.score(X_test, y_test), 3))
print(export_text(pruned, max_depth=1))
```

```text
48 12 0.84
29
0.0062 12 5 0.9
|--- feature_2 <= 0.20
|   |--- feature_3 <= 0.81
|   |   |--- truncated branch of depth 3
|   |--- feature_3 >  0.81
|   |   |--- truncated branch of depth 4
|--- feature_2 >  0.20
|   |--- feature_6 <= 0.95
|   |   |--- truncated branch of depth 2
|   |--- feature_6 >  0.95
|   |   |--- truncated branch of depth 2
```

- Sınırsız ağaç 48 yaprak, 12 derinlik; etiketlerin %10'u gürültü
  (`flip_y=0.1`) ve ağaç onları da ezberliyor. Test 0,84.
- **Budama** önce büyütüp sonra kesmek: `ccp_alpha` her yaprağa bir bedel
  koyar, bedelinden az iş gören dallar kesilir. `cost_complexity_pruning_path`
  ağacın anlamlı budama noktalarını verir (29 tane); hangisinin iyi
  olduğunu çapraz doğrulama seçer.
- Seçilen ağaç 12 yaprak, 5 derinlik; test 0,9. Hem daha iyi hem
  okunabilir. `export_text` ağacı metin olarak yazar; `max_depth=1` ilk iki
  kat, gerisi "truncated branch".

## Önceden durdurmak: min_samples_leaf

```python
from sklearn.model_selection import cross_val_score

for leaf in [1, 5, 20, 50]:
    model = DecisionTreeClassifier(min_samples_leaf=leaf, random_state=0)
    score = cross_val_score(model, X_train, y_train, cv=5).mean()
    print(leaf, model.fit(X_train, y_train).get_n_leaves(), round(score, 3))
```

```text
1 48 0.82
5 30 0.862
20 14 0.842
50 7 0.798
```

- Budamanın tersi: ağaç büyürken durdurulur. `min_samples_leaf=5` her
  yaprakta en az 5 satır ister; 48 yaprak 30'a iner, doğruluk 0,82'den
  0,862'ye çıkar.
- Çok büyük değer (50) ağacı fazla basitleştirir: 7 yaprak, 0,798.
- Benzer düğmeler: `max_depth`, `max_leaf_nodes`, `min_samples_split`.
  Hepsi aynı soruyu sorar: ağaç ne kadar ayrıntıya inebilir?

## Eksik değerle doğrudan

```python
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

X_nan = X_train.copy()
rng = np.random.default_rng(0)
X_nan[rng.random(X_nan.shape) < 0.1] = np.nan    # hücrelerin %10'u boş
print(int(np.isnan(X_nan).sum()))
for model in [DecisionTreeClassifier(random_state=0),
              RandomForestClassifier(random_state=0),
              GradientBoostingClassifier(random_state=0)]:
    try:
        model.fit(X_nan, y_train)
        print(type(model).__name__, round(model.score(X_test, y_test), 3))
    except ValueError as err:
        print(type(model).__name__, str(err).splitlines()[0])
```

```text
470
DecisionTreeClassifier 0.82
RandomForestClassifier 0.9
GradientBoostingClassifier Input X contains NaN.
```

- `DecisionTreeClassifier` ve `RandomForestClassifier` `NaN`'ı doğrudan
  kabul ediyor: her bölünmede eksik değerlerin hangi tarafa gideceğini de
  öğreniyorlar. Doldurma (imputer) adımı gerekmiyor.
- Eski `GradientBoostingClassifier` kabul etmiyor. Boosting'de eksik değeri
  doğrudan alan sınıf `HistGradientBoostingClassifier`; o Gradyan Boosting
  Kütüphaneleri bölümünde.
- Eksiklik bir bilgi taşıyorsa (form boş bırakılmış) bunu öğrenmek
  doldurmaktan iyi olabilir; tek tek ölçülür.

## feature_importances_ yanıltabilir

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer(as_frame=True)
X = data.data.iloc[:, :5].copy()
y = data.target
rng = np.random.default_rng(0)
X["row_id"] = rng.permutation(len(X))    # anlamsız, 569 farklı değer
X["coin"] = rng.integers(0, 2, len(X))   # anlamsız, 2 farklı değer
rf = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
for name, value in zip(X.columns, rf.feature_importances_):
    print(f"{name:16} {value:.3f}")
```

```text
mean radius      0.209
mean texture     0.115
mean perimeter   0.280
mean area        0.256
mean smoothness  0.102
row_id           0.031
coin             0.006
```

- `feature_importances_` her sütunun ağaçlarda sağladığı **saflık
  artışının** toplamı. Hızlı ve bedava, ama bir yanlılığı var.
- `row_id` ve `coin` ikisi de tamamen rastgele; hedefle ilgileri yok. Yine
  de `row_id` 0,031 aldı, `coin`'in beş katı. Çok farklı değeri olan sütunda
  ağaç her zaman "işe yarıyor gibi" görünen bir kesim noktası bulur; eğitim
  verisindeki gürültüye uyar.
- Bu önemler **eğitim verisinden** hesaplanır. Görülmemiş veride gerçekten
  işe yarayıp yaramadığını permütasyon önemi ölçer (Modeli Açıklamak
  bölümü).

## Modelleri birleştirmek

```python
from sklearn.ensemble import (RandomForestClassifier, StackingClassifier,
                              VotingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

base = [("lr", make_pipeline(StandardScaler(), LogisticRegression())),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(15))),
        ("rf", RandomForestClassifier(n_estimators=200, random_state=0))]
vote = VotingClassifier(base, voting="soft")
stack = StackingClassifier(base, final_estimator=LogisticRegression())
for name, model in base + [("vote", vote), ("stack", stack)]:
    print(name, round(cross_val_score(model, X_train, y_train, cv=5).mean(), 3))
```

```text
lr 0.896
knn 0.898
rf 0.911
vote 0.907
stack 0.904
```

- `VotingClassifier(voting="soft")` modellerin olasılıklarının
  ortalamasını alır. `StackingClassifier` her modelin (çapraz doğrulamayla
  üretilmiş) tahminini yeni sütun yapıp üstüne bir model daha eğitir.
- Bu veride ikisi de rastgele ormanı **geçemedi** (0,907 ve 0,904,
  orman tek başına 0,911). Birleştirme, modeller **farklı** hatalar
  yaptığında kazandırır; en iyi model zaten güçlüyse zayıflar onu aşağı
  çekebilir.
- Bedeli: üç modelin eğitimi, stacking'de bir de iç çapraz doğrulama. Her
  zaman tek en iyi modelle karşılaştırılır.

## Özet

- Ağacı sınırla: `ccp_alpha` (budama, çapraz doğrulamayla) ya da
  `min_samples_leaf` / `max_depth`.
- Ağaçlar ve rastgele orman `NaN` kabul eder; eski gradyan boosting etmez.
- `feature_importances_` çok değerli sütunları kayırır ve eğitim verisinden
  gelir; karar vermeden önce permütasyon önemine bak.
- Voting / stacking ancak farklı hatalar yapan modellerde kazandırır.
