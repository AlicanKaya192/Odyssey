# Genel Tekrar

Veri Bilimi Kütüphaneleri modülünün sonuna geldin. NumPy'nin dizilerinden
pandas'ın indeksine, birleştirme ve yeniden şekillendirmeden zamana ve
kategorilere, matplotlib ve seaborn grafiklerinden SciPy'nin istatistik ve en
iyileme araçlarına kadar veri biliminin günlük işini yapan kütüphaneleri
derinlemesine gördün. Bu bölüm yolu bir kez daha yürüyor; sonunda dört
kütüphanenin birlikte çalıştığı bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">NumPy<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">pandas<br><small>04–09</small></span><span class="arrow">→</span>
    <span class="node">Grafik<br><small>10–13</small></span><span class="arrow">→</span>
    <span class="node acc">SciPy<br><small>14–15</small></span>
  </div>
  <figcaption>Modülün yolu: önce sayı dizileri, sonra etiketli tablolar, sonra görmek, en sonda sınamak ve en iyilemek.</figcaption>
</figure>

## 1. NumPy (Bölüm 0–3)

| İş | Araç |
|---|---|
| Dizi ve tür | `np.array(..., dtype=)`, `shape`, `astype`, `int8` taşması |
| Seçmek | dilim (görünüm), maske ve dizinle seçim (kopya), `np.where` |
| Şekiller arası işlem | yayınlama: sağdan karşılaştır; `keepdims=True` |
| Hızlı fonksiyonlar | ufunc: `np.add.reduce`, `accumulate`, `outer` |
| Rastgele | `rng = np.random.default_rng(tohum)`, `choice`, `permutation` |
| Doğrusal cebir | `@`, `np.linalg.solve`, `lstsq`, `cond`, `norm` |

Dilim kopya değil görünümdür; `int8` sessizce taşar; tersini almak yerine
`solve`.

## 2. pandas (Bölüm 4–9)

| İş | Araç |
|---|---|
| Etiket | hizalama, `loc` / `iloc`, `set_index`, MultiIndex, `xs`, `sort_index` |
| Birleştirmek | `merge(how="left", validate=, indicator=True)`, `concat`, `join`, `merge_asof` |
| Şekil | `melt`, `pivot`, `pivot_table(aggfunc=)`, `stack` / `unstack`, `explode` |
| Zaman | `to_datetime(format=)`, `.dt`, `resample("ME")`, `shift`, `rolling` |
| Metin ve kategori | `.str`, `extract`, `category`, sıralı kategori, `cut` / `qcut` |
| Hız | vektörel işlem, `np.select`, Copy-on-Write, `downcast`, `transform` |

Etiket eşleşmezse `NaN`; varsayılan `inner` satır atar; `pivot` tekrarda
durur; pandas 3'te zincirli atama işe yaramaz, `loc` ile tek adımda yaz.

## 3. Grafik (Bölüm 10–13)

| İş | Araç |
|---|---|
| Nesneler | `fig, ax = plt.subplots(...)`, `sharey`, `layout="constrained"`, `plt.close` |
| Türler | `plot`, `scatter`, `bar` / `barh`, `hist`, `boxplot`, `imshow`, `fill_between` |
| Ayar | `set_major_formatter`, `annotate`, `set_yscale("log")`, `twinx`, `bar_label` |
| seaborn | `hue`, `col`, `estimator`, `errorbar`; alan ve şekil düzeyi |

Önce soru, sonra grafik; çubuk sıfırdan başlar; tek vurgu rengi; `barplot`
ortalama çizer.

## 4. SciPy (Bölüm 14–15)

| İş | Araç |
|---|---|
| Dağılım | `stats.norm(...)`: `cdf`, `sf`, `ppf`, `rvs(random_state=)` |
| Test | `ttest_ind(equal_var=False)`, `chi2_contingency`, `pearsonr` / `spearmanr` |
| Belirsizlik | `confidence_interval()`, `sem`, etki büyüklüğü |
| En iyileme | `minimize_scalar`, `minimize`, `curve_fit`, `root_scalar`, `linprog` |
| Ara değer | `np.interp`, `CubicSpline`, `PchipInterpolator` |

"Anlamlı değil" fark yok demek değildir; scipy en küçükler; kısıtı unutma.

## Hepsi birlikte

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(16)
days = pd.date_range("2026-01-01", periods=120, freq="D")
orders = pd.DataFrame({
    "date": rng.choice(days, 600),
    "store": pd.Categorical(rng.choice(["Izmir", "Ankara"], 600)),
    "amount": rng.gamma(4, 30, 600).round(2),
})
monthly = (orders.set_index("date").groupby("store", observed=True)["amount"]
           .resample("ME").sum().unstack(0).round(0).astype(int))
print(monthly.index.strftime("%Y-%m").tolist())
print(monthly.to_dict(orient="list"))
izmir = orders.loc[orders["store"] == "Izmir", "amount"]
ankara = orders.loc[orders["store"] == "Ankara", "amount"]
res = stats.ttest_ind(izmir, ankara, equal_var=False)
low, high = res.confidence_interval()
print(round(float(izmir.mean() - ankara.mean()), 2), round(float(res.pvalue), 3))
print(round(float(low), 2), round(float(high), 2))
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
for name in monthly.columns:
    ax.plot(monthly.index, monthly[name], marker="o", label=name)
