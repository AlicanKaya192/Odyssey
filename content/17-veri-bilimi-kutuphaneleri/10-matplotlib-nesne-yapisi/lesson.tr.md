# Matplotlib: Figure ve Axes

matplotlib'de aynı grafiği iki yolla çizebilirsin: `plt.plot(...)` gibi kısa
komutlarla ya da `fig, ax = plt.subplots()` ile nesneleri açıkça tutarak.
İnternetteki örneklerin yarısı birini, yarısı ötekini kullandığı için
karışıklık buradan çıkar. Bu bölüm arkadaki nesne yapısını anlatıyor:
**Figure** (tuval), **Axes** (çizim alanı) ve bunların parçaları. Bu yapıyı
bilen biri hangi örneği görürse görsün ne yaptığını anlar.

## İki yazım, aynı nesneler

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 6, 5])
plt.title("pyplot")
print(len(plt.gcf().axes), plt.gca().get_title())

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 6, 5])
ax.set_title("object")
print(fig is plt.gcf(), ax is plt.gca(), ax.figure is fig)
print(len(plt.get_fignums()))
```

```text
1 pyplot
True True True
2
```

- `plt.plot` arkada **o anki** şekli (`plt.gcf()`, get current figure) ve
  çizim alanını (`plt.gca()`) bulur, yoksa açar ve oraya çizer. Kısa yazılır
  ama hangi alana çizdiği gizlidir.
- `fig, ax = plt.subplots()` aynı nesneleri açıkça verir. Yeni şekil artık "o
  anki" şekil oldu; açık şekil sayısı 2.
- İki yazım aynı nesneleri değiştirir: `plt.title("...")` aslında
  `plt.gca().set_title("...")` demektir.
- Bu modülde nesne yazımı kullanılıyor: birden fazla çizim alanı olunca
  "o anki alan" belirsizleşir, `ax` ise hep belli.

## Bir grafiğin anatomisi

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))
line, = ax.plot([1, 2, 3, 4], [3, 5, 4, 7], marker="o", label="2026")
ax.set(title="Weekly sales", xlabel="week", ylabel="sales")
ax.legend()
print(type(fig).__name__, type(ax).__name__, type(line).__name__)
print(ax.get_xlabel(), "|", ax.get_ylabel(), "|", ax.get_title())
print(len(ax.lines), ax.get_legend() is not None)
low, high = ax.get_xlim()
print(type(ax.xaxis).__name__, round(float(low), 2), round(float(high), 2))
```

