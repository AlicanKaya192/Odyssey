# Güç Analizi

Bir testin **gücü** (power), gerçekten var olan bir etkiyi yakalama
olasılığıdır: $1 - \beta$, yani "II. tür hatayı yapmama" olasılığı. Güç
düşükse gerçek bir iyileştirme "anlamlı değil" çıkar ve çöpe gider.
**Güç analizi** testi başlatmadan **önce** "kaç kişiye ihtiyacım var?"
sorusunu cevaplar.

## Dört sayı, biri bilinmeyen

Güç analizinde dört sayı birbirine bağlıdır:

- **Etki büyüklüğü:** yakalamak istediğin en küçük fark (d ya da h).
- **Anlamlılık düzeyi** $\alpha$: yanlış alarm oranı, genellikle 0,05.
- **Güç** $1 - \beta$: genellikle 0,8.
- **Örneklem büyüklüğü** n: grup başına kişi sayısı.

Üçünü verirsin, dördüncüsü hesaplanır. `statsmodels` bunu `solve_power` ile
yapar; bilinmeyeni boş bırakırsın. Ortalamalar için `TTestIndPower`:

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

for d in [0.8, 0.5, 0.2, 0.1]:
    n = TTestIndPower().solve_power(effect_size=d, power=0.8, alpha=0.05)
    print(d, int(np.ceil(n)))
```

```text
0.8 26
0.5 64
0.2 394
0.1 1571
```

Kişi sayısı yukarı yuvarlanır (`ceil`): 25,5 kişi olmaz. Dikkat et:
**etki yarıya inince gereken kişi yaklaşık dört katına çıkıyor**
(0,2'de 394, 0,1'de 1 571). n, $1 / d^2$ ile büyür.
Küçük etkileri yakalamak pahalıdır.

## Oranlar için: kaç ziyaretçi?

Ödeme düğmesi testinde gerçek oranlar %11,4 ve %13,0'dı (veriyi biz
ürettik, o yüzden biliyoruz). Bu farkı %80 güçle yakalamak için grup başına
kaç kişi gerekir? Önce `proportion_effectsize` ile farkı Cohen's h'ye
çeviririz, sonra `NormalIndPower` (z-testine dayanır) ile çözeriz:

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

h = proportion_effectsize(0.130, 0.114)
n = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
print(round(h, 4), int(np.ceil(n)))
```

```text
0.0489 6562
```

Grup başına 6 562 kişi, toplam 13 124. 1,6 puanlık bir
fark için bu kadar çok kişi gerekiyor, çünkü h çok küçük.

## Benzetimle doğrulama

Hesabın söylediğini kendimiz deneyelim: bu büyüklükte 2000 test yapıp
kaçında farkın anlamlı çıktığını sayalım.

```python
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(401)
n_group = int(np.ceil(n))
hits = 0
for _ in range(2000):
    buy_a = rng.binomial(n_group, 0.114)
    buy_b = rng.binomial(n_group, 0.130)
    p = proportions_ztest([buy_b, buy_a], [n_group, n_group])[1]
    hits += p < 0.05
print(hits / 2000)
```

```text
0.804
```

Testlerin yaklaşık %80 kadarı farkı yakaladı: hesap tuttu.
`rng.binomial(n, p)` "n kişiden kaçı satın aldı" sayısını tek seferde
üretiyor; her kişiyi ayrı ayrı üretmeye gerek yok.

## Elimizdeki testin gücü

Önceki bölümlerde kullandığımız ödeme testinde her grupta 4000 kişi vardı.
O testin gücü neydi? Bilinmeyeni bu kez `power` yaparız. Aynı fonksiyonla
**en küçük yakalanabilir etkiyi** (minimum detectable effect, MDE) de
buluruz: %80 güçle yakalanabilecek en küçük h.

```python
power = NormalIndPower().power(effect_size=h, nobs1=4000, alpha=0.05)
mde = NormalIndPower().solve_power(nobs1=4000, power=0.8, alpha=0.05)
rate_b = np.sin(np.arcsin(np.sqrt(0.114)) + mde / 2) ** 2
print(round(power, 3))
print(round(mde, 4), round(rate_b, 4))
```

```text
0.59
0.0626 0.1347
```

- 4000'er kişiyle gerçek farkı yakalama şansı yalnızca %59.
  O testte fark anlamlı çıktı, ama bu biraz şanstı.
