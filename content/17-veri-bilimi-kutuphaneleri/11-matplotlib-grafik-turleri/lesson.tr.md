# Matplotlib Grafik Türleri

Bir grafik bir soruyu cevaplar. "İki şey birlikte artıyor mu?" sorusunun
grafiği ile "hangi şehir önde?" sorusunun grafiği farklıdır; yanlış tür
seçilince veri doğru olsa bile cevap görünmez. Bu bölüm en sık kullanılan
türleri **hangi soruya cevap verdikleriyle** birlikte anlatıyor: dağılım,
gruplu ve yığılmış çubuk, histogram, kutu grafiği, ısı haritası ve
belirsizlik bandı. Her örneğin altında matplotlib'in gerçek çıktısı var.

## Dağılım (scatter): iki sayı arasındaki ilişki

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
area = rng.uniform(40, 160, 60)
price = area * 2.1 + rng.normal(0, 25, 60)
age = rng.integers(0, 40, 60)
fig, ax = plt.subplots(figsize=(6, 3.4), layout="constrained")
points = ax.scatter(area, price, c=age, s=30, cmap="viridis")
fig.colorbar(points, ax=ax, label="age (years)")
ax.set(xlabel="area (m2)", ylabel="price (k)")
print(len(points.get_offsets()), points.get_cmap().name)
print(round(float(np.corrcoef(area, price)[0, 1]), 2))
```

```text
60 viridis
0.94
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="439.577545pt" height="253.19952pt" viewBox="0 0 439.577545 253.19952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 253.19952 
L 439.577545 253.19952 
L 439.577545 0 
L 0 0 
L 0 253.19952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 214.99952 
L 369.592482 214.99952 
L 369.592482 7.2 
L 47.288281 7.2 
L 47.288281 214.99952 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_1">
    <defs>
     <path id="C0_0_5742b25a4b" d="M 0 2.738613 
C 0.726289 2.738613 1.422928 2.450055 1.936492 1.936492 
C 2.450055 1.422928 2.738613 0.726289 2.738613 -0 
C 2.738613 -0.726289 2.450055 -1.422928 1.936492 -1.936492 
C 1.422928 -2.450055 0.726289 -2.738613 0 -2.738613 
C -0.726289 -2.738613 -1.422928 -2.450055 -1.936492 -1.936492 
C -2.450055 -1.422928 -2.738613 -0.726289 -2.738613 0 
C -2.738613 0.726289 -2.450055 1.422928 -1.936492 1.936492 
C -1.422928 2.450055 -0.726289 2.738613 0 2.738613 
z
"/>
    </defs>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="87.308523" y="161.783623" style="fill: #a0da39; stroke: #a0da39"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="132.876638" y="170.465341" style="fill: #5ac864; stroke: #5ac864"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="303.036276" y="64.684737" style="fill: #481668; stroke: #481668"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="236.984067" y="110.977754" style="fill: #8ed645; stroke: #8ed645"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="89.86469" y="156.754743" style="fill: #fde725; stroke: #fde725"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="192.056915" y="147.798262" style="fill: #8ed645; stroke: #8ed645"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="205.900973" y="125.145056" style="fill: #3dbc74; stroke: #3dbc74"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="109.643137" y="147.970087" style="fill: #414487; stroke: #414487"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="282.930137" y="58.633654" style="fill: #1f9a8a; stroke: #1f9a8a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="95.75611" y="195.663489" style="fill: #24868e; stroke: #24868e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="179.42639" y="131.855494" style="fill: #b2dd2d; stroke: #b2dd2d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="217.26242" y="101.921748" style="fill: #365c8d; stroke: #365c8d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="191.303607" y="127.762061" style="fill: #2c718e; stroke: #2c718e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="238.381766" y="73.74021" style="fill: #414487; stroke: #414487"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="283.913067" y="91.767148" style="fill: #24868e; stroke: #24868e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="349.759395" y="38.125018" style="fill: #1f9a8a; stroke: #1f9a8a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="147.162718" y="155.175844" style="fill: #277f8e; stroke: #277f8e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="256.996109" y="67.474269" style="fill: #3a538b; stroke: #3a538b"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="271.366033" y="81.031247" style="fill: #20938c; stroke: #20938c"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="149.730977" y="144.268109" style="fill: #22a884; stroke: #22a884"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="61.938472" y="205.554087" style="fill: #481f70; stroke: #481f70"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="354.942292" y="16.645433" style="fill: #1fa187; stroke: #1fa187"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="151.443375" y="127.344827" style="fill: #4ac16d; stroke: #4ac16d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="156.141462" y="125.084935" style="fill: #460b5e; stroke: #460b5e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="330.298707" y="36.226652" style="fill: #22a884; stroke: #22a884"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="237.8887" y="91.745809" style="fill: #2a788e; stroke: #2a788e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="203.567231" y="122.322159" style="fill: #ece51b; stroke: #ece51b"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="294.596345" y="81.057226" style="fill: #306a8e; stroke: #306a8e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="70.637192" y="188.250564" style="fill: #3a538b; stroke: #3a538b"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="274.606386" y="59.559173" style="fill: #4ac16d; stroke: #4ac16d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="174.306396" y="148.081044" style="fill: #b2dd2d; stroke: #b2dd2d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="88.87715" y="176.602713" style="fill: #440154; stroke: #440154"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="260.599341" y="90.472897" style="fill: #460b5e; stroke: #460b5e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="342.282324" y="43.563355" style="fill: #481f70; stroke: #481f70"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="123.947785" y="143.044808" style="fill: #365c8d; stroke: #365c8d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="251.432179" y="108.141884" style="fill: #228d8d; stroke: #228d8d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="151.37159" y="162.917885" style="fill: #1f9a8a; stroke: #1f9a8a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="285.094431" y="74.213671" style="fill: #2c718e; stroke: #2c718e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="279.188393" y="59.606343" style="fill: #c8e020; stroke: #c8e020"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="127.421812" y="138.78105" style="fill: #32b67a; stroke: #32b67a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="311.661587" y="58.347779" style="fill: #481f70; stroke: #481f70"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="259.740844" y="90.825281" style="fill: #365c8d; stroke: #365c8d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="267.321404" y="78.459869" style="fill: #482979; stroke: #482979"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="308.703989" y="66.333305" style="fill: #482979; stroke: #482979"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="190.684085" y="107.640761" style="fill: #a0da39; stroke: #a0da39"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="290.203701" y="83.076751" style="fill: #ece51b; stroke: #ece51b"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="326.310211" y="52.5018" style="fill: #2a788e; stroke: #2a788e"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="92.33398" y="167.997436" style="fill: #443a83; stroke: #443a83"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="317.654924" y="50.788356" style="fill: #a0da39; stroke: #a0da39"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="180.240056" y="121.121626" style="fill: #481668; stroke: #481668"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="206.091681" y="75.462489" style="fill: #481668; stroke: #481668"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="105.60235" y="138.609315" style="fill: #3e4c8a; stroke: #3e4c8a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="272.03235" y="58.978107" style="fill: #33638d; stroke: #33638d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="149.507258" y="168.24026" style="fill: #365c8d; stroke: #365c8d"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="324.09723" y="60.353807" style="fill: #3e4c8a; stroke: #3e4c8a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="144.501852" y="150.154192" style="fill: #443a83; stroke: #443a83"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="230.848789" y="92.488784" style="fill: #28ae80; stroke: #28ae80"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="181.967049" y="156.132506" style="fill: #20938c; stroke: #20938c"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="246.252995" y="75.929444" style="fill: #32b67a; stroke: #32b67a"/>
    </g>
    <g clip-path="url(#p6691adc1ec)">
     <use xlink:href="#C0_0_5742b25a4b" x="120.766869" y="137.530045" style="fill: #ece51b; stroke: #ece51b"/>
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
       <use xlink:href="#m15aed4d867" x="61.489281" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="61.489281" y="229.597176" transform="rotate(-0 61.489281 229.597176)">40</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="111.731532" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="111.731532" y="229.597176" transform="rotate(-0 111.731532 229.597176)">60</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="161.973782" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="161.973782" y="229.597176" transform="rotate(-0 161.973782 229.597176)">80</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="212.216033" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="212.216033" y="229.597176" transform="rotate(-0 212.216033 229.597176)">100</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="262.458284" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="262.458284" y="229.597176" transform="rotate(-0 262.458284 229.597176)">120</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="312.700534" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="312.700534" y="229.597176" transform="rotate(-0 312.700534 229.597176)">140</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="362.942785" y="214.99952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="362.942785" y="229.597176" transform="rotate(-0 362.942785 229.597176)">160</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="208.440382" y="243.597176" transform="rotate(-0 208.440382 243.597176)">area (m2)</text>
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
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="200.642023" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="204.440851" transform="rotate(-0 40.288281 204.440851)">50</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="172.014013" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="175.812841" transform="rotate(-0 40.288281 175.812841)">100</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="143.386002" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="147.18483" transform="rotate(-0 40.288281 147.18483)">150</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="114.757992" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="118.55682" transform="rotate(-0 40.288281 118.55682)">200</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="86.129981" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="89.92881" transform="rotate(-0 40.288281 89.92881)">250</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="57.501971" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="61.300799" transform="rotate(-0 40.288281 61.300799)">300</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="28.873961" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="32.672789" transform="rotate(-0 40.288281 32.672789)">350</text>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="111.09976" transform="rotate(-90 14.798438 111.09976)">price (k)</text>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 47.288281 214.99952 
L 47.288281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 369.592482 214.99952 
L 369.592482 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 47.288281 214.99952 
L 369.592482 214.99952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 7.2 
L 369.592482 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 388.262569 214.99952 
L 398.652545 214.99952 
L 398.652545 7.2 
L 388.262569 7.2 
L 388.262569 214.99952 
z
" style="fill: none"/>
   </g>
   <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAA8AAAEhCAYAAACgB/q4AAABmElEQVR4nO2ZwY0FMQxCgaS0LWH7LyX+2hLWHJDlP/cn7ICdSMMf/haa3wXVZXEpIqKsNolk2ReeMvswpZAyUspqk3Ct4syQYKTPNxgScqbP2hdPjtwkcHouL54wYO7zuRaeds3suYI3BlI9K6bMlDIc5QreGEiNJC1lzEwYMpe7+rpI9lwLfa5Uz+rrInpgiilzXTzVRzF4qjBTmRPfnpW7YmnAtU9ZfRRfn//73fa/FyQHQ30UK6fqLixbfRTfkCy5MeTAd+Zg3J0LsNqw+rr4hmSOz7dmriEER7IcGANh9VEkD6xm+syRZauPws02clbVQmVM3CT0YKwLCRFSliGMoM8KxrMcGAN7VpvEX9lYd2B3qLIwcpNoI4yJZatNYu1pv3XLQLEDO8GQPAeuPnxSZatNwu6Zls8vZtVLKfNN3CTHm6pnKKMWKj9HuVIhwRs4GNdUfo5yxULyZoakYla9lFVIZfvkHq7IWVUT3yQnVbbaJNyyj9czUspwlOnAYKZsweuZfVhOzwcxZVrKipWtNuzeGH3+A6UrjUTnD8WtAAAAAElFTkSuQmCC" id="image0b79905fca" transform="scale(1 -1) translate(0 -208.08)" x="388.08" y="-6.48" width="10.8" height="208.08"/>
   <g id="matplotlib.axis_3"/>
   <g id="matplotlib.axis_4">
    <g id="ytick_8">
     <g id="line2d_15">
      <defs>
       <path id="m004d6dcf24" d="M 0 0 
