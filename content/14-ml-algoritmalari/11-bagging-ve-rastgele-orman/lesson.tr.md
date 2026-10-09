# Bagging ve Rastgele Orman

Bölüm 10'un sonunda derin bir ağacın kararsız olduğunu ve aşırı uyduğunu
gördük. Çaresi şaşırtıcı derecede basit: **çok sayıda ağaç kur ve oylat**.
Her ağaç verinin biraz farklı bir hâlini görürse hataları da farklı olur;
ortalamada birbirini götürür. Bu bölümde topluluğu sıfırdan kuruyoruz; tek
tek ağaçlar için, bölüm 10'da yazdığımızın hızlı karşılığı olan
scikit-learn'ün `DecisionTreeClassifier`'ını yapı taşı olarak kullanıyoruz.

## Bagging: önyükleme + oylama

**Bagging** (bootstrap aggregating): her ağaç, eğitim verisinden **yerine
koyarak** çekilmiş aynı boyda bir örnekle eğitilir (ALG 2'deki bootstrap);
tahmin, ağaçların çoğunluk oyu.

```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(11)


def make(n):
    # son üç özellik gürültü
    X = rng.uniform(0, 10, (n, 6))
    score = np.sin(X[:, 0]) * 2 + (X[:, 1] - 5) * 0.6 + (X[:, 2] > 5)
    y = (score + rng.normal(0, 1.0, n) > 0.5).astype(int)
    return X, y


X, y = make(400)
Xt, yt = make(2000)

single = DecisionTreeClassifier(random_state=0).fit(X, y)
print(round((single.predict(Xt) == yt).mean(), 3))


def bagging(X, y, n_trees, seed, max_features=None):
    boot_rng = np.random.default_rng(seed)
    trees, bags = [], []
    for i in range(n_trees):
        idx = boot_rng.integers(0, len(y), len(y))     # yerine koyarak
        tree = DecisionTreeClassifier(max_features=max_features, random_state=i)
        trees.append(tree.fit(X[idx], y[idx]))
        bags.append(idx)
    return trees, bags


def vote(trees, X):
    votes = np.array([t.predict(X) for t in trees])
    return (votes.mean(axis=0) > 0.5).astype(int)


for n in (1, 5, 25, 100):
    trees, _ = bagging(X, y, n, 0)
    print(n, round((vote(trees, Xt) == yt).mean(), 3))
```

```text
0.738
1 0.732
5 0.764
25 0.782
100 0.8
```

Tek derin ağaç 0,738. Ağaç sayısı arttıkça oylama güçleniyor: 100 ağaçla 0,80.
Hiçbir ağaç tek başına daha iyi değil; kazanç, hataların farklı olmasından
geliyor. Ağaç eklemek aşırı uyuma yol açmaz, yalnızca hesap süresini artırır.

## Rastgele orman: özellikleri de karıştır

Güçlü bir özellik varsa bütün ağaçlar onu ilk soru yapar ve birbirine
benzer; benzer ağaçların oyu az şey kazandırır. **Rastgele orman (random
forest)** her bölmede özelliklerin yalnızca rastgele bir alt kümesine bakar
(sınıflandırmada genellikle `√d` tane). Ağaçlar birbirinden daha farklı olur.

```python
bag_trees, bags = bagging(X, y, 100, 0)
rf_trees, rf_bags = bagging(X, y, 100, 0, max_features="sqrt")
print(round((vote(rf_trees, Xt) == yt).mean(), 3))


def mean_agreement(trees, X):
    P = np.array([t.predict(X) for t in trees[:30]])
    pairs = [(P[i] == P[j]).mean() for i in range(30) for j in range(i + 1, 30)]
    return round(float(np.mean(pairs)), 3)


print(mean_agreement(bag_trees, Xt), mean_agreement(rf_trees, Xt))
from sklearn.ensemble import RandomForestClassifier

ref = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)
print(round((ref.predict(Xt) == yt).mean(), 3))
```

```text
0.814
0.751 0.704
0.809
```

Rastgele orman 0,814; scikit-learn'ün `RandomForestClassifier`'ı 0,809
(rastgele seçimleri farklı olduğu için birebir aynı değil, ama aynı yerde).
İkinci satır nedeni gösteriyor: bagging ağaçlarının iki tanesi testte
ortalama %75,1 aynı tahmini veriyor, rastgele orman ağaçları %70,4. Daha
bağımsız ağaçlar, daha güçlü oy.

## Torba dışı (OOB) doğrulama

Önyüklemede her ağaç örneklerin yaklaşık üçte birini hiç görmez. Her örneği
yalnızca onu **görmemiş** ağaçların oyuyla tahmin edersek, ayrı bir test seti
olmadan bir doğrulama ölçüsü elde ederiz: **torba dışı (out-of-bag, OOB)**.

```python
def oob_score(trees, bags, X, y):
    votes, counts = np.zeros(len(y)), np.zeros(len(y))
    for tree, idx in zip(trees, bags):
        # bu ağacın görmedikleri
        out = np.setdiff1d(np.arange(len(y)), idx)
        votes[out] += tree.predict(X[out])
        counts[out] += 1
    seen = counts > 0
    pred = (votes[seen] / counts[seen] > 0.5).astype(int)
    return round(float((pred == y[seen]).mean()), 3)


n = len(y)
unseen = np.mean([n - len(np.unique(b)) for b in rf_bags]) / n
print(oob_score(rf_trees, rf_bags, X, y), round(float(unseen), 3))
```

```text
0.828 0.364
```

OOB doğruluğu 0,828; 2000 örneklik ayrı testte 0,814. Yakın: OOB, veriyi
bölmeden ücretsiz bir tahmin. Her ağacın görmediği pay 0,364, yani yaklaşık
`1/e`.

## Hangi özellik önemli? Permütasyon önemi

Bir özelliğin test verisindeki değerlerini karıştır; o özelliğe dayanan bir
model bozulur, önemsiz bir özellikte bir şey değişmez.

```python
base = (vote(rf_trees, Xt) == yt).mean()
perm_rng = np.random.default_rng(1)
for j in range(6):
    Xp = Xt.copy()
    Xp[:, j] = perm_rng.permutation(Xp[:, j])
    print(j, round(base - (vote(rf_trees, Xp) == yt).mean(), 3))
```

```text
0 0.049
1 0.27
2 0.012
3 0.001
4 -0.002
5 0.005
```

`x₁` karıştırılınca doğruluk 0,27 düşüyor: en önemli özellik. `x₀` 0,049,
`x₂` 0,012; son üç (gürültü) sıfır civarında. Veriyi üreten formülle uyumlu.
Permütasyon önemi her modelde çalışır ve doğrudan "bu özellik olmasa ne
kaybederim?" sorusunu cevaplar.

## Özet

- Bagging: önyükleme örnekleriyle ağaçlar, çoğunluk oyu; hatalar birbirini
  götürür.
- Rastgele orman: her bölmede rastgele özellik alt kümesi; ağaçlar daha
  bağımsız, oy daha güçlü.
- Ağaç eklemek aşırı uyutmaz; yalnızca yavaşlatır.
- OOB: her örneği onu görmemiş ağaçlarla tahmin et; ayrı test seti olmadan
  doğrulama.
- Permütasyon önemi: özelliği karıştırınca ne kadar kayıp?
