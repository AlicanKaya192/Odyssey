# Sıfırdan Yazmak

ALG 3'te makine öğrenmesi algoritmalarını **NumPy ile sıfırdan** yazacağız ve
her birini scikit-learn'ün sonucuyla karşılaştıracağız. Amaç scikit-learn'ün
yerine bir şey koymak değil: bir modelin içinde ne olduğunu bilen kişi, onu
doğru ayarlar, hatasını teşhis eder ve sınırını bilir. "Bu model neden böyle
tahmin etti?" sorusunun cevabı çoğu zaman yirmi satırlık bir koddadır.

Bu bölüm üç alışkanlığı kuruyor: veriyi **dizi (array)** olarak düşünmek,
döngü yerine **vektör işlemi** yazmak ve her modeli aynı **`fit` / `predict`**
kalıbıyla kurmak.

## Veri bir matris

Makine öğrenmesinde veri neredeyse her zaman bir **matristir**: her satır bir
örnek (gözlem), her sütun bir özellik. NumPy'de bunun adı `X`, boyu
`(örnek sayısı, özellik sayısı)`.

```python
import numpy as np

rng = np.random.default_rng(0)
X = rng.normal(loc=[50, 3], scale=[10, 0.5], size=(200, 2))
print(X.shape)
print(X[:2].round(2))
print(X.mean(axis=0).round(2), X.std(axis=0).round(2))
```

```text
(200, 2)
[[51.26  2.93]
 [56.4   3.05]]
[49.02  3.01] [9.79 0.5 ]
```

`default_rng(0)` tohumlu bir üreteç: aynı kodu çalıştıran aynı sayıları
görür. `axis=0` "satırlar boyunca", yani **sütun başına** demek: iki
özelliğin ortalaması ve standart sapması.

<figure class="fig">
<svg viewBox="0 0 430 270" width="430" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="70" y="40" width="46" height="46"/><rect class="box" x="116" y="40" width="46" height="46"/><rect class="box" x="162" y="40" width="46" height="46"/><rect class="box" x="70" y="86" width="46" height="46"/><rect class="box" x="116" y="86" width="46" height="46"/><rect class="box" x="162" y="86" width="46" height="46"/><rect class="box" x="70" y="132" width="46" height="46"/><rect class="box" x="116" y="132" width="46" height="46"/><rect class="box" x="162" y="132" width="46" height="46"/><rect class="box" x="70" y="178" width="46" height="46"/><rect class="box" x="116" y="178" width="46" height="46"/><rect class="box" x="162" y="178" width="46" height="46"/><text class="dim" x="93.0" y="30" font-size="12" text-anchor="middle">özl. 1</text><text class="dim" x="139.0" y="30" font-size="12" text-anchor="middle">özl. 2</text><text class="dim" x="185.0" y="30" font-size="12" text-anchor="middle">özl. 3</text><text class="dim" x="62" y="67.0" font-size="12" text-anchor="end">örnek 1</text><text class="dim" x="62" y="113.0" font-size="12" text-anchor="end">örnek 2</text><text class="dim" x="62" y="159.0" font-size="12" text-anchor="end">örnek 3</text><text class="dim" x="62" y="205.0" font-size="12" text-anchor="end">örnek 4</text><line class="curve" x1="93.0" y1="46" x2="93.0" y2="238"/><polygon class="dot" points="87.0,238 99.0,238 93.0,248"/><text class="ink" x="70" y="266" font-size="13">axis=0: sütun başına</text><line class="curve2" x1="76" y1="63.0" x2="224" y2="63.0"/><polygon class="dot2" points="224,57.0 224,69.0 234,63.0"/><text class="ink" x="240" y="68.0" font-size="13">axis=1: satır başına</text></svg>
<figcaption><code>X.mean(axis=0)</code> satırlar boyunca ilerler ve her sütun için bir sayı verir; <code>axis=1</code> her satır için bir sayı.</figcaption>
</figure>

## Döngü değil, vektör işlemi

Bir doğrusal modelin tahmini her satır için `w₁x₁ + w₂x₂ + w₃x₃`. Bunu
Python döngüsüyle de, tek bir matris çarpımıyla (`X @ w`) da yazabilirsin:

```python
import time

big = rng.normal(size=(1_000_000, 3))
w = np.array([0.5, -2.0, 1.0])
t = time.perf_counter()
loop = [row[0] * w[0] + row[1] * w[1] + row[2] * w[2] for row in big]
t_loop = time.perf_counter() - t
t = time.perf_counter()
vec = big @ w
t_vec = time.perf_counter() - t
print(np.allclose(loop, vec), round(t_loop / t_vec))
```

