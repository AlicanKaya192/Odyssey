# Modeli Açıklamak

Orman ya da boosting iyi tahmin eder ama içini okumak zordur: yüzlerce
ağaç, binlerce bölme. "Model neye bakıyor? Yaş fiyatı nasıl etkiliyor?"
sorularına scikit-learn'ün `sklearn.inspection` modülü iki araçla cevap
veriyor: **permütasyon önemi** (hangi sütun ne kadar işe yarıyor) ve
**kısmi bağımlılık** (bir sütun değişince tahmin nasıl değişiyor). Bu bölüm
ikisini, tuzaklarıyla birlikte anlatıyor.

## Permütasyon önemi

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
df = pd.DataFrame({
    "area": rng.uniform(40, 200, 2000),
    "age": rng.uniform(0, 50, 2000),
    "floor": rng.integers(0, 15, 2000),
    "row_id": rng.permutation(2000),           # anlamsız
    "coin": rng.integers(0, 2, 2000),          # anlamsız
})
df["price"] = (df["area"] - 0.1 * (df["age"] - 25) ** 2
               + 8 * np.minimum(df["floor"], 8) + rng.normal(0, 15, 2000))
X, y = df.drop(columns="price"), df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
rf = RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1)
rf.fit(X_train, y_train)
perm = permutation_importance(rf, X_test, y_test, n_repeats=10,
                              random_state=0, n_jobs=-1)
print(round(rf.score(X_test, y_test), 3))
for name, impurity, mean, std in zip(X.columns, rf.feature_importances_,
                                     perm.importances_mean, perm.importances_std):
    print(f"{name:7} {impurity:6.3f} {mean:6.3f} {std:5.3f}")
```

```text
0.91
area     0.701  1.390 0.060
age      0.114  0.177 0.012
floor    0.164  0.282 0.019
row_id   0.019 -0.000 0.001
coin     0.003 -0.000 0.001
```

- Fiyatı üç sütun belirliyor: alan (doğrusal), yaş (25 yaşta en yüksek, ters
  U) ve kat (8. kata kadar artıyor, sonra sabit). `row_id` ve `coin`
  rastgele.
- **Permütasyon önemi:** test verisinde bir sütunun değerleri karıştırılır
  (satırlar arasında yer değiştirir), model yeniden skorlanır. Skor ne kadar
  düşerse sütun o kadar işe yarıyordur. Bu 10 kez tekrarlanır
  (`n_repeats`); ortalama ve sapma verilir.
- Alanı karıştırınca R² 1,39 düşüyor (0,91'den eksiye). Kat 0,282, yaş
  0,177. `row_id` ve `coin` 0: karıştırmak hiçbir şey değiştirmedi. (`-0.000`
  küçük rastgele dalgalanma.)
- İkinci sütun ormanın kendi önemi (`feature_importances_`): `row_id`'e
  0,019 vermiş, `coin`'den fazla, çünkü çok değerli sütunda eğitim
  verisinin gürültüsüne uyan kesimler buluyor. Permütasyon önemi **görülmemiş
  veride** ölçtüğü için bu yanılgıya düşmüyor.
- Permütasyon önemi her modelde çalışır (model nasıl kurulmuş olursa olsun):
  yalnızca `predict` ve bir skor gerekir.

## Kısmi bağımlılık ve tam sayı sütunu

```python
from sklearn.inspection import partial_dependence

try:
    partial_dependence(rf, X_test, ["floor"])
except ValueError as err:
    print(str(err).split(".")[0])
