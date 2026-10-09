# Lojistik Regresyon

Doğrusal regresyon bir sayı tahmin ediyordu. Sınıflandırmada (spam mı değil
mi, hasta mı sağlam mı) bir **olasılık** isteriz: 0 ile 1 arasında. Lojistik
regresyon doğrusal modelin çıktısını **sigmoid** fonksiyonundan geçirip
olasılığa çevirir. Ağırlıkların kapalı bir formülü yok; onları önceki bölümün
gradyan inişiyle bulacağız.

## Sigmoid ve log kaybı

Sigmoid `σ(z) = 1 / (1 + e⁻ᶻ)` her sayıyı 0 ile 1 arasına sıkıştırır: büyük
pozitif `z` 1'e, büyük negatif 0'a, `z = 0` tam 0,5'e gider. Model
`p = σ(A w)`. Kayıp olarak **log kaybı (log loss, cross-entropy)** kullanılır:
`−ortalama(y log p + (1 − y) log(1 − p))`. Gradyanı şaşırtıcı biçimde sade:
`Aᵀ (p − y) / n`.

<figure class="fig">
<svg viewBox="0 0 460 200" width="460" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="40" y1="170" x2="440" y2="170"/><line class="grid" x1="240.0" y1="15" x2="240.0" y2="170"/><line class="curve3" x1="40" y1="92.5" x2="440" y2="92.5"/><polyline class="curve" points="40.0,169.6 43.3,169.6 46.7,169.5 50.0,169.5 53.3,169.4 56.7,169.4 60.0,169.3 63.3,169.2 66.7,169.1 70.0,169.1 73.3,169.0 76.7,168.9 80.0,168.7 83.3,168.6 86.7,168.5 90.0,168.3 93.3,168.1 96.7,167.9 100.0,167.7 103.3,167.5 106.7,167.2 110.0,166.9 113.3,166.6 116.7,166.3 120.0,165.9 123.3,165.5 126.7,165.0 130.0,164.5 133.3,163.9 136.7,163.3 140.0,162.6 143.3,161.9 146.7,161.1 150.0,160.2 153.3,159.3 156.7,158.2 160.0,157.1 163.3,155.9 166.7,154.5 170.0,153.1 173.3,151.5 176.7,149.8 180.0,148.0 183.3,146.1 186.7,144.0 190.0,141.7 193.3,139.3 196.7,136.8 200.0,134.1 203.3,131.3 206.7,128.3 210.0,125.2 213.3,121.9 216.7,118.6 220.0,115.1 223.3,111.5 226.7,107.8 230.0,104.0 233.3,100.2 236.7,96.4 240.0,92.5 243.3,88.6 246.7,84.8 250.0,81.0 253.3,77.2 256.7,73.5 260.0,69.9 263.3,66.4 266.7,63.1 270.0,59.8 273.3,56.7 276.7,53.7 280.0,50.9 283.3,48.2 286.7,45.7 290.0,43.3 293.3,41.0 296.7,38.9 300.0,37.0 303.3,35.2 306.7,33.5 310.0,31.9 313.3,30.5 316.7,29.1 320.0,27.9 323.3,26.8 326.7,25.7 330.0,24.8 333.3,23.9 336.7,23.1 340.0,22.4 343.3,21.7 346.7,21.1 350.0,20.5 353.3,20.0 356.7,19.5 360.0,19.1 363.3,18.7 366.7,18.4 370.0,18.1 373.3,17.8 376.7,17.5 380.0,17.3 383.3,17.1 386.7,16.9 390.0,16.7 393.3,16.5 396.7,16.4 400.0,16.3 403.3,16.1 406.7,16.0 410.0,15.9 413.3,15.9 416.7,15.8 420.0,15.7 423.3,15.6 426.7,15.6 430.0,15.5 433.3,15.5 436.7,15.4 440.0,15.4" fill="none"/><circle class="dot2" cx="240.0" cy="92.5" r="5"/><text class="dim" x="34" y="174.0" font-size="11" text-anchor="end">0</text><text class="dim" x="34" y="96.5" font-size="11" text-anchor="end">0.5</text><text class="dim" x="34" y="19.0" font-size="11" text-anchor="end">1</text><text class="dim" x="40.0" y="190" font-size="11" text-anchor="middle">-6</text><text class="dim" x="240.0" y="190" font-size="11" text-anchor="middle">0</text><text class="dim" x="440.0" y="190" font-size="11" text-anchor="middle">6</text></svg>
<figcaption>Sigmoid: z = 0'da 0,5 (turuncu nokta), z büyüdükçe 1'e, küçüldükçe 0'a yaklaşır ama hiç ulaşmaz.</figcaption>
</figure>

