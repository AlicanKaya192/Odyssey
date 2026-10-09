# Düzenlileştirme

Bölüm 3'te iki sorun görmüştük: eş doğrusal özelliklerde ağırlıklar
anlamsızca büyüyordu, yüksek dereceli polinom eğitim noktalarına fazla
uyuyordu. İkisinin ortak çaresi **düzenlileştirme (regularisation)**: kayba,
ağırlıkların büyüklüğü için bir ceza eklemek. Model artık "hatayı küçült"
değil, "hatayı küçült ama ağırlıkları da küçük tut" der.

## Ridge: kareler cezası

**Ridge** kayba `α Σ wᵢ²` ekler. Normal denklem yalnızca bir terimle değişir:
`(Xᵀ X + α I) w = Xᵀ y`. Kesişim cezalandırılmaz; bunun için önce `X` ve `y`
ortalamalarından arındırılır (merkezlenir), kesişim sonra bulunur.

```python
import numpy as np

rng = np.random.default_rng(7)
n = 60
X = rng.normal(0, 1, size=(n, 8))
true_w = np.array([3.0, -2.0, 1.5, 0, 0, 0, 0, 0])   # yalnızca ilk üçü etkili
y = 1.0 + X @ true_w + rng.normal(0, 1.0, n)


def ridge(X, y, alpha):
    xm, ym = X.mean(axis=0), y.mean()
    # merkezle: kesişim cezasız
    Xc, yc = X - xm, y - ym
    w = np.linalg.solve(Xc.T @ Xc + alpha * np.eye(X.shape[1]), Xc.T @ yc)
    return ym - xm @ w, w


from sklearn.linear_model import Ridge

b, w = ridge(X, y, 10.0)
ref = Ridge(alpha=10.0).fit(X, y)
print(np.allclose(w, ref.coef_), np.isclose(b, ref.intercept_))
for alpha in (0.0, 10.0, 100.0, 1000.0):
    b, w = ridge(X, y, alpha)
    print(alpha, w[:3].round(2), round(float(np.abs(w).sum()), 2))
```

```text
True True
0.0 [ 2.88 -2.09  1.56] 7.42
10.0 [ 2.37 -1.69  1.36] 6.27
100.0 [ 0.94 -0.64  0.64] 2.79
1000.0 [ 0.14 -0.09  0.1 ] 0.43
```

scikit-learn'ün `Ridge`'i ile aynı. `α` büyüdükçe ağırlıklar sıfıra doğru
**büzülüyor** (shrinkage): `α = 0` sıradan en küçük kareler, `α = 1000`'de
ağırlıklar neredeyse sıfır. Doğru `α` ikisinin arasında; çapraz doğrulamayla
seçilir.

## Lasso: mutlak değer cezası

**Lasso** kayba `α Σ |wᵢ|` ekler. Kapalı formülü yok; **koordinat inişi**
(coordinate descent) her turda ağırlıkları tek tek, ötekiler sabitken en
iyi değerine taşır. Bir ağırlığın en iyi değeri **yumuşak eşikleme** (soft
thresholding) ile bulunur: küçük katkılar tam sıfıra çekilir.

```python
def soft(z, t):
    return np.sign(z) * max(abs(z) - t, 0.0)          # |z| ≤ t ise tam 0


def lasso(X, y, alpha, rounds=200):
    xm, ym = X.mean(axis=0), y.mean()
    Xc, yc = X - xm, y - ym
    n, d = Xc.shape
    w = np.zeros(d)
    for _ in range(rounds):
        for j in range(d):
            resid = yc - Xc @ w + Xc[:, j] * w[j]     # j hariç artık
            rho = Xc[:, j] @ resid / n
            w[j] = soft(rho, alpha) / (Xc[:, j] @ Xc[:, j] / n)
    return ym - xm @ w, w


from sklearn.linear_model import Lasso

b, w = lasso(X, y, 0.2)
ref = Lasso(alpha=0.2).fit(X, y)
print(w.round(3))
print(ref.coef_.round(3), np.allclose(w, ref.coef_, atol=1e-4))
b0, w0 = ridge(X, y, 0.0)
print(w0[3:].round(3))
```

```text
[ 2.654 -1.846  1.393  0.037  0.061  0.     0.     0.   ]
[ 2.654 -1.846  1.393  0.037  0.061  0.     0.     0.   ] True
[0.257 0.187 0.15  0.061 0.246]
```

Lasso, scikit-learn ile aynı ağırlıkları buldu. Etkisiz beş özellikten üçünü
**tam sıfır** yaptı, ikisini 0,04 ve 0,06'ya indirdi; düzenlileştirmesiz
modelde aynı beşi 0,06 ile 0,26 arasındaydı. Lasso böylece **özellik
seçimi** de yapar. Ridge ağırlıkları küçültür ama sıfır yapmaz.

