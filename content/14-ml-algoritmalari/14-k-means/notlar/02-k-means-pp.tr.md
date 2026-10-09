k-means++ başlangıcı basit bir fikre dayanır: ilk merkezi rastgele seç, sonraki
her merkezi **mevcut merkezlere uzak** noktalardan seç. Uzaklık tamamen
belirleyici değil, bir olasılık: bir noktanın seçilme şansı, en yakın merkeze
**kare uzaklığıyla** orantılı. Uzak noktalar daha olası, ama aykırı bir tek
nokta her seferinde seçilmiyor.

Dersteki `X` ve `kmeans` ile, 100 rastgele başlangıcı 100 k-means++
başlangıcıyla karşılaştıralım:

```python
def kmeans_pp(X, k, rng):
    C = [X[rng.integers(len(X))]]
    while len(C) < k:
        # her noktanın en yakın merkeze kare uzaklığı
        d = ((X[:, None, :] - np.array(C)[None]) ** 2).sum(axis=2).min(axis=1)
        C.append(X[rng.choice(len(X), p=d / d.sum())])
    return np.array(C)


for name in ("random", "k-means++"):
    r = np.random.default_rng(0)
    stuck, rounds = 0, []
    for _ in range(100):
        if name == "random":
            start = X[r.choice(len(X), 3, replace=False)]
        else:
            start = kmeans_pp(X, 3, r)
        history = kmeans(X, start)[2]
        stuck += history[-1] > 549
        rounds.append(len(history))
    print(name, stuck, np.mean(rounds))
```

```text
random 4 5.78
k-means++ 1 4.34
```

k-means++ takılmayı 4'ten 1'e indirdi ve ortalama tur sayısını 5,78'den
4,34'e düşürdü: iyi başlayan merkezler yerine daha çabuk oturuyor. Ama
takılma sıfır değil; scikit-learn bu yüzden k-means++'ı `n_init` ile birlikte
kullanıyor ve birkaç denemenin en iyisini tutuyor.

k-means++ yalnızca iyi bir başlangıç değil, bir garantisi de var: beklenen
inertia, en iyi çözümün en fazla `O(log k)` katıdır. Rastgele başlangıcın
böyle bir sınırı yok.
