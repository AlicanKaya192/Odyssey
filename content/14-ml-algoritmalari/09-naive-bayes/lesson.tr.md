# Naive Bayes

**Naive Bayes**, Bayes kuralını sınıflandırmaya uygular: bir örneğin sınıfı,
`P(sınıf) · P(özellikler | sınıf)`'ı en büyük yapan sınıftır. "Saf" (naive)
olan varsayım şu: sınıf bilindiğinde özellikler birbirinden **bağımsız**.
Böylece `P(özellikler | sınıf)` her özelliğin kendi olasılığının çarpımına
ayrılır ve model yalnızca sayarak, tek geçişte öğrenir. Varsayım gerçekte
nadiren doğrudur, ama model şaşırtıcı biçimde iyi çalışır; özellikle metinde.

## Gauss Naive Bayes

Sürekli özelliklerde her sınıf ve her özellik için bir normal dağılım
varsayılır: sınıfın içindeki ortalama ve varyans. Tahmin, her sınıf için
`log P(sınıf) + Σ log N(xᵢ | ortᵢ, varᵢ)`'nin en büyüğü.

```python
import numpy as np

rng = np.random.default_rng(9)
y = rng.integers(0, 2, 200)
shift = np.where(y[:, None] == 1, [2.0, 1.0], [0.0, -1.0])
X = rng.normal(0, 1, (200, 2)) * [1.0, 2.0] + shift


def gnb_fit(X, y):
    classes = np.unique(y)
    # scikit-learn'ün küçük payı
    eps = 1e-9 * X.var(axis=0).max()
    prior = np.array([(y == c).mean() for c in classes])
    mean = np.array([X[y == c].mean(axis=0) for c in classes])
    var = np.array([X[y == c].var(axis=0) for c in classes]) + eps
    return classes, prior, mean, var


def gnb_log_posterior(model, X):
    classes, prior, mean, var = model
    diff = X[:, None, :] - mean[None]
    norm = np.log(2 * np.pi * var)[None]
    ll = -0.5 * (norm + diff ** 2 / var[None]).sum(axis=2)
    return np.log(prior)[None] + ll


from sklearn.naive_bayes import GaussianNB

model = gnb_fit(X, y)
logp = gnb_log_posterior(model, X)
pred = model[0][logp.argmax(axis=1)]
ref = GaussianNB().fit(X, y)
print((pred == ref.predict(X)).mean(), round((pred == y).mean(), 3))
proba = np.exp(logp - logp.max(axis=1, keepdims=True))
proba /= proba.sum(axis=1, keepdims=True)
print(np.allclose(proba, ref.predict_proba(X)))
```

```text
1.0 0.855
True
```

Tahminler ve olasılıklar scikit-learn'ün `GaussianNB`'si ile aynı. Bunun için
onun varyansa eklediği küçük payı (`var_smoothing`, en büyük varyansın
milyarda biri) biz de ekledik. "Öğrenmek" yalnızca sınıf başına ortalama ve
varyans hesaplamak: `O(n · d)`.

## Neden logaritma?

Olasılıklar çarpılır; yüzlerce özellikte (metindeki kelimeler gibi) çarpım
bilgisayarın gösterebileceği en küçük sayının altına iner:

```python
probs = np.full(400, 0.01)
print(np.prod(probs), round(np.log(probs).sum(), 2))
```

```text
0.0 -1842.07
```

`0,01`'in 400 kez çarpımı 10⁻⁸⁰⁰: `float` için tam **0** (alt taşma,
underflow); bütün sınıflar sıfır olunca karar verilemez. Logaritmalar toplanır
ve −1842 rahatça saklanır. Olasılık gerekirse sonda en büyüğü çıkarılıp üs
alınır (yukarıdaki `proba` gibi).

## Çok terimli Naive Bayes: metin

Metinde özellikler kelime sayılarıdır. Her sınıf için "bu sınıfın
metinlerinde her kelimenin payı" öğrenilir. Bir sınıfta hiç geçmeyen bir
kelimenin payı 0 olursa, o kelimeyi içeren her metin o sınıftan olamaz
sayılır; bunu önlemek için her sayıya 1 eklenir (**Laplace düzeltmesi**,
`alpha = 1`).

```python
docs = ["win money now", "win a free prize now", "free money offer",
        "meeting at noon", "project meeting notes", "lunch at noon today",
        "free lunch offer", "notes for the project"]
labels = np.array([1, 1, 1, 0, 0, 0, 1, 0])          # 1: istenmeyen
vocab = sorted({w for d in docs for w in d.split()})
index = {w: i for i, w in enumerate(vocab)}


def counts(texts):
    M = np.zeros((len(texts), len(vocab)))
    for r, t in enumerate(texts):
        for w in t.split():
            if w in index:
                M[r, index[w]] += 1
    return M


C = counts(docs)


def mnb_fit(C, y, alpha=1.0):
    classes = np.unique(y)
    prior = np.log(np.array([(y == c).mean() for c in classes]))
    word = np.array([C[y == c].sum(axis=0) for c in classes]) + alpha
    return classes, prior, np.log(word / word.sum(axis=1, keepdims=True))


from sklearn.naive_bayes import MultinomialNB

classes, prior, logw = mnb_fit(C, labels)
new = counts(["free money today", "project meeting at noon", "win lunch"])
scores = prior + new @ logw.T
ref = MultinomialNB(alpha=1.0).fit(C, labels)
print(classes[scores.argmax(axis=1)].tolist(), ref.predict(new).tolist())
print(np.allclose(logw, ref.feature_log_prob_))
print(len(vocab))
```

```text
[1, 0, 1] [1, 0, 1]
True
16
```

Üç yeni metnin sınıfı ve kelime olasılıkları `MultinomialNB` ile aynı. Bir
metnin puanı, sayılar matrisiyle log olasılıkların çarpımı: tek bir matris
çarpımı. İlk spam filtrelerinin çoğu bu fikre dayanıyordu.

## Düzeltmesiz ne olur?

```python
# neredeyse düzeltmesiz
classes0, prior0, logw0 = mnb_fit(C, labels, alpha=1e-12)
s0 = prior0 + counts(["win meeting"]) @ logw0.T
print(np.round(s0, 1).tolist())
```

```text
[[-32.9, -32.9]]
```

"win" yalnızca istenmeyen, "meeting" yalnızca normal metinlerde geçmiş.
Düzeltme olmadan iki sınıf da görmediği bir kelime yüzünden −32,9'a çöküyor;
puanlar eşit ve karar anlamsız. Laplace düzeltmesi görülmemiş kelimeye
küçük ama sıfır olmayan bir pay bırakır.

## Özet

- Sınıf = `log P(sınıf) + Σ log P(xᵢ | sınıf)`'nin en büyüğü; özellikler
  sınıf içinde bağımsız varsayılır.
- Gauss NB: sınıf başına ortalama ve varyans; çok terimli NB: sınıf başına
  kelime payları.
- Olasılıklar çarpılmaz, logaritmaları toplanır (alt taşma).
- Laplace düzeltmesi (`alpha`) görülmemiş kelimeyi sıfırlanmaktan korur.
- Öğrenme tek geçiş sayma; çok hızlı ve az veriyle çalışır.