X_float = X_test.astype({"floor": float})
result = partial_dependence(rf, X_float, ["floor"], grid_resolution=15)
print(result["grid_values"][0].astype(int).tolist())
print(result["average"][0].round().astype(int).tolist())
```

```text
The column 'floor' contains integer data
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
[106, 108, 117, 124, 130, 137, 148, 159, 162, 163, 163, 164, 163, 163, 163]
```

- **Kısmi bağımlılık:** bütün test satırlarında `floor`'u önce 0, sonra 1,
  ... 14 yapıp her seferinde tahminlerin ortalaması alınır. Sonuç "kat
  değişince, diğer her şey aynıyken, ortalama tahmin nasıl değişir".
- Bu sürümde **tam sayı** türündeki sütunda hata veriyor (yuvarlama
  sorunlarına karşı). Çaresi sütunu `float`'a çevirmek:
  `astype({"floor": float})`.
- Sonuç veriyi üreten kuralı buluyor: 0'dan 8. kata kadar tahmin 106'dan
  162'ye çıkıyor, sonra 163 civarında düz kalıyor. Model "8. kattan sonra
  kat fark etmez"i kendisi öğrenmiş.

## Kısmi bağımlılığı çizmek

```python
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay

fig, axes = plt.subplots(1, 2, figsize=(8, 3.2), sharey=True)
PartialDependenceDisplay.from_estimator(rf, X_float, ["age", "floor"], ax=axes)
age = partial_dependence(rf, X_float, ["age"], grid_resolution=6)
print(age["grid_values"][0].round().astype(int).tolist())
print(age["average"][0].round().astype(int).tolist())
```

```text
[3, 12, 21, 30, 39, 48]
[118, 150, 160, 160, 147, 115]
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="500.888281pt" height="222.808781pt" viewBox="0 0 500.888281 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 500.888281 222.808781 
L 500.888281 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 184.608 
L 250.197372 184.608 
L 250.197372 7.2 
L 47.288281 7.2 
L 47.288281 184.608 
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
       <use xlink:href="#m15aed4d867" x="86.633686" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="86.633686" y="199.205656" transform="rotate(-0 86.633686 199.205656)">10</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="127.604871" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="127.604871" y="199.205656" transform="rotate(-0 127.604871 199.205656)">20</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="168.576057" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="168.576057" y="199.205656" transform="rotate(-0 168.576057 199.205656)">30</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="209.547242" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="209.547242" y="199.205656" transform="rotate(-0 209.547242 199.205656)">40</text>
     </g>
    </g>
    <g id="text_5">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="148.742827" y="213.205656" transform="rotate(-0 148.742827 213.205656)">age</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_5">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="165.346989" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="169.145817" transform="rotate(-0 40.288281 169.145817)">110</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="137.473724" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="141.272552" transform="rotate(-0 40.288281 141.272552)">120</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="109.60046" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="113.399288" transform="rotate(-0 40.288281 113.399288)">130</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="81.727196" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="85.526024" transform="rotate(-0 40.288281 85.526024)">140</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="53.853932" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="57.65276" transform="rotate(-0 40.288281 57.65276)">150</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="25.980667" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="29.779496" transform="rotate(-0 40.288281 29.779496)">160</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="95.904" transform="rotate(-90 14.798438 95.904)">Partial dependence</text>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 56.511422 142.0232 
