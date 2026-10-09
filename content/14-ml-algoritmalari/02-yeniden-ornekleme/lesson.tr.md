# Yeniden Örnekleme

Bir modelin ne kadar iyi olduğunu, **görmediği** veride ölçeriz. Ama elimizde
tek bir veri seti var: onu eğitim ve test diye bölmek, tekrar tekrar bölmek ve
etiketleri karıştırmak, hep aynı veriden "başka bir veri seti" üretmenin
yollarıdır. Bu bölümde bunları sıfırdan yazıyor ve tek bir ayrımın ne kadar
yanıltıcı olabileceğini ölçüyoruz.

## Veri ve basit bir model

İki sınıflı, iki özellikli 120 örnek. Model olarak en basitlerinden birini
kullanıyoruz: **en yakın merkez (nearest centroid)**. Her sınıfın ortalama
noktasını (merkezini) öğrenir, yeni örneği en yakın merkezin sınıfına koyar.

```python
import numpy as np

rng = np.random.default_rng(2)
n = 120
y = (rng.random(n) < 0.3).astype(int)              # yaklaşık %30 sınıf 1
X = rng.normal(0, 1, size=(n, 2)) + y[:, None] * 1.2


def centroid_fit(X, y):
    return {c: X[y == c].mean(axis=0) for c in np.unique(y)}


def centroid_predict(centers, X):
    labels = list(centers)
    dists = np.stack([((X - centers[c]) ** 2).sum(axis=1) for c in labels])
    return np.array(labels)[dists.argmin(axis=0)]


def accuracy(y_true, y_pred):
    return (y_true == y_pred).mean()


print(np.bincount(y))
```

```text
[82 38]
```

## Tek bir ayrım ne kadar güvenilir?

Eğitim/test ayrımı: indeksleri karıştır, bir kısmını teste ayır. Aynı veriyi
on farklı tohumla bölüp her seferinde modeli eğitelim:

```python
def split(n, test_size, seed):
    order = np.random.default_rng(seed).permutation(n)
    cut = int(n * test_size)
    return order[cut:], order[:cut]                # eğitim, test


scores = []
for seed in range(10):
    train, test = split(n, 0.25, seed)
    model = centroid_fit(X[train], y[train])
    scores.append(accuracy(y[test], centroid_predict(model, X[test])))
print(np.round(scores, 2).tolist())
print(round(min(scores), 2), round(max(scores), 2))
```

```text
[0.8, 0.73, 0.8, 0.77, 0.83, 0.8, 0.77, 0.83, 0.73, 0.77]
0.73 0.83
```

Aynı model, aynı veri: doğruluk 0,73 ile 0,83 arasında. 30 örneklik test
setinde üç örneğin değişmesi on puan fark yaratıyor. "Bizim model %83, öbürü
%78" diye karar vermek, bu oynaklığın içinde kalır.

## k-katlı çapraz doğrulama

**k-katlı çapraz doğrulama (k-fold cross-validation)** veriyi `k` parçaya
böler; her parça bir kez test, kalanı eğitim olur ve `k` sonucun ortalaması
alınır. Her örnek tam bir kez test edilir.

<figure class="fig">
<svg viewBox="0 0 440 175" width="440" xmlns="http://www.w3.org/2000/svg"><text class="dim" x="60" y="28" font-size="12" text-anchor="end">kat 1</text><rect class="dot" x="70" y="10" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="103.0" y="27" font-size="11" text-anchor="middle">test</text><rect class="box" x="140" y="10" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="27" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="210" y="10" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="27" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="280" y="10" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="27" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="350" y="10" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="27" font-size="11" text-anchor="middle">eğitim</text><text class="dim" x="60" y="60" font-size="12" text-anchor="end">kat 2</text><rect class="box" x="70" y="42" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="59" font-size="11" text-anchor="middle">eğitim</text><rect class="dot" x="140" y="42" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="173.0" y="59" font-size="11" text-anchor="middle">test</text><rect class="box" x="210" y="42" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="59" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="280" y="42" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="59" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="350" y="42" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="59" font-size="11" text-anchor="middle">eğitim</text><text class="dim" x="60" y="92" font-size="12" text-anchor="end">kat 3</text><rect class="box" x="70" y="74" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="91" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="140" y="74" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="91" font-size="11" text-anchor="middle">eğitim</text><rect class="dot" x="210" y="74" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="243.0" y="91" font-size="11" text-anchor="middle">test</text><rect class="box" x="280" y="74" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="91" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="350" y="74" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="91" font-size="11" text-anchor="middle">eğitim</text><text class="dim" x="60" y="124" font-size="12" text-anchor="end">kat 4</text><rect class="box" x="70" y="106" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="123" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="140" y="106" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="123" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="210" y="106" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="123" font-size="11" text-anchor="middle">eğitim</text><rect class="dot" x="280" y="106" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="313.0" y="123" font-size="11" text-anchor="middle">test</text><rect class="box" x="350" y="106" width="66" height="26" rx="3"/><text class="dim" x="383.0" y="123" font-size="11" text-anchor="middle">eğitim</text><text class="dim" x="60" y="156" font-size="12" text-anchor="end">kat 5</text><rect class="box" x="70" y="138" width="66" height="26" rx="3"/><text class="dim" x="103.0" y="155" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="140" y="138" width="66" height="26" rx="3"/><text class="dim" x="173.0" y="155" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="210" y="138" width="66" height="26" rx="3"/><text class="dim" x="243.0" y="155" font-size="11" text-anchor="middle">eğitim</text><rect class="box" x="280" y="138" width="66" height="26" rx="3"/><text class="dim" x="313.0" y="155" font-size="11" text-anchor="middle">eğitim</text><rect class="dot" x="350" y="138" width="66" height="26" rx="3" fill-opacity=".45"/><text class="ink" x="383.0" y="155" font-size="11" text-anchor="middle">test</text></svg>
<figcaption>5 katlı çapraz doğrulama: her satır bir eğitim; renkli parça o turun testi. Her örnek tam bir kez test ediliyor.</figcaption>
</figure>