L 3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="203.125262" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="206.92409" transform="rotate(-0 405.652545 206.92409)">5</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="173.439616" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="177.238444" transform="rotate(-0 405.652545 177.238444)">10</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="143.75397" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="147.552798" transform="rotate(-0 405.652545 147.552798)">15</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="114.068325" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="117.867153" transform="rotate(-0 405.652545 117.867153)">20</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="84.382679" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="88.181507" transform="rotate(-0 405.652545 88.181507)">25</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="54.697033" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="58.495861" transform="rotate(-0 405.652545 58.495861)">30</text>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m004d6dcf24" x="398.652545" y="25.011387" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="405.652545" y="28.810216" transform="rotate(-0 405.652545 28.810216)">35</text>
     </g>
    </g>
    <g id="text_24">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="429.975202" y="111.09976" transform="rotate(-90 429.975202 111.09976)">age (years)</text>
    </g>
   </g>
   <g id="LineCollection_1"/>
   <g id="patch_8">
    <path d="M 388.262569 214.99952 
L 393.457557 214.99952 
L 398.652545 214.99952 
L 398.652545 7.2 
L 393.457557 7.2 
L 388.262569 7.2 
L 388.262569 214.99952 
z
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6691adc1ec">
   <rect x="47.288281" y="7.2" width="322.304201" height="207.79952"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Alan ve fiyat birlikte artıyor; renk evin yaşı.</figcaption>
</figure>

- Her nokta bir ev: x alanı, y fiyatı. Noktaların sağa yukarı uzanan bir şerit
  oluşturması güçlü bir ilişki demek (korelasyon 0,94).
- `c=age` üçüncü bir değişkeni **renge** çevirir; `cmap` renk skalası,
  `fig.colorbar` skalanın açıklaması. `s=` nokta boyutu; dördüncü bir
  değişken için o da kullanılabilir ama okunması zorlaşır.
- Nokta sayısı binleri geçince noktalar üst üste biner; `alpha=0.3` ile yarı
  saydam yapmak yoğunluğu görünür kılar.

## Çubuk: kategorileri karşılaştırmak

```python
import matplotlib.pyplot as plt
import numpy as np

cities = ["Izmir", "Ankara", "Bursa"]
y2025 = np.array([80, 120, 50])
y2026 = np.array([95, 110, 65])
x = np.arange(len(cities))
fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3), layout="constrained")
left.bar(x - 0.2, y2025, width=0.4, label="2025")
left.bar(x + 0.2, y2026, width=0.4, label="2026")
left.set_xticks(x, cities)
left.legend()
left.set_title("Grouped")
right.bar(cities, y2025, label="2025")
right.bar(cities, y2026, bottom=y2025, label="2026")
right.set_title("Stacked")
print(len(left.patches), len(right.patches))
print([float(p.get_y()) for p in right.patches[3:]])
```

