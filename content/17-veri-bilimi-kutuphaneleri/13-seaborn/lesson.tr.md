# seaborn

matplotlib her şeyi çizebilir ama her şeyi **sen** söylersin: hangi değer
hangi renk, açıklama kutusu, gruplara göre ortalama. seaborn matplotlib'in
üstüne kurulu bir kütüphane: DataFrame'i ve sütun adlarını alır, gruplamayı,
renklendirmeyi, açıklamayı ve istatistik özetini kendisi yapar. Çıktı yine
matplotlib nesnesidir; önceki bölümlerde öğrendiğin her ayar geçerli. Bu
bölüm seaborn'un iki düzeyini, en sık kullanılan grafiklerini ve **sessizce
yaptığı hesapları** anlatıyor.

## Bu bölümün verisi

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(14)
n = 240
df = pd.DataFrame({
    "store": rng.choice(["Izmir", "Ankara", "Bursa"], n),
    "day": rng.choice(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], n),
    "hour": rng.integers(9, 21, n),
})
df["weekend"] = df["day"].isin(["Sat", "Sun"])
noise = rng.normal(0, 15, n)
df["sales"] = (50 + 4 * df["hour"] + 30 * df["weekend"] + noise).round(1)
print(df.shape, df["store"].value_counts().sort_index().to_dict())
print(df.head(3))
```

```text
(240, 5) {'Ankara': 66, 'Bursa': 87, 'Izmir': 87}
    store  day  hour  weekend  sales
0   Izmir  Tue    13    False   97.3
1   Bursa  Sat     9     True  134.3
2  Ankara  Thu     9    False  117.1
```

- Üç mağazanın satış kayıtları: gün, saat, hafta sonu mu, satış. Satış saatle
  artıyor, hafta sonu 30 fazla, üstüne gürültü.
- Bölümdeki diğer bloklar bu `df`'yi kullanıyor; bir defterde (notebook)
  olduğu gibi sırayla çalıştır.
- seaborn'un örneklerinde sık görülen `sns.load_dataset("tips")` veriyi
  **internetten** indirir. Odyssey çevrimdışı çalıştığı için burada kendi
  verimizi üretiyoruz.
- seaborn **uzun** biçimli (düzenli) veri ister: her satır bir gözlem, her
  değişken bir sütun. Yeniden şekillendirme bölümündeki `melt` burada işe
  yarar.

## İki düzey: alan ve şekil

```python
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
out = sns.histplot(df, x="sales", hue="weekend", ax=ax)
print(type(out).__name__, out is ax)
grid = sns.displot(df, x="sales", col="weekend", height=2.5)
print(type(grid).__name__, len(grid.axes.flat), type(grid.figure).__name__)
plt.close(grid.figure)
```

```text
Axes True
FacetGrid 2 Figure
```

| Düzey | Örnekler | Döndürür | Yeri |
|---|---|---|---|
| Alan (axes-level) | `histplot`, `boxplot`, `scatterplot`, `lineplot`, `heatmap` | `Axes` | `ax=` ile verdiğin alan |
| Şekil (figure-level) | `displot`, `catplot`, `relplot`, `lmplot`, `pairplot` | `FacetGrid` / `PairGrid` | kendi şeklini açar |

- Alan düzeyindeki fonksiyon matplotlib'in bir `Axes`'ine çizer; `ax=` ile
  `plt.subplots` alanlarına yerleştirilir, gerisi önceki bölümler gibi.
- Şekil düzeyindeki fonksiyon kendi şeklini kurar ve `col=` / `row=` ile
  veriyi **panellere** böler. Boyutu `figsize` değil `height` (panel başına
  inç) ve `aspect` ile verilir; `ax=` almaz.

## Dağılım: histplot ve kde

```python
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
sns.histplot(df, x="sales", hue="weekend", stat="density", common_norm=False,
             kde=True, ax=ax)
print(df.groupby("weekend")["sales"].mean().round(1).to_dict())
print(df["weekend"].value_counts().to_dict())
```

```text
{False: 109.0, True: 136.1}
{False: 165, True: 75}
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.39952pt" viewBox="0 0 440.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.39952 224.39952 
L 440.39952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 56.828906 186.198739 
L 433.19952 186.198739 
L 433.19952 7.2 
L 56.828906 7.2 
L 56.828906 186.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 73.936661 186.198739 
L 100.256285 186.198739 
L 100.256285 186.198739 
L 73.936661 186.198739 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_4">
    <path d="M 100.256285 186.198739 
L 126.575908 186.198739 
L 126.575908 186.198739 
L 100.256285 186.198739 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_5">
    <path d="M 126.575908 186.198739 
L 152.895531 186.198739 
L 152.895531 161.845169 
L 126.575908 161.845169 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_6">
    <path d="M 152.895531 186.198739 
L 179.215155 186.198739 
L 179.215155 137.491599 
L 152.895531 137.491599 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_7">
    <path d="M 179.215155 186.198739 
L 205.534778 186.198739 
L 205.534778 125.314814 
L 179.215155 125.314814 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_8">
    <path d="M 205.534778 186.198739 
L 231.854401 186.198739 
L 231.854401 64.430889 
L 205.534778 64.430889 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_9">
    <path d="M 231.854401 186.198739 
L 258.174025 186.198739 
L 258.174025 113.138029 
L 231.854401 113.138029 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_10">
    <path d="M 258.174025 186.198739 
L 284.493648 186.198739 
L 284.493648 27.900534 
L 258.174025 27.900534 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_11">
    <path d="M 284.493648 186.198739 
L 310.813271 186.198739 
L 310.813271 15.723749 
L 284.493648 15.723749 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_12">
    <path d="M 310.813271 186.198739 
L 337.132895 186.198739 
L 337.132895 125.314814 
L 310.813271 125.314814 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_13">
    <path d="M 337.132895 186.198739 
L 363.452518 186.198739 
L 363.452518 76.607674 
L 337.132895 76.607674 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_14">
    <path d="M 363.452518 186.198739 
L 389.772141 186.198739 
L 389.772141 125.314814 
L 363.452518 125.314814 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_15">
    <path d="M 389.772141 186.198739 
