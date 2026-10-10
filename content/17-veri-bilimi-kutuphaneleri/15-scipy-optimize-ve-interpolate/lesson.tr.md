# scipy.optimize ve interpolate

Birçok veri sorusu aslında bir **en iyileme** sorusudur: kârı en büyük yapan
fiyat, veriye en iyi uyan eğrinin katsayıları, bir denklemi sıfır yapan oran,
sınırlı kaynakla en çok üretim. Makine öğrenmesindeki "eğitim" de bir hata
fonksiyonunu en küçük yapmaktır. `scipy.optimize` bu soruların hazır
çözücülerini verir. Bölümün sonunda `scipy.interpolate` ile ölçümlerin
**arasını** doldurmayı göreceğiz.

## Tek değişkenli en iyileme

```python
from scipy import optimize


def cost(price):
    demand = 1000 - 8 * price
    return -(price - 20) * demand


res = optimize.minimize_scalar(cost, bounds=(20, 125), method="bounded")
print(round(float(res.x), 2), round(float(-res.fun), 1), res.success)
```

```text
72.5 22050.0 True
```

- Birim maliyeti 20 olan bir ürün; fiyat arttıkça talep düşüyor. Kâr =
  (fiyat − 20) × talep.
- scipy'nin çözücüleri **en küçüğü** arar. En büyüğü bulmak için fonksiyonun
  eksisi en küçüklenir: `cost` kârın eksisi, sonuçta `-res.fun` kâr.
