# Bayesçi Bakışa Giriş

Bu modül boyunca **frekansçı** (frequentist) istatistik kullandık: "H₀ doğru
olsaydı bu veri ne kadar şaşırtıcı olurdu?" diye sorduk ve p değeri,
güven aralığı hesapladık. Ekipler ise çoğu zaman başka bir şey sorar: "B'nin
A'dan iyi olma **olasılığı** ne?" Bu soruyu doğrudan cevaplayan yaklaşım
**Bayesçi** (Bayesian) istatistiktir. Bu bölüm onun temel fikrini ve A/B
testindeki kullanımını gösteriyor.

## Bayes teoremi: yeni bilgiyle inancı güncellemek

$$P(H \mid D) = \frac{P(D \mid H) \, P(H)}{P(D)}$$

- $P(H)$: veriden **önceki** inanç, **önsel** (prior).
- $P(D \mid H)$: H doğruysa bu verinin olasılığı, **olabilirlik**
  (likelihood).
- $P(H \mid D)$: veriyi gördükten **sonraki** inanç, **sonsal**
  (posterior).

p Değeri ve Yanlış Yorumları bölümünde benzetimle bir şey görmüştük: fikirlerin çoğu işe
yaramıyorsa "anlamlı" çıkan sonuçların önemli bir kısmı yanlış alarmdır. Bu,
Bayes teoreminin ta kendisi. "Anlamlı çıktı" verisi geldiğinde fikrin
gerçekten işe yarama olasılığı:

```python
def real_given_significant(prior, power, alpha=0.05):
    hit = prior * power
    false_alarm = (1 - prior) * alpha
    return hit / (hit + false_alarm)


for prior in [0.1, 0.5]:
    for power in [0.2, 0.8]:
        print(prior, power, round(real_given_significant(prior, power), 3))
```

```text
0.1 0.2 0.308
0.1 0.8 0.64
0.5 0.2 0.8
0.5 0.8 0.941
```

- Fikirlerin yalnızca %10'u işe yarıyorsa ve testlerin gücü 0,2 ise, anlamlı
  sonuçların ancak %31 kadarı gerçek.
- Güç 0,8 olunca bu %64 oluyor. Güç Analizi bölümündeki
  hesabın bir başka nedeni de bu.
- Önsel inanç değişince aynı "anlamlı" sonuç çok farklı bir anlam taşıyor.

## Oranlar için önsel ve sonsal: Beta dağılımı

Bir satın alma oranı için inancımızı 0 ile 1 arasında bir dağılımla
gösteririz. **Beta dağılımı** bunun için biçilmiş kaftan: Beta(a, b)
önselle başlayıp n kişiden k'sının satın aldığını görürsek sonsal
Beta(a + k, b + n − k) olur. Hesap bu kadar: önsele başarıları ve
başarısızlıkları eklemek. Beta(1, 1) her oranı eşit olası sayan "düz"
önseldir.

