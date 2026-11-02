# t-Testi

Önceki iki bölümde testin mantığını ve p değerini gördük. Şimdi en sık
kullanılan testi ayrıntısıyla öğreniyoruz: **t-testi**. Üç türü var ve her
biri farklı bir soruya cevap verir:

| Tür | Soru | scipy |
|---|---|---|
| Tek örneklem | Bu grubun ortalaması belirli bir değerden farklı mı? | `ttest_1samp` |
| İki bağımsız örneklem | İki ayrı grubun ortalaması farklı mı? | `ttest_ind` |
| Eşli (bağımlı) örneklem | Aynı birimlerin önce/sonra ölçümleri farklı mı? | `ttest_rel` |

Tek örneklem t-testini Hipotez Testinin Mantığı bölümünde kullandık. Bu
bölüm öteki ikisine ve hangisinin ne zaman seçileceğine odaklanıyor; yanlış
tür seçmek, doğru veriyle yanlış sonuç almanın en kolay yolu.

## İki bağımsız grup: tasarım testi

Yeni bir sayfa tasarımı denendi: kullanıcıların yarısı eskisini (A), yarısı
yenisini (B) gördü. Soru: yeni tasarım oturumları uzattı mı?

```python
from scipy import stats
from ab_data import make_design_test

test = make_design_test()
a = test.loc[test["group"] == "A", "minutes"]
b = test.loc[test["group"] == "B", "minutes"]
result = stats.ttest_ind(b, a, equal_var=False)
low, high = result.confidence_interval(0.95)
print(len(a), round(a.mean(), 2), round(b.mean(), 2))
print(round(result.statistic, 3), f"{result.pvalue:.4f}")
print(round(b.mean() - a.mean(), 2), round(low, 2), round(high, 2))
```

```text
500 8.47 9.79
3.644 0.0003
1.32 0.61 2.03
```

- Her grupta 500 kullanıcı. B'nin ortalaması 9,79, A'nınki
  8,47 dakika.
- p = 0,0003: fark yokken bu kadar büyük bir fark görmek çok olası
  değil.
- Farkın %95 güven aralığı 0,61 ile 2,03 dakika. Bu satır p'den
  daha çok şey söylüyor: yeni tasarım oturumu büyük olasılıkla uzatıyor ama
  ne kadar uzattığı hâlâ geniş bir aralıkta.
- Veriyi biz ürettik: gerçek etki %10, yani yaklaşık 0,9 dakika. Aralık onu
  içeriyor; gözlenen fark (1,32) şans yüzünden biraz büyük çıkmış.

## Formülün içi: Welch testi

İki grubun ortalamaları arasındaki fark, farkın standart hatasına bölünür.
Fark iki bağımsız ortalamadan geldiği için varyansları toplanır:

$$t = \dfrac{\bar{x}_B - \bar{x}_A}{\sqrt{\dfrac{s_A^2}{n_A} + \dfrac{s_B^2}{n_B}}}$$

```python
import numpy as np
from ab_data import make_design_test

test = make_design_test()
a = test.loc[test["group"] == "A", "minutes"]
b = test.loc[test["group"] == "B", "minutes"]
se = np.sqrt(a.var() / len(a) + b.var() / len(b))
print(round((b.mean() - a.mean()) / se, 3))
print(round(a.std(), 2), round(b.std(), 2))
```

```text
3.644
5.29 6.15
```

Elle bulduğumuz t, `ttest_ind`'in verdiğiyle aynı. Bu formül iki grubun
sapmalarının **farklı** olabileceğini kabul eder; adı **Welch t-testi**.
scipy'de `equal_var=False` ile seçilir.

## Student mı, Welch mi?

`ttest_ind` varsayılan olarak (`equal_var=True`) **Student t-testini**
yapar: iki grubun sapmasının eşit olduğunu varsayar ve onları birleştirir.
Sapmalar ve grup boyları farklıysa bu varsayım pahalıya patlar. Gerçek
farkın **sıfır** olduğu bir dünyada ölçelim: küçük grup (20 kişi) çok
dağınık, büyük grup (80 kişi) çok tutarlı.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(111)
small = rng.normal(10, 6, size=(5000, 20))
large = rng.normal(10, 2, size=(5000, 80))
student = stats.ttest_ind(small, large, axis=1).pvalue
welch = stats.ttest_ind(small, large, axis=1, equal_var=False).pvalue
print(round((student < 0.05).mean(), 3), round((welch < 0.05).mean(), 3))
```

```text
0.259 0.056
```

- Fark yokken Student testi %25,9 oranında "anlamlı" dedi: söz
  verilen %5'in beş katı.
- Welch %5,6: sözünü tutuyor.
- Sapmalar gerçekten eşitse Welch neredeyse hiçbir şey kaybetmez. Bu yüzden
  iki grubu karşılaştırırken varsayılan seçim **Welch** (`equal_var=False`).

## Eşli ölçümler: aynı sayfa, önce ve sonra

Bir ekip görselleri sıkıştırdı ve aynı 25 sayfanın açılış süresini önce ve
sonra ölçtü. Sayfalar birbirinden çok farklı (biri hafif, biri ağır), ama
her sayfa kendi önceki hâliyle karşılaştırılabilir.

```python
from scipy import stats
from ab_data import make_paired_speed