<figure class="fig">
<svg viewBox="0 0 460 275" width="460" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="20" y1="150" x2="200" y2="150"/><line class="grid" x1="110" y1="40" x2="110" y2="230"/><polygon class="box" points="110,95 165,150 110,205 55,150" fill-opacity=".3"/><circle class="curve2" cx="130" cy="60" r="40.3" fill="none"/><circle class="curve2" cx="130" cy="60" r="26.2" fill="none"/><circle class="curve2" cx="130" cy="60" r="12.1" fill="none"/><circle class="dot" cx="110.0" cy="95.0" r="5"/><text class="ink" x="110" y="262" font-size="12" text-anchor="middle">Lasso (L1)</text><line class="grid" x1="260" y1="150" x2="440" y2="150"/><line class="grid" x1="350" y1="40" x2="350" y2="230"/><circle class="box" cx="350" cy="150" r="55" fill-opacity=".3"/><circle class="curve2" cx="370" cy="60" r="37.2" fill="none"/><circle class="curve2" cx="370" cy="60" r="24.2" fill="none"/><circle class="curve2" cx="370" cy="60" r="11.2" fill="none"/><circle class="dot" cx="361.9" cy="96.3" r="5"/><text class="ink" x="350" y="262" font-size="12" text-anchor="middle">Ridge (L2)</text></svg>
<figcaption>Ceza bölgesi (gri) ve hata eşdeğer eğrileri (turuncu). En iyi nokta (mor), eğrinin bölgeye ilk değdiği yer: Lasso'nun köşeli bölgesinde çoğu zaman bir eksenin üstü, yani bir ağırlık tam sıfır; Ridge'in yuvarlak bölgesinde değil.</figcaption>
</figure>

## Eş doğrusallığa çare

Bölüm 3'teki sorunu küçük bir örnekte yeniden kuralım: `x₂` neredeyse `x₁`.

```python
x1 = rng.normal(0, 1, n)
x2 = x1 + rng.normal(0, 0.01, n)
yc = 2 * x1 + rng.normal(0, 0.5, n)
Xc2 = np.column_stack([x1, x2])
for alpha in (0.0, 1.0):
    print(alpha, ridge(Xc2, yc, alpha)[1].round(2))
```

```text
0.0 [ 15.7 -13.7]
1.0 [1.01 0.93]
```

Düzenlileştirme olmadan ağırlıklar 15,7 ve −13,7; küçük bir `α = 1` ile 1,01
ve 0,93: etki iki kopyaya paylaştırıldı, toplamları yine yaklaşık 2. Ceza,
"büyük ağırlıklarla birbirini götürme" yolunu kapatıyor.

## Aşırı uyuma çare

9. derece polinomu bu kez 20 noktayla ve Ridge ile kuruyoruz. Polinom
özellikleri çok farklı ölçekte olduğu için önce standartlaştırılıyor.

```python
xs = rng.uniform(-3, 3, 20)
ys = np.sin(xs) + rng.normal(0, 0.2, 20)
xt = rng.uniform(-3, 3, 300)
yt = np.sin(xt) + rng.normal(0, 0.2, 300)
P = lambda x: np.column_stack([x ** d for d in range(1, 10)])
mu, sd = P(xs).mean(axis=0), P(xs).std(axis=0)
S = lambda x: (P(x) - mu) / sd                         # eğitimin ölçüsüyle
for alpha in (0.0, 0.01, 0.1, 1.0, 10.0):
    b, w = ridge(S(xs), ys, alpha)
    test = ((b + S(xt) @ w - yt) ** 2).mean()
    print(alpha, round(test, 4))
```

```text
0.0 0.0934
0.01 0.0679
0.1 0.0778
1.0 0.1207
10.0 0.2164
```

Test hatası `α = 0`'da 0,093, `α = 0,01`'de 0,068 ile en düşük, sonra yeniden
artıyor: fazla ceza modeli de fazla basitleştiriyor (**eksik uyum**,
underfitting). Düzenlileştirme, model karmaşıklığını tek bir düğmeyle
ayarlamanın yolu.

## Özet

- Ridge: kayıp + `α Σ w²`; çözüm `(Xᵀ X + α I) w = Xᵀ y`, kesişim cezasız.
- Lasso: kayıp + `α Σ |w|`; koordinat inişi ve yumuşak eşikleme; bazı
  ağırlıkları tam sıfır yapar (özellik seçimi).
- Eş doğrusallıkta ağırlıkları kararlı kılar, aşırı uyumu azaltır.
- `α` çok küçükse aşırı, çok büyükse eksik uyum; çapraz doğrulamayla seçilir.
- Ceza ölçeğe duyarlıdır: önce standartlaştır.