Ödeme düğmesi testinde (4000'er kişi):

```python
import numpy as np
from scipy import stats
from ab_data import make_checkout_test

shop = make_checkout_test()
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
for g in ["A", "B"]:
    post = stats.beta(1 + k[g], 1 + n[g] - k[g])
    low, high = post.ppf([0.025, 0.975])
    print(g, k[g], round(post.mean(), 4), round(low, 4), round(high, 4))
```

```text
A 472 0.1182 0.1084 0.1284
B 560 0.1402 0.1296 0.1511
```

Her satırda: satın alan sayısı, sonsal ortalama ve %95'lik **inandırıcı
aralık** (credible interval). İnandırıcı aralığın okunuşu, güven aralığının
yanlış okunuşunun aynısı ve burada doğru: "Bu veriyle, oranın bu aralıkta
olma olasılığı %95."

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="494.252812pt" height="215.750906pt" viewBox="0 0 494.252812 215.750906" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 215.750906 
L 494.252812 215.750906 
L 494.252812 -0 
L 0 -0 
L 0 215.750906 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 177.550125 
L 220.254545 177.550125 
L 220.254545 22.318125 
L 7.2 22.318125 
L 7.2 177.550125 
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
       <use xlink:href="#m15aed4d867" x="16.884298" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="16.884298" y="192.147781" transform="rotate(-0 16.884298 192.147781)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="72.22314" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="72.22314" y="192.147781" transform="rotate(-0 72.22314 192.147781)">0.1</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="127.561983" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="127.561983" y="192.147781" transform="rotate(-0 127.561983 192.147781)">0.2</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="182.900826" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="182.900826" y="192.147781" transform="rotate(-0 182.900826 192.147781)">0.3</text>
     </g>
    </g>
    <g id="text_5">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="206.148562" transform="rotate(-0 113.727273 206.148562)">Satın alma oranı</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_5">
    <path d="M 16.884298 170.494125 
L 17.854344 170.391723 
L 18.501042 170.050663 
L 19.147739 169.355949 
L 19.794437 168.231679 
L 20.441135 166.631078 
L 21.087832 164.531343 
L 22.057879 160.442996 
L 23.027925 155.279047 
L 24.321321 146.90996 
L 25.938065 134.560986 
L 28.201507 115.149465 
L 32.081693 81.506147 
L 34.021786 66.629637 
L 35.63853 55.896012 
L 36.931925 48.564613 
L 38.22532 42.420332 
L 39.518716 37.488199 
L 40.488762 34.581336 
L 41.458809 32.339828 
L 42.428855 30.743593 
L 43.075553 30.025323 
L 43.722251 29.573529 
L 44.368948 29.378532 
L 45.015646 29.429997 
L 45.662344 29.717054 
L 46.309041 30.228406 
L 47.279088 31.390522 
L 48.249134 32.991082 
L 49.219181 34.989563 
L 50.512576 38.20337 
L 52.12932 42.971348 
L 54.069413 49.563006 
L 56.332855 58.100702 
L 60.213041 73.806482 
L 65.386622 94.64366 
L 68.296762 105.514435 
L 70.883552 114.410111 
L 73.470343 122.493928 
L 75.733785 128.87413 
L 77.997227 134.609063 
L 80.260669 139.718025 
L 82.52411 144.232453 
L 84.787552 148.191913 
L 86.727645 151.177636 
L 88.991087 154.226131 
L 91.254529 156.851188 
L 93.517971 159.098934 
L 95.781413 161.013427 
L 98.044854 162.635927 
L 100.308296 164.004447 
L 102.895087 165.301624 
L 105.481878 166.358008 
L 108.392017 167.308322 
L 111.625505 168.125195 
L 115.182342 168.79648 
L 119.385877 169.359927 
L 124.559459 169.813106 
L 131.026435 170.141474 
L 140.080203 170.35885 
L 155.277598 170.46944 
L 203.456574 170.494072 
L 210.570248 170.494105 
L 210.570248 170.494105 
" clip-path="url(#p3b14509d5f)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_6">
    <path d="M 16.884298 170.494125 
L 27.878158 170.394137 
L 30.464948 170.153478 
L 32.405041 169.777367 
L 34.021786 169.271415 
L 35.63853 168.535787 
L 37.255274 167.518594 
L 38.548669 166.468967 
L 39.842065 165.185156 
L 41.458809 163.222483 
L 43.075553 160.836888 
L 44.692297 158.013083 
L 46.309041 154.749309 
L 48.249134 150.27027 
L 50.189227 145.223358 
L 52.452669 138.717066 
L 55.362809 129.617952 
L 65.063273 98.519972 
L 67.326715 92.261198 
L 69.266808 87.478212 
L 71.206901 83.314516 
L 72.823645 80.360852 
L 74.44039 77.902484 
L 75.733785 76.302817 
L 77.02718 75.033642 
L 78.320576 74.095273 
L 79.613971 73.484841 
L 80.584017 73.23883 
L 81.554064 73.170607 
L 82.52411 73.275926 
L 83.817506 73.677634 
L 85.110901 74.36544 
L 86.404296 75.324066 
L 87.697692 76.536774 
L 89.314436 78.38259 
L 90.93118 80.560499 
L 92.871273 83.558462 
L 95.134715 87.501297 
L 97.721506 92.465116 
L 101.278343 99.821136 
L 113.242249 125.048476 
L 116.475738 131.192979 
L 119.709226 136.847377 
L 122.619366 141.47815 
L 125.529505 145.659666 
L 128.116296 149.000033 
L 130.703086 151.995006 
L 133.289877 154.65923 
L 135.876668 157.011605 
L 138.463458 159.073926 
L 141.050249 160.869725 
L 143.960389 162.601681 
L 146.870528 164.061592 
L 149.780668 165.282886 
L 153.014156 166.398326 
L 156.570993 167.377388 
L 160.451179 168.202785 
L 164.654714 168.870403 
L 169.504946 169.418162 
L 175.325225 169.850187 
L 182.762248 170.169987 
L 193.109411 170.376169 
L 210.570248 170.475595 
L 210.570248 170.475595 
" clip-path="url(#p3b14509d5f)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 7.2 177.550125 
L 7.2 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 220.254545 177.550125 
L 220.254545 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 7.2 177.550125 
L 220.254545 177.550125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 7.2 22.318125 
L 220.254545 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_6">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="16.318125" transform="rotate(-0 113.727273 16.318125)">60'ar kişi</text>
   </g>
   <g id="legend_1">
    <g id="line2d_7">
     <path d="M 176.393608 35.416562 
L 186.393608 35.416562 
L 196.393608 35.416562 
" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="204.393608" y="38.916562" transform="rotate(-0 204.393608 38.916562)">A</text>
    </g>
    <g id="line2d_8">
     <path d="M 176.393608 50.417344 
L 186.393608 50.417344 
L 196.393608 50.417344 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="204.393608" y="53.917344" transform="rotate(-0 204.393608 53.917344)">B</text>
    </g>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 262.865455 177.550125 
L 475.92 177.550125 
L 475.92 22.318125 
L 262.865455 22.318125 
L 262.865455 177.550125 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="262.865455" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="262.865455" y="192.147781" transform="rotate(-0 262.865455 192.147781)">0.08</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="305.476364" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="305.476364" y="192.147781" transform="rotate(-0 305.476364 192.147781)">0.10</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="348.087273" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="348.087273" y="192.147781" transform="rotate(-0 348.087273 192.147781)">0.12</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="390.698182" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="390.698182" y="192.147781" transform="rotate(-0 390.698182 192.147781)">0.14</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="433.309091" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="433.309091" y="192.147781" transform="rotate(-0 433.309091 192.147781)">0.16</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="475.92" y="177.550125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="475.92" y="192.147781" transform="rotate(-0 475.92 192.147781)">0.18</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="206.148562" transform="rotate(-0 369.392727 206.148562)">Satın alma oranı</text>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_15">
    <path d="M 92.421818 170.494125 
L 304.053629 170.407295 
L 307.788308 170.147697 
L 310.278094 169.694981 
L 311.522987 169.310869 
L 312.76788 168.771206 
L 314.012773 168.026626 
L 315.257666 167.017742 
L 316.502559 165.675223 
L 317.747452 163.920749 
L 318.992345 161.669069 
L 320.237238 158.831323 
L 321.482131 155.319732 
L 322.727024 151.053587 
L 323.971917 145.966351 
L 325.21681 140.01347 
L 326.461703 133.18036 
L 327.706596 125.489845 
L 330.196382 107.849532 
L 337.66574 50.595589 
L 338.910633 43.24289 
L 340.155526 37.260945 
L 341.400419 32.863026 
L 342.645312 30.204579 
L 343.890205 29.374125 
L 345.135098 30.3885 
L 346.379991 33.192776 
L 347.624884 37.664784 
L 348.869777 43.623738 
L 350.11467 50.842147 
L 352.604456 67.999471 
L 358.828921 114.337094 
L 361.318707 129.898764 
L 362.5636 136.580489 
L 363.808493 142.48929 
L 365.053386 147.633331 
L 366.298279 152.044497 
L 367.543172 155.772363 
L 368.788065 158.878431 
L 370.032958 161.430947 
L 371.277851 163.500503 
L 372.522744 165.156528 
L 373.767637 166.464665 
L 375.01253 167.485001 
L 376.257423 168.27102 
L 377.502316 168.869175 
L 379.992102 169.653088 
L 382.481888 170.076653 
L 386.216567 170.358966 
L 392.441032 170.47725 
L 418.583785 170.494125 
L 495.252812 170.494125 
L 495.252812 170.494125 
" clip-path="url(#p2dad15dec6)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 92.421818 170.494125 
L 347.624884 170.414392 
L 351.359563 170.20785 
L 353.849349 169.86985 
L 356.339135 169.208075 
L 357.584028 168.686703 
L 358.828921 167.988965 
L 360.073814 167.069332 
L 361.318707 165.875586 
L 362.5636 164.349519 
L 363.808493 162.428283 
L 365.053386 160.04649 
L 366.298279 157.139105 
L 367.543172 153.645109 
L 368.788065 149.511858 
L 370.032958 144.699928 
L 371.277851 139.188195 
L 372.522744 132.978787 
L 375.01253 118.617215 
L 377.502316 102.237069 
L 382.481888 68.401411 
L 383.726781 60.921252 
L 384.971674 54.272949 
L 386.216567 48.657407 
L 387.46146 44.247976 
L 388.706353 41.181492 
L 389.951246 39.551209 
L 391.196139 39.402115 
L 392.441032 40.728976 
L 393.685925 43.477205 
L 394.930818 47.546445 
L 396.175711 52.796548 
L 397.420604 59.055467 
L 399.91039 73.80781 
L 407.379748 121.635542 
L 409.869534 134.700926 
L 411.114427 140.325932 
L 412.35932 145.324209 
L 413.604213 149.7055 
L 414.849106 153.495695 
L 416.093999 156.732869 
L 417.338892 159.463491 
L 418.583785 161.738998 
L 419.828678 163.612827 
L 421.073571 165.138009 
L 422.318464 166.365295 
L 423.563357 167.341832 
L 424.80825 168.110302 
L 426.053143 168.708486 
L 428.542929 169.52015 
L 431.032715 169.982348 
L 434.767394 170.312208 
L 439.746966 170.453772 
L 453.440789 170.493813 
L 495.252812 170.494125 
L 495.252812 170.494125 
" clip-path="url(#p2dad15dec6)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 262.865455 177.550125 
L 262.865455 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 475.92 177.550125 
L 475.92 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 262.865455 177.550125 
L 475.92 177.550125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 262.865455 22.318125 
L 475.92 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="16.318125" transform="rotate(-0 369.392727 16.318125)">4000'er kişi</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p3b14509d5f">
   <rect x="7.2" y="22.318125" width="213.054545" height="155.232"/>
  </clipPath>
  <clipPath id="p2dad15dec6">
   <rect x="262.865455" y="22.318125" width="213.054545" height="155.232"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Düz önselle sonsal dağılımlar. Az veride iki eğri geniş ve büyük ölçüde üst üste; çok veride dar ve neredeyse ayrık (sağdaki eksen yakınlaştırılmış).</figcaption>
</figure>

## B'nin daha iyi olma olasılığı

İki sonsaldan çok sayıda örnek çekip karşılaştırırsak her soruyu sayarak
cevaplarız:

```python
rng = np.random.default_rng(502)
draw_a = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 200_000)
draw_b = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 200_000)
lift = draw_b - draw_a
print(round((draw_b > draw_a).mean(), 4))
print(np.round(np.percentile(lift, [2.5, 97.5]), 4))
loss_b = np.maximum(-lift, 0).mean()
loss_a = np.maximum(lift, 0).mean()
print(f"{loss_b:.1e}", round(loss_a, 4))
```

```text
0.9985
[0.0073 0.0367]
3.4e-06 0.022
```

- **P(B > A)** = 0,999: "B'nin daha iyi olma olasılığı". Ekibin
  asıl sorduğu soru buydu.
- Farkın inandırıcı aralığı, Etki Büyüklüğü bölümündeki güven aralığıyla
  (0,0073 – 0,0367) neredeyse aynı. Büyük örneklem ve düz önselde iki
  yaklaşım sayıda buluşur; **okunuşları** farklıdır.
- Son satır **beklenen kayıp** (expected loss): B'yi seçersek ve yanılıyorsak
  ortalama ne kadar kaybederiz? B'yi seçmenin kaybı çok küçük, A'da kalmanın
  kaybı yaklaşık 0,022 (satın alma oranında). Pek çok ekip kararı
  "kayıp bir eşiğin altına inince seç" kuralıyla verir.

## p ile P(B > A) aynı şey mi?

```python
from statsmodels.stats.proportion import proportions_ztest

p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]],
                      alternative="larger")[1]
print(round(p, 4), round(1 - (draw_b > draw_a).mean(), 4))
```

```text
0.0017 0.0015
```

Tek yönlü p ile $1 - P(B > A)$ burada çok yakın. Bu düz önsel ve büyük
örneklemin sonucu, bir kural değil. Anlamları yine farklı: p "fark yoksa bu
veri ne kadar şaşırtıcı?", $P(B > A)$ "bu veriyle B'nin daha iyi olma
olasılığı ne?" diye sorar. İkincisi önsele de bağlıdır.

## Önselin etkisi

Küçük bir testte (60'ar kişi) önsel sonucu belirgin biçimde değiştirir.
Geçmiş verilerden satın alma oranının %11,4 civarında olduğunu biliyorsak,
bunu 100 kişilik bilgiye denk bir önselle yazabiliriz: Beta(11,4; 88,6).

```python
small = make_checkout_test(n=60, seed=503)
k_s = small.groupby("group")["bought"].sum()
for a0, b0 in [(1, 1), (11.4, 88.6)]:
    s_a = rng.beta(a0 + k_s["A"], b0 + 60 - k_s["A"], 200_000)
    s_b = rng.beta(a0 + k_s["B"], b0 + 60 - k_s["B"], 200_000)
    print(a0, b0, round(s_a.mean(), 3), round(s_b.mean(), 3),
          round((s_b > s_a).mean(), 3))
```

```text
1 1 0.065 0.129 0.897
11.4 88.6 0.09 0.115 0.773
```

- Küçük örneklemde A 3, B 7 satın alma gördü. Düz
  önsel bu küçük sayılara tamamen inanıyor; bilgili önsel ise iki oranı da
  bildiğimiz %11,4'e doğru çekiyor (**büzülme**, shrinkage).
- P(B > A) düz önselde 0,897, bilgili önselde 0,773.
  Küçük veride "çok umut verici" görünen sonuç bilgili önselle daha ölçülü.
- 4000'er kişide iki önsel neredeyse aynı sonucu verir: veri büyüdükçe
  önselin ağırlığı erir.

Önsel, verilere bakmadan önce ve gerekçesiyle yazılır. Sonuca bakıp önsel
seçmek, eşiği sonradan seçmek kadar yanlıştır.

## Ne zaman hangisi?

- **Frekansçı:** yanlış alarm oranını önceden sabitler ve denetler; ekip
  içinde yaygın, tartışması az.
- **Bayesçi:** "B'nin daha iyi olma olasılığı" ve "beklenen kayıp" gibi karar
  vericinin anladığı sayılar verir; geçmiş bilgiyi önselle katar.
- Bayesçi yöntem de testi istediğin an durdurma sorununu sihirle çözmez;
  kurallar yine önceden yazılır.

## Özet

- Bayes teoremi önsel inancı veriyle güncelleyip sonsal inanç verir.
- Oranlarda Beta(a, b) önsel, n'de k başarıyla Beta(a + k, b + n − k)
  sonsal olur.
- İnandırıcı aralık "oran bu aralıkta, %95 olasılıkla" diye okunur.
- Sonsallardan örnek çekerek P(B > A) ve beklenen kayıp hesaplanır.
- Önsel küçük veride sonucu belirgin değiştirir, büyük veride erir;
  önceden ve gerekçeyle seçilir.