L 58.374682 139.691361 
L 60.237943 138.087743 
L 62.101204 135.714361 
L 63.964465 131.708241 
L 65.827725 126.63983 
L 67.690986 120.505662 
L 69.554247 114.366175 
L 71.417507 110.495937 
L 73.280768 106.930806 
L 75.144029 100.177455 
L 77.00729 89.497063 
L 78.87055 85.056281 
L 80.733811 81.092628 
L 82.597072 78.09608 
L 84.460332 73.798618 
L 86.323593 68.547802 
L 88.186854 64.73892 
L 90.050114 60.87461 
L 91.913375 58.564934 
L 93.776636 49.844813 
L 95.639897 48.868202 
L 97.503157 47.176316 
L 99.366418 44.890096 
L 101.229679 43.323248 
L 103.092939 41.171933 
L 104.9562 38.762692 
L 106.819461 38.011378 
L 108.682722 36.539655 
L 110.545982 34.825699 
L 112.409243 33.008377 
L 114.272504 32.320181 
L 116.135764 31.47899 
L 117.999025 30.574968 
L 119.862286 29.732872 
L 121.725546 29.233894 
L 123.588807 28.749697 
L 125.452068 28.345382 
L 127.315329 28.225956 
L 129.178589 26.64161 
L 131.04185 26.233124 
L 132.905111 25.322939 
L 134.768371 25.118294 
L 136.631632 24.709064 
L 138.494893 24.399082 
L 140.358154 24.452399 
L 142.221414 24.138973 
L 144.084675 24.327785 
L 145.947936 24.116113 
L 147.811196 24.040627 
L 149.674457 24.532263 
L 151.537718 24.584972 
L 153.400978 24.816004 
L 155.264239 24.687979 
L 157.1275 25.194912 
L 158.990761 25.538375 
L 160.854021 25.502852 
L 162.717282 25.842314 
L 164.580543 25.868028 
L 166.443803 26.709116 
L 168.307064 27.309968 
L 170.170325 27.567213 
L 172.033586 28.33743 
L 173.896846 29.268373 
L 175.760107 29.759481 
L 177.623368 32.068632 
L 179.486628 33.79672 
L 181.349889 33.640575 
L 183.21315 33.442174 
L 185.07641 34.09563 
L 186.939671 37.508142 
L 188.802932 38.620117 
L 190.666193 40.419125 
L 192.529453 46.407938 
L 194.392714 49.70958 
L 196.255975 51.710476 
L 198.119235 53.211295 
L 199.982496 55.599812 
L 201.845757 57.163406 
L 203.709018 60.882351 
L 205.572278 66.713877 
L 207.435539 69.484649 
L 209.2988 73.696556 
L 211.16206 74.828411 
L 213.025321 77.767057 
L 214.888582 80.464786 
L 216.751842 85.284758 
L 218.615103 89.479588 
L 220.478364 96.991997 
L 222.341625 102.520672 
L 224.204885 105.442867 
L 226.068146 111.118253 
L 227.931407 115.615683 
L 229.794667 118.80428 
L 231.657928 127.632663 
L 233.521189 133.992286 
L 235.38445 144.359409 
L 237.24771 146.711016 
L 239.110971 148.526677 
L 240.974232 151.805485 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="LineCollection_1">
    <path d="M 67.297089 184.608 
