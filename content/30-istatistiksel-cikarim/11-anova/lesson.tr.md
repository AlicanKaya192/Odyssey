# ANOVA: Çok Grubu Karşılaştırmak

Bu kez iki değil, dört sayfa düzeni (A, B, C, D) denendi; her birini 150
kullanıcı gördü. Soru: düzen, sayfada geçen süreyi değiştiriyor mu? İlk akla
gelen, her çifti t-testiyle karşılaştırmak: A–B, A–C, A–D, B–C, B–D, C–D,
altı test. Bu bölüm bunun neden kötü bir fikir olduğunu ölçerek gösteriyor
ve doğru aracı tanıtıyor: **varyans analizi** (analysis of variance,
**ANOVA**).

## Veri

```python
from ab_data import make_layout_test

test = make_layout_test()
summary = test.groupby("layout")["minutes"].agg(["count", "mean", "std"])
print(summary.round(2).to_string())
```

```text
        count  mean   std
layout                   
A         150  7.73  2.93
B         150  7.84  2.80
C         150  9.17  3.26
D         150  8.60  3.01
```

Dört ortalama birbirinden farklı. Ama her grup 150 kişi ve sapmalar 3
dakika civarında: bu farkların ne kadarı gerçek, ne kadarı şans?

## Altı t-testinin sorunu

Bütün grupların **gerçekten aynı** olduğu bir dünyada altı çift
karşılaştırma yapalım ve en az birinin "anlamlı" çıkma sıklığını sayalım:

```python
import itertools
import numpy as np
from scipy import stats

rng = np.random.default_rng(171)
hits = 0
for _ in range(4000):
    groups = rng.normal(8, 3, size=(4, 150))
    pairs = itertools.combinations(range(4), 2)
    p = [stats.ttest_ind(groups[i], groups[j]).pvalue for i, j in pairs]
    hits += min(p) < 0.05
print(round(hits / 4000, 3), round(1 - 0.95 ** 6, 3))
```

```text
0.19 0.265
```

- Hiçbir fark yokken deneylerin %19,0 kadarında en az bir çift
  "anlamlı" çıktı: söz verilen %5'in yaklaşık dört katı.
- Altı bağımsız test olsaydı oran $1 - 0{,}95^6 \approx$ 0,265
  olurdu. Gerçek oran biraz daha düşük, çünkü testler aynı grupları
  paylaşıyor ve birbirinden bağımsız değil. Yine de yanlış alarm şansı
  katlanıyor.
- "En az bir yanlış alarm" olasılığına **aile boyu hata oranı**
  (family-wise error rate) denir. Grup sayısı arttıkça çift sayısı hızla
  büyür: 10 grupta 45 çift.

## ANOVA'nın fikri: iki tür oynama

ANOVA tek bir soru sorar: "Grupların hepsinin ortalaması aynı mı?"
$H_0$: $\mu_A = \mu_B = \mu_C = \mu_D$. Cevabı iki tür oynamayı
karşılaştırarak bulur:

- **Gruplar arası** (between groups): grup ortalamaları genel ortalamadan ne
  kadar uzak?
- **Grup içi** (within groups): her grubun içinde kullanıcılar kendi grup
  ortalamalarından ne kadar uzak?

Gruplar gerçekten aynıysa grup ortalamaları yalnızca şans yüzünden oynar
ve iki oynama birbirine yakın çıkar. Gruplar farklıysa gruplar arası
oynama büyür. Oranlarına **F istatistiği** denir:

$$F = \dfrac{\text{gruplar arası kareler toplamı} / (k - 1)}{\text{grup içi kareler toplamı} / (N - k)}$$

$k$ grup sayısı, $N$ toplam kişi sayısı. Paydaki ve paydadaki bölenler
serbestlik dereceleri.