- MDE: h = 0,063. h'yi geri çevirince (h'nin formülünü $p_B$ için
  çözerek) %11,4'lük taban oranı ancak %13,5 düzeyine çıkarsa
  %80 güçle yakalanıyor. Gerçek oran %13,0, yani bu testin güvenle
  görebileceğinden küçük.

Test tasarlarken sorulacak soru: "Bu trafikle görebileceğim en küçük etki,
umduğum etkiden küçük mü?" Değilse test başlamadan başarısızdır.

## Güç eğrisi

Örneklem büyüdükçe güç nasıl artıyor? İki farklı gerçek etki için:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="386.791193pt" height="226.607609pt" viewBox="0 0 386.791193 226.607609" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 226.607609 
L 386.791193 226.607609 
L 386.791193 0 
L 0 0 
L 0 226.607609 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 44.103125 188.406828 
L 378.903125 188.406828 
L 378.903125 10.998828 
L 44.103125 10.998828 
L 44.103125 188.406828 
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
       <use xlink:href="#m15aed4d867" x="57.278598" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="57.278598" y="203.004484" transform="rotate(-0 57.278598 203.004484)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="108.346322" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="108.346322" y="203.004484" transform="rotate(-0 108.346322 203.004484)">5000</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="159.414046" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="159.414046" y="203.004484" transform="rotate(-0 159.414046 203.004484)">10000</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="210.481771" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.481771" y="203.004484" transform="rotate(-0 210.481771 203.004484)">15000</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="261.549495" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="261.549495" y="203.004484" transform="rotate(-0 261.549495 203.004484)">20000</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="312.617219" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="312.617219" y="203.004484" transform="rotate(-0 312.617219 203.004484)">25000</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="363.684943" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="363.684943" y="203.004484" transform="rotate(-0 363.684943 203.004484)">30000</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="211.503125" y="217.005266" transform="rotate(-0 211.503125 217.005266)">Grup başına kişi</text>
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
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="192.205656" transform="rotate(-0 37.103125 192.205656)">0.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="152.925228" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="156.724056" transform="rotate(-0 37.103125 156.724056)">0.2</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="117.443628" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="121.242456" transform="rotate(-0 37.103125 121.242456)">0.4</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="81.962028" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="85.760856" transform="rotate(-0 37.103125 85.760856)">0.6</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="46.480428" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="50.279256" transform="rotate(-0 37.103125 50.279256)">0.8</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="14.797656" transform="rotate(-0 37.103125 14.797656)">1.0</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="99.702828" transform="rotate(-90 14.797656 99.702828)">Güç</text>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 59.321307 174.599716 
L 65.449434 159.176147 
L 75.662979 133.154185 
L 81.791105 118.261009 
L 85.876523 108.855287 
L 89.961941 99.943332 
L 94.047359 91.564889 
L 98.132777 83.741936 
L 102.218195 76.482087 
L 106.303613 69.781563 
L 110.389031 63.627743 
L 114.474449 58.001338 
L 118.559867 52.878217 
L 122.645285 48.230921 
L 126.730703 44.029909 
L 130.816121 40.244559 
L 134.901539 36.84397 
L 138.986957 33.797586 
L 143.072375 31.075666 
L 147.157792 28.64964 
L 151.24321 26.492356 
L 155.328628 24.578242 
L 159.414046 22.883402 
L 163.499464 21.385662 
L 167.584882 20.064565 
L 173.713009 18.373522 
L 179.841136 16.981544 
L 185.969263 15.839759 
L 192.09739 14.906271 
L 200.268226 13.924834 
L 208.439062 13.181394 
L 218.652606 12.504081 
L 230.90886 11.955915 
L 245.207823 11.55817 
L 263.592204 11.275672 
L 292.190129 11.089229 
L 347.343271 11.008542 
L 363.684943 11.003767 
L 363.684943 11.003767 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_15">
    <path d="M 59.321307 178.281137 