```text
6 6
[80.0, 120.0, 50.0]
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
    <path d="M 33.2875 200.198739 
L 271.19952 200.198739 
L 271.19952 22.318125 
L 33.2875 22.318125 
L 33.2875 200.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 44.101683 200.198739 
L 74.999348 200.198739 
L 74.999348 87.258667 
L 44.101683 87.258667 
z
" clip-path="url(#p33698f9b97)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_4">
    <path d="M 121.345845 200.198739 
L 152.24351 200.198739 
L 152.24351 30.78863 
L 121.345845 30.78863 
z
" clip-path="url(#p33698f9b97)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_5">
    <path d="M 198.590007 200.198739 
L 229.487672 200.198739 
L 229.487672 129.611194 
L 198.590007 129.611194 
z
" clip-path="url(#p33698f9b97)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_6">
    <path d="M 74.999348 200.198739 
L 105.897013 200.198739 
L 105.897013 66.082403 
L 74.999348 66.082403 
z
" clip-path="url(#p33698f9b97)" style="fill: #ff7f0e"/>
   </g>
   <g id="patch_7">
    <path d="M 152.24351 200.198739 
L 183.141175 200.198739 
L 183.141175 44.906139 
L 152.24351 44.906139 
z
" clip-path="url(#p33698f9b97)" style="fill: #ff7f0e"/>
   </g>
   <g id="patch_8">
    <path d="M 229.487672 200.198739 
L 260.385337 200.198739 
L 260.385337 108.43493 
L 229.487672 108.43493 
z
" clip-path="url(#p33698f9b97)" style="fill: #ff7f0e"/>
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
       <use xlink:href="#m15aed4d867" x="74.999348" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="74.999348" y="214.797176" transform="rotate(-0 74.999348 214.797176)">Izmir</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="152.24351" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="152.24351" y="214.797176" transform="rotate(-0 152.24351 214.797176)">Ankara</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="229.487672" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="229.487672" y="214.796395" transform="rotate(-0 229.487672 214.796395)">Bursa</text>
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
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="203.997567" transform="rotate(-0 26.2875 203.997567)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="171.963721" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="175.762549" transform="rotate(-0 26.2875 175.762549)">20</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="143.728703" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="147.527531" transform="rotate(-0 26.2875 147.527531)">40</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="115.493685" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="119.292513" transform="rotate(-0 26.2875 119.292513)">60</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="87.258667" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="91.057495" transform="rotate(-0 26.2875 91.057495)">80</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="59.023648" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="62.822477" transform="rotate(-0 26.2875 62.822477)">100</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="33.2875" y="30.78863" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="26.2875" y="34.587459" transform="rotate(-0 26.2875 34.587459)">120</text>
     </g>
    </g>
   </g>
   <g id="patch_9">
    <path d="M 33.2875 200.198739 
L 33.2875 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 271.19952 200.198739 
L 271.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 33.2875 200.198739 
L 271.19952 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_12">
    <path d="M 33.2875 22.318125 
L 271.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_11">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="152.24351" y="16.318125" transform="rotate(-0 152.24351 16.318125)">Grouped</text>
   </g>
   <g id="legend_1">
    <g id="patch_13">
     <path d="M 206.74952 60.319687 
L 264.19952 60.319687 
Q 266.19952 60.319687 266.19952 58.319687 
L 266.19952 29.318125 
Q 266.19952 27.318125 264.19952 27.318125 
L 206.74952 27.318125 
Q 204.74952 27.318125 204.74952 29.318125 
L 204.74952 58.319687 
Q 204.74952 60.319687 206.74952 60.319687 
L 206.74952 60.319687 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="patch_14">
     <path d="M 208.74952 38.916562 
L 228.74952 38.916562 
L 228.74952 31.916562 
L 208.74952 31.916562 
z
" style="fill: #1f77b4"/>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="236.74952" y="38.916562" transform="rotate(-0 236.74952 38.916562)">2025</text>
    </g>
    <g id="patch_15">
     <path d="M 208.74952 53.917344 
L 228.74952 53.917344 
L 228.74952 46.917344 
L 208.74952 46.917344 
z
" style="fill: #ff7f0e"/>
    </g>
    <g id="text_13">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="236.74952" y="53.917344" transform="rotate(-0 236.74952 53.917344)">2026</text>
    </g>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_16">
    <path d="M 303.2875 200.198739 
L 541.19952 200.198739 
L 541.19952 22.318125 
L 303.2875 22.318125 
L 303.2875 200.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_17">
    <path d="M 314.101683 200.198739 
L 375.897013 200.198739 
L 375.897013 141.273484 
L 314.101683 141.273484 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_18">
    <path d="M 391.345845 200.198739 
L 453.141175 200.198739 
L 453.141175 111.810856 
L 391.345845 111.810856 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_19">
    <path d="M 468.590007 200.198739 
L 530.385337 200.198739 
L 530.385337 163.370454 
L 468.590007 163.370454 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_20">
    <path d="M 314.101683 141.273484 
L 375.897013 141.273484 
L 375.897013 71.299743 
L 314.101683 71.299743 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #ff7f0e"/>
   </g>
   <g id="patch_21">
    <path d="M 391.345845 111.810856 
L 453.141175 111.810856 
L 453.141175 30.78863 
L 391.345845 30.78863 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #ff7f0e"/>
   </g>
   <g id="patch_22">
    <path d="M 468.590007 163.370454 
L 530.385337 163.370454 
L 530.385337 115.493685 
L 468.590007 115.493685 
z
" clip-path="url(#pca20b9b7d1)" style="fill: #ff7f0e"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="344.999348" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="344.999348" y="214.797176" transform="rotate(-0 344.999348 214.797176)">Izmir</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="422.24351" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="422.24351" y="214.797176" transform="rotate(-0 422.24351 214.797176)">Ankara</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="499.487672" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="499.487672" y="214.796395" transform="rotate(-0 499.487672 214.796395)">Bursa</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_8">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.2875" y="200.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.2875" y="203.997567" transform="rotate(-0 296.2875 203.997567)">0</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.2875" y="163.370454" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.2875" y="167.169282" transform="rotate(-0 296.2875 167.169282)">50</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.2875" y="126.54217" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.2875" y="130.340998" transform="rotate(-0 296.2875 130.340998)">100</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.2875" y="89.713885" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.2875" y="93.512714" transform="rotate(-0 296.2875 93.512714)">150</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="303.2875" y="52.885601" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="296.2875" y="56.684429" transform="rotate(-0 296.2875 56.684429)">200</text>
     </g>
    </g>
   </g>
   <g id="patch_23">
    <path d="M 303.2875 200.198739 
L 303.2875 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 541.19952 200.198739 
L 541.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 303.2875 200.198739 
L 541.19952 200.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 303.2875 22.318125 
L 541.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_22">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="422.24351" y="16.318125" transform="rotate(-0 422.24351 16.318125)">Stacked</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p33698f9b97">
   <rect x="33.2875" y="22.318125" width="237.91202" height="177.880614"/>
  </clipPath>
  <clipPath id="pca20b9b7d1">
   <rect x="303.2875" y="22.318125" width="237.91202" height="177.880614"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Solda yıllar yan yana, sağda üst üste.</figcaption>
</figure>

- **Gruplu:** her şehirde iki yıl yan yana. Çubuklar `x - 0.2` ve `x + 0.2`
  konumlarına, `0.4` genişlikte konur; etiketler `set_xticks(x, cities)` ile
  ortaya. Soru: "her şehirde hangi yıl daha iyi?"
- **Yığılmış:** ikinci seri `bottom=y2025` ile birincinin **üstüne** başlar
  (2026 çubuklarının tabanı 80, 120, 50). Soru: "toplam ne kadar, parçalar
  nasıl paylaşıyor?" Üstteki parçaların boyunu karşılaştırmak zordur, çünkü
  tabanları farklı.
- Çubuk grafiğinin ekseni **sıfırdan** başlamalı: çubuğun boyu değeri
  anlatır; kesik eksen küçük farkı büyük gösterir.

## Histogram: bir sayının dağılımı

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)
morning = rng.normal(30, 6, 400)
evening = rng.normal(42, 9, 400)
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
opts = dict(bins=20, range=(0, 80), alpha=0.6)
counts, edges, _ = ax.hist(morning, **opts, label="morning")
ax.hist(evening, **opts, label="evening")
ax.set(xlabel="minutes", ylabel="people")
ax.legend()
print(int(counts.sum()), len(edges), float(edges[1] - edges[0]))
dens, _ = np.histogram(morning, bins=20, range=(0, 80), density=True)
print(round(float((dens * 4).sum()), 6))
```