```python
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
groups = [g["minutes"].to_numpy() for _, g in test.groupby("layout")]
values = test["minutes"].to_numpy()
grand = values.mean()
between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
within = sum(((g - g.mean()) ** 2).sum() for g in groups)
k, n = len(groups), len(values)
f = (between / (k - 1)) / (within / (n - k))
print(round(between, 1), round(within, 1), round(f, 3))
print(f"{stats.f.sf(f, k - 1, n - k):.1e}")
result = stats.f_oneway(*groups)
print(round(result.statistic, 3), f"{result.pvalue:.1e}")
```

```text
208.2 5378.4 7.692
4.8e-05
7.692 4.8e-05
```

- Gruplar arası kareler toplamı 208,2, grup içi 5378,4.
  Ortalama karelere çevrilince F = 7,692: gruplar arası oynama, şansın
  açıklayacağından yaklaşık 7,7 kat büyük.
- p **F dağılımından** gelir (`stats.f.sf`), iki serbestlik derecesiyle
  (3 ve 596). `stats.f_oneway` aynı hesabı tek satırda yapıyor.
- p çok küçük: düzenlerin hepsi aynı değil. Ama **hangileri** farklı? ANOVA
  bunu söylemez.

## Etki büyüklüğü: η²

Toplam oynamanın ne kadarı gruplardan geliyor? **Eta kare** ($\eta^2$):

$$\eta^2 = \dfrac{\text{gruplar arası}}{\text{gruplar arası} + \text{grup içi}}$$

Burada $\eta^2$ = 0,037: süre farklarının yalnızca yaklaşık %4'ü
düzenden geliyor; geri kalanı kullanıcılar arasındaki doğal fark. Önemli bir
düzen farkı olabilir, ama kullanıcıların davranışını büyük ölçüde başka
şeyler belirliyor.

## Hangi gruplar farklı? Tukey testi

ANOVA "en az biri farklı" dedikten sonra çiftlere bakmak için çoklu
karşılaştırmayı hesaba katan bir **post-hoc** (sonradan yapılan) test
kullanılır. En yaygını **Tukey HSD** (honestly significant difference):
altı çifti birlikte değerlendirir ve aile boyu hata oranını %5'te tutar.

```python
import itertools
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
names = sorted(test["layout"].unique())
groups = [test.loc[test["layout"] == n, "minutes"] for n in names]
res = stats.tukey_hsd(*groups)
for i, j in itertools.combinations(range(4), 2):
    diff = float(res.statistic[i, j])
    p = float(res.pvalue[i, j])
    print(names[i], names[j], round(diff, 2), round(p, 4))
```

```text
A B -0.1 0.9911
A C -1.44 0.0002
A D -0.87 0.0609
B C -1.34 0.0007
B D -0.77 0.1229
C D 0.57 0.3475
```