```text
True 195
```

Sonuçlar aynı (`np.allclose` küçük yuvarlama farklarını tolere ederek
karşılaştırır); ama bu bilgisayarda döngü yüz kattan fazla yavaş. NumPy'nin
işlemleri C ile yazılmış ve bütün diziyi tek seferde işliyor. Bu modülde kural
şu: **satır satır döngü yerine dizi işlemi**. Döngü yalnızca algoritmanın
kendi adımları için (gradyan inişinin turları, ağacın düğümleri) kalır.

## `fit` / `predict` kalıbı

scikit-learn'deki her model aynı sözleşmeye uyar: `fit(X, y)` veriden
öğrenir ve öğrendiklerini sonu `_` ile biten özelliklerde saklar (`mean_`,
`coef_`); `transform` ya da `predict` öğrendiğini yeni veriye uygular. Biz de
aynısını yapacağız. İlk örnek, özellikleri ortalaması 0, standart sapması 1
olacak şekilde ölçekleyen **standartlaştırıcı**:

```python
class Standardizer:
    def fit(self, X):
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        return self                    # zincirleme: .fit(X).transform(X)

    def transform(self, X):
        return (X - self.mean_) / self.scale_


from sklearn.preprocessing import StandardScaler

mine = Standardizer().fit(X).transform(X)
theirs = StandardScaler().fit(X).transform(X)
print(np.allclose(mine, theirs))
print(mine.mean(axis=0).round(6) + 0, mine.std(axis=0).round(6))
sample_std = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
print(np.allclose(sample_std, theirs), np.abs(sample_std - theirs).max().round(4))
```

```text
True
[0. 0.] [1. 1.]
False 0.0094
```

Bizimki scikit-learn'ünkiyle aynı. `X - self.mean_` satırında **yayın
(broadcasting)** çalışıyor: `(200, 2)` boyutlu matristen `(2,)` boyutlu
vektör çıkarılınca NumPy vektörü her satıra uyguluyor.

Son satır küçük bir tuzak: istatistikte örneklem standart sapması `n − 1`'e
bölünür (`ddof=1`), scikit-learn ise `n`'e böler (`ddof=0`). Fark küçük ama
sonuç artık aynı değil. Sıfırdan yazarken bu tür ayrıntılar karşılaştırmayla
yakalanır.

## En basit model: çoğunluk sınıfı

Bir sınıflandırıcıyı değerlendirmeden önce sorulacak ilk soru: "hep en sık
sınıfı söyleyen bir model ne kadar başarılı?" Bu bir **taban çizgisi
(baseline)**; modelin bunu geçmesi gerekir.

```python
from collections import Counter


class MajorityClassifier:
    def fit(self, X, y):
        self.label_ = Counter(y).most_common(1)[0][0]
        return self

    def predict(self, X):
        return np.full(len(X), self.label_)


from sklearn.dummy import DummyClassifier

y = (X[:, 0] > 55).astype(int)
ours = MajorityClassifier().fit(X, y).predict(X)
ref = DummyClassifier(strategy="most_frequent").fit(X, y).predict(X)
print(np.bincount(y), (ours == ref).all(), (ours == y).mean())
```

```text
[145  55] True 0.725
```

200 örneğin 145'i sınıf 0'da; hep "0" diyen model %72,5 doğru. %75 doğruluk
veren bir model ilk bakışta iyi görünür, ama taban çizgisini ancak biraz
geçiyordur. Bölüm 6'da doğruluğun neden tek başına yanıltıcı olduğunu
göreceğiz.

## Özet

- Veri bir matris: satırlar örnek, sütunlar özellik; `axis=0` sütun başına.
- Döngü yerine dizi işlemi (`X @ w`, `X.mean(axis=0)`); bu bilgisayarda yüz
  kattan fazla hızlı.
- `fit` öğrenir ve `_` ile biten özelliklere yazar; `transform` / `predict`
  uygular; `fit` `self` döndürür.
- Her sıfırdan yazılan model scikit-learn ile `np.allclose` ya da `==` ile
  karşılaştırılır; fark varsa sebebi bir ayrıntıdadır (`ddof` gibi).
- Taban çizgisi: hep en sık sınıfı söyleyen model.
