# Matplotlib Özelleştirme

Varsayılan matplotlib grafiği doğrudur ama çoğu zaman **söylemek istediğini**
söylemez: eksende `1e6` yazar, tarihler üst üste biner, asıl nokta
kalabalığın içinde kaybolur. Bu bölüm bir grafiği rapora hazır hâle getiren
ayarları anlatıyor: eksen yazılarının biçimi, not ve ok, logaritmik eksen, iki
y ekseni, sadeleştirme ve tarih ekseni. Hepsinin ölçütü aynı: okuyan kişi
mesajı **ilk bakışta** görebiliyor mu?

## Eksen yazılarını biçimlendirmek

```python
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter

months = ["Jan", "Feb", "Mar", "Apr"]
revenue = [1_250_000, 1_480_000, 1_310_000, 1_720_000]
growth = [0.0, 0.184, -0.115, 0.313]
fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3), layout="constrained")
left.bar(months, revenue)
left.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
right.plot(months, growth, marker="o")
right.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
fig.canvas.draw()
print([t.get_text() for t in left.get_yticklabels()][:3])
print([t.get_text() for t in right.get_yticklabels()][:3])
```

```text
['0', '250,000', '500,000']
['−20%', '−10%', '0%']
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="548.39952pt" height="224.39952pt" viewBox="0 0 548.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 548.39952 224.39952 
L 548.39952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 65.09375 200.198739 
L 281.34327 200.198739 
L 281.34327 7.2 
L 65.09375 7.2 
L 65.09375 200.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 74.923274 200.198739 
L 116.310742 200.198739 
L 116.310742 66.617109 
L 74.923274 66.617109 
z
" clip-path="url(#p0f686fd707)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_4">
    <path d="M 126.657609 200.198739 
L 168.045077 200.198739 
L 168.045077 42.038089 
L 126.657609 42.038089 
z
" clip-path="url(#p0f686fd707)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_5">
    <path d="M 178.391943 200.198739 
L 219.779411 200.198739 
L 219.779411 60.205191 
L 178.391943 60.205191 
z
" clip-path="url(#p0f686fd707)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_6">
    <path d="M 230.126278 200.198739 
L 271.513746 200.198739 
L 271.513746 16.390416 
L 230.126278 16.390416 
z
" clip-path="url(#p0f686fd707)" style="fill: #1f77b4"/>
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
       <use xlink:href="#m15aed4d867" x="95.617008" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="95.617008" y="214.796395" transform="rotate(-0 95.617008 214.796395)">Jan</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="147.351343" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="147.351343" y="214.797176" transform="rotate(-0 147.351343 214.797176)">Feb</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="199.085677" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="199.085677" y="214.796395" transform="rotate(-0 199.085677 214.796395)">Mar</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="250.820012" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="250.820012" y="214.796395" transform="rotate(-0 250.820012 214.796395)">Apr</text>
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
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="203.997567" transform="rotate(-0 58.09375 203.997567)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="173.482413" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="177.281241" transform="rotate(-0 58.09375 177.281241)">250,000</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="146.766087" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="150.564915" transform="rotate(-0 58.09375 150.564915)">500,000</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="120.049761" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="123.848589" transform="rotate(-0 58.09375 123.848589)">750,000</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="93.333435" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="97.132263" transform="rotate(-0 58.09375 97.132263)">1,000,000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="66.617109" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="70.415937" transform="rotate(-0 58.09375 70.415937)">1,250,000</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="39.900783" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="43.699611" transform="rotate(-0 58.09375 43.699611)">1,500,000</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="65.09375" y="13.184457" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="58.09375" y="16.983285" transform="rotate(-0 58.09375 16.983285)">1,750,000</text>
     </g>
    </g>
   </g>
   <g id="patch_7">
    <path d="M 65.09375 200.198739 
L 65.09375 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 281.34327 200.198739 
L 281.34327 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 65.09375 200.198739 
L 281.34327 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 65.09375 7.2 
L 281.34327 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_11">
    <path d="M 324.95 200.198739 
L 541.19952 200.198739 
L 541.19952 7.2 
L 324.95 7.2 
L 324.95 200.198739 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_5">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="334.779524" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="334.779524" y="214.796395" transform="rotate(-0 334.779524 214.796395)">Jan</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="400.309681" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="400.309681" y="214.797176" transform="rotate(-0 400.309681 214.797176)">Feb</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m15aed4d867" x="465.839839" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="465.839839" y="214.796395" transform="rotate(-0 465.839839 214.796395)">Mar</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m15aed4d867" x="531.369996" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="531.369996" y="214.796395" transform="rotate(-0 531.369996 214.796395)">Apr</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_9">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="324.95" y="185.277001" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="317.95" y="189.075829" transform="rotate(-0 317.95 189.075829)">−10%</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="324.95" y="144.283216" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="317.95" y="148.082044" transform="rotate(-0 317.95 148.082044)">0%</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m5c8d5162d3" x="324.95" y="103.289432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="317.95" y="107.08826" transform="rotate(-0 317.95 107.08826)">10%</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="324.95" y="62.295647" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="317.95" y="66.094475" transform="rotate(-0 317.95 66.094475)">20%</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m5c8d5162d3" x="324.95" y="21.301862" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="317.95" y="25.10069" transform="rotate(-0 317.95 25.10069)">30%</text>
     </g>
    </g>
   </g>
   <g id="line2d_22">
    <path d="M 334.779524 144.283216 
L 400.309681 68.854652 
L 465.839839 191.426069 
L 531.369996 15.97267 
" clip-path="url(#pefff10a228)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#pefff10a228)">
     <use xlink:href="#m98ae7f93d8" x="334.779524" y="144.283216" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="400.309681" y="68.854652" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="465.839839" y="191.426069" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="531.369996" y="15.97267" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="patch_12">
    <path d="M 324.95 200.198739 
L 324.95 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_13">
    <path d="M 541.19952 200.198739 
L 541.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_14">
    <path d="M 324.95 200.198739 
L 541.19952 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_15">
    <path d="M 324.95 7.2 
L 541.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p0f686fd707">
   <rect x="65.09375" y="7.2" width="216.24952" height="192.998739"/>
  </clipPath>
  <clipPath id="pefff10a228">
   <rect x="324.95" y="7.2" width="216.24952" height="192.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Solda binlik ayraç, sağda yüzde.</figcaption>
</figure>

- Büyük sayılar varsayılan olarak bilimsel gösterimle yazılır (eksenin
  tepesinde `1e6`). `StrMethodFormatter("{x:,.0f}")` f-string kuralıyla
  binlik ayraç koyar: `250,000`.
- Oranlar 0–1 arasında saklanır ama yüzde olarak okunur.
  `PercentFormatter(xmax=1)` 0,184'ü `18%` yazar; `decimals=0` ondalığı atar.
- İşaret yazıları ancak şekil **çizilince** kesinleşir; okumak için önce
  `fig.canvas.draw()`. matplotlib eksiyi tireden uzun, gerçek eksi işaretiyle
  (`−`) yazar.

## Not ve ok: dikkati çekmek

```python
import matplotlib.pyplot as plt
import numpy as np