pages = make_paired_speed()
diff = pages["before"] - pages["after"]
print(round(diff.mean(), 1), round(diff.std(), 1))
print(round(pages["before"].std(), 1))
print(round(stats.ttest_rel(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.ttest_ind(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.ttest_1samp(diff, 0).pvalue, 4))
```

```text
17.2 34.9
153.4
0.0211
0.7022
0.0211
```

- Sayfa başına ortalama kazanç 17,2 ms. Farkların sapması yalnızca
  34,9 ms, sayfaların kendi sapması ise 153,4 ms.
- **Eşli t-testi** (`ttest_rel`) p = 0,0211: kazanç anlamlı.
- Aynı veriye bağımsız grup testi uygulanınca p = 0,7022: hiçbir şey
  görünmüyor. Sayfalar arasındaki büyük fark (hafif ve ağır sayfalar),
  20 ms'lik kazancı gürültünün içine gömüyor.
- Son satır: eşli test aslında **farkların** tek örneklem t-testidir; p
  birebir aynı.

Bu tek bir veri setinin şansı mı? Aynı deneyi 500 farklı sayfa grubuyla
tekrarlayalım:

```python
import numpy as np
from scipy import stats
from ab_data import make_paired_speed

paired, unpaired = [], []
for seed in range(1000, 1500):
    pages = make_paired_speed(seed=seed)
    before, after = pages["before"], pages["after"]
    paired.append(stats.ttest_rel(before, after).pvalue < 0.05)
    unpaired.append(stats.ttest_ind(before, after).pvalue < 0.05)
print(round(np.mean(paired), 3), round(np.mean(unpaired), 3))
```

```text
0.782 0.0
```

Eşli test gerçek 20 ms'lik kazancı tekrarların %78,2 kadarında
yakaladı, bağımsız grup testi %0,0. Verinin yapısı eşliyse
eşli test kullanılır; bu, aynı veriden çok daha fazla bilgi çıkarmak
demektir.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="373.330781pt" height="230.984pt" viewBox="0 0 373.330781 230.984" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 230.984 
L 373.330781 230.984 
L 373.330781 0 
L 0 0 
L 0 230.984 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 53.650781 206.784 
L 366.130781 206.784 
L 366.130781 7.2 
L 53.650781 7.2 
L 53.650781 206.784 
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
       <use xlink:href="#m15aed4d867" x="112.240781" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="112.240781" y="221.381656" transform="rotate(-0 112.240781 221.381656)">önce</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="307.540781" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="307.540781" y="221.381656" transform="rotate(-0 307.540781 221.381656)">sonra</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_3">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="189.823304" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="193.622132" transform="rotate(-0 46.650781 193.622132)">600</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="163.527652" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="167.32648" transform="rotate(-0 46.650781 167.32648)">700</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="137.232" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="141.030828" transform="rotate(-0 46.650781 141.030828)">800</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="110.936348" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="114.735176" transform="rotate(-0 46.650781 114.735176)">900</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="84.640696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="88.439524" transform="rotate(-0 46.650781 88.439524)">1000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="58.345043" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="62.143872" transform="rotate(-0 46.650781 62.143872)">1100</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="32.049391" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="35.848219" transform="rotate(-0 46.650781 35.848219)">1200</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="106.992" transform="rotate(-90 14.798438 106.992)">Açılış süresi (ms)</text>
    </g>
   </g>
   <g id="line2d_10">
    <path d="M 112.240781 76.226087 
L 307.540781 84.903652 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m0653a46230" d="M 0 1.5 
C 0.397805 1.5 0.77937 1.341951 1.06066 1.06066 
C 1.341951 0.77937 1.5 0.397805 1.5 0 
C 1.5 -0.397805 1.341951 -0.77937 1.06066 -1.06066 
C 0.77937 -1.341951 0.397805 -1.5 0 -1.5 
C -0.397805 -1.5 -0.77937 -1.341951 -1.06066 -1.06066 
C -1.341951 -0.77937 -1.5 -0.397805 -1.5 0 
C -1.5 0.397805 -1.341951 0.77937 -1.06066 1.06066 
C -0.77937 1.341951 -0.397805 1.5 0 1.5 
z
" style="stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </defs>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="76.226087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="84.903652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 112.240781 23.10887 
L 307.540781 22.057043 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="23.10887" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="22.057043" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 112.240781 164.842435 
L 307.540781 185.878957 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="164.842435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="185.878957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 112.240781 107.254957 
L 307.540781 128.554435 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="107.254957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="128.554435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 112.240781 57.293217 
L 307.540781 65.970783 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="57.293217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 112.240781 63.078261 
L 307.540781 71.49287 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="63.078261" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="71.49287" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 112.240781 55.715478 
L 307.540781 55.978435 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="55.715478" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="55.978435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_17">
    <path d="M 112.240781 111.199304 
L 307.540781 101.995826 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="111.199304" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="101.995826" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_18">
    <path d="M 112.240781 65.970783 
L 307.540781 58.345043 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="58.345043" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_19">
    <path d="M 112.240781 20.216348 
L 307.540781 16.272 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="20.216348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="16.272" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_20">
    <path d="M 112.240781 67.285565 
L 307.540781 78.592696 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="67.285565" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="78.592696" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_21">
    <path d="M 112.240781 64.130087 
L 307.540781 65.970783 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="64.130087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_22">
    <path d="M 112.240781 134.076522 
L 307.540781 129.869217 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="134.076522" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="129.869217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_23">
    <path d="M 112.240781 184.301217 
L 307.540781 197.712 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="184.301217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="197.712" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_24">
    <path d="M 112.240781 131.446957 
L 307.540781 128.291478 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="131.446957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="128.291478" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_25">
    <path d="M 112.240781 115.406609 
L 307.540781 114.354783 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="115.406609" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="114.354783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_26">
    <path d="M 112.240781 64.130087 
L 307.540781 75.96313 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="64.130087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="75.96313" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_27">
    <path d="M 112.240781 116.458435 
L 307.540781 111.199304 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="116.458435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="111.199304" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_28">
    <path d="M 112.240781 110.936348 
L 307.540781 103.310609 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="110.936348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="103.310609" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_29">
    <path d="M 112.240781 103.573565 
L 307.540781 114.354783 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="103.573565" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="114.354783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_30">
    <path d="M 112.240781 42.041739 
L 307.540781 54.663652 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="42.041739" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="54.663652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_31">
    <path d="M 112.240781 104.888348 
L 307.540781 107.78087 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="104.888348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="107.78087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_32">
    <path d="M 112.240781 115.143652 
L 307.540781 125.661913 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="115.143652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="125.661913" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_33">
    <path d="M 112.240781 100.15513 
L 307.540781 116.721391 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="100.15513" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="116.721391" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_34">
    <path d="M 112.240781 100.15513 
L 307.540781 96.210783 
" clip-path="url(#p2b7d30b22d)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p2b7d30b22d)">
     <use xlink:href="#m0653a46230" x="112.240781" y="100.15513" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="96.210783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 53.650781 206.784 
L 53.650781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 366.130781 206.784 
L 366.130781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 53.650781 206.784 
L 366.130781 206.784 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 53.650781 7.2 
L 366.130781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p2b7d30b22d">
   <rect x="53.650781" y="7.2" width="312.48" height="199.584"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Her çizgi bir sayfa. Sayfalar arasındaki fark yüzlerce milisaniye; her sayfanın kendi içindeki iniş ise küçük ama hemen hepsinde aynı yönde. Eşli test bu ikinciye bakar.</figcaption>
</figure>

## Varsayımlar

- **Bağımsızlık:** gruptaki ölçümler birbirinden bağımsız olmalı (aynı
  kullanıcı iki kez sayılmamalı). Eşli testte bağımsız olan **çiftlerdir**.
- **Normallik:** küçük örneklemde ortalamaların çan biçimli olması gerekir.
  Merkezi limit teoremi sayesinde büyük örneklemde (burada 500'er kişi)
  verinin çarpık olması sorun değil. Küçük ve çok çarpık örneklemde
  parametrik olmayan testlere ya da bootstrap'e bak.
- **Eşit sapma:** yalnızca Student testi ister; Welch istemez.

## Özet

- Bağımsız iki grup → `ttest_ind(..., equal_var=False)` (Welch). Varsayılan
  Student testi, sapmalar ve grup boyları farklıyken yanlış alarm üretir.
- Aynı birimlerin önce/sonra ölçümü → `ttest_rel`. Farkların tek örneklem
  testine eşittir ve birimler arası farkı ayıkladığı için çok daha
  güçlüdür.
- p'nin yanına farkı ve güven aralığını (`confidence_interval`) koy.
