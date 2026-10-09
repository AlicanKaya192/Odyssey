# Karar Ağacı

**Karar ağacı** veriyi evet/hayır sorularıyla böler: "x₀ ≤ 5,97 mi?" Her soru
veriyi ikiye ayırır, her yaprakta bir tahmin durur. Tahmin, kökten yaprağa
bir yürüyüş (Temel Algoritmalar modülündeki ağaçlar). Model okunabilir, ölçeklemeye ihtiyaç
duymaz, sayıları ve kategorileri birlikte kaldırır. Bu bölümde scikit-learn'ün
kullandığı **CART** algoritmasını sıfırdan yazıyoruz.

## Saflık ölçüsü: Gini

İyi bir soru, iki tarafı olabildiğince "saf" (tek sınıflı) bırakandır.
**Gini safsızlığı** `1 − Σ pₖ²`: tek sınıflı bir grupta 0, iki sınıf yarı
yarıya ise 0,5. Bir bölmenin değeri, iki tarafın Gini'lerinin örnek sayısıyla
ağırlıklı ortalamasıdır; en küçük olan seçilir. Aday eşikler, bir özelliğin
sıralı farklı değerlerinin orta noktaları.

```python
import numpy as np

rng = np.random.default_rng(10)


def make(n):
    X = rng.uniform(0, 10, (n, 3))
    y = ((X[:, 0] > 6) | ((X[:, 1] > 7) & (X[:, 0] > 3))).astype(int)
    flip = rng.random(n) < 0.1                         # %10 gürültü
    return X, np.where(flip, 1 - y, y)


X, y = make(300)
Xt, yt = make(1000)


def gini(y):
    if len(y) == 0:
        return 0.0
    p = np.bincount(y, minlength=2) / len(y)
    return 1 - (p ** 2).sum()


def best_split(X, y):
    best = (None, None, gini(y))
    for j in range(X.shape[1]):
        values = np.unique(X[:, j])
        for t in (values[:-1] + values[1:]) / 2:       # orta noktalar
            left = X[:, j] <= t
            gl, gr = gini(y[left]), gini(y[~left])
            g = (left.sum() * gl + (~left).sum() * gr) / len(y)
            if g < best[2] - 1e-12:
                best = (j, t, g)
    return best


j, t, g = best_split(X, y)
print(j, round(t, 3), round(gini(y), 4), round(g, 4))
```

```text
0 5.969 0.5 0.2856
```

Veri `x₀ > 6` kuralıyla üretilmişti (artı `x₁`'e bağlı bir parça ve gürültü).
En iyi ilk soru `x₀ ≤ 5,969`: Gini 0,5'ten 0,286'ya indi.

## Ağacı büyütmek

Aynı soruyu her iki tarafta yeniden sor (özyineleme), derinlik sınırına ya da
saf bir gruba gelince yaprak koy: yaprak, gruptaki çoğunluk sınıfı.

```python
def build(X, y, depth, max_depth):
    if depth == max_depth or gini(y) == 0:
        return {"leaf": int(np.bincount(y, minlength=2).argmax())}
    j, t, g = best_split(X, y)
    if j is None:
        return {"leaf": int(np.bincount(y, minlength=2).argmax())}
    left = X[:, j] <= t
    return {"feature": j, "threshold": t,
            "left": build(X[left], y[left], depth + 1, max_depth),
            "right": build(X[~left], y[~left], depth + 1, max_depth)}


def predict_one(node, x):
    while "leaf" not in node:                         # kökten yaprağa
        go_left = x[node["feature"]] <= node["threshold"]
        node = node["left"] if go_left else node["right"]
    return node["leaf"]


def predict(tree, X):
    return np.array([predict_one(tree, x) for x in X])


def show(node, indent=""):
    if "leaf" in node:
        print(f"{indent}return {node['leaf']}")
        return
    print(f"{indent}if x{node['feature']} <= {node['threshold']:.2f}:")
    show(node["left"], indent + "    ")
    print(f"{indent}else:")
    show(node["right"], indent + "    ")


from sklearn.tree import DecisionTreeClassifier

tree = build(X, y, 0, 2)
show(tree)
tree = build(X, y, 0, 3)
ref = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)
print(ref.tree_.feature[0], round(ref.tree_.threshold[0], 3))
pt = predict(tree, Xt)
print((pt == ref.predict(Xt)).mean(), round((pt == yt).mean(), 3))
```

```text
if x0 <= 5.97:
    if x1 <= 7.16:
        return 0
    else:
        return 0
else:
    if x0 <= 9.89:
        return 1
    else:
        return 0
0 5.969
1.0 0.895
```

İki katlı ağaç, okunabilir bir kural listesi. Üç katlı ağacımızın kökü
scikit-learn'ünküyle aynı (`x₀`, 5,969) ve bin test örneğinin hepsinde aynı
tahmini veriyor; doğruluk 0,895.

## Derinlik: aşırı uyumun düğmesi

```python
for depth in (1, 2, 3, 5, 10, 20):
    tr = build(X, y, 0, depth)
    acc_train = (predict(tr, X) == y).mean()
    acc_test = (predict(tr, Xt) == yt).mean()
    print(depth, round(acc_train, 3), round(acc_test, 3))
```

```text
1 0.823 0.819
2 0.823 0.811
3 0.89 0.895
5 0.933 0.855
10 1.0 0.81
20 1.0 0.81
```

Derinlik arttıkça eğitim doğruluğu 1'e çıkıyor: ağaç her gürültülü örneğe
kendi yaprağını açıyor. Test doğruluğu ise 3. katta en iyi (0,895), 10 katta
0,81'e düşüyor. Sınırsız bir ağaç eğitim verisini ezberler; derinlik, yaprak
başına en az örnek (`min_samples_leaf`) ya da budama ile sınırlanır. Bir
sonraki bölüm başka bir çare getiriyor: birçok ağacın ortalaması.

## Özet

- Ağaç, veriyi "özellik ≤ eşik" sorularıyla böler; tahmin kökten yaprağa
  yürüyüş.
- CART her düğümde Gini'yi en çok düşüren özellik ve eşiği arar; aday eşikler
  orta noktalar.
- Model açgözlüdür: her düğümde o anki en iyi bölmeyi seçer, geri dönmez.
- Derinlik büyüdükçe eğitim doğruluğu 1'e çıkar, test düşer: aşırı uyum.
- Ölçekleme gerekmez; ağaç okunabilir kurallar verir.