days = np.arange(1, 15)
visits = np.array([120, 118, 125, 130, 128, 135, 310,
                   140, 138, 142, 145, 150, 148, 155])
peak = int(visits.argmax())
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
ax.plot(days, visits, marker="o")
ax.annotate("campaign day", xy=(days[peak], visits[peak]),
            xytext=(days[peak] + 2, 280), arrowprops=dict(arrowstyle="->"))
ax.axhline(visits.mean(), linestyle="--", linewidth=1, label="mean")
ax.legend(loc="upper left")
ax.set(xlabel="day", ylabel="visits")
print(int(days[peak]), int(visits[peak]), round(float(visits.mean()), 1))
```

```text
7 310 148.9
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.39952pt" viewBox="0 0 440.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.39952 224.39952 
L 440.39952 0 
L 0 0 
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
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="91.816501" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="91.816501" y="200.796395" transform="rotate(-0 91.816501 200.796395)">2</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="145.790101" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="145.790101" y="200.796395" transform="rotate(-0 145.790101 200.796395)">4</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="199.763701" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="199.763701" y="200.796395" transform="rotate(-0 199.763701 200.796395)">6</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="253.737301" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="253.737301" y="200.796395" transform="rotate(-0 253.737301 200.796395)">8</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="307.7109" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="307.7109" y="200.796395" transform="rotate(-0 307.7109 200.796395)">10</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="361.6845" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="361.6845" y="200.796395" transform="rotate(-0 361.6845 200.796395)">12</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="415.6581" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="415.6581" y="200.796395" transform="rotate(-0 415.6581 200.796395)">14</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="214.797176" transform="rotate(-0 240.243901 214.797176)">day</text>
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
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="150.941411" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="154.74024" transform="rotate(-0 40.288281 154.74024)">150</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="108.564816" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="112.363644" transform="rotate(-0 40.288281 112.363644)">200</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="66.188221" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="69.987049" transform="rotate(-0 40.288281 69.987049)">250</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="23.811625" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="27.610454" transform="rotate(-0 40.288281 27.610454)">300</text>
     </g>
    </g>
    <g id="text_13">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="96.699369" transform="rotate(-90 14.798438 96.699369)">visits</text>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 64.829701 176.367369 
