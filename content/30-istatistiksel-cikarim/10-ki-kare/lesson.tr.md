# Ki-Kare Testleri

Önceki bölümde iki oranı karşılaştırdık. Ama bazı sorular ikiden fazla
kategori içerir: siparişler haftanın günlerine eşit mi dağılıyor? Alışveriş
yapma oranı cihaza (mobil, masaüstü, tablet) göre değişiyor mu? Bu tür
**sayım** (count) sorularının ortak aracı **ki-kare testi** (chi-square
test, $\chi^2$). Fikri basit: her kategoride **gözlenen** sayıyı, $H_0$
doğru olsaydı **beklenecek** sayıyla karşılaştır.

## Uyum iyiliği: siparişler günlere eşit mi dağılıyor?

1400 siparişin hangi gün geldiğine bakalım. $H_0$: her gün eşit olası; o
zaman her güne $1400 / 7 = 200$ sipariş beklenir.

$$\chi^2 = \sum \dfrac{(\text{gözlenen} - \text{beklenen})^2}{\text{beklenen}}$$

Her kategorinin sapması karesi alınıp beklenene bölünür ve toplanır. Fark
büyüdükçe $\chi^2$ büyür.

```python
import numpy as np
from scipy import stats
from ab_data import make_weekday_orders

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
observed = make_weekday_orders().value_counts().reindex(days)
expected = np.full(7, observed.sum() / 7)
print(observed.tolist())
print(round(((observed - expected) ** 2 / expected).sum(), 2))
result = stats.chisquare(observed)
print(round(result.statistic, 2), round(result.pvalue, 4))
```

```text
[182, 174, 195, 172, 217, 216, 244]
21.45
21.45 0.0015
```

- Hafta sonu sayıları (216 ve 244) 200'ün belirgin üstünde.
- Elle bulduğumuz $\chi^2$ = 21,45, `stats.chisquare` ile aynı.
  Varsayılan olarak her kategoriye eşit beklenen sayı kullanır; başka bir
  beklenti için `f_exp=` verilir.
- p = 0,0015: günler eşit olsaydı bu kadar dengesiz bir tablo görmek
  çok nadir olurdu. Bu tür teste **uyum iyiliği testi** (goodness-of-fit
  test) denir: veri beklenen dağılıma uyuyor mu?

## Ki-kare dağılımı nereden geliyor?