L 67.297089 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 86.904295 184.608 
L 86.904295 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 105.604049 184.608 
L 105.604049 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 120.536819 184.608 
L 120.536819 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 138.992637 184.608 
L 138.992637 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 159.89656 184.608 
L 159.89656 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 184.013571 184.608 
L 184.013571 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 205.338406 184.608 
L 205.338406 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 229.127144 184.608 
L 229.127144 175.7376 
" clip-path="url(#p9ab65b44be)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
   </g>
   <g id="patch_3">
    <path d="M 47.288281 184.608 
L 47.288281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 250.197372 184.608 
L 250.197372 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 47.288281 184.608 
L 250.197372 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 7.2 
L 250.197372 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 290.77919 184.608 
L 493.688281 184.608 
L 493.688281 7.2 
L 290.77919 7.2 
L 290.77919 184.608 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="300.002331" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="300.002331" y="199.205656" transform="rotate(-0 300.002331 199.205656)">0</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="365.881906" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="365.881906" y="199.205656" transform="rotate(-0 365.881906 199.205656)">5</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="431.761481" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="431.761481" y="199.205656" transform="rotate(-0 431.761481 199.205656)">10</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="392.233736" y="213.206438" transform="rotate(-0 392.233736 213.206438)">floor</text>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_7">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="165.346989" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="137.473724" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="109.60046" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="81.727196" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="53.853932" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="290.77919" y="25.980667" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="280.876847" y="95.904" transform="rotate(-90 280.876847 95.904)">Partial dependence</text>
    </g>
   </g>
   <g id="line2d_21">
    <path d="M 300.002331 176.544 
L 313.178246 170.314592 
L 326.354161 146.898413 
L 339.530076 126.841213 
L 352.705991 109.034712 
L 365.881906 90.951243 
L 379.057821 59.459744 
L 392.233736 29.090979 
L 405.409651 19.615237 
L 418.585566 17.457928 
L 431.761481 16.600028 
L 444.937396 15.264 
L 458.113311 16.410573 
L 471.289226 16.394227 
L 484.465141 16.626268 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="LineCollection_2">
    <path d="M 313.178246 184.608 
L 313.178246 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 339.530076 184.608 
L 339.530076 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 352.705991 184.608 
L 352.705991 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 379.057821 184.608 
L 379.057821 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 392.233736 184.608 
L 392.233736 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 418.585566 184.608 
L 418.585566 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 431.761481 184.608 
L 431.761481 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 458.113311 184.608 
L 458.113311 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
    <path d="M 471.289226 184.608 
L 471.289226 175.7376 
" clip-path="url(#p4976ef00ed)" style="fill: none; stroke: #000000; stroke-width: 1.5"/>
   </g>
   <g id="patch_8">
    <path d="M 290.77919 184.608 
L 290.77919 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 493.688281 184.608 
L 493.688281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 290.77919 184.608 
L 493.688281 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 290.77919 7.2 
L 493.688281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p9ab65b44be">
   <rect x="47.288281" y="7.2" width="202.909091" height="177.408"/>
  </clipPath>
  <clipPath id="p4976ef00ed">
   <rect x="290.77919" y="7.2" width="202.909091" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Yaşın etkisi ters U (tepe 25 civarı); katın etkisi 8. kata kadar artıp duruyor.</figcaption>
</figure>

- `PartialDependenceDisplay.from_estimator` aynı hesabı yapıp çizer. Altta
  küçük çizgiler (çentikler) verinin nerede yoğun olduğunu gösterir; uçlarda
  veri azsa eğri güvenilmezdir.
- Yaş eğrisi ters U: 3 yaşta 118, 21–30 yaşta 160, 48 yaşta 115. Veriyi
  üreten kural 25 yaşta tepe yapıyordu. Doğrusal bir model bunu tek bir
  katsayıyla gösteremezdi.
- Kısmi bağımlılık bir **ortalama**; herkes için aynı etki demek değildir
  (bkz. "Herkes İçin Aynı mı?" notu).

## Birbirine bağlı sütunlar

```python
X2 = X.assign(area_copy=X["area"] + rng.normal(0, 2, 2000))
X2_train, X2_test = X2.loc[X_train.index], X2.loc[X_test.index]
rf2 = RandomForestRegressor(n_estimators=200, random_state=0, n_jobs=-1)
rf2.fit(X2_train, y_train)
perm2 = permutation_importance(rf2, X2_test, y_test, n_repeats=10,
                               random_state=0, n_jobs=-1)
print(round(rf2.score(X2_test, y_test), 3))
for name in ["area", "area_copy", "floor"]:
    print(name, round(perm2.importances_mean[X2.columns.get_loc(name)], 3))
```

```text
0.911
area 0.588
area_copy 0.188
floor 0.282
```

- Alanın neredeyse aynısı olan bir sütun ekledik. Model skoru değişmedi
  (0,911), ama alanın önemi 1,39'dan 0,588'e düştü; kopya 0,188 aldı.
- Bir sütunu karıştırınca model aynı bilgiyi kopyasından alabiliyor; iki
  sütunun da önemi küçük görünüyor. İkisinin toplamı bile tek başına alanın
  önemine yetmiyor.
- Ders: permütasyon önemi düşük diye bir sütunun bilgisiz olduğu
  söylenemez; önce sütunlar arasındaki bağlantıya (korelasyon, VIF) bakılır.
  Bağlı sütunlar birlikte karıştırılarak ya da biri çıkarılarak
  değerlendirilir.

## Özet

- `permutation_importance(model, X_test, y_test)`: görülmemiş veride, her
  modelde çalışan önem; eğitimdeki saflık önemi yanıltabilir.
- `partial_dependence` / `PartialDependenceDisplay`: bir sütunun ortalama
  etkisinin biçimi. Tam sayı sütunu önce `float`.
- Birbirine bağlı sütunlarda permütasyon önemi bölünür ve küçülür.
- Bunların hiçbiri neden-sonuç söylemez: model **neye baktığını** gösterir,
  dünyanın nasıl işlediğini değil.