L 91.816501 178.062432 
L 118.803301 172.129709 
L 145.790101 167.89205 
L 172.776901 169.587113 
L 199.763701 163.65439 
L 226.750501 15.336306 
L 253.737301 159.41673 
L 280.7241 161.111794 
L 307.7109 157.721667 
L 334.6977 155.179071 
L 361.6845 150.941411 
L 388.6713 152.636475 
L 415.6581 146.703752 
" clip-path="url(#p85c489fea2)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p85c489fea2)">
     <use xlink:href="#m98ae7f93d8" x="64.829701" y="176.367369" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="91.816501" y="178.062432" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="118.803301" y="172.129709" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="145.790101" y="167.89205" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="172.776901" y="169.587113" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="199.763701" y="163.65439" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="226.750501" y="15.336306" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="253.737301" y="159.41673" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="280.7241" y="161.111794" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="307.7109" y="157.721667" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="334.6977" y="155.179071" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="361.6845" y="150.941411" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="388.6713" y="152.636475" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="415.6581" y="146.703752" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 47.288281 151.910019 
L 433.19952 151.910019 
" clip-path="url(#p85c489fea2)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #1f77b4"/>
   </g>
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
   <g id="patch_7">
    <path d="M 286.802884 30.667988 
Q 257.746166 23.249659 229.772734 16.107898 
" style="fill: none; stroke: #000000; stroke-linecap: round"/>
    <path d="M 233.153677 19.035222 
L 229.772734 16.107898 
L 234.143159 15.159538 
" style="fill: none; stroke: #000000; stroke-linecap: round"/>
   </g>
   <g id="text_14">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="280.7241" y="40.762264" transform="rotate(-0 280.7241 40.762264)">campaign day</text>
   </g>
   <g id="legend_1">
    <g id="patch_8">
     <path d="M 54.288281 30.200781 
L 114.647656 30.200781 
Q 116.647656 30.200781 116.647656 28.200781 
L 116.647656 14.2 
Q 116.647656 12.2 114.647656 12.2 
L 54.288281 12.2 
Q 52.288281 12.2 52.288281 14.2 
L 52.288281 28.200781 
Q 52.288281 30.200781 54.288281 30.200781 
L 54.288281 30.200781 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_14">
     <path d="M 56.288281 20.298437 
L 66.288281 20.298437 
L 76.288281 20.298437 
" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: #1f77b4"/>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="84.288281" y="23.798437" transform="rotate(-0 84.288281 23.798437)">mean</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p85c489fea2">
   <rect x="47.288281" y="7.2" width="385.911239" height="178.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Ok sıçramanın sebebini söylüyor; kesik çizgi ortalama.</figcaption>
</figure>

- `annotate(metin, xy=nokta, xytext=yazının yeri, arrowprops=...)` bir
  noktayı açıklar. Grafik bir şey **anlatıyorsa** anlatılan yer işaretlenmeli;
  okuyan kişi 7. günün neden sıçradığını kendi tahmin etmemeli.
- `axhline` yatay bir referans çizgisi çeker (ortalama, hedef, sınır).
  Dikeyi `axvline`.
- Dikkat: 310'luk tek gün ortalamayı 148,9'a çekti; günlerin çoğu bu çizginin
  altında. Aykırı bir değer varken ortalamayı çizmek yanıltabilir; medyan
  daha dürüst olabilir.

## Logaritmik eksen

```python
import matplotlib.pyplot as plt
import numpy as np

weeks = np.arange(0, 11)
users = 50 * 2.0 ** weeks
fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3), layout="constrained")
left.plot(weeks, users, marker="o")
left.set_title("linear")
right.plot(weeks, users, marker="o")
right.set_yscale("log")
right.set_title("log")
print(int(users[-1]), right.get_yscale())
print(np.allclose(np.diff(np.log10(users)), np.log10(2)))
```

```text
51200 log
True
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="548.39952pt" height="224.39952pt" viewBox="0 0 548.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 548.39952 224.39952 
L 548.39952 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 46.0125 200.19952 
L 278.30577 200.19952 
L 278.30577 22.318125 
L 46.0125 22.318125 
L 46.0125 200.19952 
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
       <use xlink:href="#m15aed4d867" x="56.571285" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="56.571285" y="214.797176" transform="rotate(-0 56.571285 214.797176)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="98.806425" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="98.806425" y="214.797176" transform="rotate(-0 98.806425 214.797176)">2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="141.041565" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="141.041565" y="214.797176" transform="rotate(-0 141.041565 214.797176)">4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="183.276705" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="183.276705" y="214.797176" transform="rotate(-0 183.276705 214.797176)">6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="225.511845" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="225.511845" y="214.797176" transform="rotate(-0 225.511845 214.797176)">8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="267.746985" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="267.746985" y="214.797176" transform="rotate(-0 267.746985 214.797176)">10</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="192.272077" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="196.070905" transform="rotate(-0 39.0125 196.070905)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="160.657148" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="164.455976" transform="rotate(-0 39.0125 164.455976)">10000</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="129.04222" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="132.841048" transform="rotate(-0 39.0125 132.841048)">20000</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="97.427291" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="101.226119" transform="rotate(-0 39.0125 101.226119)">30000</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="65.812363" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="69.611191" transform="rotate(-0 39.0125 69.611191)">40000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="46.0125" y="34.197434" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="39.0125" y="37.996262" transform="rotate(-0 39.0125 37.996262)">50000</text>
     </g>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 56.571285 192.114002 
L 77.688855 191.955927 
L 98.806425 191.639778 
L 119.923995 191.00748 
L 141.041565 189.742882 
L 162.159135 187.213688 
L 183.276705 182.1553 
L 204.394275 172.038522 
L 225.511845 151.804968 
L 246.629415 111.33786 
L 267.746985 30.403643 
" clip-path="url(#pd990c969c1)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#pd990c969c1)">
     <use xlink:href="#m98ae7f93d8" x="56.571285" y="192.114002" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="77.688855" y="191.955927" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="98.806425" y="191.639778" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="119.923995" y="191.00748" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="141.041565" y="189.742882" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="162.159135" y="187.213688" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="183.276705" y="182.1553" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="204.394275" y="172.038522" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="225.511845" y="151.804968" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="246.629415" y="111.33786" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="267.746985" y="30.403643" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 46.0125 200.19952 
L 46.0125 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 278.30577 200.19952 
L 278.30577 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 46.0125 200.19952 
L 278.30577 200.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 46.0125 22.318125 
L 278.30577 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_13">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="162.159135" y="16.318125" transform="rotate(-0 162.159135 16.318125)">linear</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 308.90625 200.19952 
L 541.19952 200.19952 
L 541.19952 22.318125 
L 308.90625 22.318125 
L 308.90625 200.19952 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="319.465035" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="319.465035" y="214.797176" transform="rotate(-0 319.465035 214.797176)">0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m15aed4d867" x="361.700175" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="361.700175" y="214.797176" transform="rotate(-0 361.700175 214.797176)">2</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m15aed4d867" x="403.935315" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="403.935315" y="214.797176" transform="rotate(-0 403.935315 214.797176)">4</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m15aed4d867" x="446.170455" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="446.170455" y="214.797176" transform="rotate(-0 446.170455 214.797176)">6</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m15aed4d867" x="488.405595" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="488.405595" y="214.797176" transform="rotate(-0 488.405595 214.797176)">8</text>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m15aed4d867" x="530.640735" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="530.640735" y="214.797176" transform="rotate(-0 530.640735 214.797176)">10</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_7">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="308.90625" y="175.942966" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <g style="fill: currentColor" transform="translate(284.30625 180.642966)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">2</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m5c8d5162d3" x="308.90625" y="122.223948" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <g style="fill: currentColor" transform="translate(284.30625 126.923948)">
       <text>
        <tspan x="0" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.674688" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.804688" style="font-size: 7px; font-family:inherit; fill: currentColor">3</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m5c8d5162d3" x="308.90625" y="68.504929" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <g style="fill: currentColor" transform="translate(284.30625 73.154929)">
       <text>
        <tspan x="0" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">1</tspan>
        <tspan x="6.362305" y="-0.762187" style="font-size: 10px; font-family:inherit; fill: currentColor">0</tspan>
        <tspan x="12.820312" y="-4.892187" style="font-size: 7px; font-family:inherit; fill: currentColor">4</tspan>
       </text>
      </g>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_23">
      <defs>
       <path id="m0fd5f78bf4" d="M 0 0 
L -2 0 
" style="stroke: currentColor; stroke-width: 0.6"/>
      </defs>
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="197.319913" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="192.114002" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="187.860463" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="184.264147" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="181.148877" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="178.401014" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_16">
     <g id="line2d_29">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="159.77193" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_17">
     <g id="line2d_30">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="150.312481" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_18">
     <g id="line2d_31">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="143.600894" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_19">
     <g id="line2d_32">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="138.394984" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_20">
     <g id="line2d_33">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="134.141445" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_21">
     <g id="line2d_34">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="130.545129" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_22">
     <g id="line2d_35">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="127.429858" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_23">
     <g id="line2d_36">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="124.681995" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_24">
     <g id="line2d_37">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="106.052912" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_25">
     <g id="line2d_38">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="96.593462" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_26">
     <g id="line2d_39">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="89.881876" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_27">
     <g id="line2d_40">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="84.675965" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_28">
     <g id="line2d_41">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="80.422426" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_29">
     <g id="line2d_42">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="76.82611" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_30">
     <g id="line2d_43">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="73.71084" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_31">
     <g id="line2d_44">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="70.962977" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_32">
     <g id="line2d_45">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="52.333893" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_33">
     <g id="line2d_46">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="42.874444" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_34">
     <g id="line2d_47">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="36.162857" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_35">
     <g id="line2d_48">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="30.956947" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_36">
     <g id="line2d_49">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="26.703408" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
    <g id="ytick_37">
     <g id="line2d_50">
      <g>
       <use xlink:href="#m0fd5f78bf4" x="308.90625" y="23.107092" style="fill: currentColor; stroke: currentColor; stroke-width: 0.6"/>
      </g>
     </g>
    </g>
   </g>
   <g id="line2d_51">
    <path d="M 319.465035 192.114002 
L 340.582605 175.942966 
L 361.700175 159.77193 
L 382.817745 143.600894 
L 403.935315 127.429858 
L 425.052885 111.258823 
L 446.170455 95.087787 
L 467.288025 78.916751 
L 488.405595 62.745715 
L 509.523165 46.574679 
L 530.640735 30.403643 
" clip-path="url(#p08d6cbb5c9)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p08d6cbb5c9)">
     <use xlink:href="#m98ae7f93d8" x="319.465035" y="192.114002" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="340.582605" y="175.942966" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="361.700175" y="159.77193" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="382.817745" y="143.600894" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="403.935315" y="127.429858" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="425.052885" y="111.258823" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="446.170455" y="95.087787" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="467.288025" y="78.916751" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="488.405595" y="62.745715" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="509.523165" y="46.574679" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="530.640735" y="30.403643" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="patch_8">
    <path d="M 308.90625 200.19952 
L 308.90625 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 541.19952 200.19952 
L 541.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 308.90625 200.19952 
L 541.19952 200.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 308.90625 22.318125 
L 541.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_23">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="425.052885" y="16.318125" transform="rotate(-0 425.052885 16.318125)">log</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pd990c969c1">
   <rect x="46.0125" y="22.318125" width="232.29327" height="177.881395"/>
  </clipPath>
  <clipPath id="p08d6cbb5c9">
   <rect x="308.90625" y="22.318125" width="232.29327" height="177.881395"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Aynı veri: doğrusal eksende ilk haftalar kayboluyor, log eksende düz çizgi.</figcaption>
</figure>

- Her hafta iki katına çıkan bir sayı 10 haftada 50'den 51 200'e varır.
  Doğrusal eksende ilk haftalar sıfıra yapışır, son iki nokta dışında hiçbir
  şey görünmez.
- `set_yscale("log")` eksende eşit aralıkları eşit **oranlar** yapar
  (10, 100, 1000). Sabit oranla büyüme düz bir çizgi olur: her adımda log
  değeri aynı miktar artıyor.
- Logaritmik eksen sıfırı ve eksi değerleri gösteremez. Okuyanın eksenin log
  olduğunu fark etmesi için başlıkta ya da etikette söylenmeli.

## İki y ekseni: twinx

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
temp = [8, 10, 14, 18, 23, 28]
sales = [120, 130, 180, 260, 390, 520]
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
line1, = ax.plot(months, temp, color="tab:orange", marker="o", label="temperature")
ax.set_ylabel("temperature (C)")
ax2 = ax.twinx()
line2, = ax2.plot(months, sales, color="tab:blue", marker="s",
                  label="ice cream sales")
ax2.set_ylabel("sales")
ax.legend(handles=[line1, line2], loc="upper left")
print(len(fig.axes), ax.get_ylim()[1] < ax2.get_ylim()[1])
```

```text
2 True
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.39952pt" viewBox="0 0 440.39952 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 440.39952 224.39952 
L 440.39952 0 
L 0 0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 50.465625 200.198739 
L 393.111239 200.198739 
L 393.111239 7.2 
L 50.465625 7.2 
L 50.465625 200.198739 
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
       <use xlink:href="#m15aed4d867" x="66.040426" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="66.040426" y="214.796395" transform="rotate(-0 66.040426 214.796395)">Jan</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="128.339628" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="128.339628" y="214.797176" transform="rotate(-0 128.339628 214.797176)">Feb</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="190.638831" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="190.638831" y="214.796395" transform="rotate(-0 190.638831 214.796395)">Mar</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="252.938033" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="252.938033" y="214.796395" transform="rotate(-0 252.938033 214.796395)">Apr</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="315.237236" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="315.237236" y="214.796395" transform="rotate(-0 315.237236 214.796395)">May</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="377.536438" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="377.536438" y="214.796395" transform="rotate(-0 377.536438 214.796395)">Jun</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="195.812404" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="199.611232" transform="rotate(-0 43.465625 199.611232)">7.5</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="173.880729" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="177.679557" transform="rotate(-0 43.465625 177.679557)">10.0</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="151.949054" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="155.747882" transform="rotate(-0 43.465625 155.747882)">12.5</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="130.017379" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="133.816207" transform="rotate(-0 43.465625 133.816207)">15.0</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="108.085704" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="111.884532" transform="rotate(-0 43.465625 111.884532)">17.5</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="86.154029" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="89.952858" transform="rotate(-0 43.465625 89.952858)">20.0</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="64.222355" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="68.021183" transform="rotate(-0 43.465625 68.021183)">22.5</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="42.29068" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="46.089508" transform="rotate(-0 43.465625 46.089508)">25.0</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="50.465625" y="20.359005" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="43.465625" y="24.157833" transform="rotate(-0 43.465625 24.157833)">27.5</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="103.699369" transform="rotate(-90 14.797656 103.699369)">temperature (C)</text>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 66.040426 191.426069 
L 128.339628 173.880729 
L 190.638831 138.790049 
L 252.938033 103.699369 
L 315.237236 59.83602 
L 377.536438 15.97267 
" clip-path="url(#p6e1f806ce9)" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p6e1f806ce9)">
     <use xlink:href="#m43dc4bf304" x="66.040426" y="191.426069" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="128.339628" y="173.880729" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="190.638831" y="138.790049" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="252.938033" y="103.699369" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="315.237236" y="59.83602" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#m43dc4bf304" x="377.536438" y="15.97267" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 50.465625 200.198739 
L 50.465625 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 393.111239 200.198739 
L 393.111239 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 50.465625 200.198739 
L 393.111239 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 50.465625 7.2 
L 393.111239 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 57.465625 45.201562 
L 167.140625 45.201562 
Q 169.140625 45.201562 169.140625 43.201562 
L 169.140625 14.2 
Q 169.140625 12.2 167.140625 12.2 
L 57.465625 12.2 
Q 55.465625 12.2 55.465625 14.2 
L 55.465625 43.201562 
Q 55.465625 45.201562 57.465625 45.201562 
L 57.465625 45.201562 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_17">
     <path d="M 59.465625 20.298438 
L 69.465625 20.298438 
L 79.465625 20.298438 
" style="fill: none; stroke: #ff7f0e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m43dc4bf304" x="69.465625" y="20.298438" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="23.798438" transform="rotate(-0 87.465625 23.798438)">temperature</text>
    </g>
    <g id="line2d_18">
     <path d="M 59.465625 35.299219 
L 69.465625 35.299219 
L 79.465625 35.299219 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
     <defs>
      <path id="m4334b5412b" d="M -3 3 
L 3 3 
L 3 -3 
L -3 -3 
z
" style="stroke: #1f77b4; stroke-linejoin: miter"/>
     </defs>
     <g>
      <use xlink:href="#m4334b5412b" x="69.465625" y="35.299219" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="87.465625" y="38.799219" transform="rotate(-0 87.465625 38.799219)">ice cream sales</text>
    </g>
   </g>
  </g>
  <g id="axes_2">
   <g id="matplotlib.axis_3">
    <g id="ytick_10">
     <g id="line2d_19">
      <defs>
       <path id="m004d6dcf24" d="M 0 0 
L 3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="203.997567" transform="rotate(-0 400.111239 203.997567)">100</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="178.267064" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="182.065892" transform="rotate(-0 400.111239 182.065892)">150</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="156.335389" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="160.134217" transform="rotate(-0 400.111239 160.134217)">200</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="134.403714" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="138.202542" transform="rotate(-0 400.111239 138.202542)">250</text>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_23">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="112.472039" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="116.270867" transform="rotate(-0 400.111239 116.270867)">300</text>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="90.540364" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_24">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="94.339193" transform="rotate(-0 400.111239 94.339193)">350</text>
     </g>
    </g>
    <g id="ytick_16">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="68.60869" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_25">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="72.407518" transform="rotate(-0 400.111239 72.407518)">400</text>
     </g>
    </g>
    <g id="ytick_17">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="46.677015" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_26">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="50.475843" transform="rotate(-0 400.111239 50.475843)">450</text>
     </g>
    </g>
    <g id="ytick_18">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m004d6dcf24" x="393.111239" y="24.74534" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_27">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="400.111239" y="28.544168" transform="rotate(-0 400.111239 28.544168)">500</text>
     </g>
    </g>
    <g id="text_28">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="430.797176" y="103.699369" transform="rotate(-90 430.797176 103.699369)">sales</text>
    </g>
   </g>
   <g id="line2d_28">
    <path d="M 66.040426 191.426069 
L 128.339628 187.039734 
L 190.638831 165.108059 
L 252.938033 130.017379 
L 315.237236 72.995025 
L 377.536438 15.97267 
" clip-path="url(#p6e1f806ce9)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#p6e1f806ce9)">
     <use xlink:href="#m4334b5412b" x="66.040426" y="191.426069" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     <use xlink:href="#m4334b5412b" x="128.339628" y="187.039734" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     <use xlink:href="#m4334b5412b" x="190.638831" y="165.108059" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     <use xlink:href="#m4334b5412b" x="252.938033" y="130.017379" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     <use xlink:href="#m4334b5412b" x="315.237236" y="72.995025" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
     <use xlink:href="#m4334b5412b" x="377.536438" y="15.97267" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
    </g>
   </g>
   <g id="patch_8">
    <path d="M 50.465625 200.198739 
L 50.465625 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 393.111239 200.198739 
L 393.111239 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 50.465625 200.198739 
L 393.111239 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 50.465625 7.2 
L 393.111239 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6e1f806ce9">
   <rect x="50.465625" y="7.2" width="342.645614" height="192.998739"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Solda sıcaklık, sağda satış ekseni; ölçek keyfi.</figcaption>
</figure>

- `ax.twinx()` aynı x eksenini paylaşan **ikinci** bir alan açar; y ekseni
  sağda. Şekilde artık iki alan var.
- Birimleri farklı iki seriyi (derece ve adet) tek grafikte gösterir. Ama iki
  eksenin ölçeği **keyfidir**: biri değiştirilince çizgiler kesişir ya da
  ayrılır ve "birlikte artıyor" izlenimi değişir. Genelde iki ayrı alan
  (`sharex=True`) daha dürüsttür.
- İki alanın açıklamaları ayrı tutulur; tek kutuda göstermek için çizgiler
  `handles=` ile toplanır. Renkleri eksen yazısıyla eşleştirmek hangi
  çizginin hangi eksene ait olduğunu belli eder.

## Sadeleştirmek: mesajı öne çıkar

```python
import matplotlib.pyplot as plt

cities = ["Bursa", "Izmir", "Ankara", "Istanbul"]
sales = [65, 95, 110, 240]
settings = {"axes.spines.top": False, "axes.spines.right": False, "font.size": 11}
with plt.rc_context(settings):
    fig, ax = plt.subplots(figsize=(6, 2.8), layout="constrained")
    bars = ax.barh(cities, sales, color="lightgray")
    bars[-1].set_color("tab:blue")
    ax.bar_label(bars, padding=3)
    ax.set_xlabel("sales")
    ax.set_title("Istanbul sells almost as much as the other three")
print(ax.spines["top"].get_visible(), plt.rcParams["axes.spines.top"])
print(sum(sales[:-1]), sales[-1])
```

```text
False True
270 240
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39581pt" height="209.99952pt" viewBox="0 0 440.39581 209.99952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 209.99952 
L 440.39581 209.99952 
L 440.39581 0 
L 0 0 
L 0 209.99952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 58.210313 169.798661 
L 425.613584 169.798661 
L 425.613584 23.229937 
L 58.210313 23.229937 
L 58.210313 169.798661 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 58.210313 163.136446 
L 152.977029 163.136446 
L 152.977029 135.085016 
L 58.210313 135.085016 
z
" clip-path="url(#pb7dc6049ae)" style="fill: #d3d3d3"/>
   </g>
   <g id="patch_4">
    <path d="M 58.210313 128.072158 
L 196.715514 128.072158 
L 196.715514 100.020728 
L 58.210313 100.020728 
z
" clip-path="url(#pb7dc6049ae)" style="fill: #d3d3d3"/>
   </g>
   <g id="patch_5">
    <path d="M 58.210313 93.00787 
L 218.584756 93.00787 
L 218.584756 64.95644 
L 58.210313 64.95644 
z
" clip-path="url(#pb7dc6049ae)" style="fill: #d3d3d3"/>
   </g>
   <g id="patch_6">
    <path d="M 58.210313 57.943582 
L 408.11819 57.943582 
L 408.11819 29.892152 
L 58.210313 29.892152 
z
" clip-path="url(#pb7dc6049ae)" style="fill: #1f77b4; stroke: #1f77b4; stroke-linejoin: miter"/>
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
       <use xlink:href="#m15aed4d867" x="58.210313" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="58.210313" y="185.156082" transform="rotate(-0 58.210313 185.156082)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="131.107787" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="131.107787" y="185.156082" transform="rotate(-0 131.107787 185.156082)">50</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="204.005262" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="204.005262" y="185.156082" transform="rotate(-0 204.005262 185.156082)">100</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="276.902736" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="276.902736" y="185.156082" transform="rotate(-0 276.902736 185.156082)">150</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="349.800211" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="349.800211" y="185.156082" transform="rotate(-0 349.800211 185.156082)">200</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="422.697685" y="169.798661" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="422.697685" y="185.156082" transform="rotate(-0 422.697685 185.156082)">250</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 11px; font-family:inherit; text-anchor: middle; fill: currentColor" x="241.911948" y="200.156942" transform="rotate(-0 241.911948 200.156942)">sales</text>
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
       <use xlink:href="#m5c8d5162d3" x="58.210313" y="149.110731" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 11px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.210313" y="153.289442" transform="rotate(-0 51.210313 153.289442)">Bursa</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.210313" y="114.046443" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 11px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.210313" y="118.225584" transform="rotate(-0 51.210313 118.225584)">Izmir</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.210313" y="78.982155" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 11px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.210313" y="83.161296" transform="rotate(-0 51.210313 83.161296)">Ankara</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="58.210313" y="43.917867" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 11px; font-family:inherit; text-anchor: end; fill: currentColor" x="51.210313" y="48.097008" transform="rotate(-0 51.210313 48.097008)">Istanbul</text>
     </g>
    </g>
   </g>
   <g id="patch_7">
    <path d="M 58.210313 169.798661 
L 58.210313 23.229937 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 58.210313 169.798661 
L 425.613584 169.798661 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_12">
    <text style="font-size: 11px; font-family:inherit; text-anchor: start; fill: currentColor" x="155.977029" y="151.968153" transform="rotate(-0 155.977029 151.968153)">65</text>
   </g>
   <g id="text_13">
    <text style="font-size: 11px; font-family:inherit; text-anchor: start; fill: currentColor" x="199.715514" y="116.903865" transform="rotate(-0 199.715514 116.903865)">95</text>
   </g>
   <g id="text_14">
    <text style="font-size: 11px; font-family:inherit; text-anchor: start; fill: currentColor" x="221.584756" y="81.839577" transform="rotate(-0 221.584756 81.839577)">110</text>
   </g>
   <g id="text_15">
    <text style="font-size: 11px; font-family:inherit; text-anchor: start; fill: currentColor" x="411.11819" y="46.775289" transform="rotate(-0 411.11819 46.775289)">240</text>
   </g>
   <g id="text_16">
    <text style="font-size: 13.2px; font-family:inherit; text-anchor: middle; fill: currentColor" x="241.911948" y="17.229937" transform="rotate(-0 241.911948 17.229937)">Istanbul sells almost as much as the other three</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pb7dc6049ae">
   <rect x="58.210313" y="23.229937" width="367.403272" height="146.568723"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Tek vurgu rengi, çubukta değer, çerçevesiz.</figcaption>
</figure>

- Üst ve sağ çerçeve çizgisi (spine) bilgi taşımaz; kaldırınca grafik
  hafifler.
- Hepsi gri, **bir tanesi** renkli: göz önce İstanbul'a gider. Başlık da
  ne görüleceğini söyler (240'a karşı diğer üçünün toplamı 270).
- `bar_label` değerleri çubuğun ucuna yazar; eksenden okutmaktan kolaydır.
- `plt.rc_context(ayarlar)` ayarları yalnızca `with` bloğunun içinde
  değiştirir: blok bitince `axes.spines.top` yeniden `True`. Bütün betik için
  `plt.rcParams[...] = ...` ya da `plt.style.use(...)`.

## Tarih ekseni

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

days = pd.date_range("2026-01-01", periods=120, freq="D")
values = range(120)
fig, ax = plt.subplots(figsize=(6, 2.8), layout="constrained")
ax.plot(days, values)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.canvas.draw()
print([t.get_text() for t in ax.get_xticklabels()])
```

```text
['Jan 2026', 'Feb 2026', 'Mar 2026', 'Apr 2026', 'May 2026']
```

- matplotlib tarihleri doğrudan çizer; ama işaretlerin **nerede** olacağını
  (`MonthLocator`: her ay başı) ve **nasıl** yazılacağını (`DateFormatter`)
  ayrı ayrı söylemek gerekir.
- `"%b %Y"` `strftime` kodlarıdır (önceki bölümdeki pandas tarihleriyle
  aynı). Ay adları bilgisayarın diline göre değil İngilizce yazılır.
- Kendiliğinden kısa yazım için `mdates.ConciseDateFormatter(locator)`.

## Özet

- Eksen yazıları: `StrMethodFormatter("{x:,.0f}")`, `PercentFormatter(xmax=1)`;
  okumadan önce `fig.canvas.draw()`.
- `annotate` ve `axhline` anlatılan yeri işaretler.
- Katlanarak büyüyen veri için `set_yscale("log")`; okuyana söyle.
- `twinx` iki birimi bir arada gösterir ama ölçek keyfidir; çoğu zaman iki
  ayrı alan daha iyi.
- Gereksiz çerçeveyi kaldır, tek vurgu rengi kullan, değeri çubuğa yaz.
  `rc_context` geçici, `rcParams` kalıcı.