L 416.091765 186.198739 
L 416.091765 161.845169 
L 389.772141 161.845169 
z
" clip-path="url(#p39288904d0)" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_16">
    <path d="M 73.936661 186.198739 
L 100.256285 186.198739 
L 100.256285 164.05913 
L 73.936661 164.05913 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_17">
    <path d="M 100.256285 186.198739 
L 126.575908 186.198739 
L 126.575908 108.710107 
L 100.256285 108.710107 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_18">
    <path d="M 126.575908 186.198739 
L 152.895531 186.198739 
L 152.895531 92.105401 
L 126.575908 92.105401 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_19">
    <path d="M 152.895531 186.198739 
L 179.215155 186.198739 
L 179.215155 36.756378 
L 152.895531 36.756378 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_20">
    <path d="M 179.215155 186.198739 
L 205.534778 186.198739 
L 205.534778 42.29128 
L 179.215155 42.29128 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_21">
    <path d="M 205.534778 186.198739 
L 231.854401 186.198739 
L 231.854401 25.686574 
L 205.534778 25.686574 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_22">
    <path d="M 231.854401 186.198739 
L 258.174025 186.198739 
L 258.174025 25.686574 
L 231.854401 25.686574 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_23">
    <path d="M 258.174025 186.198739 
L 284.493648 186.198739 
L 284.493648 136.384619 
L 258.174025 136.384619 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_24">
    <path d="M 284.493648 186.198739 
L 310.813271 186.198739 
L 310.813271 158.524228 
L 284.493648 158.524228 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_25">
    <path d="M 310.813271 186.198739 
L 337.132895 186.198739 
L 337.132895 169.594032 
L 310.813271 169.594032 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_26">
    <path d="M 337.132895 186.198739 
L 363.452518 186.198739 
L 363.452518 175.128934 
L 337.132895 175.128934 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_27">
    <path d="M 363.452518 186.198739 
L 389.772141 186.198739 
L 389.772141 186.198739 
L 363.452518 186.198739 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
   </g>
   <g id="patch_28">
    <path d="M 389.772141 186.198739 
L 416.091765 186.198739 
L 416.091765 186.198739 
L 389.772141 186.198739 
z
" clip-path="url(#p39288904d0)" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
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
       <use xlink:href="#m15aed4d867" x="61.190817" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="61.190817" y="200.796395" transform="rotate(-0 61.190817 200.796395)">60</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="117.839013" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="117.839013" y="200.796395" transform="rotate(-0 117.839013 200.796395)">80</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="174.487209" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="174.487209" y="200.796395" transform="rotate(-0 174.487209 200.796395)">100</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="231.135405" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="231.135405" y="200.796395" transform="rotate(-0 231.135405 200.796395)">120</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="287.783601" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="287.783601" y="200.796395" transform="rotate(-0 287.783601 200.796395)">140</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="344.431797" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="344.431797" y="200.796395" transform="rotate(-0 344.431797 200.796395)">160</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="401.079993" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="401.079993" y="200.796395" transform="rotate(-0 401.079993 200.796395)">180</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="245.014213" y="214.797176" transform="rotate(-0 245.014213 214.797176)">sales</text>
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
       <use xlink:href="#m5c8d5162d3" x="56.828906" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828906" y="189.997567" transform="rotate(-0 49.828906 189.997567)">0.000</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828906" y="143.767327" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828906" y="147.566155" transform="rotate(-0 49.828906 147.566155)">0.005</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828906" y="101.335914" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828906" y="105.134743" transform="rotate(-0 49.828906 105.134743)">0.010</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828906" y="58.904502" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828906" y="62.70333" transform="rotate(-0 49.828906 62.70333)">0.015</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="56.828906" y="16.47309" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="49.828906" y="20.271918" transform="rotate(-0 49.828906 20.271918)">0.020</text>
     </g>
    </g>
    <g id="text_14">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="96.699369" transform="rotate(-90 14.798438 96.699369)">Density</text>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 73.936661 185.647819 
L 80.814151 185.191206 
L 85.972268 184.669132 
L 91.130385 183.944102 
L 96.288502 182.96981 
L 101.446619 181.702202 
L 106.604737 180.104233 
L 110.043481 178.842248 
L 113.482226 177.41798 
L 118.640343 174.97707 
L 123.79846 172.182882 
L 128.956578 169.062552 
L 134.114695 165.653504 
L 139.272812 161.99695 
L 146.150301 156.800677 
L 153.027791 151.291931 
L 159.90528 145.48934 
L 166.78277 139.374902 
L 173.660259 132.919308 
L 180.537749 126.119195 
L 189.134611 117.23374 
L 201.170217 104.680576 
L 206.328335 99.563388 
L 211.486452 94.776488 
L 214.925196 91.818344 
L 218.363941 89.071162 
L 221.802686 86.545354 
L 225.241431 84.24063 
L 228.680176 82.145738 
L 233.838293 79.347504 
L 238.99641 76.865889 
L 247.593272 73.095036 
L 271.664485 62.803832 
L 275.10323 61.594795 
L 278.541975 60.586977 
L 281.980719 59.83371 
L 285.419464 59.382935 
L 288.858209 59.273545 
L 292.296954 59.532453 
L 295.735698 60.172624 
L 299.174443 61.192221 
L 302.613188 62.574964 
L 306.051933 64.291647 
L 309.490677 66.302704 
L 312.929422 68.561572 
L 318.087539 72.305945 
L 324.965029 77.719324 
L 335.281263 86.216236 
L 345.597497 94.968259 
L 352.474987 101.105988 
L 357.633104 105.972937 
L 362.791221 111.111036 
L 367.949338 116.524955 
L 374.826828 124.110408 
L 397.178669 149.272563 
L 402.336786 154.567032 
L 407.494903 159.477739 
L 410.933648 162.509337 
L 414.372392 165.333338 
L 416.091765 166.665151 
L 416.091765 166.665151 
" clip-path="url(#p39288904d0)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_14">
    <path d="M 73.936661 171.040003 
L 77.375406 168.728672 
L 80.814151 166.127398 
L 84.252896 163.163301 
L 87.69164 159.761853 
L 91.130385 155.860027 
L 94.56913 151.420614 
L 98.007875 146.445061 
L 101.446619 140.982095 
L 104.885364 135.129815 
L 118.640343 110.991922 
L 122.079088 105.608352 
L 125.517833 100.714452 
L 128.956578 96.325522 
L 132.395322 92.391356 
L 135.834067 88.805636 
L 149.589046 75.006594 
L 153.027791 71.088481 
L 156.466536 66.898507 
L 161.624653 60.241212 
L 168.502142 51.28982 
L 171.940887 47.100258 
L 175.379632 43.27788 
L 178.818377 39.92377 
L 182.257121 37.105014 
L 183.976494 35.907697 
L 185.695866 34.853607 
L 187.415238 33.941795 
L 189.134611 33.16967 
L 190.853983 32.533222 
L 192.573356 32.027231 
L 194.292728 31.645474 
L 197.731473 31.225916 
L 201.170217 31.211699 
L 204.608962 31.534755 
L 208.047707 32.126321 
L 211.486452 32.921756 
L 216.644569 34.382058 
L 221.802686 36.078433 
L 226.960803 38.053586 
L 230.399548 39.631463 
L 233.838293 41.547962 
L 235.557665 42.67758 
L 237.277037 43.947455 
L 238.99641 45.377526 
L 240.715782 46.987243 
L 242.435155 48.794816 
L 244.154527 50.816457 
L 245.873899 53.065632 
L 247.593272 55.552371 
L 249.312644 58.282661 
L 251.032016 61.25796 
L 254.470761 67.924808 
L 257.909506 75.464741 
L 261.348251 83.712158 
L 266.506368 96.894387 
L 273.383857 114.519586 
L 276.822602 122.738721 
L 280.261347 130.266911 
L 283.700092 136.959065 
L 285.419464 139.965557 
L 287.138836 142.740529 
L 288.858209 145.285273 
L 290.577581 147.604789 
L 292.296954 149.707348 
L 294.016326 151.604007 
L 295.735698 153.308078 
L 297.455071 154.834588 
L 299.174443 156.19974 
L 302.613188 158.513571 
L 306.051933 160.384005 
L 309.490677 161.935951 
L 314.648794 163.894215 
L 323.245656 166.760817 
L 335.281263 170.800086 
L 345.597497 174.520787 
L 357.633104 178.901622 
L 362.791221 180.606716 
L 367.949338 182.103836 
L 373.107455 183.343854 
L 378.265572 184.309344 
L 383.42369 185.014548 
L 388.581807 185.497177 
L 395.459296 185.879767 
L 404.056158 186.096131 
L 416.091765 186.18298 
L 416.091765 186.18298 
" clip-path="url(#p39288904d0)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_29">
    <path d="M 56.828906 186.198739 
L 56.828906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_30">
    <path d="M 433.19952 186.198739 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_31">
    <path d="M 56.828906 186.198739 
L 433.19952 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_32">
    <path d="M 56.828906 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_33">
     <path d="M 369.096395 60.202344 
L 426.19952 60.202344 
Q 428.19952 60.202344 428.19952 58.202344 
L 428.19952 14.2 
Q 428.19952 12.2 426.19952 12.2 
L 369.096395 12.2 
Q 367.096395 12.2 367.096395 14.2 
L 367.096395 58.202344 
Q 367.096395 60.202344 369.096395 60.202344 
L 369.096395 60.202344 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="375.269051" y="23.798438" transform="rotate(-0 375.269051 23.798438)">weekend</text>
    </g>
    <g id="patch_34">
     <path d="M 371.096395 38.799219 
L 391.096395 38.799219 
L 391.096395 31.799219 
L 371.096395 31.799219 
z
" style="fill: #1f77b4; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="399.096395" y="38.799219" transform="rotate(-0 399.096395 38.799219)">False</text>
    </g>
    <g id="patch_35">
     <path d="M 371.096395 53.8 
L 391.096395 53.8 
L 391.096395 46.8 
L 371.096395 46.8 
z
" style="fill: #ff7f0e; fill-opacity: 0.5; stroke: #000000; stroke-linejoin: miter"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="399.096395" y="53.8" transform="rotate(-0 399.096395 53.8)">True</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p39288904d0">
   <rect x="56.828906" y="7.2" width="376.370614" height="178.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Gruplar kendi toplamlarına bölündü; hafta sonu sağa kaymış.</figcaption>
</figure>

- `hue="weekend"` veriyi sütunun değerlerine göre renklere ayırır ve
  açıklamayı kendisi ekler.
- Grupların boyu farklı: 165 hafta içi, 75 hafta sonu kaydı. Ham sayı
  (`stat="count"`, varsayılan) hafta sonunu küçük gösterirdi.
  `stat="density"` ile `common_norm=False` her grubu **kendi** toplamına
  böler; şekiller karşılaştırılabilir olur.
- `kde=True` histogramın üstüne yumuşatılmış yoğunluk eğrisi çizer. Hafta
  sonu dağılımı sağa kaymış: ortalamalar 109,0 ve 136,1.

## barplot ortalamayı çizer, toplamı değil

```python
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
sns.barplot(df, x="store", y="sales", order=["Izmir", "Ankara", "Bursa"], ax=ax)
heights = [round(float(p.get_height()), 1) for p in ax.patches]
means = df.groupby("store")["sales"].mean().round(1)
print(heights)
print(means[["Izmir", "Ankara", "Bursa"]].tolist())
print(df.groupby("store")["sales"].sum().round(0).astype(int).to_dict())
```

```text
[116.6, 116.9, 118.9]
[116.6, 116.9, 118.9]
{'Ankara': 7714, 'Bursa': 10341, 'Izmir': 10140}
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.39952pt" viewBox="0 0 440.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.39952 224.39952 
L 440.39952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 186.198739 
L 433.19952 186.198739 
L 433.19952 7.2 
L 47.288281 7.2 
L 47.288281 186.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 60.151989 186.198739 
L 163.061653 186.198739 
L 163.061653 26.447548 
L 60.151989 26.447548 
z
" clip-path="url(#p03129543d0)" style="fill: #3274a1"/>
   </g>
   <g id="patch_4">
    <path d="M 188.789069 186.198739 
L 291.698732 186.198739 
L 291.698732 25.987295 
L 188.789069 25.987295 
z
" clip-path="url(#p03129543d0)" style="fill: #3274a1"/>
   </g>
   <g id="patch_5">
    <path d="M 317.426148 186.198739 
L 420.335812 186.198739 
L 420.335812 23.280851 
L 317.426148 23.280851 
z
" clip-path="url(#p03129543d0)" style="fill: #3274a1"/>
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
       <use xlink:href="#m15aed4d867" x="111.606821" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="111.606821" y="200.797176" transform="rotate(-0 111.606821 200.797176)">Izmir</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="240.243901" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="200.797176" transform="rotate(-0 240.243901 200.797176)">Ankara</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="368.88098" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="368.88098" y="200.796395" transform="rotate(-0 368.88098 200.796395)">Bursa</text>
     </g>
    </g>
    <g id="text_4">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="214.797176" transform="rotate(-0 240.243901 214.797176)">store</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_4">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="189.997567" transform="rotate(-0 40.288281 189.997567)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="158.785542" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="162.58437" transform="rotate(-0 40.288281 162.58437)">20</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="131.372346" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="135.171174" transform="rotate(-0 40.288281 135.171174)">40</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="103.959149" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="107.757977" transform="rotate(-0 40.288281 107.757977)">60</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="76.545952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="80.34478" transform="rotate(-0 40.288281 80.34478)">80</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="49.132756" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="52.931584" transform="rotate(-0 40.288281 52.931584)">100</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="21.719559" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="25.518387" transform="rotate(-0 40.288281 25.518387)">120</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="96.699369" transform="rotate(-90 14.798438 96.699369)">sales</text>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 111.606821 33.241491 
L 111.606821 19.818674 
" clip-path="url(#p03129543d0)" style="fill: none; stroke: #424242; stroke-width: 2.25; stroke-linecap: square"/>
   </g>
   <g id="line2d_12">
    <path d="M 240.243901 33.15081 
L 240.243901 18.827726 
" clip-path="url(#p03129543d0)" style="fill: none; stroke: #424242; stroke-width: 2.25; stroke-linecap: square"/>
   </g>
   <g id="line2d_13">
    <path d="M 368.88098 31.301574 
L 368.88098 15.723749 
" clip-path="url(#p03129543d0)" style="fill: none; stroke: #424242; stroke-width: 2.25; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 186.198739 
L 47.288281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_7">
    <path d="M 433.19952 186.198739 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 47.288281 186.198739 
L 433.19952 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 47.288281 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p03129543d0">
   <rect x="47.288281" y="7.2" width="385.911239" height="178.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Çubuklar ortalama, siyah çizgiler %95 güven aralığı.</figcaption>
</figure>

- seaborn'un `barplot`'u her grubun **ortalamasını** çizer (`estimator="mean"`)
  ve üstüne %95 güven aralığını siyah çizgiyle ekler. Çubuk boyları
  `groupby().mean()` ile birebir aynı.
- Üç mağazanın ortalaması neredeyse eşit; ama **toplam** satışta Ankara
  (7714) ötekilerden çok geride, çünkü daha az kaydı var. "Ankara az satıyor"
  sorusunun cevabı hangi grafiğe baktığına göre değişir.
- Toplam isteniyorsa `estimator="sum"`; aralık istenmiyorsa `errorbar=None`.
  Sayım için `countplot`. **Bir seaborn grafiği bir hesap yapıyorsa hangi
  hesap olduğunu bil.**

## lineplot tekrarları toplar

```python
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
sns.lineplot(df, x="hour", y="sales", hue="weekend", ax=ax)
print(len(df), df["hour"].nunique(), df.groupby("hour").size().max())
print(len(ax.collections))
```

```text
240 12 26
2
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.39952pt" viewBox="0 0 440.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.39952 224.39952 
L 440.39952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 186.198739 
L 433.19952 186.198739 
L 433.19952 7.2 
L 47.288281 7.2 
L 47.288281 186.198739 
z
" style="fill: none"/>
   </g>
   <g id="FillBetweenPolyCollection_1">
    <defs>
     <path id="m8bf0343595" d="M 64.829701 -102.729117 
L 64.829701 -46.337088 
L 96.723192 -65.349644 
L 128.616683 -73.816896 
L 160.510174 -71.511632 
L 192.403664 -63.505739 
L 224.297155 -81.759708 
L 256.190646 -100.305306 
L 288.084137 -99.249201 
L 319.977628 -102.336691 
L 351.871118 -122.22387 
L 383.764609 -118.826393 
L 415.6581 -125.376195 
L 415.6581 -154.4891 
L 415.6581 -154.4891 
L 383.764609 -143.81548 
L 351.871118 -147.233724 
L 319.977628 -119.113977 
L 288.084137 -116.528424 
L 256.190646 -119.181183 
L 224.297155 -105.093634 
L 192.403664 -89.86833 
L 160.510174 -100.879061 
L 128.616683 -94.783145 
L 96.723192 -85.658465 
L 64.829701 -102.729117 
z
" style="stroke: #1f77b4; stroke-opacity: 0.2"/>
    </defs>
    <g clip-path="url(#p03129543d0)">
     <use xlink:href="#m8bf0343595" x="0" y="224.39952" style="fill: #1f77b4; fill-opacity: 0.2; stroke: #1f77b4; stroke-opacity: 0.2"/>
    </g>
   </g>
   <g id="FillBetweenPolyCollection_2">
    <path d="M 64.829701 104.606492 
L 64.829701 136.379762 
L 96.723192 112.085728 
L 128.616683 115.064527 
L 160.510174 125.707784 
L 192.403664 106.707113 
L 224.297155 107.654457 
L 256.190646 71.525529 
L 288.084137 86.770039 
L 319.977628 51.251486 
L 351.871118 58.552598 
L 351.871118 26.21298 
L 351.871118 26.21298 
L 319.977628 15.336306 
L 288.084137 41.697754 
L 256.190646 39.940998 
L 224.297155 44.960175 
L 192.403664 73.097379 
L 160.510174 94.15344 
L 128.616683 82.075002 
L 96.723192 98.791914 
L 64.829701 104.606492 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; fill-opacity: 0.2; stroke: #ff7f0e; stroke-opacity: 0.2"/>
    <path d="M 415.6581 35.824097 
L 415.6581 55.585652 
L 415.6581 35.824097 
L 415.6581 35.824097 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; fill-opacity: 0.2; stroke: #ff7f0e; stroke-opacity: 0.2"/>
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
       <use xlink:href="#m15aed4d867" x="96.723192" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="96.723192" y="200.796395" transform="rotate(-0 96.723192 200.796395)">10</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="160.510174" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="160.510174" y="200.796395" transform="rotate(-0 160.510174 200.796395)">12</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="224.297155" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="224.297155" y="200.796395" transform="rotate(-0 224.297155 200.796395)">14</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="288.084137" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="288.084137" y="200.796395" transform="rotate(-0 288.084137 200.796395)">16</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="351.871118" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="351.871118" y="200.796395" transform="rotate(-0 351.871118 200.796395)">18</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="415.6581" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="415.6581" y="200.796395" transform="rotate(-0 415.6581 200.796395)">20</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="214.797176" transform="rotate(-0 240.243901 214.797176)">hour</text>
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
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="167.886921" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="171.685749" transform="rotate(-0 40.288281 171.685749)">80</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="135.06269" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="138.861518" transform="rotate(-0 40.288281 138.861518)">100</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="102.238458" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="106.037287" transform="rotate(-0 40.288281 106.037287)">120</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="69.414227" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="73.213055" transform="rotate(-0 40.288281 73.213055)">140</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="36.589996" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="40.388824" transform="rotate(-0 40.288281 40.388824)">160</text>
     </g>
    </g>
    <g id="text_13">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="96.699369" transform="rotate(-90 14.798438 96.699369)">sales</text>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 64.829701 149.866418 
L 96.723192 150.279065 
L 128.616683 140.688398 
L 160.510174 137.737864 
L 192.403664 147.371776 
L 224.297155 131.487193 
L 256.190646 114.469803 
L 288.084137 116.8343 
L 319.977628 114.254472 
L 351.871118 90.396486 
L 383.764609 91.920708 
L 415.6581 83.178521 
" clip-path="url(#p03129543d0)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_13">
    <path d="M 64.829701 120.54969 
L 96.723192 104.741306 
L 128.616683 98.791914 
L 160.510174 109.50082 
L 192.403664 89.054059 
L 224.297155 69.797177 
L 256.190646 56.331426 
L 288.084137 65.065017 
L 319.977628 32.486967 
L 351.871118 42.680714 
L 383.764609 73.845498 
L 415.6581 45.397831 
" clip-path="url(#p03129543d0)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="line2d_14"/>
   <g id="line2d_15"/>
   <g id="patch_3">
    <path d="M 47.288281 186.198739 
L 47.288281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 433.19952 186.198739 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 47.288281 186.198739 
L 433.19952 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 54.288281 60.202344 
L 111.391406 60.202344 
Q 113.391406 60.202344 113.391406 58.202344 
L 113.391406 14.2 
Q 113.391406 12.2 111.391406 12.2 
L 54.288281 12.2 
Q 52.288281 12.2 52.288281 14.2 
L 52.288281 58.202344 
Q 52.288281 60.202344 54.288281 60.202344 
L 54.288281 60.202344 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="text_14">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="60.460938" y="23.798438" transform="rotate(-0 60.460938 23.798438)">weekend</text>
    </g>
    <g id="line2d_16">
     <path d="M 56.288281 35.299219 
L 66.288281 35.299219 
L 76.288281 35.299219 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="84.288281" y="38.799219" transform="rotate(-0 84.288281 38.799219)">False</text>
    </g>
    <g id="line2d_17">
     <path d="M 56.288281 50.3 
L 66.288281 50.3 
L 76.288281 50.3 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="84.288281" y="53.8" transform="rotate(-0 84.288281 53.8)">True</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p03129543d0">
   <rect x="47.288281" y="7.2" width="385.911239" height="178.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Her saatin ortalaması ve belirsizlik bandı.</figcaption>
</figure>

- 240 satır ama yalnızca 12 farklı saat var; bir saatte 26'ya kadar kayıt
  düşüyor. `lineplot` aynı x'teki değerlerin **ortalamasını** çizer ve
  belirsizlik **bandını** (burada iki renk için iki bant) ekler.
- Bu çoğu zaman istenen şeydir, ama habersiz olunca şaşırtır: veride olmayan
  bir "ortalama çizgi" görürsün. Her noktayı ayrı görmek için
  `scatterplot`; toplamadan çizmek için `estimator=None`.

## Paneller: relplot

```python
grid = sns.relplot(df, x="hour", y="sales", col="store", hue="weekend",
                   col_order=["Izmir", "Ankara", "Bursa"], height=2.6, aspect=0.9)
grid.set_titles("{col_name}")
print(grid.axes.shape, [ax.get_title() for ax in grid.axes.flat])
```

```text
(1, 3) ['Izmir', 'Ankara', 'Bursa']
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="559.149045pt" height="179.679219pt" viewBox="0 0 559.149045 179.679219" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 179.679219 
L 559.149045 179.679219 
L 559.149045 0 
L 0 0 
L 0 179.679219 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 141.478437 
L 184.912868 141.478437 
L 184.912868 20.798437 
L 47.288281 20.798437 
L 47.288281 141.478437 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_1">
    <defs>
     <path id="C0_0_ca53a4b268" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 -0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
"/>
    </defs>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="106.204422" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="91.582598" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="97.031725" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="83.590545" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="70.785096" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="109.019804" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="121.916071" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.665743" y="91.673416" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="26.283892" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="91.128504" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="48.0804" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="82.863994" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="99.120557" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="86.496746" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="112.925012" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="123.005897" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="111.653549" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="116.557763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="99.211375" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="85.861014" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="59.251111" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="106.386059" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="82.137444" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="88.585578" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="72.692291" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="78.413874" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="95.033711" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="93.217336" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="86.496746" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="93.217336" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="121.916071" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="83.499726" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="167.283272" y="60.613392" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="67.788076" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="39.089341" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="88.131484" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="121.461978" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="81.955807" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="53.892802" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="91.673416" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="114.287294" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="84.498733" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="92.12751" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="76.779136" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="103.38904" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="71.96574" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="60.885849" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="93.308155" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="64.246144" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="104.569684" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="98.394006" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="86.769202" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="73.146385" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="66.062519" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="90.129497" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="100.301201" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="155.90934" y="48.80695" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="99.211375" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="50.441689" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.665743" y="83.136451" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.039676" y="76.143404" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="79.049605" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.665743" y="105.387053" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="96.486812" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="85.679377" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="95.669443" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="73.782116" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="51.713152" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="120.735427" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="111.56273" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="115.831213" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="129.635668" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="53.543944" y="97.304181" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="107.657522" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="64.917877" y="120.190515" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="121.787541" y="97.213362" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.665743" y="86.769202" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="77.687324" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="82.954813" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="92.036692" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.665743" y="84.68037" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="144.535407" y="103.025764" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.413608" y="100.301201" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="178.657205" y="52.439702" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="96.850087" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="133.161474" y="85.588558" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pe50cd7eb09)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.29181" y="109.473898" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
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
       <use xlink:href="#m15aed4d867" x="64.917877" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="64.917877" y="156.076094" transform="rotate(-0 64.917877 156.076094)">10</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="121.787541" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="121.787541" y="156.076094" transform="rotate(-0 121.787541 156.076094)">15</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="178.657205" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="178.657205" y="156.076094" transform="rotate(-0 178.657205 156.076094)">20</text>
     </g>
    </g>
    <g id="text_4">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="116.100575" y="170.076875" transform="rotate(-0 116.100575 170.076875)">hour</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_4">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="126.457011" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="130.255839" transform="rotate(-0 40.288281 130.255839)">75</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="103.752315" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="107.551143" transform="rotate(-0 40.288281 107.551143)">100</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="81.047619" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="84.846447" transform="rotate(-0 40.288281 84.846447)">125</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="58.342923" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="62.141751" transform="rotate(-0 40.288281 62.141751)">150</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="35.638227" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="39.437055" transform="rotate(-0 40.288281 39.437055)">175</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="81.138437" transform="rotate(-90 14.798438 81.138437)">sales</text>
    </g>
   </g>
   <g id="line2d_9"/>
   <g id="line2d_10"/>
   <g id="patch_3">
    <path d="M 47.288281 141.478437 
L 47.288281 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 47.288281 141.478437 
L 184.912868 141.478437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_11">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="116.100575" y="14.798437" transform="rotate(-0 116.100575 14.798437)">Izmir</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_5">
    <path d="M 199.611832 141.478437 
L 337.236419 141.478437 
L 337.236419 20.798437 
L 199.611832 20.798437 
L 199.611832 141.478437 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_2">
    <defs>
     <path id="C1_0_ca53a4b268" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 -0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
"/>
    </defs>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="205.867495" y="88.222303" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="96.032718" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="262.737159" y="102.299214" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="285.485025" y="95.215349" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="108.928985" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="79.776156" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="82.319082" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="72.056559" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="81.774169" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="76.688317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="285.485025" y="76.688317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="262.737159" y="99.211375" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="100.573657" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="217.241428" y="125.00391" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="86.133471" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="94.307161" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="80.684344" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="106.022784" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="70.240183" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="91.673416" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="239.989294" y="88.40394" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="73.963754" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="217.241428" y="87.314115" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="63.882869" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="262.737159" y="97.758275" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="296.858958" y="99.211375" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="58.978654" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="102.299214" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="78.141418" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="296.858958" y="35.638227" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="97.304181" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="79.594518" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="78.050599" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="107.203428" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="84.952826" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="66.334976" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="217.241428" y="118.101683" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="296.858958" y="93.489792" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="35.819864" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="110.018811" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="239.989294" y="107.475885" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="106.476878" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="60.06848" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="77.687324" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="296.858958" y="90.67441" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="79.776156" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="80.139431" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="262.737159" y="114.105656" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="217.241428" y="115.740394" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="285.485025" y="112.652556" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="239.989294" y="112.016824" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="296.858958" y="102.753308" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="117.829226" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="285.485025" y="85.043645" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="57.162279" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="66.970707" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="274.111092" y="80.502706" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="90.765229" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="251.363226" y="134.903158" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="319.606823" y="88.494759" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="228.615361" y="116.557763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="77.414867" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="239.989294" y="104.751321" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="43.539461" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="330.980756" y="64.246144" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pc9d9af2ec3)">
     <use xlink:href="#C1_0_ca53a4b268" x="308.232891" y="77.414867" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="217.241428" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="217.241428" y="156.076094" transform="rotate(-0 217.241428 156.076094)">10</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="274.111092" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="274.111092" y="156.076094" transform="rotate(-0 274.111092 156.076094)">15</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="330.980756" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="330.980756" y="156.076094" transform="rotate(-0 330.980756 156.076094)">20</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="268.424126" y="170.076875" transform="rotate(-0 268.424126 170.076875)">hour</text>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_6">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="199.611832" y="126.457011" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="199.611832" y="103.752315" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="199.611832" y="81.047619" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="199.611832" y="58.342923" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="199.611832" y="35.638227" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="patch_6">
    <path d="M 199.611832 141.478437 
L 199.611832 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_7">
    <path d="M 199.611832 141.478437 
L 337.236419 141.478437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="268.424126" y="14.798437" transform="rotate(-0 268.424126 14.798437)">Ankara</text>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_8">
    <path d="M 351.935383 141.478437 
L 489.55997 141.478437 
L 489.55997 20.798437 
L 351.935383 20.798437 
L 351.935383 141.478437 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_3">
    <defs>
     <path id="C2_0_ca53a4b268" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 -0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
"/>
    </defs>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="358.191046" y="72.601472" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="88.767215" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="60.522574" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="415.06071" y="60.431755" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="78.867968" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="102.480852" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="62.157312" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="62.793043" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="100.936932" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="119.100689" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="369.564979" y="118.555776" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="80.775162" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="46.445662" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="114.196475" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="369.564979" y="120.55379" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="57.162279" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="358.191046" y="103.298221" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="105.023778" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="358.191046" y="135.992983" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="66.970707" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="92.490785" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="61.158305" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="93.126517" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="50.623326" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="92.763242" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="69.422814" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="47.263031" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="126.729467" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="105.477872" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="108.474891" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="77.324049" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="89.94786" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="119.191508" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="70.331002" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="69.876908" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="51.440695" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="369.564979" y="102.480852" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="46.990575" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="415.06071" y="102.026758" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="83.318088" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="81.229256" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="84.317095" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="103.843133" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="41.904723" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="358.191046" y="115.922032" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="85.588558" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="89.13049" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="75.235217" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="94.852074" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="86.315108" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="94.216342" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="34.185126" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="460.556441" y="76.415861" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="54.07444" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="369.564979" y="121.007884" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="415.06071" y="78.504693" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="64.336962" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="72.147378" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="61.067486" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="124.368179" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="96.940906" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="415.06071" y="119.282327" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="369.564979" y="120.462971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="97.395" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="74.054572" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="105.750328" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="97.576637" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="108.384073" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="106.113603" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="380.938912" y="115.649575" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="103.116583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="40.814897" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="99.211375" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="106.022784" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="78.958787" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="449.182509" y="44.810924" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="86.678383" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="76.415861" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="134.358245" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="358.191046" y="98.757282" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="48.716132" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="437.808576" y="85.951833" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="426.434643" y="74.23621" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="403.686777" y="93.853067" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="471.930374" y="90.311135" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="483.304307" y="62.611406" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pf0b69e3c9f)">
     <use xlink:href="#C2_0_ca53a4b268" x="392.312845" y="113.015831" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_5">
    <g id="xtick_7">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m15aed4d867" x="369.564979" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.564979" y="156.076094" transform="rotate(-0 369.564979 156.076094)">10</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m15aed4d867" x="426.434643" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="426.434643" y="156.076094" transform="rotate(-0 426.434643 156.076094)">15</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m15aed4d867" x="483.304307" y="141.478437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="483.304307" y="156.076094" transform="rotate(-0 483.304307 156.076094)">20</text>
     </g>
    </g>
    <g id="text_20">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="420.747677" y="170.076875" transform="rotate(-0 420.747677 170.076875)">hour</text>
    </g>
   </g>
   <g id="matplotlib.axis_6">
    <g id="ytick_11">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m5c8d5162d3" x="351.935383" y="126.457011" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_23">
      <g>
       <use xlink:href="#m5c8d5162d3" x="351.935383" y="103.752315" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m5c8d5162d3" x="351.935383" y="81.047619" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m5c8d5162d3" x="351.935383" y="58.342923" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m5c8d5162d3" x="351.935383" y="35.638227" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="patch_9">
    <path d="M 351.935383 141.478437 
L 351.935383 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 351.935383 141.478437 
L 489.55997 141.478437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_21">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="420.747677" y="14.798437" transform="rotate(-0 420.747677 14.798437)">Bursa</text>
   </g>
  </g>
  <g id="legend_1">
   <g id="text_22">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="501.218576" y="77.436875" transform="rotate(-0 501.218576 77.436875)">weekend</text>
   </g>
   <g id="line2d_27">
    <defs>
     <path id="m977914378c" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
"/>
    </defs>
    <g>
     <use xlink:href="#m977914378c" x="507.04592" y="88.937656" style="fill: #1f77b4"/>
    </g>
   </g>
   <g id="text_23">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="525.04592" y="92.437656" transform="rotate(-0 525.04592 92.437656)">False</text>
   </g>
   <g id="line2d_28">
    <defs>
     <path id="m0e6841bf8e" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
"/>
    </defs>
    <g>
     <use xlink:href="#m0e6841bf8e" x="507.04592" y="103.938437" style="fill: #ff7f0e"/>
    </g>
   </g>
   <g id="text_24">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="525.04592" y="107.438437" transform="rotate(-0 525.04592 107.438437)">True</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pe50cd7eb09">
   <rect x="47.288281" y="20.798437" width="137.624587" height="120.68"/>
  </clipPath>
  <clipPath id="pc9d9af2ec3">
   <rect x="199.611832" y="20.798437" width="137.624587" height="120.68"/>
  </clipPath>
  <clipPath id="pf0b69e3c9f">
   <rect x="351.935383" y="20.798437" width="137.624587" height="120.68"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Her mağazaya bir panel, ortak eksenler.</figcaption>
</figure>

- `col="store"` her mağazaya bir panel açar; eksenler varsayılan olarak
  **ortak**, yani paneller doğrudan karşılaştırılabilir.
- Aynı grafiği gruplar için tekrarlamak (small multiples) çok gruplu veride
  tek bir kalabalık grafikten daha okunaklıdır.
- `set_titles("{col_name}")` panel başlıklarını kısaltır (varsayılanı
  `store = Izmir`).

## Isı haritası

```python
table = df.pivot_table(index="day", columns="store", values="sales", aggfunc="mean")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
table = table.loc[days, ["Izmir", "Ankara", "Bursa"]]
fig, ax = plt.subplots(figsize=(5, 3.4), layout="constrained")
sns.heatmap(table, annot=True, fmt=".0f", cmap="viridis", ax=ax)
gap = table.loc["Sat"].mean() - table.loc["Mon"].mean()
print(table.shape, round(float(gap), 1))
```

```text
(7, 3) 21.7
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="367.719125pt" height="253.19952pt" viewBox="0 0 367.719125 253.19952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 253.19952 
L 367.719125 253.19952 
L 367.719125 0 
L 0 0 
L 0 253.19952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 38.201563 214.998739 
L 310.430253 214.998739 
L 310.430253 7.2 
L 38.201563 7.2 
L 38.201563 214.998739 
z
" style="fill: none"/>
   </g>
   <g id="QuadMesh_1">
    <path d="M 38.201563 7.2 
L 128.944459 7.2 
L 128.944459 36.885534 
L 38.201563 36.885534 
L 38.201563 7.2 
" clip-path="url(#p6ce77fbbc2)" style="fill: #46307e"/>
    <path d="M 128.944459 7.2 
L 219.687356 7.2 
L 219.687356 36.885534 
L 128.944459 36.885534 
L 128.944459 7.2 
" clip-path="url(#p6ce77fbbc2)" style="fill: #306a8e"/>
    <path d="M 219.687356 7.2 
L 310.430253 7.2 
L 310.430253 36.885534 
L 219.687356 36.885534 
L 219.687356 7.2 
" clip-path="url(#p6ce77fbbc2)" style="fill: #440154"/>
    <path d="M 38.201563 36.885534 
L 128.944459 36.885534 
L 128.944459 66.571068 
L 38.201563 66.571068 
L 38.201563 36.885534 
" clip-path="url(#p6ce77fbbc2)" style="fill: #471365"/>
    <path d="M 128.944459 36.885534 
L 219.687356 36.885534 
L 219.687356 66.571068 
L 128.944459 66.571068 
L 128.944459 36.885534 
" clip-path="url(#p6ce77fbbc2)" style="fill: #471365"/>
    <path d="M 219.687356 36.885534 
L 310.430253 36.885534 
L 310.430253 66.571068 
L 219.687356 66.571068 
L 219.687356 36.885534 
" clip-path="url(#p6ce77fbbc2)" style="fill: #46075a"/>
    <path d="M 38.201563 66.571068 
L 128.944459 66.571068 
L 128.944459 96.256602 
L 38.201563 96.256602 
L 38.201563 66.571068 
" clip-path="url(#p6ce77fbbc2)" style="fill: #443b84"/>
    <path d="M 128.944459 66.571068 
L 219.687356 66.571068 
L 219.687356 96.256602 
L 128.944459 96.256602 
L 128.944459 66.571068 
" clip-path="url(#p6ce77fbbc2)" style="fill: #39558c"/>
    <path d="M 219.687356 66.571068 
L 310.430253 66.571068 
L 310.430253 96.256602 
L 219.687356 96.256602 
L 219.687356 66.571068 
" clip-path="url(#p6ce77fbbc2)" style="fill: #482071"/>
    <path d="M 38.201563 96.256602 
L 128.944459 96.256602 
L 128.944459 125.942136 
L 38.201563 125.942136 
L 38.201563 96.256602 
" clip-path="url(#p6ce77fbbc2)" style="fill: #46075a"/>
    <path d="M 128.944459 96.256602 
L 219.687356 96.256602 
L 219.687356 125.942136 
L 128.944459 125.942136 
L 128.944459 96.256602 
" clip-path="url(#p6ce77fbbc2)" style="fill: #365c8d"/>
    <path d="M 219.687356 96.256602 
L 310.430253 96.256602 
L 310.430253 125.942136 
L 219.687356 125.942136 
L 219.687356 96.256602 
" clip-path="url(#p6ce77fbbc2)" style="fill: #297b8e"/>
    <path d="M 38.201563 125.942136 
L 128.944459 125.942136 
L 128.944459 155.627671 
L 38.201563 155.627671 
L 38.201563 125.942136 
" clip-path="url(#p6ce77fbbc2)" style="fill: #414487"/>
    <path d="M 128.944459 125.942136 
L 219.687356 125.942136 
L 219.687356 155.627671 
L 128.944459 155.627671 
L 128.944459 125.942136 
" clip-path="url(#p6ce77fbbc2)" style="fill: #472e7c"/>
    <path d="M 219.687356 125.942136 
L 310.430253 125.942136 
L 310.430253 155.627671 
L 219.687356 155.627671 
L 219.687356 125.942136 
" clip-path="url(#p6ce77fbbc2)" style="fill: #481c6e"/>
    <path d="M 38.201563 155.627671 
L 128.944459 155.627671 
L 128.944459 185.313205 
L 38.201563 185.313205 
L 38.201563 155.627671 
" clip-path="url(#p6ce77fbbc2)" style="fill: #81d34d"/>
    <path d="M 128.944459 155.627671 
L 219.687356 155.627671 
L 219.687356 185.313205 
L 128.944459 185.313205 
L 128.944459 155.627671 
" clip-path="url(#p6ce77fbbc2)" style="fill: #1f988b"/>
    <path d="M 219.687356 155.627671 
L 310.430253 155.627671 
L 310.430253 185.313205 
L 219.687356 185.313205 
L 219.687356 155.627671 
" clip-path="url(#p6ce77fbbc2)" style="fill: #90d743"/>
    <path d="M 38.201563 185.313205 
L 128.944459 185.313205 
L 128.944459 214.998739 
L 38.201563 214.998739 
L 38.201563 185.313205 
" clip-path="url(#p6ce77fbbc2)" style="fill: #c5e021"/>
    <path d="M 128.944459 185.313205 
L 219.687356 185.313205 
L 219.687356 214.998739 
L 128.944459 214.998739 
L 128.944459 185.313205 
" clip-path="url(#p6ce77fbbc2)" style="fill: #fde725"/>
    <path d="M 219.687356 185.313205 
L 310.430253 185.313205 
L 310.430253 214.998739 
L 219.687356 214.998739 
L 219.687356 185.313205 
" clip-path="url(#p6ce77fbbc2)" style="fill: #f1e51d"/>
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
       <use xlink:href="#m15aed4d867" x="83.573011" y="214.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="83.573011" y="229.597176" transform="rotate(-0 83.573011 229.597176)">Izmir</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="174.315908" y="214.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="174.315908" y="229.597176" transform="rotate(-0 174.315908 229.597176)">Ankara</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="265.058805" y="214.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="265.058805" y="229.596395" transform="rotate(-0 265.058805 229.596395)">Bursa</text>
     </g>
    </g>
    <g id="text_4">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="174.315908" y="243.597176" transform="rotate(-0 174.315908 243.597176)">store</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_4">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="22.042767" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 32.584955) rotate(-90)">Mon</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="51.728301" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 60.268145) rotate(-90)">Tue</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="81.413835" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 92.315398) rotate(-90)">Wed</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="111.099369" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 120.490776) rotate(-90)">Thu</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="140.784903" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 146.741153) rotate(-90)">Fri</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="170.470438" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 178.668875) rotate(-90)">Sat</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="38.201563" y="200.155972" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; fill: currentColor" transform="translate(28.799219 209.66769) rotate(-90)">Sun</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="111.099369" transform="rotate(-90 14.798438 111.099369)">day</text>
    </g>
   </g>
   <g id="text_13">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="83.573011" y="24.640423" transform="rotate(-0 83.573011 24.640423)">108</text>
   </g>
   <g id="text_14">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="24.640423" transform="rotate(-0 174.315908 24.640423)">116</text>
   </g>
   <g id="text_15">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="265.058805" y="24.640423" transform="rotate(-0 265.058805 24.640423)">103</text>
   </g>
   <g id="text_16">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="83.573011" y="54.325957" transform="rotate(-0 83.573011 54.325957)">105</text>
   </g>
   <g id="text_17">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="54.325957" transform="rotate(-0 174.315908 54.325957)">105</text>
   </g>
   <g id="text_18">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="265.058805" y="54.325957" transform="rotate(-0 265.058805 54.325957)">104</text>
   </g>
   <g id="text_19">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="83.573011" y="84.011492" transform="rotate(-0 83.573011 84.011492)">110</text>
   </g>
   <g id="text_20">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="84.011492" transform="rotate(-0 174.315908 84.011492)">113</text>
   </g>
   <g id="text_21">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="265.058805" y="84.011492" transform="rotate(-0 265.058805 84.011492)">106</text>
   </g>
   <g id="text_22">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="83.573011" y="113.697026" transform="rotate(-0 83.573011 113.697026)">104</text>
   </g>
   <g id="text_23">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="113.697026" transform="rotate(-0 174.315908 113.697026)">114</text>
   </g>
   <g id="text_24">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="265.058805" y="113.697026" transform="rotate(-0 265.058805 113.697026)">119</text>
   </g>
   <g id="text_25">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="83.573011" y="143.38256" transform="rotate(-0 83.573011 143.38256)">111</text>
   </g>
   <g id="text_26">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="143.38256" transform="rotate(-0 174.315908 143.38256)">108</text>
   </g>
   <g id="text_27">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="265.058805" y="143.38256" transform="rotate(-0 265.058805 143.38256)">106</text>
   </g>
   <g id="text_28">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #262626" x="83.573011" y="173.068094" transform="rotate(-0 83.573011 173.068094)">134</text>
   </g>
   <g id="text_29">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="174.315908" y="173.068094" transform="rotate(-0 174.315908 173.068094)">124</text>
   </g>
   <g id="text_30">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #262626" x="265.058805" y="173.068094" transform="rotate(-0 265.058805 173.068094)">135</text>
   </g>
   <g id="text_31">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #262626" x="83.573011" y="202.753628" transform="rotate(-0 83.573011 202.753628)">138</text>
   </g>
   <g id="text_32">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #262626" x="174.315908" y="202.753628" transform="rotate(-0 174.315908 202.753628)">142</text>
   </g>
   <g id="text_33">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #262626" x="265.058805" y="202.753628" transform="rotate(-0 265.058805 202.753628)">141</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_3">
    <path d="M 324.041688 214.998739 
L 334.431625 214.998739 
L 334.431625 7.2 
L 324.041688 7.2 
L 324.041688 214.998739 
z
" style="fill: none"/>
   </g>
   <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAA4AAAEhCAYAAABPxZGGAAABnElEQVR4nO2YwW3FMAxDSdqjdYTuP4pVdIEeaICu7J/7w5MsWgnCL34XjGeCcjhMiogaZVE4UeqEb6QHUgobkTbKorAzDvYJANrMcR4IANlnjro/cmyzAeD2WH7kYIK8f471wKlWnx7rwCZHukfFjUwb4RrrwCZH+lrRNqJPcpB9scrz4USP9cAcK92jPB+OHI7iRl4fOXkYmt0O9DGyy7dc5V9zNMG63ygPw2eOfz3T+p+PEyGXh+GJ2zEfKFUehk8ALtnkcsHZJ+TzjWVVFijPh08A/tccZ/VZHThwrcoF0QSUh+HE4VSfObJNqfIw7GQV+XHUA0Z02QD0QVwfACJslCnEgTnqQOTKBdGkR1kUfkvF9YczGxmFNhtAL4DoUqosCs+c6rr+Iit+OONAAJYLlgeOdKmyKGz1SHuOKz6OlTZyddkAw78dyzSiHjAu11jpAGA1CfncMC7XWPEArD4BqPg4VnocSGd15D8CkR9HdfkGGOlSZVHYKXX4PSJthGukC4LZUgW/R3qg3B4H4kbaRsVLlQXubHKP/QE5fY1E2aJM3AAAAABJRU5ErkJggg==" id="imagee53a0a2cf1" transform="scale(1 -1) translate(0 -208.08)" x="324" y="-6.48" width="10.08" height="208.08"/>
   <g id="matplotlib.axis_3"/>
   <g id="matplotlib.axis_4">
    <g id="ytick_8">
     <g id="line2d_11">
      <defs>
       <path id="m004d6dcf24" d="M 0 0 
L 3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="204.806153" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_34">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="208.604981" transform="rotate(-0 341.431625 208.604981)">105</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="177.7646" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_35">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="181.563428" transform="rotate(-0 341.431625 181.563428)">110</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="150.723046" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_36">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="154.521874" transform="rotate(-0 341.431625 154.521874)">115</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="123.681492" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_37">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="127.48032" transform="rotate(-0 341.431625 127.48032)">120</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="96.639939" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_38">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="100.438767" transform="rotate(-0 341.431625 100.438767)">125</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="69.598385" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_39">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="73.397213" transform="rotate(-0 341.431625 73.397213)">130</text>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="42.556831" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_40">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="46.355659" transform="rotate(-0 341.431625 46.355659)">135</text>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m004d6dcf24" x="334.431625" y="15.515278" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_41">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="341.431625" y="19.314106" transform="rotate(-0 341.431625 19.314106)">140</text>
     </g>
    </g>
   </g>
   <g id="LineCollection_1"/>
   <g id="patch_4">
    <path d="M 324.041688 214.998739 
L 329.236656 214.998739 
L 334.431625 214.998739 
L 334.431625 7.2 
L 329.236656 7.2 
L 324.041688 7.2 
L 324.041688 214.998739 
z
" style="fill: none"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6ce77fbbc2">
   <rect x="38.201563" y="7.2" width="272.228691" height="207.798739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Gün × mağaza ortalama satış; hafta sonu satırları açık.</figcaption>
</figure>

- `heatmap` bir DataFrame'i doğrudan çizer: satır ve sütun adları eksenlere,
  değerler hücrelere. `annot=True` sayıları yazar, `fmt=".0f"` biçimini
  seçer; yazı rengini hücreye göre kendisi ayarlar.
- Önceki bölümde matplotlib ile on satırda yaptığımız iş tek çağrı. Ama
  günlerin sırasını yine **sen** verirsin (`table.loc[days]`); yoksa
  alfabetik dizilir.
- Hafta sonu satırları belirgin açık: cumartesi ortalaması pazartesiden 21,7
  fazla. İki yönlü bir değerde (korelasyon) `center=0` ve iki renkli skala.

## Özet

- seaborn DataFrame + sütun adı alır; `hue`, `col`, `row` gruplamayı yapar.
- Alan düzeyi `Axes` döndürür (`ax=`); şekil düzeyi kendi şeklini ve
  panellerini kurar (`height`, `aspect`).
- `barplot` ortalama + güven aralığı çizer, toplam değil; `lineplot` aynı
  x'leri toplar. Hangi hesabın yapıldığını bil: `estimator`, `errorbar`.
- Farklı boyutlu grupları karşılaştırırken `stat="density"`,
  `common_norm=False`.
- Çıktı matplotlib nesnesi; başlık, eksen ve kaydetme önceki bölümler gibi.