p değeri **ki-kare dağılımından** gelir. Bu dağılımın tek parametresi
serbestlik derecesi: uyum iyiliğinde kategori sayısı eksi 1 (burada 6).
Neden eksi 1? Altı günün sayısını bilirsen yedincisi toplamdan çıkar; yalnızca
altısı serbesttir. Benzetimle doğrulayalım: günlerin gerçekten eşit olduğu
bir dünyada 10 000 kez 1400 sipariş dağıt.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(151)
counts = rng.multinomial(1400, [1 / 7] * 7, size=10000)
chi = ((counts - 200) ** 2 / 200).sum(axis=1)
print(round(chi.mean(), 2))
print(round((chi >= 21.45).mean(), 4), round(stats.chi2.sf(21.45, df=6), 4))
```

```text
6.04
0.0017 0.0015
```

- $H_0$ altında $\chi^2$'nin ortalaması 6,04: serbestlik derecesine
  (6) çok yakın. Ki-kare dağılımının ortalaması serbestlik derecesine
  eşittir.
- Bizim değerimizi (21,45) aşan benzetimlerin payı 0,0017,
  formülün verdiği 0,0015: aynı soru, iki yol.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="405pt" height="211.720781pt" viewBox="0 0 405 211.720781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 211.720781 
L 405 211.720781 
L 405 0 
L 0 0 
L 0 211.720781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 173.52 
L 397.8 173.52 
L 397.8 7.2 
L 7.2 7.2 
L 7.2 173.52 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 24.954545 173.52 
L 30.872727 173.52 
L 30.872727 170.330738 
L 24.954545 170.330738 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_4">
    <path d="M 30.872727 173.52 
L 36.790909 173.52 
L 36.790909 153.852886 
L 30.872727 153.852886 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_5">
    <path d="M 36.790909 173.52 
L 42.709091 173.52 
L 42.709091 130.730738 
L 36.790909 130.730738 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_6">
    <path d="M 42.709091 173.52 
L 48.627273 173.52 
L 48.627273 93.788456 
L 42.709091 93.788456 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_7">
    <path d="M 48.627273 173.52 
L 54.545455 173.52 
L 54.545455 71.995168 
L 48.627273 71.995168 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_8">
    <path d="M 54.545455 173.52 
L 60.463636 173.52 
L 60.463636 53.391141 
L 54.545455 53.391141 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_9">
    <path d="M 60.463636 173.52 
L 66.381818 173.52 
L 66.381818 25.485101 
L 60.463636 25.485101 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_10">
    <path d="M 66.381818 173.52 
L 72.3 173.52 
L 72.3 26.81396 
L 66.381818 26.81396 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_11">
    <path d="M 72.3 173.52 
L 78.218182 173.52 
L 78.218182 17.246174 
L 72.3 17.246174 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_12">
    <path d="M 78.218182 173.52 
L 84.136364 173.52 
L 84.136364 18.840805 
L 78.218182 18.840805 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_13">
    <path d="M 84.136364 173.52 
L 90.054545 173.52 
L 90.054545 15.12 
L 84.136364 15.12 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_14">
    <path d="M 90.054545 173.52 
L 95.972727 173.52 
L 95.972727 27.345503 
L 90.054545 27.345503 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_15">
    <path d="M 95.972727 173.52 
L 101.890909 173.52 
L 101.890909 35.850201 
L 95.972727 35.850201 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_16">
    <path d="M 101.890909 173.52 
L 107.809091 173.52 
L 107.809091 45.683758 
L 101.890909 45.683758 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_17">
    <path d="M 107.809091 173.52 
L 113.727273 173.52 
L 113.727273 44.886443 
L 107.809091 44.886443 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_18">
    <path d="M 113.727273 173.52 
L 119.645455 173.52 
L 119.645455 60.56698 
L 113.727273 60.56698 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_19">
    <path d="M 119.645455 173.52 
L 125.563636 173.52 
L 125.563636 69.33745 
L 119.645455 69.33745 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_20">
    <path d="M 125.563636 173.52 
L 131.481818 173.52 
L 131.481818 84.752215 
L 125.563636 84.752215 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_21">
    <path d="M 131.481818 173.52 
L 137.4 173.52 
L 137.4 87.675705 
L 131.481818 87.675705 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_22">
    <path d="M 137.4 173.52 
L 143.318182 173.52 
L 143.318182 104.419329 
L 137.4 104.419329 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_23">
    <path d="M 143.318182 173.52 
L 149.236364 173.52 
L 149.236364 106.279732 
L 143.318182 106.279732 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_24">
    <path d="M 149.236364 173.52 
L 155.154545 173.52 
L 155.154545 115.315973 
L 149.236364 115.315973 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_25">
    <path d="M 155.154545 173.52 
L 161.072727 173.52 
L 161.072727 123.554899 
L 155.154545 123.554899 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_26">
    <path d="M 161.072727 173.52 
L 166.990909 173.52 
L 166.990909 120.897181 
L 161.072727 120.897181 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_27">
    <path d="M 166.990909 173.52 
L 172.909091 173.52 
L 172.909091 130.99651 
L 166.990909 130.99651 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_28">
    <path d="M 172.909091 173.52 
L 178.827273 173.52 
L 178.827273 134.185772 
L 172.909091 134.185772 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_29">
    <path d="M 178.827273 173.52 
L 184.745455 173.52 
L 184.745455 141.361611 
L 178.827273 141.361611 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_30">
    <path d="M 184.745455 173.52 
L 190.663636 173.52 
L 190.663636 148.53745 
L 184.745455 148.53745 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_31">
    <path d="M 190.663636 173.52 
L 196.581818 173.52 
L 196.581818 150.132081 
L 190.663636 150.132081 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_32">
    <path d="M 196.581818 173.52 
L 202.5 173.52 
L 202.5 155.181745 
L 196.581818 155.181745 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_33">
    <path d="M 202.5 173.52 
L 208.418182 173.52 
L 208.418182 160.762953 
L 202.5 160.762953 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_34">
    <path d="M 208.418182 173.52 
L 214.336364 173.52 
L 214.336364 157.042148 
L 208.418182 157.042148 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_35">
    <path d="M 214.336364 173.52 
L 220.254545 173.52 
L 220.254545 161.560268 
L 214.336364 161.560268 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_36">
    <path d="M 220.254545 173.52 
L 226.172727 173.52 
L 226.172727 161.028725 
L 220.254545 161.028725 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_37">
    <path d="M 226.172727 173.52 
L 232.090909 173.52 
L 232.090909 162.623356 
L 226.172727 162.623356 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_38">
    <path d="M 232.090909 173.52 
L 238.009091 173.52 
L 238.009091 167.67302 
L 232.090909 167.67302 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_39">
    <path d="M 238.009091 173.52 
L 243.927273 173.52 
L 243.927273 166.344161 
L 238.009091 166.344161 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_40">
    <path d="M 243.927273 173.52 
L 249.845455 173.52 
L 249.845455 167.938792 
L 243.927273 167.938792 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_41">
    <path d="M 249.845455 173.52 
L 255.763636 173.52 
L 255.763636 168.736107 
L 249.845455 168.736107 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_42">
    <path d="M 255.763636 173.52 
L 261.681818 173.52 
L 261.681818 169.001879 
L 255.763636 169.001879 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_43">
    <path d="M 261.681818 173.52 
L 267.6 173.52 
L 267.6 170.330738 
L 261.681818 170.330738 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_44">
    <path d="M 267.6 173.52 
L 273.518182 173.52 
L 273.518182 171.128054 
L 267.6 171.128054 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_45">
    <path d="M 273.518182 173.52 
L 279.436364 173.52 
L 279.436364 170.59651 
L 273.518182 170.59651 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_46">
    <path d="M 279.436364 173.52 
L 285.354545 173.52 
L 285.354545 170.862282 
L 279.436364 170.862282 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_47">
    <path d="M 285.354545 173.52 
L 291.272727 173.52 
L 291.272727 171.128054 
L 285.354545 171.128054 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_48">
    <path d="M 291.272727 173.52 
L 297.190909 173.52 
L 297.190909 171.925369 
L 291.272727 171.925369 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_49">
    <path d="M 297.190909 173.52 
L 303.109091 173.52 
L 303.109091 172.722685 
L 297.190909 172.722685 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_50">
    <path d="M 303.109091 173.52 
L 309.027273 173.52 
L 309.027273 171.393826 
L 303.109091 171.393826 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_51">
    <path d="M 309.027273 173.52 
L 314.945455 173.52 
L 314.945455 172.456913 
L 309.027273 172.456913 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_52">
    <path d="M 314.945455 173.52 
L 320.863636 173.52 
L 320.863636 172.456913 
L 314.945455 172.456913 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_53">
    <path d="M 320.863636 173.52 
L 326.781818 173.52 
L 326.781818 173.254228 
L 320.863636 173.254228 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_54">
    <path d="M 326.781818 173.52 
L 332.7 173.52 
L 332.7 172.456913 
L 326.781818 172.456913 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_55">
    <path d="M 332.7 173.52 
L 338.618182 173.52 
L 338.618182 173.52 
L 332.7 173.52 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_56">
    <path d="M 338.618182 173.52 
L 344.536364 173.52 
L 344.536364 173.52 
L 338.618182 173.52 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_57">
    <path d="M 344.536364 173.52 
L 350.454545 173.52 
L 350.454545 173.254228 
L 344.536364 173.254228 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_58">
    <path d="M 350.454545 173.52 
L 356.372727 173.52 
L 356.372727 172.722685 
L 350.454545 172.722685 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_59">
    <path d="M 356.372727 173.52 
L 362.290909 173.52 
L 362.290909 173.254228 
L 356.372727 173.254228 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_60">
    <path d="M 362.290909 173.52 
L 368.209091 173.52 
L 368.209091 173.254228 
L 362.290909 173.254228 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_61">
    <path d="M 368.209091 173.52 
L 374.127273 173.52 
L 374.127273 173.52 
L 368.209091 173.52 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_62">
    <path d="M 374.127273 173.52 
L 380.045455 173.52 
L 380.045455 172.988456 
L 374.127273 172.988456 
z
" clip-path="url(#pcaf7761f0c)" style="fill: #8b5cf6; opacity: 0.75"/>
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
       <use xlink:href="#m15aed4d867" x="24.954545" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="24.954545" y="188.117656" transform="rotate(-0 24.954545 188.117656)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="93.241259" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="93.241259" y="188.117656" transform="rotate(-0 93.241259 188.117656)">5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="161.527972" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="161.527972" y="188.117656" transform="rotate(-0 161.527972 188.117656)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="229.814685" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="229.814685" y="188.117656" transform="rotate(-0 229.814685 188.117656)">15</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="298.101399" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="298.101399" y="188.117656" transform="rotate(-0 298.101399 188.117656)">20</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="366.388112" y="173.52" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="366.388112" y="188.117656" transform="rotate(-0 366.388112 188.117656)">25</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="202.118437" transform="rotate(-0 202.5 202.118437)">χ² (günler gerçekten eşitken)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_7">
    <path d="M 24.954545 173.52 
L 26.14214 172.99899 
L 27.329735 171.524629 
L 28.51733 169.221431 
L 29.704926 166.203237 
L 30.892521 162.57397 
L 32.080116 158.428348 
L 34.455306 148.924848 
L 36.830496 138.290637 
L 41.580876 115.49283 
L 46.331256 92.909641 
L 49.894041 77.217551 
L 52.269231 67.621533 
L 54.644421 58.823733 
L 57.019611 50.880024 
L 59.394801 43.821252 
L 61.769991 37.657864 
L 64.145181 32.383873 
L 66.520371 27.980236 
L 68.895561 24.417719 
L 70.083156 22.940565 
L 71.270751 21.659329 
L 72.458346 20.568509 
L 73.645941 19.662356 
L 74.833536 18.93492 
L 76.021131 18.380089 
L 77.208726 17.991633 
L 78.396321 17.763236 
L 79.583916 17.688524 
L 80.771511 17.761101 
L 81.959106 17.974569 
L 83.146701 18.322553 
L 84.334296 18.798718 
L 86.709486 20.110592 
L 89.084676 21.861034 
L 91.459866 24.002548 
L 93.835056 26.489619 
L 96.210246 29.278956 
L 99.773031 33.940914 
L 103.335816 39.064053 
L 108.086196 46.416137 
L 114.024171 56.118579 
L 129.462907 81.677145 
L 135.400882 90.985774 
L 140.151262 98.066015 
L 144.901642 104.77328 
L 149.652022 111.080652 
L 154.402402 116.973818 
L 159.152782 122.448608 
L 163.903162 127.508853 
L 168.653542 132.164564 
L 173.403922 136.430378 
L 178.154302 140.324262 
L 182.904682 143.866448 
L 187.655062 147.07856 
L 192.405442 149.982913 
L 197.155822 152.601959 
L 201.906202 154.957859 
L 206.656583 157.072158 
L 211.406963 158.965547 
L 216.157343 160.657693 
L 222.095318 162.518005 
L 228.033293 164.126323 
L 233.971268 165.513238 
L 241.096838 166.924008 
L 248.222408 168.098008 
L 256.535573 169.217352 
L 264.848738 170.114407 
L 274.349498 170.920621 
L 285.037853 171.608484 
L 298.101399 172.213109 
L 313.540134 172.691056 
L 332.541654 173.050328 
L 358.668744 173.30758 
L 380.045455 173.410038 
L 380.045455 173.410038 
" clip-path="url(#pcaf7761f0c)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_8">
    <path d="M 317.904545 173.52 
L 317.904545 7.2 
" clip-path="url(#pcaf7761f0c)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_63">
    <path d="M 7.2 173.52 
L 7.2 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_64">
    <path d="M 397.8 173.52 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_65">
    <path d="M 7.2 173.52 
L 397.8 173.52 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_66">
    <path d="M 7.2 7.2 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pcaf7761f0c">
   <rect x="7.2" y="7.2" width="390.6" height="166.32"/>
  </clipPath>
 </defs>
</svg>
<figcaption>10 000 benzetimin χ² değerleri (mor) ve 6 serbestlik dereceli ki-kare dağılımı (turuncu). Kesik çizgi bizim değerimiz: dağılımın uzak kuyruğunda.</figcaption>
</figure>

## Bağımsızlık testi: alışveriş cihaza bağlı mı?

İki kategorik değişken arasında ilişki var mı diye sormak için **çapraz
tablo** (contingency table) kurulur: satırlar cihaz, sütunlar
alışveriş yaptı mı. $H_0$: iki değişken **bağımsız**, yani alışveriş oranı
her cihazda aynı.

```python
import pandas as pd
from scipy import stats
from ab_data import make_devices

