# Doğrulama Araçları

`cross_val_score(model, X, y, cv=5)` yazınca veri beş parçaya bölünüyor.
Ama **nasıl** bölündüğü skoru değiştirir: sınıflar katlara dengesiz
dağılabilir, aynı hastanın satırları hem eğitime hem teste düşebilir, zaman
sırası bozulabilir. scikit-learn her durum için ayrı bir bölücü (splitter)
veriyor. Bu bölüm bölücüleri, birkaç ölçüyü birden veren `cross_validate`'i
ve iki eğri fonksiyonunu (`learning_curve`, `validation_curve`) anlatıyor.

## KFold ve StratifiedKFold

```python
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold

y = np.array([0] * 90 + [1] * 10)   # 100 satır, 10'u pozitif, sıralı
X = np.zeros((100, 1))
for cv in [KFold(5), StratifiedKFold(5)]:
    print([int(y[test].sum()) for _, test in cv.split(X, y)])
```

```text
[0, 0, 0, 0, 10]
[2, 2, 2, 2, 2]
```

- Bir bölücünün `split(X, y)` metodu her kat için `(eğitim, test)` sıra
  numaralarını verir. Her test katındaki pozitif sayısını saydık.
- `KFold(5)` satırları sırayla beşe böler. Veri sıralı olduğu için ilk dört
  test katında **hiç** pozitif yok, sonuncusunda hepsi var. Böyle bir katta
  "pozitifi bulma" başarısı ölçülemez.
- `StratifiedKFold` her kata sınıf oranını korur: her katta 2 pozitif.
- `cv=5` gibi bir **sayı** verildiğinde sınıflandırıcı için
  `StratifiedKFold(5)` kullanılır. Regresyonda (hedef sayı) `KFold(5)`
  kullanılır ve **karıştırmaz**.

## Sıralı veride karıştırmamak

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.tree import DecisionTreeRegressor

X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=4)
order = np.argsort(y)               # dosya hedefe göre sıralanmış olsun
X, y = X[order], y[order]
for cv in [5, KFold(5, shuffle=True, random_state=0)]:
    scores = cross_val_score(DecisionTreeRegressor(random_state=0), X, y, cv=cv)
    print(scores.round(2), round(scores.mean(), 3))
```

```text
[ -4.13 -13.08 -10.47  -9.43  -2.93] -8.009
[0.82 0.78 0.86 0.84 0.76] 0.811
```

- Veri hedefe göre sıralı (fiyata göre dizilmiş bir dosya gibi). `cv=5`
  karıştırmadığı için her test katı, eğitimde hiç görülmemiş bir fiyat
  aralığı. Ağaç gördüğü aralığın dışını tahmin edemez; R² **eksiye** düştü.
- `KFold(5, shuffle=True, random_state=0)` satırları önce karıştırıyor:
  ortalama R² 0,811. Model aynı, yalnızca bölme değişti.
- Dosyanın nasıl sıralandığını bilmiyorsan karıştırarak böl. İstisna zaman:
  orada karıştırmak geleceği eğitime sokar (aşağıda).

## Gruplar: aynı kişi iki tarafta olmasın

```python
import numpy as np
from sklearn.model_selection import GroupKFold, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

rng = np.random.default_rng(3)
centers = rng.normal(size=(40, 5))       # 40 hasta
labels = rng.integers(0, 2, size=40)     # etiket hastaya göre, rastgele
groups = np.repeat(np.arange(40), 6)     # her hastadan 6 ölçüm
X = centers[groups] + rng.normal(scale=0.1, size=(240, 5))
y = labels[groups]
model = KNeighborsClassifier(n_neighbors=3)
plain = cross_val_score(model, X, y, cv=KFold(5, shuffle=True, random_state=0))
grouped = cross_val_score(model, X, y, cv=GroupKFold(5), groups=groups)
print(round(plain.mean(), 3), round(grouped.mean(), 3))
```

```text
1.0 0.588
```

- Etiket rastgele: ölçümlerde hastalığı gösteren **hiçbir** şey yok. Ama
  aynı hastanın 6 ölçümü birbirine çok benziyor.
- Düz `KFold` aynı hastanın ölçümlerini eğitime ve teste dağıtıyor. Model
  teste gelen ölçümün "kardeşini" eğitimde bulup etiketini kopyalıyor:
  doğruluk 1,0. Ölçtüğü şey hastalık değil, hastayı tanımak.
- `GroupKFold` bir hastanın bütün satırlarını aynı kata koyuyor
  (`groups=groups` ile). Model yeni hastalarda sınanıyor: 0,588, şans
  düzeyine yakın, yani gerçek durum.
- Aynı müşteri, aynı cihaz, aynı oturum, aynı fotoğrafçı: model yarın **yeni**
  bir gruba uygulanacaksa doğrulama da grup bazlı yapılır. Sınıf oranı da
  korunsun istenirse `StratifiedGroupKFold`.

## TimeSeriesSplit

```python
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

