# Boosting

Bagging bağımsız ağaçları yan yana kurup oylatıyordu. **Boosting** ağaçları
**sırayla** kurar: her yeni model, öncekilerin hâlâ yaptığı hataya odaklanır.
Tek başına zayıf (sığ) modeller böylece güçlü bir modele dönüşür. Tablo
verisinde en başarılı yöntemlerin çoğu (XGBoost, LightGBM, CatBoost) bu
fikrin hızlandırılmış hâlleridir.

## Gradyan artırma: artıklara ağaç

Regresyonda fikir çok sade: önce herkese ortalamayı tahmin et. Sonra
**artıklara** (gerçek − tahmin) küçük bir ağaç uydur ve tahmine ağacın
çıktısının küçük bir kısmını (`lr`, öğrenme oranı) ekle. Tekrarla. Kare
hatada artık, kaybın gradyanının tersidir; adı buradan gelir.

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(12)
X = rng.uniform(0, 10, (200, 1))
y = np.sin(X[:, 0]) * 3 + 0.3 * X[:, 0] + rng.normal(0, 0.5, 200)
Xt = rng.uniform(0, 10, (1000, 1))
yt = np.sin(Xt[:, 0]) * 3 + 0.3 * Xt[:, 0] + rng.normal(0, 0.5, 1000)


def boost(X, y, n_trees, lr, depth=2):
    start = y.mean()
    pred = np.full(len(y), start)
    trees = []
    for _ in range(n_trees):
        resid = y - pred                                # şimdiye kadarki hata
        tree = DecisionTreeRegressor(max_depth=depth).fit(X, resid)
        # hatanın bir kısmını düzelt
        pred += lr * tree.predict(X)
        trees.append(tree)
    return start, trees


def boost_predict(model, X, lr):
    start, trees = model
    return start + lr * sum(t.predict(X) for t in trees)


def mse(a, b):
    return ((a - b) ** 2).mean()


for n in (1, 10, 50, 200):
    m = boost(X, y, n, 0.1)
    train = mse(y, boost_predict(m, X, 0.1))
    test = mse(yt, boost_predict(m, Xt, 0.1))
    print(n, round(train, 3), round(test, 3))
from sklearn.ensemble import GradientBoostingRegressor

m = boost(X, y, 100, 0.1)
ref = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=2,
                                random_state=0).fit(X, y)
print(np.allclose(boost_predict(m, Xt, 0.1), ref.predict(Xt)))
```

```text
1 3.985 3.914
10 1.379 1.252
50 0.217 0.321
200 0.095 0.342
True
```

Tek ağaçla test hatası 3,9; 50 ağaçla 0,32. Tahminlerimiz scikit-learn'ün
`GradientBoostingRegressor`'ı ile birebir aynı. Ama dikkat: 200 ağaçta eğitim
hatası düşmeye devam ederken (0,095) test hatası yeniden artıyor (0,342).
Bagging'den farklı olarak boosting'de **ağaç eklemek aşırı uyutabilir**; ağaç
sayısı çapraz doğrulamayla ya da erken durdurmayla seçilir.

## Öğrenme oranı: küçük adımlar

```python
for lr in (1.0, 0.1):
    m = boost(X, y, 300, lr, depth=3)
    train = mse(y, boost_predict(m, X, lr))
    test = mse(yt, boost_predict(m, Xt, lr))
    print(lr, round(train, 3), round(test, 3))
```

```text
1.0 0.0 0.534
0.1 0.021 0.425
```

`lr = 1` her ağacın tahminini tam ekliyor: eğitim hatası 0, test 0,534 (ezber).
`lr = 0,1` her seferinde yalnızca onda birini ekliyor: test 0,425. Küçük oran
ve daha çok ağaç, genellikle daha iyi genelleyen modeldir (**büzülme**,
shrinkage).

## AdaBoost: yanlışları ağırlaştır

Sınıflandırmada boosting'in ilk ünlü biçimi **AdaBoost**. Her turda tek
sorulu bir ağaç (karar kütüğü) örnek ağırlıklarıyla eğitilir; yanlış
sınıflanan örneklerin ağırlığı artırılır, böylece sonraki kütük onlara bakar.
Her kütüğün oyu, hatasına göre bir katsayıyla (`α`) ağırlıklandırılır.

```python
from sklearn.tree import DecisionTreeClassifier

Xc = rng.uniform(-3, 3, (300, 2))
yc = (Xc[:, 0] ** 2 + Xc[:, 1] ** 2 < 4).astype(int)   # daire içi: 1
Xct = rng.uniform(-3, 3, (1000, 2))
yct = (Xct[:, 0] ** 2 + Xct[:, 1] ** 2 < 4).astype(int)


def adaboost(X, y, rounds):
    s = np.where(y == 1, 1, -1)
    w = np.full(len(y), 1 / len(y))
    stumps, alphas = [], []
    for _ in range(rounds):
        stump = DecisionTreeClassifier(max_depth=1).fit(X, y, sample_weight=w)
        h = np.where(stump.predict(X) == 1, 1, -1)
        err = w[h != s].sum() / w.sum()
        alpha = np.log((1 - err) / err)                 # az hata, büyük oy
        # yanlışları ağırlaştır
        w = w * np.exp(alpha * (h != s))
        w /= w.sum()
        stumps.append(stump)
        alphas.append(alpha)
    return stumps, alphas


def ada_predict(model, X):
    stumps, alphas = model
    score = 0
    for stump, alpha in zip(stumps, alphas):
        score = score + alpha * np.where(stump.predict(X) == 1, 1, -1)
    return (score > 0).astype(int)


from sklearn.ensemble import AdaBoostClassifier

model = adaboost(Xc, yc, 50)
ref = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=50)
ref.fit(Xc, yc)
ours = ada_predict(model, Xct)
print((ours == ref.predict(Xct)).mean())
one = DecisionTreeClassifier(max_depth=1).fit(Xc, yc)
print(round((one.predict(Xct) == yct).mean(), 3), round((ours == yct).mean(), 3))
```

```text
1.0
0.644 0.948
```

Sınıf bir dairenin içi; tek bir kütük yalnızca bir eksene dik tek bir çizgi
çizebilir ve %64,4'te kalıyor. Elli kütüğün ağırlıklı oyu daireyi çok sayıda
çizgiyle sarıyor: %94,8. Tahminlerimiz scikit-learn'ün `AdaBoostClassifier`'ı
ile aynı.

## Özet

- Boosting modelleri sırayla kurar; her yeni model öncekilerin hatasına
  odaklanır.
- Gradyan artırma: başlangıç ortalama, her turda artıklara sığ bir ağaç,
  `lr` kadar ekle.
- Boosting'de ağaç sayısı aşırı uyutabilir; erken durdurma ya da çapraz
  doğrulamayla seçilir.
- Küçük öğrenme oranı + daha çok ağaç genellikle daha iyi genelleştirir.
- AdaBoost: yanlış sınıflananları ağırlaştır, kütükleri hatalarına göre
  oylat.