```text
Figure Axes Line2D
week | sales | Weekly sales
1 True
XAxis 0.85 4.15
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="376.563281pt" height="226.838906pt" viewBox="0 0 376.563281 226.838906" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 226.838906 
L 376.563281 226.838906 
L 376.563281 0 
L 0 0 
L 0 226.838906 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 34.563281 188.638125 
L 369.363281 188.638125 
L 369.363281 22.318125 
L 34.563281 22.318125 
L 34.563281 188.638125 
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
       <use xlink:href="#m15aed4d867" x="49.781463" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="49.781463" y="203.235781" transform="rotate(-0 49.781463 203.235781)">1.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="100.508736" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="100.508736" y="203.235781" transform="rotate(-0 100.508736 203.235781)">1.5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="151.236009" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="151.236009" y="203.235781" transform="rotate(-0 151.236009 203.235781)">2.0</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="201.963281" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="201.963281" y="203.235781" transform="rotate(-0 201.963281 203.235781)">2.5</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="252.690554" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="252.690554" y="203.235781" transform="rotate(-0 252.690554 203.235781)">3.0</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="303.417827" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="303.417827" y="203.235781" transform="rotate(-0 303.417827 203.235781)">3.5</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="354.145099" y="188.638125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="354.145099" y="203.235781" transform="rotate(-0 354.145099 203.235781)">4.0</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="201.963281" y="217.236563" transform="rotate(-0 201.963281 217.236563)">week</text>
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
       <use xlink:href="#m5c8d5162d3" x="34.563281" y="181.078125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.563281" y="184.876953" transform="rotate(-0 27.563281 184.876953)">3</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.563281" y="143.278125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.563281" y="147.076953" transform="rotate(-0 27.563281 147.076953)">4</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.563281" y="105.478125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.563281" y="109.276953" transform="rotate(-0 27.563281 109.276953)">5</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.563281" y="67.678125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.563281" y="71.476953" transform="rotate(-0 27.563281 71.476953)">6</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="34.563281" y="29.878125" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="27.563281" y="33.676953" transform="rotate(-0 27.563281 33.676953)">7</text>
     </g>
    </g>
    <g id="text_14">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798437" y="105.478125" transform="rotate(-90 14.798437 105.478125)">sales</text>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 49.781463 181.078125 
L 151.236009 105.478125 
L 252.690554 143.278125 
L 354.145099 29.878125 
" clip-path="url(#p0b1ca53b63)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p0b1ca53b63)">
     <use xlink:href="#m98ae7f93d8" x="49.781463" y="181.078125" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="151.236009" y="105.478125" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="252.690554" y="143.278125" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="354.145099" y="29.878125" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 34.563281 188.638125 
L 34.563281 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 369.363281 188.638125 
L 369.363281 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 34.563281 188.638125 
L 369.363281 188.638125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 34.563281 22.318125 
L 369.363281 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_15">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="201.963281" y="16.318125" transform="rotate(-0 201.963281 16.318125)">Weekly sales</text>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 41.563281 45.318906 
L 99.013281 45.318906 
Q 101.013281 45.318906 101.013281 43.318906 
L 101.013281 29.318125 
Q 101.013281 27.318125 99.013281 27.318125 
L 41.563281 27.318125 
Q 39.563281 27.318125 39.563281 29.318125 
L 39.563281 43.318906 
Q 39.563281 45.318906 41.563281 45.318906 
L 41.563281 45.318906 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_14">
     <path d="M 43.563281 35.416563 
L 53.563281 35.416563 
L 63.563281 35.416563 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m98ae7f93d8" x="53.563281" y="35.416563" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="71.563281" y="38.916563" transform="rotate(-0 71.563281 38.916563)">2026</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p0b1ca53b63">
   <rect x="34.563281" y="22.318125" width="334.8" height="166.32"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Bir şekil (Figure), içinde bir alan (Axes): başlık, iki eksen, bir çizgi ve açıklama.</figcaption>
</figure>

| Nesne | Ne | Örnek metot |
|---|---|---|
| `Figure` | bütün tuval; kaydedilen şey | `fig.savefig`, `fig.suptitle` |
| `Axes` | bir çizim alanı: eksenler, başlık, çizgiler | `ax.plot`, `ax.set_title` |
| `Axis` | tek bir eksen (`ax.xaxis`, `ax.yaxis`) | işaretler ve sınırlar |
| `Line2D`, `Rectangle`, `Text` | çizilen her şey (**Artist**) | renk, kalınlık |

- `Axes` ile `Axis` farklı şeyler: **Axes** bütün çizim alanı, **Axis**
  onun tek bir ekseni. İsim benzerliği sık karışıklık sebebi.
- `ax.plot` çizdiği çizgileri bir liste olarak döndürür; `line, = ...` tek
  elemanı açar. Çizgiyi sonradan değiştirmek için tutulur.
- `ax.set(title=..., xlabel=..., ylabel=...)` birden fazla ayarı tek
  çağrıda yapar; her `set_` metodunun bir `get_` karşılığı vardır.
- Eksen sınırları veriden **biraz geniş** seçilir (1–4 verisi için 0,85–4,15):
  noktalar kenara yapışmasın diye.

## Birden fazla çizim alanı

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 3, figsize=(8, 4), layout="constrained")
print(type(axes).__name__, axes.shape)
for i, ax in enumerate(axes.flat):
    ax.plot([0, 1], [0, i])
    ax.set_title(f"panel {i}")
axes[1, 2].set_title("last")
print(len(fig.axes), axes[1, 2].get_title())
one = plt.subplots()[1]
row = plt.subplots(1, 3)[1]
print(type(one).__name__, row.shape)
```