ax.set(title="Monthly revenue", ylabel="amount")
ax.legend()
fig.savefig("monthly.png")
print(len(ax.lines))
```

```text
['2026-01', '2026-02', '2026-03', '2026-04']
{'Ankara': [9413, 8160, 8430, 8263], 'Izmir': [10863, 7946, 9156, 9237]}
6.61 0.177
-3.0 16.22
2
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.398185pt" height="224.39952pt" viewBox="0 0 440.398185 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.398185 224.39952 
L 440.398185 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 60.0125 200.19952 
L 416.710422 200.19952 
L 416.710422 22.318125 
L 60.0125 22.318125 
L 60.0125 200.19952 
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
       <use xlink:href="#m15aed4d867" x="79.869534" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="79.869534" y="214.797176" transform="rotate(-0 79.869534 214.797176)">2026-02-01</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="130.87843" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="130.87843" y="214.797176" transform="rotate(-0 130.87843 214.797176)">2026-02-15</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="181.887326" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="181.887326" y="214.797176" transform="rotate(-0 181.887326 214.797176)">2026-03-01</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="232.896222" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="232.896222" y="214.797176" transform="rotate(-0 232.896222 214.797176)">2026-03-15</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="294.835596" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="294.835596" y="214.797176" transform="rotate(-0 294.835596 214.797176)">2026-04-01</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="345.844492" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="345.844492" y="214.797176" transform="rotate(-0 345.844492 214.797176)">2026-04-15</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="404.140373" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="404.140373" y="214.797176" transform="rotate(-0 404.140373 214.797176)">2026-05-01</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="189.120392" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="192.919221" transform="rotate(-0 53.0125 192.919221)">8000</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="161.401784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="165.200613" transform="rotate(-0 53.0125 165.200613)">8500</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="133.683176" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="137.482004" transform="rotate(-0 53.0125 137.482004)">9000</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="105.964568" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="109.763396" transform="rotate(-0 53.0125 109.763396)">9500</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="78.24596" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="82.044788" transform="rotate(-0 53.0125 82.044788)">10000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="50.527352" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="54.32618" transform="rotate(-0 53.0125 54.32618)">10500</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="60.0125" y="22.808744" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="53.0125" y="26.607572" transform="rotate(-0 53.0125 26.607572)">11000</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="111.258822" transform="rotate(-90 14.797656 111.258822)">amount</text>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 76.226042 110.787606 
L 178.243834 180.250438 
L 291.192103 165.282389 
L 400.49688 174.540405 
" clip-path="url(#p4a7d0a8874)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p4a7d0a8874)">
     <use xlink:href="#m98ae7f93d8" x="76.226042" y="110.787606" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="178.243834" y="180.250438" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="291.192103" y="165.282389" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="400.49688" y="174.540405" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 76.226042 30.403643 
L 178.243834 192.114002 
L 291.192103 125.034971 
L 400.49688 120.544556 
" clip-path="url(#p4a7d0a8874)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p4a7d0a8874)">
     <use xlink:href="#m43dc4bf304" x="76.226042" y="30.403643" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="178.243834" y="192.114002" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="291.192103" y="125.034971" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="400.49688" y="120.544556" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 60.0125 200.19952 
L 60.0125 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 416.710422 200.19952 
L 416.710422 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 60.0125 200.19952 
L 416.710422 200.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 60.0125 22.318125 
L 416.710422 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="238.361461" y="16.318125" transform="rotate(-0 238.361461 16.318125)">Monthly revenue</text>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 342.549485 60.319687 
L 409.710422 60.319687 
Q 411.710422 60.319687 411.710422 58.319687 
L 411.710422 29.318125 
Q 411.710422 27.318125 409.710422 27.318125 
L 342.549485 27.318125 
Q 340.549485 27.318125 340.549485 29.318125 
L 340.549485 58.319687 
Q 340.549485 60.319687 342.549485 60.319687 
L 342.549485 60.319687 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_17">
     <path d="M 344.549485 35.416562 
L 354.549485 35.416562 
L 364.549485 35.416562 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m98ae7f93d8" x="354.549485" y="35.416562" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="372.549485" y="38.916562" transform="rotate(-0 372.549485 38.916562)">Ankara</text>
    </g>
    <g id="line2d_18">
     <path d="M 344.549485 50.417344 
L 354.549485 50.417344 
L 364.549485 50.417344 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m43dc4bf304" x="354.549485" y="50.417344" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="372.549485" y="53.917344" transform="rotate(-0 372.549485 53.917344)">Izmir</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p4a7d0a8874">
   <rect x="60.0125" y="22.318125" width="356.697922" height="177.881395"/>
  </clipPath>
 </defs>
</svg>
<figcaption>İki mağazanın aylık cirosu.</figcaption>
</figure>

- **NumPy** sabit tohumlu üreteçle 600 sipariş üretti (`gamma` dağılımı:
  tutarlar sağa çarpık, eksi yok).
- **pandas** mağazayı kategori yaptı, tarihi indekse taşıdı, mağaza başına
  aylık topladı (`groupby` + `resample("ME")`) ve mağazaları `unstack` ile
  sütunlara çevirdi.
- **SciPy** iki mağazanın sipariş tutarlarını Welch testiyle karşılaştırdı:
  İzmir ortalama 6,61 fazla ama aralık −3,0 ile 16,22 arası, p = 0,177. Veri
  farkı göstermeye yetmiyor.
- **matplotlib** iki mağazanın aylık cirosunu çizdi ve kaydetti.

## Sonra

Bu modülün araçları bir sonraki adımın zemini: **ML Kütüphaneleri**
modülünde scikit-learn'ün ön işleme, pipeline, model seçimi ve
metrikleri bu tabloların ve dizilerin üstüne kuruluyor. Notlarda bütün
modülün tek sayfalık özeti ve buradan nereye gidileceği var.