users = make_devices()
table = pd.crosstab(users["device"], users["bought"])
result = stats.chi2_contingency(table)
print(table.values.tolist())
print(round(result.statistic, 2), result.dof, f"{result.pvalue:.1e}")
print(result.expected_freq.round(1).tolist())
print(users.groupby("device")["bought"].mean().round(3).to_dict())
```

```text
[[782, 126], [1633, 157], [268, 34]]
16.79 2 2.3e-04
[[812.1, 95.9], [1600.9, 189.1], [270.1, 31.9]]
{'desktop': 0.139, 'mobile': 0.088, 'tablet': 0.113}
```

- Satırlar sırasıyla masaüstü, mobil, tablet; sütunlar "almadı, aldı".
- **Beklenen sayılar** (`expected_freq`): cihaz ile alışveriş bağımsız
  olsaydı her hücrede olacak sayılar. Satır toplamı × sütun toplamı / genel
  toplam ile bulunur. Masaüstünde 96 alışveriş beklenirken 126 gözlendi;
  mobilde 189 beklenirken 157.
- Serbestlik derecesi (satır − 1) × (sütun − 1) = 2 × 1 = 2.
- p = 2,3e-04: oranlar cihaza göre gerçekten değişiyor. Masaüstü
  0,139, mobil 0,088, tablet 0,113.

## İlişki ne kadar güçlü? Cramér's V

p yine "ilişki sıfır mı?" sorusuna cevap verir; "ne kadar güçlü?" sorusuna
değil. Çapraz tablolar için yaygın etki büyüklüğü **Cramér's V**: 0 (hiç
ilişki yok) ile 1 (tam ilişki) arasında.

```python
import pandas as pd
from scipy import stats
from ab_data import make_devices