```text
ndarray (2, 3)
6 last
Axes (3,)
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="581.32018pt" height="296.39952pt" viewBox="0 0 581.32018 296.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 296.39952 
L 581.32018 296.39952 
L 581.32018 0 
L 0 0 
L 0 296.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 51.207813 128.19952 
L 200.922803 128.19952 
L 200.922803 22.318125 
L 51.207813 22.318125 
L 51.207813 128.19952 
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
       <use xlink:href="#m15aed4d867" x="58.013039" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="58.013039" y="142.797176" transform="rotate(-0 58.013039 142.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="126.065308" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="126.065308" y="142.797176" transform="rotate(-0 126.065308 142.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="194.117576" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="194.117576" y="142.797176" transform="rotate(-0 194.117576 142.797176)">1.0</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="123.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="127.185557" transform="rotate(-0 44.207813 127.185557)">−0.050</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="99.322776" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="103.121604" transform="rotate(-0 44.207813 103.121604)">−0.025</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="75.258822" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="79.057651" transform="rotate(-0 44.207813 79.057651)">0.000</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="51.194869" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="54.993697" transform="rotate(-0 44.207813 54.993697)">0.025</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="27.130916" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="30.929744" transform="rotate(-0 44.207813 30.929744)">0.050</text>
     </g>
    </g>
   </g>
   <g id="line2d_9">
    <path d="M 58.013039 75.258822 
L 194.117576 75.258822 
" clip-path="url(#p4180a2fa7a)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 51.207813 128.19952 
L 51.207813 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 200.922803 128.19952 
L 200.922803 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 51.207813 128.19952 
L 200.922803 128.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 51.207813 22.318125 
L 200.922803 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_9">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="126.065308" y="16.318125" transform="rotate(-0 126.065308 16.318125)">panel 0</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 240.414583 128.19952 
L 390.129574 128.19952 
L 390.129574 22.318125 
L 240.414583 22.318125 
L 240.414583 128.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="247.21981" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="247.21981" y="142.797176" transform="rotate(-0 247.21981 142.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="315.272079" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="315.272079" y="142.797176" transform="rotate(-0 315.272079 142.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="383.324347" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="383.324347" y="142.797176" transform="rotate(-0 383.324347 142.797176)">1.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="123.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="127.185557" transform="rotate(-0 233.414583 127.185557)">0.00</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="99.322776" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="103.121604" transform="rotate(-0 233.414583 103.121604)">0.25</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="75.258822" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="79.057651" transform="rotate(-0 233.414583 79.057651)">0.50</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="51.194869" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="54.993697" transform="rotate(-0 233.414583 54.993697)">0.75</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="27.130916" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="30.929744" transform="rotate(-0 233.414583 30.929744)">1.00</text>
     </g>
    </g>
   </g>
   <g id="line2d_18">
    <path d="M 247.21981 123.386729 
L 383.324347 27.130916 
" clip-path="url(#p347903bbeb)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 240.414583 128.19952 
L 240.414583 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 390.129574 128.19952 
L 390.129574 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 240.414583 128.19952 
L 390.129574 128.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 240.414583 22.318125 
L 390.129574 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_18">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="315.272079" y="16.318125" transform="rotate(-0 315.272079 16.318125)">panel 1</text>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_12">
    <path d="M 423.258854 128.19952 
L 572.973845 128.19952 
L 572.973845 22.318125 
L 423.258854 22.318125 
L 423.258854 128.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_5">
    <g id="xtick_7">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m15aed4d867" x="430.064081" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="430.064081" y="142.797176" transform="rotate(-0 430.064081 142.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m15aed4d867" x="498.116349" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="498.116349" y="142.797176" transform="rotate(-0 498.116349 142.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m15aed4d867" x="566.168618" y="128.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="566.168618" y="142.797176" transform="rotate(-0 566.168618 142.797176)">1.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_6">
    <g id="ytick_11">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="123.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="127.185557" transform="rotate(-0 416.258854 127.185557)">0.0</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_23">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="99.322776" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="103.121604" transform="rotate(-0 416.258854 103.121604)">0.5</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="75.258822" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_24">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="79.057651" transform="rotate(-0 416.258854 79.057651)">1.0</text>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="51.194869" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_25">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="54.993697" transform="rotate(-0 416.258854 54.993697)">1.5</text>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="27.130916" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_26">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="30.929744" transform="rotate(-0 416.258854 30.929744)">2.0</text>
     </g>
    </g>
   </g>
   <g id="line2d_27">
    <path d="M 430.064081 123.386729 
L 566.168618 27.130916 
" clip-path="url(#p00350b5a1c)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_13">
    <path d="M 423.258854 128.19952 
L 423.258854 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_14">
    <path d="M 572.973845 128.19952 
L 572.973845 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_15">
    <path d="M 423.258854 128.19952 
L 572.973845 128.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_16">
    <path d="M 423.258854 22.318125 
L 572.973845 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_27">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="498.116349" y="16.318125" transform="rotate(-0 498.116349 16.318125)">panel 2</text>
   </g>
  </g>
  <g id="axes_4">
   <g id="patch_17">
    <path d="M 51.207813 272.19952 
L 200.922803 272.19952 
L 200.922803 166.318125 
L 51.207813 166.318125 
L 51.207813 272.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_7">
    <g id="xtick_10">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m15aed4d867" x="58.013039" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_28">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="58.013039" y="286.797176" transform="rotate(-0 58.013039 286.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_29">
      <g>
       <use xlink:href="#m15aed4d867" x="126.065308" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_29">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="126.065308" y="286.797176" transform="rotate(-0 126.065308 286.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_30">
      <g>
       <use xlink:href="#m15aed4d867" x="194.117576" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_30">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="194.117576" y="286.797176" transform="rotate(-0 194.117576 286.797176)">1.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_8">
    <g id="ytick_16">
     <g id="line2d_31">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="267.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_31">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="271.185557" transform="rotate(-0 44.207813 271.185557)">0</text>
     </g>
    </g>
    <g id="ytick_17">
     <g id="line2d_32">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="235.301458" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_32">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="239.100286" transform="rotate(-0 44.207813 239.100286)">1</text>
     </g>
    </g>
    <g id="ytick_18">
     <g id="line2d_33">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="203.216187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_33">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="207.015015" transform="rotate(-0 44.207813 207.015015)">2</text>
     </g>
    </g>
    <g id="ytick_19">
     <g id="line2d_34">
      <g>
       <use xlink:href="#m5c8d5162d3" x="51.207813" y="171.130916" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_34">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="44.207813" y="174.929744" transform="rotate(-0 44.207813 174.929744)">3</text>
     </g>
    </g>
   </g>
   <g id="line2d_35">
    <path d="M 58.013039 267.386729 
L 194.117576 171.130916 
" clip-path="url(#peaf9e35ec2)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_18">
    <path d="M 51.207813 272.19952 
L 51.207813 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_19">
    <path d="M 200.922803 272.19952 
L 200.922803 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_20">
    <path d="M 51.207813 272.19952 
L 200.922803 272.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_21">
    <path d="M 51.207813 166.318125 
L 200.922803 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_35">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="126.065308" y="160.318125" transform="rotate(-0 126.065308 160.318125)">panel 3</text>
   </g>
  </g>
  <g id="axes_5">
   <g id="patch_22">
    <path d="M 240.414583 272.19952 
L 390.129574 272.19952 
L 390.129574 166.318125 
L 240.414583 166.318125 
L 240.414583 272.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_9">
    <g id="xtick_13">
     <g id="line2d_36">
      <g>
       <use xlink:href="#m15aed4d867" x="247.21981" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_36">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="247.21981" y="286.797176" transform="rotate(-0 247.21981 286.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_37">
      <g>
       <use xlink:href="#m15aed4d867" x="315.272079" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_37">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="315.272079" y="286.797176" transform="rotate(-0 315.272079 286.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_15">
     <g id="line2d_38">
      <g>
       <use xlink:href="#m15aed4d867" x="383.324347" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_38">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="383.324347" y="286.797176" transform="rotate(-0 383.324347 286.797176)">1.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_10">
    <g id="ytick_20">
     <g id="line2d_39">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="267.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_39">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="271.185557" transform="rotate(-0 233.414583 271.185557)">0</text>
     </g>
    </g>
    <g id="ytick_21">
     <g id="line2d_40">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="243.322776" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_40">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="247.121604" transform="rotate(-0 233.414583 247.121604)">1</text>
     </g>
    </g>
    <g id="ytick_22">
     <g id="line2d_41">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="219.258822" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_41">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="223.057651" transform="rotate(-0 233.414583 223.057651)">2</text>
     </g>
    </g>
    <g id="ytick_23">
     <g id="line2d_42">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="195.194869" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_42">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="198.993697" transform="rotate(-0 233.414583 198.993697)">3</text>
     </g>
    </g>
    <g id="ytick_24">
     <g id="line2d_43">
      <g>
       <use xlink:href="#m5c8d5162d3" x="240.414583" y="171.130916" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_43">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="233.414583" y="174.929744" transform="rotate(-0 233.414583 174.929744)">4</text>
     </g>
    </g>
   </g>
   <g id="line2d_44">
    <path d="M 247.21981 267.386729 
L 383.324347 171.130916 
" clip-path="url(#p76e3c04ba3)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_23">
    <path d="M 240.414583 272.19952 
L 240.414583 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 390.129574 272.19952 
L 390.129574 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 240.414583 272.19952 
L 390.129574 272.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 240.414583 166.318125 
L 390.129574 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_44">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="315.272079" y="160.318125" transform="rotate(-0 315.272079 160.318125)">panel 4</text>
   </g>
  </g>
  <g id="axes_6">
   <g id="patch_27">
    <path d="M 423.258854 272.19952 
L 572.973845 272.19952 
L 572.973845 166.318125 
L 423.258854 166.318125 
L 423.258854 272.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_11">
    <g id="xtick_16">
     <g id="line2d_45">
      <g>
       <use xlink:href="#m15aed4d867" x="430.064081" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_45">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="430.064081" y="286.797176" transform="rotate(-0 430.064081 286.797176)">0.0</text>
     </g>
    </g>
    <g id="xtick_17">
     <g id="line2d_46">
      <g>
       <use xlink:href="#m15aed4d867" x="498.116349" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_46">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="498.116349" y="286.797176" transform="rotate(-0 498.116349 286.797176)">0.5</text>
     </g>
    </g>
    <g id="xtick_18">
     <g id="line2d_47">
      <g>
       <use xlink:href="#m15aed4d867" x="566.168618" y="272.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_47">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="566.168618" y="286.797176" transform="rotate(-0 566.168618 286.797176)">1.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_12">
    <g id="ytick_25">
     <g id="line2d_48">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="267.386729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_48">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="271.185557" transform="rotate(-0 416.258854 271.185557)">0</text>
     </g>
    </g>
    <g id="ytick_26">
     <g id="line2d_49">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="228.884404" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_49">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="232.683232" transform="rotate(-0 416.258854 232.683232)">2</text>
     </g>
    </g>
    <g id="ytick_27">
     <g id="line2d_50">
      <g>
       <use xlink:href="#m5c8d5162d3" x="423.258854" y="190.382078" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_50">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="416.258854" y="194.180907" transform="rotate(-0 416.258854 194.180907)">4</text>
     </g>
    </g>
   </g>
   <g id="line2d_51">
    <path d="M 430.064081 267.386729 
L 566.168618 171.130916 
" clip-path="url(#p4853517efb)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_28">
    <path d="M 423.258854 272.19952 
L 423.258854 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_29">
    <path d="M 572.973845 272.19952 
L 572.973845 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_30">
    <path d="M 423.258854 272.19952 
L 572.973845 272.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_31">
    <path d="M 423.258854 166.318125 
L 572.973845 166.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_51">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="498.116349" y="160.318125" transform="rotate(-0 498.116349 160.318125)">last</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p4180a2fa7a">
   <rect x="51.207813" y="22.318125" width="149.714991" height="105.881395"/>
  </clipPath>
  <clipPath id="p347903bbeb">
   <rect x="240.414583" y="22.318125" width="149.714991" height="105.881395"/>
  </clipPath>
  <clipPath id="p00350b5a1c">
   <rect x="423.258854" y="22.318125" width="149.714991" height="105.881395"/>
  </clipPath>
  <clipPath id="peaf9e35ec2">
   <rect x="51.207813" y="166.318125" width="149.714991" height="105.881395"/>
  </clipPath>
  <clipPath id="p76e3c04ba3">
   <rect x="240.414583" y="166.318125" width="149.714991" height="105.881395"/>
  </clipPath>
  <clipPath id="p4853517efb">
   <rect x="423.258854" y="166.318125" width="149.714991" height="105.881395"/>
  </clipPath>
 </defs>
</svg>
<figcaption><code>plt.subplots(2, 3)</code>: altı alan, her biri kendi başlığıyla.</figcaption>
</figure>

- `plt.subplots(2, 3)` 2 satır, 3 sütun çizim alanı açar; `axes` bir NumPy
  dizisidir, şekli `(2, 3)`. Tek alan `axes[1, 2]` ile seçilir.
- `axes.flat` iki boyutlu diziyi tek sırada dolaşır: bütün panellere aynı
  işi yapmanın kısa yolu.
- `layout="constrained"` başlıkların komşu panelin sayılarına binmesini
  önler; ayrıntısı "Yerleşim" notunda.
- Dikkat: dönen şeyin türü boyuta göre değişir. `plt.subplots()` tek bir
  `Axes`, `plt.subplots(1, 3)` **tek boyutlu** dizi (`axes[0]`, `axes[1, 0]`
  değil). Hepsinde iki boyutlu dizi istersen `squeeze=False`.

## Ortak eksen

```python
import matplotlib.pyplot as plt