```text
400 21 4.0
1.0
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
    <path d="M 64.829701 186.198739 
L 82.371121 186.198739 
L 82.371121 186.198739 
L 64.829701 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_4">
    <path d="M 82.371121 186.198739 
L 99.912541 186.198739 
L 99.912541 186.198739 
L 82.371121 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_5">
    <path d="M 99.912541 186.198739 
L 117.453961 186.198739 
L 117.453961 184.801403 
L 99.912541 184.801403 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_6">
    <path d="M 117.453961 186.198739 
L 134.995381 186.198739 
L 134.995381 180.609395 
L 117.453961 180.609395 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_7">
    <path d="M 134.995381 186.198739 
L 152.536801 186.198739 
L 152.536801 168.033371 
L 134.995381 168.033371 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_8">
    <path d="M 152.536801 186.198739 
L 170.078221 186.198739 
L 170.078221 134.497308 
L 152.536801 134.497308 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_9">
    <path d="M 170.078221 186.198739 
L 187.619641 186.198739 
L 187.619641 77.206532 
L 170.078221 77.206532 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_10">
    <path d="M 187.619641 186.198739 
L 205.161061 186.198739 
L 205.161061 15.723749 
L 187.619641 15.723749 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_11">
    <path d="M 205.161061 186.198739 
L 222.702481 186.198739 
L 222.702481 82.795876 
L 205.161061 82.795876 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_12">
    <path d="M 222.702481 186.198739 
L 240.243901 186.198739 
L 240.243901 116.33194 
L 222.702481 116.33194 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_13">
    <path d="M 240.243901 186.198739 
L 257.785321 186.198739 
L 257.785321 162.444027 
L 240.243901 162.444027 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_14">
    <path d="M 257.785321 186.198739 
L 275.326741 186.198739 
L 275.326741 180.609395 
L 257.785321 180.609395 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_15">
    <path d="M 275.326741 186.198739 
L 292.86816 186.198739 
L 292.86816 186.198739 
L 275.326741 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_16">
    <path d="M 292.86816 186.198739 
L 310.40958 186.198739 
L 310.40958 186.198739 
L 292.86816 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_17">
    <path d="M 310.40958 186.198739 
L 327.951 186.198739 
L 327.951 186.198739 
L 310.40958 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_18">
    <path d="M 327.951 186.198739 
L 345.49242 186.198739 
L 345.49242 186.198739 
L 327.951 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_19">
    <path d="M 345.49242 186.198739 
L 363.03384 186.198739 
L 363.03384 186.198739 
L 345.49242 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_20">
    <path d="M 363.03384 186.198739 
L 380.57526 186.198739 
L 380.57526 186.198739 
L 363.03384 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_21">
    <path d="M 380.57526 186.198739 
L 398.11668 186.198739 
L 398.11668 186.198739 
L 380.57526 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_22">
    <path d="M 398.11668 186.198739 
L 415.6581 186.198739 
L 415.6581 186.198739 
L 398.11668 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #1f77b4; opacity: 0.6"/>
   </g>
   <g id="patch_23">
    <path d="M 64.829701 186.198739 
L 82.371121 186.198739 
L 82.371121 186.198739 
L 64.829701 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_24">
    <path d="M 82.371121 186.198739 
L 99.912541 186.198739 
L 99.912541 186.198739 
L 82.371121 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_25">
    <path d="M 99.912541 186.198739 
L 117.453961 186.198739 
L 117.453961 186.198739 
L 99.912541 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_26">
    <path d="M 117.453961 186.198739 
L 134.995381 186.198739 
L 134.995381 183.404067 
L 117.453961 183.404067 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_27">
    <path d="M 134.995381 186.198739 
L 152.536801 186.198739 
L 152.536801 177.814723 
L 134.995381 177.814723 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_28">
    <path d="M 152.536801 186.198739 
L 170.078221 186.198739 
L 170.078221 180.609395 
L 152.536801 180.609395 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_29">
    <path d="M 170.078221 186.198739 
L 187.619641 186.198739 
L 187.619641 173.622715 
L 170.078221 173.622715 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_30">
    <path d="M 187.619641 186.198739 
L 205.161061 186.198739 
L 205.161061 135.894644 
L 187.619641 135.894644 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_31">
    <path d="M 205.161061 186.198739 
L 222.702481 186.198739 
L 222.702481 113.537268 
L 205.161061 113.537268 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_32">
    <path d="M 222.702481 186.198739 
L 240.243901 186.198739 
L 240.243901 102.35858 
L 222.702481 102.35858 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_33">
    <path d="M 240.243901 186.198739 
L 257.785321 186.198739 
L 257.785321 95.3719 
L 240.243901 95.3719 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_34">
    <path d="M 257.785321 186.198739 
L 275.326741 186.198739 
L 275.326741 88.38522 
L 257.785321 88.38522 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_35">
    <path d="M 275.326741 186.198739 
L 292.86816 186.198739 
L 292.86816 123.31862 
L 275.326741 123.31862 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_36">
    <path d="M 292.86816 186.198739 
L 310.40958 186.198739 
L 310.40958 148.470667 
L 292.86816 148.470667 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_37">
    <path d="M 310.40958 186.198739 
L 327.951 186.198739 
L 327.951 163.841363 
L 310.40958 163.841363 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_38">
    <path d="M 327.951 186.198739 
L 345.49242 186.198739 
L 345.49242 177.814723 
L 327.951 177.814723 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_39">
    <path d="M 345.49242 186.198739 
L 363.03384 186.198739 
L 363.03384 183.404067 
L 345.49242 183.404067 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_40">
    <path d="M 363.03384 186.198739 
L 380.57526 186.198739 
L 380.57526 186.198739 
L 363.03384 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_41">
    <path d="M 380.57526 186.198739 
L 398.11668 186.198739 
L 398.11668 186.198739 
L 380.57526 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
   </g>
   <g id="patch_42">
    <path d="M 398.11668 186.198739 
L 415.6581 186.198739 
L 415.6581 186.198739 
L 398.11668 186.198739 
z
" clip-path="url(#p03129543d0)" style="fill: #ff7f0e; opacity: 0.6"/>
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
       <use xlink:href="#m15aed4d867" x="64.829701" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="64.829701" y="200.796395" transform="rotate(-0 64.829701 200.796395)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="108.683251" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="108.683251" y="200.796395" transform="rotate(-0 108.683251 200.796395)">10</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="152.536801" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="152.536801" y="200.796395" transform="rotate(-0 152.536801 200.796395)">20</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="196.390351" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="196.390351" y="200.796395" transform="rotate(-0 196.390351 200.796395)">30</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="240.243901" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="200.796395" transform="rotate(-0 240.243901 200.796395)">40</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="284.09745" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="284.09745" y="200.796395" transform="rotate(-0 284.09745 200.796395)">50</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="327.951" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="327.951" y="200.796395" transform="rotate(-0 327.951 200.796395)">60</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="371.80455" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="371.80455" y="200.796395" transform="rotate(-0 371.80455 200.796395)">70</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="415.6581" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="415.6581" y="200.796395" transform="rotate(-0 415.6581 200.796395)">80</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="214.797176" transform="rotate(-0 240.243901 214.797176)">minutes</text>
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
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="189.997567" transform="rotate(-0 40.288281 189.997567)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="158.252019" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="162.050847" transform="rotate(-0 40.288281 162.050847)">20</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="130.3053" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="134.104128" transform="rotate(-0 40.288281 134.104128)">40</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="102.35858" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="106.157408" transform="rotate(-0 40.288281 106.157408)">60</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="74.411861" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="78.210689" transform="rotate(-0 40.288281 78.210689)">80</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="46.465141" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="50.263969" transform="rotate(-0 40.288281 50.263969)">100</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="18.518421" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="22.31725" transform="rotate(-0 40.288281 22.31725)">120</text>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="96.699369" transform="rotate(-90 14.798438 96.699369)">people</text>
    </g>
   </g>
   <g id="patch_43">
    <path d="M 47.288281 186.198739 
L 47.288281 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_44">
    <path d="M 433.19952 186.198739 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_45">
    <path d="M 47.288281 186.198739 
L 433.19952 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_46">
    <path d="M 47.288281 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_47">
     <path d="M 352.602645 45.201563 
L 426.19952 45.201563 
Q 428.19952 45.201563 428.19952 43.201563 
L 428.19952 14.2 
Q 428.19952 12.2 426.19952 12.2 
L 352.602645 12.2 
Q 350.602645 12.2 350.602645 14.2 
L 350.602645 43.201563 
Q 350.602645 45.201563 352.602645 45.201563 
L 352.602645 45.201563 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="patch_48">
     <path d="M 354.602645 23.798438 
L 374.602645 23.798438 
L 374.602645 16.798438 
L 354.602645 16.798438 
z
" style="fill: #1f77b4; opacity: 0.6"/>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.602645" y="23.798438" transform="rotate(-0 382.602645 23.798438)">morning</text>
    </g>
    <g id="patch_49">
     <path d="M 354.602645 38.799219 
L 374.602645 38.799219 
L 374.602645 31.799219 
L 354.602645 31.799219 
z
" style="fill: #ff7f0e; opacity: 0.6"/>
    </g>
    <g id="text_20">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.602645" y="38.799219" transform="rotate(-0 382.602645 38.799219)">evening</text>
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
<figcaption>Aynı kutularla iki dağılım: akşam süreleri hem daha uzun hem daha yayvan.</figcaption>
</figure>

- Histogram değerleri **aralıklara** (kutulara) bölüp her aralıkta kaç tane
  olduğunu sayar. 20 kutu için 21 sınır gerekir; her kutu 4 dakika.
- İki dağılımı üst üste koyarken **aynı** `range` ve `bins` verilmeli (burada
  ikisi de `opts` sözlüğünden); yoksa
  kutular farklı genişlikte olur ve yükseklikler karşılaştırılamaz.
  `alpha` örtüşen kısmı gösterir.
- `density=True` sayı yerine yoğunluk verir: kutuların alanı toplamı 1.
  Farklı büyüklükteki grupları karşılaştırmak için.
- Kutu sayısı sonucu değiştirir: çok az kutu şekli siler, çok fazla kutu
  gürültü gösterir. Birkaç değer dene.

## Kutu grafiği: grupların dağılımını yan yana koymak

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(5)
groups = {"A": rng.normal(50, 5, 80), "B": rng.normal(55, 12, 80),
          "C": np.append(rng.normal(48, 4, 78), [80, 85])}
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
parts = ax.boxplot(list(groups.values()), tick_labels=list(groups))
ax.set_ylabel("score")
print([round(float(np.median(v)), 1) for v in groups.values()])
print([len(f.get_ydata()) for f in parts["fliers"]])
```