- `bounds=(20, 125)` aramayı anlamlı aralıkla sınırlar (maliyetin altında
  satılmaz, 125'te talep sıfır). En iyi fiyat 72,5, kâr 22 050.
- Sonuç bir nesne: `x` çözüm, `fun` o noktadaki değer, `success` çözücünün
  başarılı bitip bitmediği. **`success`'e her zaman bak.**

## Çok değişkenli en iyileme

```python
import numpy as np
from scipy import optimize


def rosen(p):
    x, y = p
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


res = optimize.minimize(rosen, x0=[-1.0, 2.0])
print(res.x.round(4).tolist(), res.success, res.nit)
res2 = optimize.minimize(rosen, x0=[-1.0, 2.0], method="Nelder-Mead")
print(res2.x.round(3).tolist(), res2.nfev > res.nfev)
```

```text
[1.0, 1.0] True 35
[1.0, 1.0] True
```

- `minimize(f, x0=başlangıç)`: `f` bir **dizi** alır, tek sayı döndürür.
  Rosenbrock fonksiyonu en iyileme yöntemlerini sınamak için kullanılan dar,
  kıvrık bir vadi; en küçüğü (1, 1).
- Varsayılan yöntem (BFGS) eğimi kullanır: 35 adımda buldu. `Nelder-Mead`
  eğim kullanmaz; fonksiyon türevlenemiyorsa işe yarar ama çok daha fazla
  fonksiyon çağrısı gerekti.
- Makine öğrenmesi modellerinin eğitimi aynı işin büyük ölçeklisidir:
  binlerce katsayı, bir hata fonksiyonu, eğimle aşağı inmek.

## Başlangıç noktası önemlidir

```python
import numpy as np
from scipy import optimize


def bumpy(x):
    return np.sin(3 * x[0]) + 0.1 * x[0] ** 2


for start in [-2.0, 0.0, 2.0]:
    res = optimize.minimize(bumpy, x0=[start])
    print(start, round(float(res.x[0]), 3), round(float(res.fun), 3))
results = [optimize.minimize(bumpy, x0=[s]) for s in np.linspace(-5, 5, 11)]
best = min(results, key=lambda r: r.fun)
print(round(float(best.x[0]), 3), round(float(best.fun), 3))
```

```text
-2.0 -2.561 -0.33
0.0 -0.512 -0.973
2.0 1.537 -0.759
-0.512 -0.973
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="469.19952pt" height="224.39819pt" viewBox="0 0 469.19952 224.39819" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39819 
L 469.19952 224.39819 
L 469.19952 -0 
L 0 -0 
L 0 224.39819 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 52.483594 186.19819 
L 461.99952 186.19819 
L 461.99952 9.026854 
L 52.483594 9.026854 
L 52.483594 186.19819 
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
       <use xlink:href="#m15aed4d867" x="71.097954" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="71.097954" y="200.795847" transform="rotate(-0 71.097954 200.795847)">−4</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="117.633855" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="117.633855" y="200.795847" transform="rotate(-0 117.633855 200.795847)">−3</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="164.169755" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="164.169755" y="200.795847" transform="rotate(-0 164.169755 200.795847)">−2</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="210.705656" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.705656" y="200.795847" transform="rotate(-0 210.705656 200.795847)">−1</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="257.241557" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="257.241557" y="200.795847" transform="rotate(-0 257.241557 200.795847)">0</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="303.777458" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="303.777458" y="200.795847" transform="rotate(-0 303.777458 200.795847)">1</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="350.313358" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.313358" y="200.795847" transform="rotate(-0 350.313358 200.795847)">2</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="396.849259" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="396.849259" y="200.795847" transform="rotate(-0 396.849259 200.795847)">3</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="443.38516" y="186.19819" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="443.38516" y="200.795847" transform="rotate(-0 443.38516 200.795847)">4</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="257.241557" y="214.795847" transform="rotate(-0 257.241557 214.795847)">x</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_10">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="179.435632" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="183.23446" transform="rotate(-0 45.483594 183.23446)">−1.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="155.373231" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="159.17206" transform="rotate(-0 45.483594 159.17206)">−0.5</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="131.310831" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="135.109659" transform="rotate(-0 45.483594 135.109659)">0.0</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="107.24843" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="111.047258" transform="rotate(-0 45.483594 111.047258)">0.5</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="83.18603" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="86.984858" transform="rotate(-0 45.483594 86.984858)">1.0</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="59.123629" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="62.922457" transform="rotate(-0 45.483594 62.922457)">1.5</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="35.061229" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="38.860057" transform="rotate(-0 45.483594 38.860057)">2.0</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="52.483594" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="45.483594" y="14.797656" transform="rotate(-0 45.483594 14.797656)">2.5</text>
     </g>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="97.612522" transform="rotate(-90 14.798438 97.612522)">bumpy(x)</text>
    </g>
   </g>
   <g id="line2d_18">
    <path d="M 71.097954 28.488684 
L 72.964055 25.337754 
L 74.830157 22.612356 
L 76.696258 20.373866 
L 78.562359 18.676398 
L 79.49541 18.045277 
L 80.42846 17.566022 
L 81.361511 17.243024 
L 82.294562 17.080097 
L 83.227612 17.080461 
L 84.160663 17.246732 
L 85.093714 17.580913 
L 86.026764 18.084383 
L 86.959815 18.757896 
L 87.892866 19.601577 
L 88.825916 20.614922 
L 90.692017 23.145453 
L 92.558119 26.332988 
L 94.42422 30.151306 
L 96.290321 34.564848 
L 98.156423 39.529223 
L 100.022524 44.991856 
L 102.821676 53.986968 
L 105.620828 63.737462 
L 110.286081 80.966674 
L 115.884385 101.678522 
L 118.683537 111.399994 
L 121.482689 120.347766 
L 123.34879 125.765761 
L 125.214891 130.672568 
L 127.080992 135.013201 
L 128.947094 138.740631 
L 130.813195 141.816473 
L 132.679296 144.211535 
L 133.612347 145.147272 
L 134.545398 145.906242 
L 135.478448 146.487547 
L 136.411499 146.890918 
L 137.34455 147.116716 
L 138.2776 147.165929 
L 139.210651 147.04017 
L 140.143701 146.741672 
L 141.076752 146.273278 
L 142.009803 145.638431 
L 142.942853 144.841163 
L 144.808955 142.778342 
L 146.675056 140.128222 
L 148.541157 136.942479 
L 150.407259 133.280306 
L 152.27336 129.207557 
L 155.072512 122.486468 
L 158.804714 112.792114 
L 165.336069 95.660504 
L 168.135221 88.97216 
L 170.001322 84.924754 
L 171.867423 81.287895 
L 173.733525 78.124502 
L 175.599626 75.490423 
L 177.465727 73.433633 
L 178.398778 72.634388 
L 179.331828 71.99354 
L 180.264879 71.514583 
L 181.19793 71.200411 
L 182.13098 71.053307 
L 183.064031 71.074939 
L 183.997082 71.266346 
L 184.930132 71.627943 
L 185.863183 72.159512 
L 186.796233 72.86021 
L 187.729284 73.728565 
L 189.595385 75.959269 
L 191.461487 78.827601 
L 193.327588 82.300098 
L 195.193689 86.334341 
L 197.059791 90.879565 
L 199.858942 98.525925 
L 202.658094 106.964503 
L 206.390297 119.010869 
L 213.854702 143.385166 
L 216.653854 151.772896 
L 219.453006 159.342426 
L 221.319107 163.819374 
L 223.185208 167.769488 
L 225.05131 171.139864 
L 226.917411 173.885756 
L 228.783512 175.97122 
L 229.716563 176.757596 
L 230.649614 177.369634 
L 231.582664 177.805524 
L 232.515715 178.064084 
L 233.448766 178.144754 
L 234.381816 178.047608 
L 235.314867 177.773346 
L 236.247917 177.323297 
L 237.180968 176.69941 
L 238.114019 175.904249 
L 239.047069 174.940985 
L 240.913171 172.525783 
L 242.779272 169.490785 
L 244.645373 165.881707 
L 246.511475 161.752338 
L 248.377576 157.163767 
L 251.176728 149.569082 
L 254.90893 138.508308 
L 263.306386 112.889102 
L 266.105538 105.108689 
L 268.90469 98.138681 
L 270.770791 94.053315 
L 272.636892 90.485144 
L 274.502994 87.48401 
L 276.369095 85.091337 
L 277.302146 84.133665 
L 278.235196 83.339529 
L 279.168247 82.711491 
L 280.101298 82.251503 
L 281.034348 81.960891 
L 281.967399 81.840358 
L 282.900449 81.889974 
L 283.8335 82.109184 
L 284.766551 82.496802 
L 285.699601 83.05102 
L 286.632652 83.769413 
L 287.565703 84.648951 
L 289.431804 86.876356 
L 291.297905 89.697291 
L 293.164007 93.067008 
L 295.030108 96.932606 
L 296.896209 101.233787 
L 299.695361 108.354575 
L 303.427564 118.706235 
L 310.891969 139.918191 
L 313.691121 147.196335 
L 315.557222 151.629786 
L 317.423323 155.644814 
L 319.289424 159.17628 
L 321.155526 162.16581 
L 323.021627 164.562641 
L 323.954678 165.525194 
L 324.887728 166.324351 
L 325.820779 166.956215 
L 326.75383 167.417479 
L 327.68688 167.705438 
L 328.619931 167.818001 
L 329.552982 167.753697 
L 330.486032 167.511682 
L 331.419083 167.091739 
L 332.352133 166.494281 
L 333.285184 165.720351 
L 334.218235 164.771612 
L 336.084336 162.359459 
L 337.950437 159.283348 
L 339.816539 155.57818 
L 341.68264 151.287726 
L 343.548741 146.463991 
L 346.347893 138.36046 
L 349.147045 129.420179 
L 352.879248 116.639531 
L 361.276703 87.47809 
L 364.075855 78.613781 
L 366.875007 70.602279 
L 368.741108 65.843348 
L 370.60721 61.615914 
L 372.473311 57.967602 
L 374.339412 54.937446 
L 376.205514 52.55532 
L 377.138564 51.613991 
L 378.071615 50.841507 
L 379.004666 50.238859 
L 379.937716 49.806406 
L 380.870767 49.543879 
L 381.803817 49.45038 
L 382.736868 49.524386 
L 383.669919 49.763755 
L 384.602969 50.165731 
L 385.53602 50.726956 
L 386.469071 51.443483 
L 388.335172 53.323795 
L 390.201273 55.76388 
L 392.067374 58.71264 
L 393.933476 62.1114 
L 395.799577 65.894755 
L 398.598729 72.133851 
L 402.330932 81.097504 
L 407.929235 94.589414 
L 410.728387 100.751929 
L 412.594489 104.463036 
L 414.46059 107.771491 
L 416.326691 110.610734 
L 418.192792 112.920764 
L 420.058894 114.649007 
L 420.991944 115.280748 
L 421.924995 115.751073 
L 422.858046 116.055816 
L 423.791096 116.1914 
L 424.724147 116.154841 
L 425.657198 115.943768 
L 426.590248 115.556425 
L 427.523299 114.991679 
L 428.456349 114.249026 
L 429.3894 113.32859 
L 430.322451 112.231127 
L 432.188552 109.511261 
L 434.054653 106.107879 
L 435.920755 102.049091 
L 437.786856 97.372257 
L 439.652957 92.123447 
L 441.519058 86.356774 
L 443.38516 80.133614 
L 443.38516 80.133614 
" clip-path="url(#p8dfdaae91d)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_19">
    <defs>
     <path id="me6745b22d4" d="M 0 3 
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
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#me6745b22d4" x="164.169755" y="98.614095" style="fill-opacity: 0; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="line2d_20">
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
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#m43dc4bf304" x="138.072104" y="147.17018" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="line2d_21">
    <defs>
     <path id="m9f10827d7b" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #2ca02c"/>
    </defs>
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#m9f10827d7b" x="257.241557" y="131.310831" style="fill-opacity: 0; stroke: #2ca02c"/>
    </g>
   </g>
   <g id="line2d_22">
    <defs>
     <path id="m70db61e8b1" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #2ca02c"/>
    </defs>
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#m70db61e8b1" x="233.405216" y="178.144948" style="fill: #2ca02c; stroke: #2ca02c"/>
    </g>
   </g>
   <g id="line2d_23">
    <defs>
     <path id="m216d7f1fe2" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #d62728"/>
    </defs>
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#m216d7f1fe2" x="350.313358" y="125.507726" style="fill-opacity: 0; stroke: #d62728"/>
    </g>
   </g>
   <g id="line2d_24">
    <defs>
     <path id="m4d7487b0a7" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #d62728"/>
    </defs>
    <g clip-path="url(#p8dfdaae91d)">
     <use xlink:href="#m4d7487b0a7" x="328.748151" y="167.819672" style="fill: #d62728; stroke: #d62728"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 52.483594 186.19819 
L 52.483594 9.026854 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 461.99952 186.19819 
L 461.99952 9.026854 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 52.483594 186.19819 
L 461.99952 186.19819 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 52.483594 9.026854 
L 461.99952 9.026854 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_7">
    <path d="M 163.221995 100.377454 
Q 151.120606 122.892741 139.813175 143.930824 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: round"/>
    <path d="M 143.468545 141.35434 
L 139.813175 143.930824 
L 139.945209 139.460638 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: round"/>
   </g>
   <g id="patch_8">
    <path d="M 256.335182 133.091694 
Q 245.324348 154.726 235.074199 174.865697 
" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linecap: round"/>
    <path d="M 238.670965 172.208015 
L 235.074199 174.865697 
L 235.106113 170.393675 
" style="fill: none; stroke: #2ca02c; stroke-width: 1.5; stroke-linecap: round"/>
   </g>
   <g id="patch_9">
    <path d="M 349.406472 127.287079 
Q 339.53186 146.66153 330.418787 164.541806 
" style="fill: none; stroke: #d62728; stroke-width: 1.5; stroke-linecap: round"/>
    <path d="M 334.017071 161.886179 
L 330.418787 164.541806 
L 330.453256 160.069803 
" style="fill: none; stroke: #d62728; stroke-width: 1.5; stroke-linecap: round"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p8dfdaae91d">
   <rect x="52.483594" y="9.026854" width="409.515926" height="177.171337"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Üç başlangıç (boş daire), üç farklı çukur (dolu daire). En derini ortadaki.</figcaption>
</figure>

- Bu fonksiyonun birden fazla çukuru var. Eğimle inen bir çözücü **başladığı
  yere en yakın** çukurda durur: üç başlangıç, üç farklı cevap. Üçü de
  `success=True` der; çözücü yalnızca bulunduğu çukurun dibinde olduğunu bilir.
- Basit bir önlem: birçok noktadan başlatıp en iyisini almak. 11 başlangıç
  içinden en derin çukur −0,512'de, değeri −0,973.

## Veriye eğri uydurmak: curve_fit

```python
import numpy as np
from scipy import optimize


def decay(t, a, k):
    return a * np.exp(-k * t)


rng = np.random.default_rng(13)
t = np.linspace(0, 10, 25)
y = decay(t, 80, 0.35) + rng.normal(0, 2, t.size)
params, cov = optimize.curve_fit(decay, t, y, p0=[50, 0.1])
errors = np.sqrt(np.diag(cov))
print(params.round(3).tolist(), errors.round(3).tolist())
print(round(float(np.log(2) / params[1]), 2))
```

```text
[79.985, 0.34] [1.599, 0.01]
2.04
```

- `curve_fit(model, x, y, p0=tahmin)` modelin parametrelerini, kareler
  toplamını en küçük yapacak şekilde bulur. Modelin ilk argümanı x, gerisi
  parametreler.
- Gürültülü veriden gerçek değerlere (80 ve 0,35) çok yakın sonuç çıktı:
  79,985 ve 0,34. `cov` belirsizliği verir; köşegeninin karekökü her
  parametrenin standart hatası (±1,6 ve ±0,01).
- `p0` başlangıç tahminidir. Doğrusal olmayan modellerde kötü bir başlangıç
  çözücüyü yanlış yere götürebilir (önceki başlık); kabaca doğru bir tahmin
  ver.
- Parametreden anlamlı bir sonuç türetmek: yarılanma süresi ln 2 / k = 2,04.

## Kök bulmak: root_scalar

```python
from scipy import optimize


def balance(rate):
    return 10_000 * (1 + rate) ** 5 - 15_000


sol = optimize.root_scalar(balance, bracket=[0.0, 0.5])
print(round(float(sol.root), 5), sol.converged, sol.iterations < 20)
print(abs(balance(sol.root)) < 1e-6)
try:
    optimize.root_scalar(balance, bracket=[0.2, 0.5])
except ValueError as error:
    print("ValueError:", error)
```

```text
0.08447 True True
True
ValueError: f(a) and f(b) must have different signs
```

- Soru: 10 000 lira 5 yılda 15 000 olsun; yıllık faiz ne olmalı? Denklemi
  `f(oran) = 0` biçiminde yazıp sıfır noktasını aratıyoruz: %8,447.
- `bracket=[a, b]` kökün bulunduğu aralık. Fonksiyonun iki uçta **zıt
  işaretli** olması gerekir; [0,2; 0,5] aralığında iki uç da pozitif, kök
  yok, çözücü hemen hata verir.

## Doğrusal programlama: linprog

```python
from scipy import optimize

profit = [-30, -50]
hours = [[2, 4], [3, 2]]
limit = [80, 90]
free = [(0, None), (0, None)]
res = optimize.linprog(profit, A_ub=hours, b_ub=limit, bounds=free)
print(res.x.round(2).tolist(), round(float(-res.fun), 1), res.status)
print((res.x @ [[2, 3], [4, 2]]).round(2).tolist())
```

```text
[25.0, 7.5] 1125.0 0
[80.0, 90.0]
```

- İki ürün: biri 30, öteki 50 kâr bırakıyor. Birinci makinede 80, ikincide
  90 saat var; ürünlerin makine başına saatleri `hours`. Kaçar tane
  üretmeli?
- Amaç ve kısıtlar **doğrusal** olunca `linprog` kesin en iyiyi bulur: 25 ve
  7,5 adet, kâr 1125. Yine en küçükleme yapar; kârın eksisi verilir.
- Son satır her makinenin kullanılan saati: 80 ve 90, ikisi de **tam dolu**.
  En iyi çözüm genellikle kısıtların kesiştiği bir köşededir.
- `status` 0 başarı demek. Tam sayı adet gerekiyorsa `integrality=[1, 1]`.

## Ara değer bulmak: interpolate

```python
import numpy as np
from scipy import interpolate

hours = np.array([0, 3, 6, 9, 12])
temp = np.array([12.0, 10.0, 15.0, 22.0, 25.0])
print(round(float(np.interp(7.5, hours, temp)), 2))
spline = interpolate.CubicSpline(hours, temp)
pchip = interpolate.PchipInterpolator(hours, temp)
print(round(float(spline(7.5)), 2), round(float(pchip(7.5)), 2))
fine = np.linspace(0, 12, 121)
print(round(float(spline(fine).min()), 2), round(float(pchip(fine).min()), 2))
print(round(float(np.interp(15, hours, temp)), 2), round(float(spline(15)), 2))
```

```text
18.5
18.61 18.7
9.65 10.0
25.0 17.75
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="469.19952pt" height="224.39952pt" viewBox="0 0 469.19952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 469.19952 224.39952 
L 469.19952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 50.465625 186.198739 
L 461.99952 186.198739 
L 461.99952 7.2 
L 50.465625 7.2 
L 50.465625 186.198739 
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
       <use xlink:href="#m15aed4d867" x="69.171711" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="69.171711" y="200.796395" transform="rotate(-0 69.171711 200.796395)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="131.525332" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="131.525332" y="200.796395" transform="rotate(-0 131.525332 200.796395)">2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="193.878952" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="193.878952" y="200.796395" transform="rotate(-0 193.878952 200.796395)">4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="256.232573" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="256.232573" y="200.796395" transform="rotate(-0 256.232573 200.796395)">6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="318.586193" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="318.586193" y="200.796395" transform="rotate(-0 318.586193 200.796395)">8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="380.939813" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="380.939813" y="200.796395" transform="rotate(-0 380.939813 200.796395)">10</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="443.293434" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="443.293434" y="200.796395" transform="rotate(-0 443.293434 200.796395)">12</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="256.232573" y="214.797176" transform="rotate(-0 256.232573 214.797176)">hour</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_8">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="174.354198" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="178.153026" transform="rotate(-0 43.465625 178.153026)">10.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="147.953595" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="151.752423" transform="rotate(-0 43.465625 151.752423)">12.5</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="121.552993" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="125.351821" transform="rotate(-0 43.465625 125.351821)">15.0</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="95.15239" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="98.951218" transform="rotate(-0 43.465625 98.951218)">17.5</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="68.751788" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="72.550616" transform="rotate(-0 43.465625 72.550616)">20.0</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="42.351185" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="46.150013" transform="rotate(-0 43.465625 46.150013)">22.5</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="15.950583" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="19.749411" transform="rotate(-0 43.465625 19.749411)">25.0</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="96.699369" transform="rotate(-90 14.797656 96.699369)">temperature</text>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 69.171711 153.233716 
L 161.292135 174.035798 
L 163.172144 174.088865 
L 255.292568 122.083658 
L 257.172577 120.810061 
L 349.293001 48.002772 
L 351.17301 47.153707 
L 443.293434 15.950583 
L 443.293434 15.950583 
" clip-path="url(#paad2e22ca5)" style="fill: none; stroke: #7f7f7f; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 69.171711 153.233716 
L 72.931728 156.141096 
L 76.691746 158.851203 
L 80.451763 161.367294 
L 84.21178 163.69263 
L 87.971798 165.830469 
L 91.731815 167.78407 
L 95.491832 169.556691 
L 99.25185 171.151592 
L 103.011867 172.572032 
L 106.771884 173.82127 
L 110.531902 174.902565 
L 114.291919 175.819175 
L 118.051936 176.57436 
L 121.811954 177.171378 
L 125.571971 177.613489 
L 129.331988 177.903951 
L 134.972014 178.062432 
L 140.61204 177.898036 
L 146.252066 177.421761 
L 151.892092 176.644607 
L 157.532118 175.577571 
L 163.172144 174.231654 
L 168.81217 172.617855 
L 174.452196 170.747171 
L 180.092222 168.630603 
L 185.732248 166.279149 
L 191.372274 163.703807 
L 197.0123 160.915578 
L 202.652326 157.92546 
L 210.17236 153.643597 
L 217.692395 149.048446 
L 225.21243 144.166078 
L 232.732464 139.022565 
L 240.252499 133.643978 
L 249.652542 126.629892 
L 259.052585 119.340233 
L 270.332637 110.309375 
L 287.252715 96.422627 
L 311.692828 76.358114 
L 322.97288 67.380386 
L 332.372923 60.153315 
L 341.772966 53.228957 
L 349.293001 47.952448 
L 356.813036 42.946862 
L 364.33307 38.246502 
L 369.973096 34.942174 
L 375.613122 31.843304 
L 381.253148 28.964366 
L 386.893174 26.319831 
L 392.5332 23.924172 
L 398.173226 21.79186 
L 403.813252 19.93737 
L 409.453278 18.375172 
L 415.093304 17.119739 
L 420.73333 16.185544 
L 424.493347 15.748359 
L 428.253365 15.464666 
L 432.013382 15.338755 
L 435.773399 15.374911 
L 439.533417 15.577425 
L 443.293434 15.950583 
L 443.293434 15.950583 
" clip-path="url(#paad2e22ca5)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_17">
    <path d="M 69.171711 153.233716 
L 74.811737 156.547581 
L 80.451763 159.498287 
L 86.091789 162.106675 
L 91.731815 164.393584 
L 97.371841 166.379854 
L 103.011867 168.086327 
L 108.651893 169.533841 
L 114.291919 170.743237 
L 119.931945 171.735355 
L 125.571971 172.531036 
L 133.092005 173.322393 
L 140.61204 173.850976 
L 148.132075 174.166183 
L 157.532118 174.335389 
L 165.052153 174.293785 
L 168.81217 173.953354 
L 172.572187 173.327909 
L 176.332205 172.4346 
L 180.092222 171.29058 
L 183.852239 169.913002 
L 187.612257 168.319019 
L 191.372274 166.525781 
L 195.132291 164.550443 
L 200.772317 161.283516 
L 206.412343 157.703344 
L 212.052369 153.867815 
L 219.572404 148.456612 
L 230.852456 139.981752 
L 244.012516 130.10417 
L 251.532551 124.731846 
L 264.692611 115.568487 
L 270.332637 111.177869 
L 275.972663 106.530788 
L 283.492698 100.030992 
L 294.77275 89.895883 
L 309.812819 76.348786 
L 317.332854 69.854753 
L 322.97288 65.213676 
L 328.612906 60.830502 
L 334.252932 56.760342 
L 339.892958 53.058306 
L 343.652975 50.822011 
L 347.412992 48.79015 
L 353.053018 46.076744 
L 366.213079 40.007154 
L 377.493131 35.072895 
L 386.893174 31.218083 
L 394.413209 28.339548 
L 401.933243 25.672056 
L 409.453278 23.241953 
L 416.973313 21.075585 
L 424.493347 19.199299 
L 430.133373 17.998298 
L 435.773399 16.986403 
L 441.413425 16.174727 
L 443.293434 15.950583 
L 443.293434 15.950583 
" clip-path="url(#paad2e22ca5)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: #1f77b4; stroke-width: 1.5"/>
   </g>
   <g id="line2d_18">
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
    <g clip-path="url(#paad2e22ca5)">
     <use xlink:href="#m98ae7f93d8" x="69.171711" y="153.233716" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="162.702142" y="174.354198" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="256.232573" y="121.552993" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="349.763003" y="47.631306" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="443.293434" y="15.950583" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_19">
    <path d="M 50.465625 174.354198 
L 461.99952 174.354198 
" clip-path="url(#paad2e22ca5)" style="fill: none; stroke-dasharray: 0.8,1.32; stroke-dashoffset: 0; stroke: #1f77b4; stroke-width: 0.8"/>
   </g>
   <g id="patch_3">
    <path d="M 50.465625 186.198739 
L 50.465625 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 461.99952 186.198739 
L 461.99952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 50.465625 186.198739 
L 461.99952 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 50.465625 7.2 
L 461.99952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 57.465625 75.203125 
L 148.154688 75.203125 
Q 150.154688 75.203125 150.154688 73.203125 
L 150.154688 14.2 
Q 150.154688 12.2 148.154688 12.2 
L 57.465625 12.2 
Q 55.465625 12.2 55.465625 14.2 
L 55.465625 73.203125 
Q 55.465625 75.203125 57.465625 75.203125 
L 57.465625 75.203125 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_20">
     <path d="M 59.465625 20.298438 
L 69.465625 20.298438 
L 79.465625 20.298438 
" style="fill: none; stroke: #7f7f7f; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="23.798438" transform="rotate(-0 87.465625 23.798438)">np.interp</text>
    </g>
    <g id="line2d_21">
     <path d="M 59.465625 35.299219 
L 69.465625 35.299219 
L 79.465625 35.299219 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="38.799219" transform="rotate(-0 87.465625 38.799219)">CubicSpline</text>
    </g>
    <g id="line2d_22">
     <path d="M 59.465625 50.3 
L 69.465625 50.3 
L 79.465625 50.3 
" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: #1f77b4; stroke-width: 1.5"/>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="53.8" transform="rotate(-0 87.465625 53.8)">Pchip</text>
    </g>
    <g id="line2d_23">
     <g>
      <use xlink:href="#m98ae7f93d8" x="69.465625" y="65.300781" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_20">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="68.800781" transform="rotate(-0 87.465625 68.800781)">measured</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="paad2e22ca5">
   <rect x="50.465625" y="7.2" width="411.533895" height="178.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Spline 0–3 arasında en küçük ölçümün (noktalı çizgi) altına iniyor; Pchip inmiyor.</figcaption>
</figure>

- Sıcaklık 3 saatte bir ölçülmüş; 7,5'teki değer?
  `np.interp` iki komşu nokta arasında düz çizgi çeker: 18,5.
- `CubicSpline` noktalardan **yumuşak** bir eğri geçirir (18,61). Ama
  yumuşaklık bedelsiz değil: eğri 0–3 arasında en küçük ölçümün (10) **altına**
  iniyor, 9,65. Hiç ölçülmemiş bir değer üretti.
- `PchipInterpolator` aşmayan bir eğri: ölçümler arasında yeni tepe ya da
  çukur üretmez, en küçük değeri 10,0'da kalır. Fiziksel sınırı olan veride
  (yüzde, stok, sıcaklık) daha güvenli.
- **Aralığın dışı** başka bir sorudur. 15. saat için `np.interp` son değeri
  tekrarlar (25), spline eğrisini uzatır (17,75). İkisi de tahmin değil,
  varsayımdır; interpolasyon ölçümlerin arası içindir.

## Özet

- scipy en küçüğü arar; en büyüğü bulmak için eksisini ver. `success`'e bak.
- `minimize_scalar` (tek değişken, `bounds`), `minimize` (çok değişken,
  `x0`). Çok çukurlu fonksiyonda birçok başlangıç dene.
- `curve_fit` model parametreleri ve belirsizlikleri (`cov`) verir.
- `root_scalar` için zıt işaretli bir `bracket`; `linprog` doğrusal kısıtlı
  en iyi köşe.
- `np.interp` doğrusal; `CubicSpline` yumuşak ama aşabilir; `Pchip` aşmaz.
  Aralığın dışına çıkma.