fig, (left, right) = plt.subplots(1, 2, sharey=True, figsize=(7, 2.6),
                               layout="constrained")
left.plot([1, 2, 3], [10, 20, 15])
right.plot([1, 2, 3], [100, 120, 90])
left.set_title("Izmir")
right.set_title("Ankara")
print(left.get_ylim() == right.get_ylim())
fig.suptitle("Same y axis")
```

```text
True
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="512.39952pt" height="195.59952pt" viewBox="0 0 512.39952 195.59952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 195.59952 
L 512.39952 195.59952 
L 512.39952 0 
L 0 0 
L 0 195.59952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 33.2875 171.39952 
L 264.49327 171.39952 
L 264.49327 40.319542 
L 33.2875 40.319542 
L 33.2875 171.39952 
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
       <use xlink:href="#m15aed4d867" x="43.796853" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="43.796853" y="185.997176" transform="rotate(-0 43.796853 185.997176)">1.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="96.343619" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="96.343619" y="185.997176" transform="rotate(-0 96.343619 185.997176)">1.5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="148.890385" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="148.890385" y="185.997176" transform="rotate(-0 148.890385 185.997176)">2.0</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="201.437151" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="201.437151" y="185.997176" transform="rotate(-0 201.437151 185.997176)">2.5</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="253.983917" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="253.983917" y="185.997176" transform="rotate(-0 253.983917 185.997176)">3.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_6">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="149.191755" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="152.990583" transform="rotate(-0 26.2875 152.990583)">25</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="122.109115" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="125.907943" transform="rotate(-0 26.2875 125.907943)">50</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="95.026475" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="98.825303" transform="rotate(-0 26.2875 98.825303)">75</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="67.943835" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="71.742663" transform="rotate(-0 26.2875 71.742663)">100</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="40.861195" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="44.660023" transform="rotate(-0 26.2875 44.660023)">125</text>
     </g>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 43.796853 165.441339 