```text
[49.0, 53.4, 48.0]
[0, 0, 2]
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
    <path d="M 40.925 200.19952 
L 433.19952 200.19952 
L 433.19952 7.2 
L 40.925 7.2 
L 40.925 200.19952 
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
       <use xlink:href="#m15aed4d867" x="106.304087" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="106.304087" y="214.797176" transform="rotate(-0 106.304087 214.797176)">A</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="237.06226" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="237.06226" y="214.797176" transform="rotate(-0 237.06226 214.797176)">B</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="367.820433" y="200.19952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="367.820433" y="214.797176" transform="rotate(-0 367.820433 214.797176)">C</text>
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
       <use xlink:href="#m5c8d5162d3" x="40.925" y="167.68852" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="171.487349" transform="rotate(-0 33.925 171.487349)">40</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="133.973895" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="137.772723" transform="rotate(-0 33.925 137.772723)">50</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="100.259269" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="104.058097" transform="rotate(-0 33.925 104.058097)">60</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="66.544644" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="70.343472" transform="rotate(-0 33.925 70.343472)">70</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925" y="32.830018" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925" y="36.628846" transform="rotate(-0 33.925 36.628846)">80</text>
     </g>
    </g>
    <g id="text_9">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="103.69976" transform="rotate(-90 14.797656 103.69976)">score</text>
    </g>
   </g>
   <g id="line2d_9">
    <path d="M 86.690361 148.948176 
L 125.917813 148.948176 
L 125.917813 126.326094 
L 86.690361 126.326094 
L 86.690361 148.948176 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_10">
    <path d="M 106.304087 148.948176 
L 106.304087 167.651716 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_11">
    <path d="M 106.304087 126.326094 
L 106.304087 92.98142 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_12">
    <path d="M 96.497224 167.651716 
L 116.11095 167.651716 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_13">
    <path d="M 96.497224 92.98142 
L 116.11095 92.98142 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_14"/>
   <g id="line2d_15">
    <path d="M 217.448534 143.634914 
L 256.675986 143.634914 
L 256.675986 97.642743 
L 217.448534 97.642743 
L 217.448534 143.634914 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 237.06226 143.634914 
L 237.06226 191.426815 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_17">
    <path d="M 237.06226 97.642743 
L 237.06226 38.335741 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_18">
    <path d="M 227.255397 191.426815 
L 246.869123 191.426815 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_19">
    <path d="M 227.255397 38.335741 
L 246.869123 38.335741 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_20"/>
   <g id="line2d_21">
    <path d="M 348.206707 148.714822 
L 387.434159 148.714822 
L 387.434159 127.976424 
L 348.206707 127.976424 
L 348.206707 148.714822 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_22">
    <path d="M 367.820433 148.714822 
L 367.820433 173.054072 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_23">
    <path d="M 367.820433 127.976424 
L 367.820433 103.312039 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_24">
    <path d="M 358.01357 173.054072 
L 377.627296 173.054072 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_25">
    <path d="M 358.01357 103.312039 
L 377.627296 103.312039 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #000000; stroke-linecap: square"/>
   </g>
   <g id="line2d_26">
    <defs>
     <path id="m4e7f8f4885" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #000000"/>
    </defs>
    <g clip-path="url(#p560017cdf6)">
     <use xlink:href="#m4e7f8f4885" x="367.820433" y="32.830018" style="fill-opacity: 0; stroke: #000000"/>
     <use xlink:href="#m4e7f8f4885" x="367.820433" y="15.972705" style="fill-opacity: 0; stroke: #000000"/>
    </g>
   </g>
   <g id="line2d_27">
    <path d="M 86.690361 137.400799 
L 125.917813 137.400799 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #ff7f0e"/>
   </g>
   <g id="line2d_28">
    <path d="M 217.448534 122.353004 
L 256.675986 122.353004 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #ff7f0e"/>
   </g>
   <g id="line2d_29">
    <path d="M 348.206707 140.679205 
L 387.434159 140.679205 
" clip-path="url(#p560017cdf6)" style="fill: none; stroke: #ff7f0e"/>
   </g>
   <g id="patch_3">
    <path d="M 40.925 200.19952 
L 40.925 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 433.19952 200.19952 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 40.925 200.19952 
L 433.19952 200.19952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 40.925 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p560017cdf6">
   <rect x="40.925" y="7.2" width="392.27452" height="192.99952"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Medyan, çeyrekler ve C'nin iki aykırı değeri.</figcaption>
</figure>

- Kutunun ortasındaki çizgi **medyan**, kutunun alt ve üst kenarı çeyrekler
  (verinin ortadaki yarısı kutunun içinde). Bıyıklar kutudan en fazla 1,5
  kutu boyu uzanır; dışında kalanlar tek tek nokta olarak çizilir (aykırı).
- B'nin kutusu daha uzun: puanları daha **dağınık**. C'de iki aykırı değer
  (80 ve 85) ayrı nokta olarak göründü; histogramda kaybolabilirlerdi.
- Çok grubu tek bakışta karşılaştırmak için histogramdan kısadır; ama iki
  tepeli bir dağılımı gizler. İkisi birbirini tamamlar.

## Isı haritası: bir tablo, renkle

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(6)
data = rng.normal(size=(200, 4))
data[:, 1] = data[:, 0] * 0.8 + data[:, 1] * 0.6
data[:, 3] = -data[:, 2] * 0.7 + data[:, 3] * 0.7
corr = np.corrcoef(data, rowvar=False)
names = ["a", "b", "c", "d"]
fig, ax = plt.subplots(figsize=(4.2, 3.4), layout="constrained")
image = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(4), names)
ax.set_yticks(range(4), names)
for i in range(4):
    for j in range(4):
        ink = "white" if abs(corr[i, j]) > 0.5 else "black"
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", color=ink)
fig.colorbar(image, ax=ax)
print(corr.shape, round(float(corr[0, 1]), 2), round(float(corr[2, 3]), 2))
```