```python
import numpy as np

rng = np.random.default_rng(5)
n = 300
X = rng.normal(0, 1, size=(n, 2))
logit = 0.5 + 2.0 * X[:, 0] - 1.0 * X[:, 1]             # gerçek ağırlıklar
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
A = np.column_stack([np.ones(n), X])


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def log_loss(w):
    p = sigmoid(A @ w)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()


def gradient(w):
    return A.T @ (sigmoid(A @ w) - y) / n


w = np.zeros(3)
for step in range(1, 3001):
    w -= 0.5 * gradient(w)
    if step in (1, 100, 1000, 3000):
        print(step, round(log_loss(w), 4), w.round(3))
pred = (sigmoid(A @ w) >= 0.5).astype(int)
print(round((pred == y).mean(), 3))
```

```text
1 0.6502 [ 0.032  0.128 -0.075]
100 0.4509 [ 0.431  1.812 -0.939]
1000 0.4507 [ 0.445  1.879 -0.97 ]
3000 0.4507 [ 0.445  1.879 -0.97 ]
0.763
```

Kayıp 0,65'ten 0,45'e indi ve orada kaldı. Veriyi `0,5 + 2x₁ − x₂` ile
ürettiğimiz için ağırlıklar (0,445, 1,879, −0,97) gerçeğe yakın. Doğruluk
0,763: veri rastgele etiketlendiği için (olasılıkla) mükemmel ayırmak zaten
mümkün değil.

## scikit-learn ile karşılaştırma

scikit-learn'ün `LogisticRegression`'ı varsayılan olarak düzenlileştirme
uygular (bölüm 7). Karşılaştırmak için onu kapatıyoruz: `C=np.inf`.

```python
from sklearn.linear_model import LogisticRegression

ref = LogisticRegression(C=np.inf).fit(X, y)
theirs = np.r_[ref.intercept_, ref.coef_[0]]
print(theirs.round(3), np.allclose(w, theirs, atol=1e-3))
print((ref.predict(X) == pred).mean())
```

```text
[ 0.445  1.878 -0.971] True
1.0
```

Ağırlıklar binde bir hassasiyetle aynı, tahminlerin hepsi aynı. scikit-learn
gradyan inişi yerine daha akıllı bir yöntem (L-BFGS) kullanır, ama aynı
kaybın aynı dibine iner.

## Eşik

Model olasılık verir; sınıf kararı bir **eşikle** verilir. 0,5 doğal
görünür, ama tek seçenek değil. Hastalığı kaçırmanın bedeli büyükse eşik
düşürülür: daha çok kişi "pozitif" denir.

```python
p = sigmoid(A @ w)
for t in (0.5, 0.3):
    print(t, int((p >= t).sum()), round(((p >= t) == y).mean(), 3))
```

```text
0.5 176 0.763
0.3 226 0.75
```

Eşik 0,3'e inince pozitif dediğimiz örnek 176'dan 226'ya çıktı; doğruluk
biraz düştü (0,763 → 0,75). Hangisinin daha iyi olduğu doğrulukla değil,
hataların bedeliyle belirlenir; bölüm 6'nın konusu.

## Neden MSE değil log kaybı?

Gerçek sınıf 0 iken modelin sınıf 1'e verdiği olasılık arttıkça iki kaybın
cezası:

```python
for prob in (0.6, 0.9, 0.99):
    print(prob, round(-np.log(1 - prob), 3), round(prob ** 2, 3))
```

```text
0.6 0.916 0.36
0.9 2.303 0.81
0.99 4.605 0.98
```

MSE cezası en fazla 1'e çıkıyor (0,98); log kaybı ise kendinden emin yanlışa
4,6 ceza veriyor ve olasılık 1'e yaklaştıkça sınırsız büyüyor. Ayrıca
sigmoidle birlikte MSE'nin kayıp yüzeyi çukurlu olabilir; log kaybınınki tek
çukurlu (dışbükey), gradyan inişi dibi kesin bulur.

## Özet

- `p = σ(A w)`, sigmoid çıktıyı 0–1 arasına sıkıştırır.
- Log kaybı: `−ort(y log p + (1 − y) log(1 − p))`; gradyanı `Aᵀ (p − y) / n`.
- Kapalı formül yok; gradyan inişi ile scikit-learn'ün (`C=np.inf`) aynı
  ağırlıklarına ulaştık.
- Sınıf kararı eşikle verilir; eşik hataların bedeline göre seçilir.
- Log kaybı kendinden emin yanlışı ağır cezalandırır ve dışbükeydir.