- `res.statistic[i, j]` birinci eksi ikinci grubun ortalama farkı.
- C, A'dan ve B'den belirgin farklı (p'ler 0,0002 ve 0,0007).
- A–D (p = 0,0609) sınırda, C–D (p = 0,3475) değil.
- Gerçek ortalamalar A 8,0, B 8,0, C 8,8, D 8,2 idi. Tukey C'nin öne çıktığını
  doğru buldu; C ile D arasındaki 0,6 dakikalık gerçek farkı ise 150'şer
  kişiyle ayırt edemedi. "Anlamlı değil" yine "fark yok" demek değil.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="386.103906pt" height="208.808pt" viewBox="0 0 386.103906 208.808" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 208.808 
L 386.103906 208.808 
L 386.103906 0 
L 0 0 
L 0 208.808 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 44.103906 184.608 
L 378.903906 184.608 
L 378.903906 7.2 
L 44.103906 7.2 
L 44.103906 184.608 
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
       <use xlink:href="#m15aed4d867" x="91.932478" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="91.932478" y="199.205656" transform="rotate(-0 91.932478 199.205656)">A</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="171.646763" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="171.646763" y="199.205656" transform="rotate(-0 171.646763 199.205656)">B</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="251.361049" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="251.361049" y="199.205656" transform="rotate(-0 251.361049 199.205656)">C</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="331.075335" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="331.075335" y="199.205656" transform="rotate(-0 331.075335 199.205656)">D</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="160.722691" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="164.521519" transform="rotate(-0 37.103906 164.521519)">7.5</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="127.67383" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="131.472658" transform="rotate(-0 37.103906 131.472658)">8.0</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="94.62497" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="98.423798" transform="rotate(-0 37.103906 98.423798)">8.5</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="61.576109" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="65.374937" transform="rotate(-0 37.103906 65.374937)">9.0</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="28.527248" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="32.326077" transform="rotate(-0 37.103906 32.326077)">9.5</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="95.904" transform="rotate(-90 14.798438 95.904)">Ortalama süre (dakika)</text>
    </g>
   </g>
   <g id="LineCollection_1">
    <path d="M 91.932478 176.544 
L 91.932478 114.108656 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_10">
    <defs>
     <path id="mef9653b673" d="M 6 0 
L -6 -0 
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="91.932478" y="176.544" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_11">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="91.932478" y="114.108656" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_2">
    <path d="M 171.646763 168.463991 
L 171.646763 108.687104 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_12">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="171.646763" y="168.463991" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_13">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="171.646763" y="108.687104" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_3">
    <path d="M 251.361049 84.762829 
L 251.361049 15.264 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_14">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="251.361049" y="84.762829" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_15">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="251.361049" y="15.264" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_4">
    <path d="M 331.075335 120.096131 
L 331.075335 55.916637 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_16">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="331.075335" y="120.096131" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_17">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="331.075335" y="55.916637" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_18">
    <defs>
     <path id="mee854baf65" d="M 0 3.5 
C 0.928211 3.5 1.81853 3.131218 2.474874 2.474874 
C 3.131218 1.81853 3.5 0.928211 3.5 0 
C 3.5 -0.928211 3.131218 -1.81853 2.474874 -2.474874 
C 1.81853 -3.131218 0.928211 -3.5 0 -3.5 
C -0.928211 -3.5 -1.81853 -3.131218 -2.474874 -2.474874 
C -3.131218 -1.81853 -3.5 -0.928211 -3.5 0 
C -3.5 0.928211 -3.131218 1.81853 -2.474874 2.474874 
C -1.81853 3.131218 -0.928211 3.5 0 3.5 
z
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="91.932478" y="145.326328" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_19">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="171.646763" y="138.575548" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_20">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="251.361049" y="50.013414" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_21">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="331.075335" y="88.006384" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 44.103906 184.608 
L 44.103906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 378.903906 184.608 
L 378.903906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 44.103906 184.608 
L 378.903906 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 44.103906 7.2 
L 378.903906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p8aac6f4af8">
   <rect x="44.103906" y="7.2" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Dört düzenin ortalaması ve %95 güven aralığı. C öne çıkıyor; A ile B neredeyse aynı, D arada.</figcaption>
</figure>

## Varsayımlar

- **Bağımsızlık:** her kullanıcı tek grupta.
- **Normallik:** grup ortalamaları çan biçimli olmalı; büyük gruplarda
  merkezi limit teoremi bunu sağlar.
- **Eşit varyans:** klasik ANOVA, Student t-testi gibi, grupların sapmalarını
  eşit varsayar. Sapmalar belirgin farklıysa **Welch ANOVA** kullanılır
  (`statsmodels.stats.oneway.anova_oneway(..., use_var="unequal")`).

## Özet

- Çok grubu çift çift t-testiyle karşılaştırmak yanlış alarmları katlar (aile
  boyu hata oranı).
- ANOVA tek testte "hepsi aynı mı?" diye sorar: F = gruplar arası oynama /
  grup içi oynama (`stats.f_oneway`).
- Hangi grupların farklı olduğunu Tukey HSD gibi bir post-hoc test söyler
  (`stats.tukey_hsd`).
- $\eta^2$ farkın ne kadarının gruplardan geldiğini ölçer; p'nin yanına koy.