```text
(4, 4) 0.77 -0.68
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="306.095154pt" height="253.19952pt" viewBox="0 0 306.095154 253.19952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 253.19952 
L 306.095154 253.19952 
L 306.095154 0 
L 0 0 
L 0 253.19952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 20.548438 228.998739 
L 238.548348 228.998739 
L 238.548348 10.998828 
L 20.548438 10.998828 
L 20.548438 228.998739 
z
" style="fill: none"/>
   </g>
   <g clip-path="url(#p772b4ad87e)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAS4AAAEuCAYAAAAwQP9DAAAEcUlEQVR4nO3WPS6EURiG4flRCI0tKFUKrT3Yhd4KxApEaxcau1ColFPpRCaEjILPFkZ13Ml11ad48hZ3zvzr5XmasZVpsXSpPzi9eXSvPzi5OnevLS22fQjwXwgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkDN/ff+YRo+o2F3OR09Iudg7Gj0h5eHydvSEDD8uIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnLm94fH0+gRFXer9egJKdefT6MnpCw2b6MnZPhxATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5AjXECOcAE5wgXkCBeQI1xAjnABOcIF5AgXkCNcQI5wATnCBeQIF5Czc7daj96QcXZ4MHpCyuZ7Gj0hZf/ne/SEDD8uIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gBzhAnKEC8gRLiBHuIAc4QJyhAvIES4gR7iAHOECcoQLyBEuIEe4gFnNLy0DIRMdbsn0AAAAAElFTkSuQmCC" id="image43b906fc6d" transform="scale(1 -1) translate(0 -217.44)" x="20.88" y="-11.27952" width="217.44" height="217.44"/>
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
       <use xlink:href="#m15aed4d867" x="47.798426" y="228.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="47.798426" y="243.596395" transform="rotate(-0 47.798426 243.596395)">a</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="102.298404" y="228.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="102.298404" y="243.597176" transform="rotate(-0 102.298404 243.597176)">b</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="156.798382" y="228.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="156.798382" y="243.596395" transform="rotate(-0 156.798382 243.596395)">c</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="211.298359" y="228.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="211.298359" y="243.597176" transform="rotate(-0 211.298359 243.597176)">d</text>
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
       <use xlink:href="#m5c8d5162d3" x="20.548438" y="38.248817" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="13.548438" y="42.047645" transform="rotate(-0 13.548438 42.047645)">a</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="20.548438" y="92.748795" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="13.548438" y="96.548013" transform="rotate(-0 13.548438 96.548013)">b</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="20.548438" y="147.248772" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="13.548438" y="151.0476" transform="rotate(-0 13.548438 151.0476)">c</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="20.548438" y="201.74875" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="13.548438" y="205.547969" transform="rotate(-0 13.548438 205.547969)">d</text>
     </g>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 20.548438 228.998739 
L 20.548438 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 238.548348 228.998739 
L 238.548348 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 20.548438 228.998739 
L 238.548348 228.998739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 20.548438 10.998828 
L 238.548348 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_9">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="47.798426" y="40.846473" transform="rotate(-0 47.798426 40.846473)">1.00</text>
   </g>
   <g id="text_10">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="102.298404" y="40.846473" transform="rotate(-0 102.298404 40.846473)">0.77</text>
   </g>
   <g id="text_11">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="156.798382" y="40.846473" transform="rotate(-0 156.798382 40.846473)">-0.04</text>
   </g>
   <g id="text_12">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="211.298359" y="40.846473" transform="rotate(-0 211.298359 40.846473)">0.07</text>
   </g>
   <g id="text_13">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="47.798426" y="95.346451" transform="rotate(-0 47.798426 95.346451)">0.77</text>
   </g>
   <g id="text_14">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="102.298404" y="95.346451" transform="rotate(-0 102.298404 95.346451)">1.00</text>
   </g>
   <g id="text_15">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="156.798382" y="95.346451" transform="rotate(-0 156.798382 95.346451)">-0.01</text>
   </g>
   <g id="text_16">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="211.298359" y="95.346451" transform="rotate(-0 211.298359 95.346451)">0.06</text>
   </g>
   <g id="text_17">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="47.798426" y="149.846429" transform="rotate(-0 47.798426 149.846429)">-0.04</text>
   </g>
   <g id="text_18">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="102.298404" y="149.846429" transform="rotate(-0 102.298404 149.846429)">-0.01</text>
   </g>
   <g id="text_19">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="156.798382" y="149.846429" transform="rotate(-0 156.798382 149.846429)">1.00</text>
   </g>
   <g id="text_20">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="211.298359" y="149.846429" transform="rotate(-0 211.298359 149.846429)">-0.68</text>
   </g>
   <g id="text_21">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="47.798426" y="204.346406" transform="rotate(-0 47.798426 204.346406)">0.07</text>
   </g>
   <g id="text_22">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle" x="102.298404" y="204.346406" transform="rotate(-0 102.298404 204.346406)">0.06</text>
   </g>
   <g id="text_23">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="156.798382" y="204.346406" transform="rotate(-0 156.798382 204.346406)">-0.68</text>
   </g>
   <g id="text_24">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: #ffffff" x="211.298359" y="204.346406" transform="rotate(-0 211.298359 204.346406)">1.00</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 250.349846 228.998739 
L 261.249842 228.998739 
L 261.249842 10.998828 
L 250.349846 10.998828 
L 250.349846 228.998739 
z
" style="fill: none"/>
   </g>
   <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAA8AAAEuCAYAAABRUUhtAAABt0lEQVR4nO2a0XEEMQhDhUz6SUvpvwZDJiUEPjQa3/6/ASTA672Lr++fxvDJ4MFjMMck/iKfRdq0FCyDtLSKMsGOo88ck3Du7WMIc0zCtj1zBZMhW0OxgCM0NWfIYIanVdRZhQUcKrX5XnumLG0KrQpVb9NT7fBc+scS5piEtOZ8Um1u4LCEw9SqeK2301Tt84FtrArVi+uZsxBevs97gqXu/nxWNYdqh1Hnc1ieGAzPkSRU9+fwXPqE6jtJyKyCKO1cTVWEqGbO40IqGFaRQ2YVLL9KxSoyFpGxihyyEwOy3oZlk8DycI9VzT3+5w8SXZvIJVIbm7RhKVguay5Lq8pU7XZUOyzbM113WH12mM0aunO4SxUZq7TvtRyMWll1RWl36dS+qpqvqrehmmeOSdjWnLK0OSaxb89y3GEt6+2+q01SC7hkke8CLtn53J6C9SbtWkTmmISvYK0bjDK16r5mFcckliOZSsFaVnPLrGpPtdtyMKot2/M6ps0xieVI5oNTxTGJ/RtgLyJflVWlSptjEn9pb36juzsYhpE5R/GkYClLm/O4MFa7nxuMkkW+H6v+9ZgK9gt8K03uVf23zQAAAABJRU5ErkJggg==" id="imagec0335f3bc6" transform="scale(1 -1) translate(0 -217.44)" x="250.56" y="-10.8" width="10.8" height="217.44"/>
   <g id="matplotlib.axis_3"/>
   <g id="matplotlib.axis_4">
    <g id="ytick_5">
     <g id="line2d_9">
      <defs>
       <path id="m004d6dcf24" d="M 0 0 
L 3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="228.998739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_25">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="232.797567" transform="rotate(-0 268.249842 232.797567)">−1.00</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="201.74875" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_26">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="205.547578" transform="rotate(-0 268.249842 205.547578)">−0.75</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="174.498761" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_27">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="178.297589" transform="rotate(-0 268.249842 178.297589)">−0.50</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="147.248772" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_28">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="151.0476" transform="rotate(-0 268.249842 151.0476)">−0.25</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="119.998783" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_29">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="123.797612" transform="rotate(-0 268.249842 123.797612)">0.00</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="92.748795" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_30">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="96.547623" transform="rotate(-0 268.249842 96.547623)">0.25</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="65.498806" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_31">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="69.297634" transform="rotate(-0 268.249842 69.297634)">0.50</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="38.248817" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_32">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="42.047645" transform="rotate(-0 268.249842 42.047645)">0.75</text>
     </g>
    </g>
    <g id="ytick_13">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m004d6dcf24" x="261.249842" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_33">
      <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="268.249842" y="14.797656" transform="rotate(-0 268.249842 14.797656)">1.00</text>
     </g>
    </g>
   </g>
   <g id="LineCollection_1"/>
   <g id="patch_8">
    <path d="M 250.349846 228.998739 
L 255.799844 228.998739 
L 261.249842 228.998739 
L 261.249842 10.998828 
L 255.799844 10.998828 
L 250.349846 10.998828 
L 250.349846 228.998739 
z
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p772b4ad87e">
   <rect x="20.548438" y="10.998828" width="217.999911" height="217.999911"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Korelasyon matrisi: kırmızı pozitif, mavi negatif, beyaz sıfır.</figcaption>
</figure>

- `imshow` bir matrisi hücre hücre renge çevirir. Korelasyon matrisi en sık
  örnek: a ile b güçlü pozitif (0,77, kırmızı), c ile d güçlü negatif
  (−0,68, mavi).
- **İki yönlü** bir değerde (−1…+1) ortası beyaz, iki ucu farklı renk olan
  bir skala (`RdBu_r`) ve simetrik sınır (`vmin=-1, vmax=1`) seçilir;
  yoksa sıfır ortada durmaz ve renkler yanıltır.
- Hücre sayısı azsa değeri `ax.text` ile yazmak renk tahmin ettirmekten iyidir. Yazının rengi hücreye göre seçilir (`ink`): koyu hücrede beyaz, açıkta siyah.

## Belirsizlik bandı

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
days = np.arange(1, 31)
runs = 100 + days * 2 + rng.normal(0, 8, (50, 30))
mean = runs.mean(axis=0)
std = runs.std(axis=0)
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
ax.plot(days, mean, label="mean")
ax.fill_between(days, mean - std, mean + std, alpha=0.3, label="mean ± 1 std")
ax.set(xlabel="day", ylabel="visitors")
ax.legend()
print(runs.shape, round(float(mean[0]), 1), round(float(std.mean()), 1))
```