X = np.arange(12).reshape(-1, 1)    # 12 ay, sırayla
for train, test in TimeSeriesSplit(n_splits=4).split(X):
    print(train.min(), train.max(), test.tolist())
print("gap=1")
for train, test in TimeSeriesSplit(n_splits=3, test_size=2, gap=1).split(X):
    print(train.min(), train.max(), test.tolist())
```

```text
0 3 [4, 5]
0 5 [6, 7]
0 7 [8, 9]
0 9 [10, 11]
gap=1
0 4 [6, 7]
0 6 [8, 9]
0 8 [10, 11]
```

- Her katta eğitim **hep geçmiş**, test hemen ardından gelen dönem. Eğitim
  penceresi her katta büyüyor (0–3, 0–5, 0–7, 0–9).
- `gap=1` eğitimle test arasına bir dönem boşluk koyuyor: 0–4 ile eğitip
  6–7'yi test etmek. Tahminin bir ay sonra kullanılacağı durumda dürüst olan
  budur.
- Zaman serisinde karıştırmak (`shuffle=True`) yarının verisini dünün
  modeline öğretir; skor gerçekte ulaşılamayacak kadar iyi çıkar.

## cross_validate: birkaç ölçü, eğitim skoru

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=400, n_features=10, n_informative=4,
                           weights=[0.8], flip_y=0.05, random_state=6)
res = cross_validate(DecisionTreeClassifier(random_state=0), X, y, cv=5,
                     scoring=["accuracy", "f1"], return_train_score=True)
print(sorted(res))
for key in ["train_accuracy", "test_accuracy", "test_f1"]:
    print(key, round(res[key].mean(), 3))
```

```text
['fit_time', 'score_time', 'test_accuracy', 'test_f1', 'train_accuracy', 'train_f1']
train_accuracy 1.0
test_accuracy 0.82
test_f1 0.593
```

- `cross_val_score` tek bir ölçünün dizisini verir; `cross_validate` bir
  **sözlük** verir: her ölçü için `test_<ad>`, istenirse `train_<ad>`, ve
  `fit_time` / `score_time` (saniye).
- Eğitim doğruluğu 1,0, test 0,82: derinliği sınırsız ağaç eğitimi
  ezberlemiş. Bu farkı görmek için `return_train_score=True` gerekir.