L 148.890385 154.608283 
L 253.983917 160.024811 
" clip-path="url(#pbf9fef0cbd)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 33.2875 171.39952 
L 33.2875 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 264.49327 171.39952 
L 264.49327 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 33.2875 171.39952 
L 264.49327 171.39952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 33.2875 40.319542 
L 264.49327 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_11">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="148.890385" y="34.319542" transform="rotate(-0 148.890385 34.319542)">Izmir</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 273.99375 171.39952 
L 505.19952 171.39952 
L 505.19952 40.319542 
L 273.99375 40.319542 
L 273.99375 171.39952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="284.503103" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="284.503103" y="185.997176" transform="rotate(-0 284.503103 185.997176)">1.0</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="337.049869" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="337.049869" y="185.997176" transform="rotate(-0 337.049869 185.997176)">1.5</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="389.596635" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="389.596635" y="185.997176" transform="rotate(-0 389.596635 185.997176)">2.0</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m15aed4d867" x="442.143401" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="442.143401" y="185.997176" transform="rotate(-0 442.143401 185.997176)">2.5</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m15aed4d867" x="494.690167" y="171.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="494.690167" y="185.997176" transform="rotate(-0 494.690167 185.997176)">3.0</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_6">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="273.99375" y="149.191755" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="273.99375" y="122.109115" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m5c8d5162d3" x="273.99375" y="95.026475" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="273.99375" y="67.943835" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m5c8d5162d3" x="273.99375" y="40.861195" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="line2d_22">
    <path d="M 284.503103 67.943835 
L 389.596635 46.277723 
L 494.690167 78.776891 
" clip-path="url(#p7b41fc7f00)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 273.99375 171.39952 
L 273.99375 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 505.19952 171.39952 
L 505.19952 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 273.99375 171.39952 
L 505.19952 171.39952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 273.99375 40.319542 
L 505.19952 40.319542 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_17">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="389.596635" y="34.319542" transform="rotate(-0 389.596635 34.319542)">Ankara</text>
   </g>
  </g>
  <g id="text_18">
   <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="256.19976" y="16.318125" transform="rotate(-0 256.19976 16.318125)">Same y axis</text>
  </g>
 </g>
 <defs>
  <clipPath id="pbf9fef0cbd">
   <rect x="33.2875" y="40.319542" width="231.20577" height="131.079978"/>
  </clipPath>
  <clipPath id="p7b41fc7f00">
   <rect x="273.99375" y="40.319542" width="231.20577" height="131.079978"/>
  </clipPath>
 </defs>
</svg>
<figcaption><code>sharey=True</code>: iki alan aynı y eksenini kullanıyor; İzmir'in küçüklüğü görünüyor.</figcaption>
</figure>

- Yan yana iki grafik karşılaştırılacaksa eksenleri **aynı** olmalı. Her
  alan kendi sınırını seçseydi İzmir'in 20'si ile Ankara'nın 120'si aynı
  yükseklikte görünürdü.
- `sharey=True` bütün alanlara tek y ekseni verir; İzmir'in çizgisi altta
  basık kaldı, çünkü gerçekten küçük. `sharex` x için aynısı.
- `fig.suptitle` bütün şeklin başlığı; her alanın kendi `set_title`'ı ayrı.
- Tek alana iki farklı ölçekte veri koymak (iki ayrı y ekseni)
  `ax.twinx()` ile olur; okunması zordur, özelleştirme bölümünde.

## Boyut, çözünürlük ve kaydetmek

```python
import matplotlib.pyplot as plt
from matplotlib.image import imread

fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
ax.plot([1, 2, 3], [1, 4, 9])
print(fig.get_size_inches().tolist(), fig.dpi)
fig.savefig("a.png")
fig.savefig("b.png", dpi=200)
print(imread("a.png").shape[:2], imread("b.png").shape[:2])
fig.savefig("c.png", bbox_inches="tight")
h, w = imread("c.png").shape[:2]
print(w < 400 and h < 300)
```

```text
[4.0, 3.0] 100
(300, 400) (600, 800)
True
```

- `figsize` **inç** cinsindendir (4 × 3). Piksel = inç × `dpi` (dots per
  inch): 4 × 100 = 400 piksel genişlik. Resmin şekli `(yükseklik, genişlik)`
  olarak okunur: `(300, 400)`.
- `savefig(..., dpi=200)` aynı grafiği iki kat çözünürlükte kaydeder: yazılar
  ve çizgiler aynı **oranda** kalır, yalnızca daha keskin olur. Sunum ve
  basılı belge için.
- `bbox_inches="tight"` kenardaki boşluğu kırpar; resim küçüldü. Uzun eksen
  etiketlerinin kesilmesini de önler.
- Dosya türü uzantıdan gelir: `.png` resim, `.svg` ve `.pdf` ölçeklenince
  bulanmayan vektör.

## Şekilleri kapatmak

```python
import warnings
import matplotlib.pyplot as plt

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    for i in range(25):
        fig, ax = plt.subplots()
        ax.plot([0, i])
print(len(plt.get_fignums()), len(caught) > 0)
print(str(caught[0].message).split(".")[0])
plt.close("all")
for i in range(25):
    fig, ax = plt.subplots()
    ax.plot([0, i])
    fig.savefig(f"chart_{i}.png")
    plt.close(fig)
print(len(plt.get_fignums()))
```

```text
25 True
More than 20 figures have been opened
0
```

- pyplot açtığı her şekli kapatılana kadar **hatırlar**. Döngüde grafik
  üreten bir betik her turda bellek biriktirir; 20'yi geçince matplotlib
  uyarır.
- Kaydettikten sonra `plt.close(fig)`: şekil bırakılır, açık şekil sayısı 0
  kalır. Hepsini kapatmak için `plt.close("all")`.
- Defterde (Jupyter) şekiller hücre bitince gösterilir ve kapanır; aynı kod
  betik olarak çalışınca bu birikim ortaya çıkar.

## Özet

- `plt.plot` "o anki" alana çizer; `fig, ax = plt.subplots()` nesneleri
  açıkça verir. Birden fazla alanda nesne yazımı.
- Figure tuval, Axes çizim alanı, Axis tek eksen; çizilen her şey Artist.
- `plt.subplots(r, c)` dizi döndürür; şekli boyuta göre değişir.
  Karşılaştırmada `sharex` / `sharey`.
- Piksel = `figsize` × `dpi`; `bbox_inches="tight"` boşluğu kırpar.
- Döngüde `savefig` sonrası `plt.close(fig)`.