```text
(50, 30) 101.6 7.7
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="224.399418pt" viewBox="0 0 440.39952 224.399418" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.399418 
L 440.39952 224.399418 
L 440.39952 0 
L 0 0 
L 0 224.399418 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 186.198637 
L 433.19952 186.198637 
L 433.19952 10.420439 
L 47.288281 10.420439 
L 47.288281 186.198637 
z
" style="fill: none"/>
   </g>
   <g id="FillBetweenPolyCollection_1">
    <path d="M 64.829701 147.622362 
L 64.829701 178.208719 
L 76.927232 175.598988 
L 89.024763 173.788572 
L 101.122294 168.538072 
L 113.219825 165.75895 
L 125.317356 158.408286 
L 137.414887 150.282001 
L 149.512418 152.366801 
L 161.609949 147.44979 
L 173.70748 141.141353 
L 185.805011 133.291581 
L 197.902542 130.570559 
L 210.000073 129.163763 
L 222.097604 124.790555 
L 234.195135 110.850169 
L 246.292666 122.356308 
L 258.390197 106.294187 
L 270.487728 99.756386 
L 282.585259 97.792132 
L 294.68279 97.741777 
L 306.780321 90.303752 
L 318.877852 84.405294 
L 330.975383 79.1011 
L 343.072914 79.769044 
L 355.170445 68.619212 
L 367.267976 70.330391 
L 379.365507 61.663856 
L 391.463038 65.070665 
L 403.560569 49.703742 
L 415.6581 56.327734 
L 415.6581 23.378797 
L 415.6581 23.378797 
L 403.560569 18.410357 
L 391.463038 30.012239 
L 379.365507 25.856334 
L 367.267976 38.387901 
L 355.170445 37.39513 
L 343.072914 46.762668 
L 330.975383 48.508016 
L 318.877852 51.448308 
L 306.780321 61.185012 
L 294.68279 61.748993 
L 282.585259 63.182104 
L 270.487728 69.205023 
L 258.390197 71.078119 
L 246.292666 78.550836 
L 234.195135 80.036504 
L 222.097604 91.439566 
L 210.000073 93.388149 
L 197.902542 94.708584 
L 185.805011 103.303155 
L 173.70748 109.025427 
L 161.609949 109.982666 
L 149.512418 115.043092 
L 137.414887 114.651703 
L 125.317356 119.503643 
L 113.219825 127.895054 
L 101.122294 134.664566 
L 89.024763 138.64963 
L 76.927232 138.301953 
L 64.829701 147.622362 
z
" clip-path="url(#p0388ef0430)" style="fill: #1f77b4; fill-opacity: 0.3"/>
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
       <use xlink:href="#m15aed4d867" x="52.73217" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="52.73217" y="200.796293" transform="rotate(-0 52.73217 200.796293)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="113.219825" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.219825" y="200.796293" transform="rotate(-0 113.219825 200.796293)">5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="173.70748" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="173.70748" y="200.796293" transform="rotate(-0 173.70748 200.796293)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="234.195135" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="234.195135" y="200.796293" transform="rotate(-0 234.195135 200.796293)">15</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="294.68279" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="294.68279" y="200.796293" transform="rotate(-0 294.68279 200.796293)">20</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="355.170445" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="355.170445" y="200.796293" transform="rotate(-0 355.170445 200.796293)">25</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="415.6581" y="186.198637" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="415.6581" y="200.796293" transform="rotate(-0 415.6581 200.796293)">30</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="240.243901" y="214.797074" transform="rotate(-0 240.243901 214.797074)">day</text>
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
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="166.357643" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="170.156471" transform="rotate(-0 40.288281 170.156471)">100</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="144.163527" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="147.962355" transform="rotate(-0 40.288281 147.962355)">110</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="121.96941" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="125.768238" transform="rotate(-0 40.288281 125.768238)">120</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="99.775294" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="103.574122" transform="rotate(-0 40.288281 103.574122)">130</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="77.581177" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="81.380006" transform="rotate(-0 40.288281 81.380006)">140</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="55.387061" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="59.185889" transform="rotate(-0 40.288281 59.185889)">150</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="33.192945" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="36.991773" transform="rotate(-0 40.288281 36.991773)">160</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="14.797656" transform="rotate(-0 40.288281 14.797656)">170</text>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="98.309538" transform="rotate(-90 14.798438 98.309538)">visitors</text>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 64.829701 162.91554 
L 76.927232 156.95047 
L 89.024763 156.219101 
L 101.122294 151.601319 
L 113.219825 146.827002 
L 125.317356 138.955965 
L 137.414887 132.466852 
L 149.512418 133.704947 
L 161.609949 128.716228 
L 173.70748 125.08339 
L 185.805011 118.297368 
L 197.902542 112.639571 
L 210.000073 111.275956 
L 222.097604 108.11506 
L 234.195135 95.443337 
L 246.292666 100.453572 
L 258.390197 88.686153 
L 270.487728 84.480705 
L 282.585259 80.487118 
L 294.68279 79.745385 
L 306.780321 75.744382 
L 318.877852 67.926801 
L 330.975383 63.804558 
L 343.072914 63.265856 
L 355.170445 53.007171 
L 367.267976 54.359146 
L 379.365507 43.760095 
L 391.463038 47.541452 
L 403.560569 34.057049 
L 415.6581 39.853266 
" clip-path="url(#p0388ef0430)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 47.288281 186.198637 
L 47.288281 10.420439 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 433.19952 186.198637 
L 433.19952 10.420439 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 47.288281 186.198637 
L 433.19952 186.198637 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 10.420439 
L 433.19952 10.420439 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 54.288281 48.422001 
L 154.402344 48.422001 
Q 156.402344 48.422001 156.402344 46.422001 
L 156.402344 17.420439 
Q 156.402344 15.420439 154.402344 15.420439 
L 54.288281 15.420439 
Q 52.288281 15.420439 52.288281 17.420439 
L 52.288281 46.422001 
Q 52.288281 48.422001 54.288281 48.422001 
L 54.288281 48.422001 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_17">
     <path d="M 56.288281 23.518876 
L 66.288281 23.518876 
L 76.288281 23.518876 
" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="84.288281" y="27.018876" transform="rotate(-0 84.288281 27.018876)">mean</text>
    </g>
    <g id="patch_8">
     <path d="M 56.288281 42.019657 
L 76.288281 42.019657 
L 76.288281 35.019657 
L 56.288281 35.019657 
z
" style="fill: #1f77b4; fill-opacity: 0.3"/>
    </g>
    <g id="text_19">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="84.288281" y="42.019657" transform="rotate(-0 84.288281 42.019657)">mean ± 1 std</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p0388ef0430">
   <rect x="47.288281" y="10.420439" width="385.911239" height="175.778198"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Ortalama çizgi, ± 1 standart sapma bant.</figcaption>
</figure>

- 50 tekrarlı bir ölçümün ortalaması çizgi, ± 1 standart sapma bant.
  `fill_between(x, alt, üst)` iki eğri arasını boyar.
- Tek bir çizgi "değer tam bu" der; bant "değer bu aralıkta oynuyor" der.
  Tahmin ve ölçüm grafiklerinde bandı göstermek dürüstlüktür.

## Hangi soru, hangi grafik?

| Soru | Grafik | matplotlib |
|---|---|---|
| Zamanla nasıl değişiyor? | çizgi | `ax.plot` |
| İki sayı birlikte mi değişiyor? | dağılım | `ax.scatter` |
| Hangi kategori önde? | çubuk (sıralı) | `ax.bar`, `ax.barh` |
| Bir sayı nasıl dağılmış? | histogram | `ax.hist` |
| Grupların dağılımı nasıl farklı? | kutu | `ax.boxplot` |
| Bir tablonun deseni ne? | ısı haritası | `ax.imshow` |
| Tahmin ne kadar kesin? | çizgi + bant | `ax.fill_between` |

## Özet

- Önce soruyu belirle, sonra grafiği seç.
- Dağılımda üçüncü değişken renge (`c=`, `colorbar`); çok noktada `alpha`.
- Gruplu çubuk karşılaştırır, yığılmış çubuk toplamı gösterir; çubuk ekseni
  sıfırdan başlar.
- Histogramlar aynı `bins` ve `range` ile karşılaştırılır; kutu grafiği
  medyanı, yayılımı ve aykırıları gösterir.
- İki yönlü değerde ortası nötr renk skalası ve simetrik sınır.