- Veri dengesiz (%80'i bir sınıf): doğruluk 0,82 iyi görünürken F1 0,593.
  Ölçüleri yan yana görmek, tek sayının yanıltmasını önler.

## learning_curve: daha çok veri işe yarar mı?

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve

sizes, train, test = learning_curve(LogisticRegression(), X, y, cv=5,
                                    train_sizes=[0.1, 0.25, 0.5, 1.0])
print(sizes.tolist())
print(train.mean(axis=1).round(3).tolist())
print(test.mean(axis=1).round(3).tolist())
```

```text
[32, 80, 160, 320]
[0.894, 0.852, 0.855, 0.841]
[0.775, 0.825, 0.822, 0.83]
```

- `train_sizes` eğitim katının oranları: 320 satırlık eğitimin %10'u 32
  satır. Her boyutta modeli 5 kez eğitip eğitim ve test skorunu verir.
- 32 satırda eğitim 0,894, test 0,775: az veriyle model eğitime uyuyor ama
  genellemiyor. 320 satırda eğitim 0,841, test 0,83: aradaki fark 0,01'e
  indi ve test skoru 80 satırdan beri neredeyse yerinde sayıyor.
- Eğriler birleşmiş ve düzleşmişse daha çok veri toplamak bu modele pek
  bir şey kazandırmaz; daha güçlü model ya da daha iyi özellik gerekir.

## validation_curve: tek bir ayarın etkisi

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier

depths = [1, 2, 3, 5, 8, 12]
train, test = validation_curve(DecisionTreeClassifier(random_state=0), X, y,
                               param_name="max_depth", param_range=depths, cv=5)
print(train.mean(axis=1).round(3).tolist())
print(test.mean(axis=1).round(3).tolist())
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot(depths, train.mean(axis=1), marker="o", label="train")
ax.plot(depths, test.mean(axis=1), marker="o", label="test")
ax.set_xlabel("max_depth")
ax.set_ylabel("accuracy")
ax.legend()
```

```text
[0.841, 0.876, 0.882, 0.922, 0.967, 0.999]
[0.828, 0.857, 0.838, 0.83, 0.822, 0.822]
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="398.828125pt" height="222.808781pt" viewBox="0 0 398.828125 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 398.828125 222.808781 
L 398.828125 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 56.828125 184.608 
L 391.628125 184.608 
L 391.628125 7.2 
L 56.828125 7.2 
L 56.828125 184.608 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="99.715728" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="99.715728" y="199.205656" transform="rotate(-0 99.715728 199.205656)">2</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="155.054571" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="155.054571" y="199.205656" transform="rotate(-0 155.054571 199.205656)">4</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="210.393414" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.393414" y="199.205656" transform="rotate(-0 210.393414 199.205656)">6</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="265.732257" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="265.732257" y="199.205656" transform="rotate(-0 265.732257 199.205656)">8</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="321.0711" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="321.0711" y="199.205656" transform="rotate(-0 321.0711 199.205656)">10</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="376.409943" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="376.409943" y="199.205656" transform="rotate(-0 376.409943 199.205656)">12</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="224.228125" y="213.206438" transform="rotate(-0 224.228125 213.206438)">max_depth</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_7">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="174.25634" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="178.055169" transform="rotate(-0 49.828125 178.055169)">0.825</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="151.379745" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="155.178573" transform="rotate(-0 49.828125 155.178573)">0.850</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="128.503149" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="132.301977" transform="rotate(-0 49.828125 132.301977)">0.875</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="105.626553" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="109.425381" transform="rotate(-0 49.828125 109.425381)">0.900</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="82.749957" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="86.548786" transform="rotate(-0 49.828125 86.548786)">0.925</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="59.873362" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="63.67219" transform="rotate(-0 49.828125 63.67219)">0.950</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="36.996766" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="40.795594" transform="rotate(-0 49.828125 40.795594)">0.975</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828125" y="14.12017" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828125" y="17.918998" transform="rotate(-0 49.828125 17.918998)">1.000</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="95.904" transform="rotate(-90 14.797656 95.904)">accuracy</text>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 72.046307 159.386553 
L 99.715728 127.931234 
L 127.38515 122.212085 
L 182.723993 85.609532 
L 265.732257 44.43166 
L 376.409943 15.264 
" clip-path="url(#pa154a6d0a8)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m98ae7f93d8" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#pa154a6d0a8)">
     <use xlink:href="#m98ae7f93d8" x="72.046307" y="159.386553" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="99.715728" y="127.931234" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="127.38515" y="122.212085" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="182.723993" y="85.609532" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="265.732257" y="44.43166" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="376.409943" y="15.264" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 72.046307 171.968681 
L 99.715728 144.516766 
L 127.38515 162.818043 
L 182.723993 169.681021 
L 265.732257 176.544 
L 376.409943 176.544 
" clip-path="url(#pa154a6d0a8)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m43dc4bf304" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#pa154a6d0a8)">
     <use xlink:href="#m43dc4bf304" x="72.046307" y="171.968681" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="99.715728" y="144.516766" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="127.38515" y="162.818043" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="182.723993" y="169.681021" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="265.732257" y="176.544" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="376.409943" y="176.544" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 56.828125 184.608 
L 56.828125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 391.628125 184.608 
L 391.628125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 56.828125 184.608 
L 391.628125 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 56.828125 7.2 
L 391.628125 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 63.828125 45.201563 
L 119.103125 45.201563 
Q 121.103125 45.201563 121.103125 43.201563 
L 121.103125 14.2 
Q 121.103125 12.2 119.103125 12.2 
L 63.828125 12.2 
Q 61.828125 12.2 61.828125 14.2 
L 61.828125 43.201563 
Q 61.828125 45.201563 63.828125 45.201563 
L 63.828125 45.201563 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_17">
     <path d="M 65.828125 20.298438 
L 75.828125 20.298438 
L 85.828125 20.298438 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m98ae7f93d8" x="75.828125" y="20.298438" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="93.828125" y="23.798438" transform="rotate(-0 93.828125 23.798438)">train</text>
    </g>
    <g id="line2d_18">
     <path d="M 65.828125 35.299219 
L 75.828125 35.299219 
L 85.828125 35.299219 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m43dc4bf304" x="75.828125" y="35.299219" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="93.828125" y="38.799219" transform="rotate(-0 93.828125 38.799219)">test</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pa154a6d0a8">
   <rect x="56.828125" y="7.2" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Eğitim skoru derinlikle tırmanıyor, test 2'de tepe yapıp düşüyor.</figcaption>
</figure>

- `validation_curve` tek bir ayarın (`param_name`) değerlerini çapraz
  doğrulamayla dener. Izgara aramanın tek ayarlı, eğitim skorunu da veren
  hâli.
- Derinlik arttıkça eğitim skoru 0,841'den 0,999'a tırmanıyor; test 2'de en
  yüksek (0,857), sonra düşüyor. İki eğrinin açıldığı yer aşırı öğrenmenin
  başladığı yer.

## Özet

- Sınıflandırmada `StratifiedKFold`; sıralı olabilecek veride
  `shuffle=True`; aynı kişi/cihaz birden fazla satırdaysa `GroupKFold`;
  zamanda `TimeSeriesSplit`.
- Bölücü nesnesi `cv=` ile her araca verilir: `cross_val_score`,
  `cross_validate`, `GridSearchCV`, `learning_curve`.
- `cross_validate` birkaç ölçü ve eğitim skoru; `learning_curve` veri
  miktarının, `validation_curve` tek bir ayarın etkisi.