L 71.577561 170.559626 
L 85.876523 161.267359 
L 130.816121 131.851956 
L 145.115084 122.855804 
L 157.371337 115.397268 
L 169.627591 108.208913 
L 181.883845 101.316827 
L 192.09739 95.81332 
L 202.310935 90.535797 
L 212.524479 85.488772 
L 222.738024 80.674385 
L 232.951569 76.092727 
L 243.165114 71.742137 
L 253.378659 67.619477 
L 263.592204 63.720369 
L 273.805749 60.039415 
L 284.019293 56.570392 
L 294.232838 53.306423 
L 304.446383 50.240128 
L 316.702637 46.810576 
L 328.958891 43.640657 
L 341.215145 40.716245 
L 353.471398 38.023145 
L 363.684943 35.945415 
L 363.684943 35.945415 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 44.103125 46.480428 
L 378.903125 46.480428 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: currentColor"/>
   </g>
   <g id="patch_3">
    <path d="M 44.103125 188.406828 
L 44.103125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 378.903125 188.406828 
L 378.903125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 44.103125 188.406828 
L 378.903125 188.406828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 44.103125 10.998828 
L 378.903125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="line2d_17">
     <path d="M 263.632812 158.503703 
L 273.632812 158.503703 
L 283.632812 158.503703 
" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="291.632812" y="162.003703" transform="rotate(-0 291.632812 162.003703)">11,4% → 13,0%</text>
    </g>
    <g id="line2d_18">
     <path d="M 263.632812 173.504484 
L 273.632812 173.504484 
L 283.632812 173.504484 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="291.632812" y="177.004484" transform="rotate(-0 291.632812 177.004484)">11,4% → 12,2%</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p80e0e5b987">
   <rect x="44.103125" y="10.998828" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Kesikli çizgi %80 güç. Turuncu eğri yarı büyüklükte bir fark; aynı güce çok daha sağda ulaşıyor.</figcaption>
</figure>

Etki yarıya inince aynı güce ulaşmak için yaklaşık dört kat kişi gerekiyor;
eğri sağa kayıyor.

## Kazananın laneti: düşük güç etkiyi abartır

Düşük güçlü bir testte "anlamlı" çıkan sonuçlar sistemli olarak **gerçek
etkiden büyüktür**. Nedeni: küçük örneklemde gerçek etki gürültünün
altında kalır; yalnızca şansın da büyüttüğü sonuçlar eşiği aşar. Buna
**kazananın laneti** (winner's curse) ya da **M tipi hata** (büyüklük
hatası) denir. Benzetimle görelim; gerçek fark 0,016:

```python
def curse(n_group, reps=2000):
    lifts, hits = [], 0
    for _ in range(reps):
        buy_a = rng.binomial(n_group, 0.114)
        buy_b = rng.binomial(n_group, 0.130)
        p = proportions_ztest([buy_b, buy_a], [n_group, n_group])[1]
        if p < 0.05 and buy_b > buy_a:
            hits += 1
            lifts.append((buy_b - buy_a) / n_group)
    return round(hits / reps, 2), round(float(np.mean(lifts)) / 0.016, 2)


for n_group in [1000, 4000, 6562]:
    print(n_group, *curse(n_group))
```

```text
1000 0.2 2.27
4000 0.59 1.3
6562 0.79 1.12
```

İkinci sütun güç, üçüncüsü anlamlı çıkan testlerdeki ortalama farkın
gerçek farka oranı.

- 1000'er kişide güç yalnızca %20; anlamlı çıkan testler farkı
  ortalama 2,3 kat büyük gösteriyor.
- Güç arttıkça abartma azalıyor; %80 güçte oran 1'e yakın.
- 4000'er kişilik ödeme testinde de bulduğumuz fark (2,2 puan) gerçek
  farktan (1,6 puan) büyüktü. Kazananın laneti tam olarak bu.

"Küçük testte büyük etki bulduk" haberine bu yüzden şüpheyle bakılır.
Yeterli güçle tekrarlanmayan bir sonuç büyük olasılıkla abartılıdır.

## Özet

- Güç, gerçek bir etkiyi yakalama olasılığıdır; genellikle 0,8 hedeflenir.
- Etki, $\alpha$, güç ve n'den üçü verilince dördüncüsü `solve_power` ile
  bulunur; n etkinin karesiyle ters orantılı büyür.
- Oranlarda önce `proportion_effectsize` ile h, sonra `NormalIndPower`.
- Hesap benzetimle doğrulanabilir.
- Var olan trafikle en küçük yakalanabilir etki (MDE) hesaplanır; umulan
  etkiden büyükse test başlamadan başarısızdır.
- Düşük güçte anlamlı çıkan sonuçlar etkiyi abartır.