```python
def kfold(n, k):
    sizes = [n // k + (1 if i < n % k else 0) for i in range(k)]
    start = 0
    for size in sizes:
        test = np.arange(start, start + size)
        train = np.concatenate([np.arange(0, start), np.arange(start + size, n)])
        yield train, test
        start += size


from sklearn.model_selection import KFold

ours = [t.tolist() for _, t in kfold(n, 5)]
theirs = [t.tolist() for _, t in KFold(n_splits=5).split(X)]
print(ours == theirs, [len(t) for t in ours])


def cv_score(X, y, k, seed):
    order = np.random.default_rng(seed).permutation(len(y))
    Xs, ys = X[order], y[order]
    accs = []
    for train, test in kfold(len(ys), k):
        model = centroid_fit(Xs[train], ys[train])
        accs.append(accuracy(ys[test], centroid_predict(model, Xs[test])))
    return np.mean(accs)


cv = [cv_score(X, y, 5, seed) for seed in range(10)]
print(round(min(cv), 3), round(max(cv), 3))
print(round(np.std(scores), 3), round(np.std(cv), 3))
```

```text
True [24, 24, 24, 24, 24]
0.767 0.783
0.034 0.006
```

Bizim katlarımız scikit-learn'ün `KFold`'u ile birebir aynı. On farklı
karıştırmada 5 katlı sonuç 0,767 ile 0,783 arasında kaldı; standart sapması
tek ayrımınkinin (0,034) beşte biri kadar (0,006). Bedeli: model bir yerine
beş kez eğitiliyor.

## Katmanlı ayırma

Sınıflar dengesizse (burada 82'ye 38) rastgele bir test setine azınlık sınıfı
bazen az, bazen çok düşer. **Katmanlı (stratified)** ayırma her sınıfı kendi
içinde böler; test setindeki oranlar bütün verideki gibi kalır.

```python
def stratified_split(y, test_size, seed):
    rng = np.random.default_rng(seed)
    train, test = [], []
    for c in np.unique(y):
        idx = rng.permutation(np.flatnonzero(y == c))
        cut = round(len(idx) * test_size)
        test.extend(idx[:cut])
        train.extend(idx[cut:])
    return np.array(train), np.array(test)


plain = [int(y[split(n, 0.25, s)[1]].sum()) for s in range(10)]   # sınıf 1 sayısı
strat = [int(y[stratified_split(y, 0.25, s)[1]].sum()) for s in range(10)]
print(plain)
print(strat)
```

```text
[10, 14, 7, 9, 12, 5, 13, 10, 13, 10]
[10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
```

Rastgele ayrımda 30 kişilik testte sınıf 1'den 5 ile 14 arasında örnek var;
katmanlı ayrımda her seferinde 10. Azınlık sınıfı ne kadar küçükse bu fark o
kadar önemli: scikit-learn sınıflandırmada `StratifiedKFold` kullanır.

## Permütasyon testi: model bir şey öğrendi mi?

Doğruluk 0,775. Bu şans eseri olabilir mi? **Permütasyon testi** etiketleri
karıştırıp (özelliklerle bağını koparıp) aynı ölçümü yüzlerce kez tekrarlar.
Gerçek sonuç bu "anlamsız" sonuçların çoğundan iyiyse model gerçekten bir
şey öğrenmiştir.

```python
real = cv_score(X, y, 5, 0)
fake = []
perm_rng = np.random.default_rng(9)
for _ in range(200):
    fake.append(cv_score(X, perm_rng.permutation(y), 5, 0))
p_value = (np.sum(np.array(fake) >= real) + 1) / (len(fake) + 1)
print(round(real, 3), round(np.mean(fake), 3), round(max(fake), 3))
print(round(p_value, 4))
```

```text
0.775 0.506 0.617
0.005
```

Karıştırılmış etiketlerle doğruluk ortalama 0,506, en iyi ihtimalle 0,617;
gerçek sonuç (0,775) hiçbirinin yakınında değil. p değeri `1/201` ≈ 0,005:
bu sonucun tesadüf olması çok olasılıksız.

## Özet

- Tek bir eğitim/test ayrımı oynaktır: aynı modelde 0,73 ile 0,83.
- k-katlı çapraz doğrulama her örneği bir kez test eder; sonucu çok daha
  kararlı, bedeli `k` kat eğitim.
- Dengesiz sınıflarda katmanlı ayırma oranları korur.
- Permütasyon testi, sonucun şanstan iyi olup olmadığını ölçer.
- Ölçekleyici ve model her katta **yalnızca o katın eğitim kısmıyla** `fit`
  edilir; yoksa veri sızar.