users = make_devices()
table = pd.crosstab(users["device"], users["bought"])
print(round(float(stats.contingency.association(table, method="cramer")), 3))
```

```text
0.075
```

V = 0,075: istatistiksel olarak kesin ama zayıf bir ilişki. Cihaz
alışverişi biraz etkiliyor; tek başına çok az şey açıklıyor. Bu, iş
kararı açısından önemsiz demek değil: 5 puanlık oran farkı (mobil ile
masaüstü) para demektir. Ama "cihaz alışverişin belirleyicisi" demek abartı.

## 2×2 tablo ve oran testi aynı şey

Önceki bölümdeki ödeme düğmesi testini ki-kare ile yapalım:

```python
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_checkout_test

test = make_checkout_test()
table = pd.crosstab(test["group"], test["bought"])
plain = stats.chi2_contingency(table, correction=False)
z, p = proportions_ztest(table[1].values, table.sum(axis=1).values)
print(round(plain.statistic, 3), round(z ** 2, 3))
print(round(plain.pvalue, 4), round(p, 4))
print(round(stats.chi2_contingency(table).pvalue, 4))
```

```text
8.615 8.615
0.0033 0.0033
0.0037
```

- 2×2 tabloda $\chi^2 = z^2$ ve p değerleri aynı: iki oran z-testi, ki-kare
  testinin özel bir hâli.
- Son satır: `chi2_contingency` 2×2 tablolarda varsayılan olarak **Yates
  düzeltmesi** (continuity correction) uygular ve biraz daha büyük p verir
  (0,0037). Tutucu bir ayardır; z-testiyle aynı sonucu istiyorsan
  `correction=False` yaz.

## Kullanım koşulları

- Sayılar **sayım** olmalı: oran ya da yüzde değil. Tabloya yüzde koyarsan
  test, örneklemin ne kadar büyük olduğunu bilemez.
- Her gözlem tek bir hücrede olmalı (bağımsız gözlemler).
- **Beklenen** sayıların hepsi en az 5 olmalı (gözlenen değil). Değilse
  kategorileri birleştir ya da 2×2'de Fisher'ın kesin testine geç.

## Özet

- Ki-kare: $\sum (G - B)^2 / B$; gözlenen ile beklenen sayıların uzaklığı.
- Uyum iyiliği (`stats.chisquare`): bir dağılıma uyuyor mu? sd = kategori − 1.
- Bağımsızlık (`stats.chi2_contingency`): iki kategorik değişken ilişkili
  mi? sd = (satır − 1)(sütun − 1).
- Gücü Cramér's V ile ölç; 2×2 tabloda ki-kare iki oran z-testinin aynısı.
