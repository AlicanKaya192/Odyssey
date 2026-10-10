When you meet a new data set, the first question is "which columns are
related?" `pairplot` shows every pair of numeric columns in one figure: the
distribution of each column on the diagonal, pairwise scatter plots in the
other cells.

```python
import numpy as np
import pandas as pd
import seaborn as sns

rng = np.random.default_rng(15)
n = 150
size = rng.uniform(40, 160, n)
rooms = np.clip((size / 35 + rng.normal(0, 0.6, n)).round(), 1, 6)
age = rng.uniform(0, 40, n)
price = (size * 2.2 - age * 1.5 + rng.normal(0, 20, n)).round(1)
homes = pd.DataFrame({"size": size.round(1), "rooms": rooms,
                      "age": age.round(1), "price": price,
                      "garden": rng.random(n) < 0.4})
grid = sns.pairplot(homes, hue="garden", height=1.5, corner=True)
print(grid.axes.shape)
print(homes.drop(columns="garden").corr().round(2)["price"].to_dict())
```

```text
(4, 4)
{'size': 0.95, 'rooms': 0.8, 'age': -0.32, 'price': 1.0}
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="492.506262pt" height="427.438437pt" viewBox="0 0 492.506262 427.438437" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 427.438437 
L 492.506262 427.438437 
L 492.506262 0 
L 0 0 
L 0 427.438437 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 47.288281 96.182318 
L 130.547934 96.182318 
L 130.547934 7.2 
L 47.288281 7.2 
L 47.288281 96.182318 
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
       <use xlink:href="#m15aed4d867" x="52.479366" y="96.182318" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="124.706803" y="96.182318" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 47.288281 96.182318 
L 130.547934 96.182318 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_4">
    <path d="M 47.288281 193.867431 
L 130.547934 193.867431 
L 130.547934 104.885113 
L 47.288281 104.885113 
L 47.288281 193.867431 
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
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.935353" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="102.280184" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.839819" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="68.874994" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.698864" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="73.244754" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="98.090992" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.875933" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.715171" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="109.214018" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.799521" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="103.50805" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="90.97659" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="107.733355" y="108.929763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="67.719355" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="105.458191" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="83.826074" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.964467" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="90.073747" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="107.87781" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.261999" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="106.288807" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.184649" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="108.852881" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.041133" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.871749" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="82.598207" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="92.385025" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="77.686741" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="101.594023" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.120106" y="189.82278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.068624" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="70.175088" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="77.614514" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="82.453752" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="74.364279" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.192333" y="189.82278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="75.664373" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="68.658312" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.767592" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.220763" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="85.017826" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="105.891556" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="70.789021" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="93.974029" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="82.020388" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="68.044378" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.438384" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="85.198395" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="109.214018" y="108.929763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.474498" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="104.591462" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.446068" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.623137" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="103.941415" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="84.837258" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="104.699803" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="106.505489" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="82.273184" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="98.343788" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="102.171843" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.152975" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.751285" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="75.628259" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.120106" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="83.464936" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="70.030633" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.971467" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="69.380586" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.076308" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.189088" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="84.403893" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.061624" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="84.620575" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.264561" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="75.664373" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.228447" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="80.214702" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.751285" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="79.203518" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="94.624075" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="104.08587" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="67.972151" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.076308" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="93.649005" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="87.509673" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="95.563032" y="108.929763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="75.808828" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="107.444446" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="110.080747" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="102.858003" y="108.929763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="92.24057" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="103.038572" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.068624" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="104.447007" y="108.929763" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="88.556971" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="79.167404" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.084931" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="88.412516" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.02551" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.104738" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="98.596585" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="78.372902" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="74.003142" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="92.132229" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.823512" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="98.343788" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.174404" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="67.755469" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="76.061624" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="104.483121" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.068624" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="101.160659" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="99.174404" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="92.673935" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="80.936976" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="79.311859" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="93.829574" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="93.685119" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="106.722171" y="108.929763" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="94.046256" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.482182" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="67.647127" y="189.82278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="95.526918" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="105.024826" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="94.696303" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="89.459814" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="81.587023" y="169.599526" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="109.972406" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="79.636882" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="100.763408" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="88.340288" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.482182" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="68.008265" y="189.82278" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="101.774592" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.354034" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="107.588901" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="108.383402" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="106.036011" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="96.61033" y="149.376272" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="74.617075" y="189.82278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="75.556032" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="83.284368" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="74.508734" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="107.986151" y="129.153018" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="86.101238" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="97.549287" y="149.376272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="73.930915" y="189.82278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="91.771092" y="129.153018" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6b281bf15b)">
     <use xlink:href="#C0_0_ca53a4b268" x="71.041817" y="169.599526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="52.479366" y="193.867431" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="124.706803" y="193.867431" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_3">
    <g id="ytick_1">
     <g id="line2d_5">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="169.599526" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="173.398354" transform="rotate(-0 40.288281 173.398354)">2</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="129.153018" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="132.951846" transform="rotate(-0 40.288281 132.951846)">4</text>
     </g>
    </g>
    <g id="text_3">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="27.523438" y="149.376272" transform="rotate(-90 27.523438 149.376272)">rooms</text>
    </g>
   </g>
   <g id="line2d_7"/>
   <g id="line2d_8"/>
   <g id="patch_5">
    <path d="M 47.288281 193.867431 
L 47.288281 104.885113 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 47.288281 193.867431 
L 130.547934 193.867431 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_7">
    <path d="M 143.322832 193.867431 
L 226.582485 193.867431 
L 226.582485 104.885113 
L 143.322832 104.885113 
L 143.322832 193.867431 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_4">
    <g id="xtick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="151.996367" y="193.867431" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="206.92352" y="193.867431" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="patch_8">
    <path d="M 143.322832 193.867431 
L 226.582485 193.867431 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_4">
   <g id="patch_9">
    <path d="M 47.288281 291.552544 
L 130.547934 291.552544 
L 130.547934 202.570225 
L 47.288281 202.570225 
L 47.288281 291.552544 
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
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.935353" y="223.323257" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="102.280184" y="237.79027" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.839819" y="266.113014" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="68.874994" y="240.031639" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.698864" y="242.884289" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="73.244754" y="275.486009" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="98.090992" y="222.915736" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.875933" y="247.774547" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.715171" y="286.69285" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="109.214018" y="244.106854" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.799521" y="270.799512" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="103.50805" y="274.670966" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="90.97659" y="211.505134" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="107.733355" y="272.022076" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="67.719355" y="279.153702" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="105.458191" y="254.702412" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="83.826074" y="277.727377" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="76.964467" y="261.834039" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="90.073747" y="273.24464" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="107.87781" y="225.972147" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.261999" y="255.924977" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="106.288807" y="272.022076" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="87.184649" y="280.172506" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="108.852881" y="231.066166" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.041133" y="206.614876" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.871749" y="241.050442" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="82.598207" y="271.003272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="92.385025" y="237.994031" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="77.686741" y="209.467527" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="101.594023" y="274.467205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.120106" y="253.072326" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.068624" y="266.316775" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="70.175088" y="275.689769" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="77.614514" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="82.453752" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="74.364279" y="286.896611" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.192333" y="214.765306" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="75.664373" y="220.063085" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="68.658312" y="249.812155" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.767592" y="239.216596" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="87.220763" y="243.08805" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="85.017826" y="252.053523" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="105.891556" y="274.263444" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="70.789021" y="217.006674" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="93.974029" y="241.865485" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="82.020388" y="285.266525" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="68.044378" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.438384" y="236.363945" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="85.198395" y="255.924977" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="109.214018" y="237.58651" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.474498" y="266.520536" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="104.591462" y="265.297971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.446068" y="280.783788" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.623137" y="220.470607" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="103.941415" y="279.561224" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="84.837258" y="229.639841" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="104.699803" y="278.134898" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="106.505489" y="269.576947" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="82.273184" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="98.343788" y="267.131818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="102.171843" y="287.507893" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="110.152975" y="284.859003" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.751285" y="233.103773" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="75.628259" y="240.642921" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.120106" y="270.39199" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="83.464936" y="236.975227" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="70.030633" y="216.802913" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.971467" y="241.457964" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="69.380586" y="237.994031" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="87.076308" y="237.79027" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="110.189088" y="241.661725" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="84.403893" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="76.061624" y="223.93454" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="84.620575" y="229.43608" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.264561" y="226.583429" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="75.664373" y="210.078809" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.228447" y="214.765306" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="80.214702" y="249.812155" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.751285" y="254.906173" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="79.203518" y="211.708895" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="94.624075" y="246.144461" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="104.08587" y="241.661725" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="67.972151" y="256.128738" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="87.076308" y="224.342061" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="93.649005" y="249.608394" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="87.509673" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="95.563032" y="279.357463" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="75.808828" y="266.724297" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="107.444446" y="206.614876" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="110.080747" y="267.53934" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="102.858003" y="261.222756" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="92.24057" y="214.154024" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="103.038572" y="253.072326" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.068624" y="266.113014" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="104.447007" y="239.420356" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="88.556971" y="254.09113" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="79.167404" y="285.674046" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.084931" y="277.116095" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="88.412516" y="247.774547" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="76.02551" y="236.363945" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.104738" y="237.994031" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="98.596585" y="228.213515" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="78.372902" y="242.273007" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="74.003142" y="282.413874" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="92.132229" y="270.799512" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.823512" y="226.583429" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="98.343788" y="259.59267" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="99.174404" y="213.542742" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="67.755469" y="239.216596" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="76.061624" y="258.166345" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="104.483121" y="267.131818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.068624" y="244.310614" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="101.160659" y="280.376267" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="99.174404" y="276.912334" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="92.673935" y="248.793351" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="80.936976" y="258.981388" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="79.311859" y="273.855923" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="93.829574" y="260.000192" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="93.685119" y="279.764984" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="106.722171" y="231.066166" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="94.046256" y="240.031639" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.482182" y="221.489411" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="67.647127" y="232.28873" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="95.526918" y="252.664805" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="105.024826" y="216.191631" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="94.696303" y="226.379669" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="89.459814" y="249.200872" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="81.587023" y="241.050442" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="109.972406" y="229.232319" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="79.636882" y="224.749583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="100.763408" y="272.633358" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="88.340288" y="238.401553" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.482182" y="274.467205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="68.008265" y="210.078809" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="101.774592" y="213.950263" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.354034" y="230.251123" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="107.588901" y="285.674046" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="108.383402" y="222.100693" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="106.036011" y="273.855923" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="96.61033" y="251.23848" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="74.617075" y="253.887369" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="75.556032" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="83.284368" y="238.605313" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="74.508734" y="220.878128" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="107.986151" y="275.689769" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="86.101238" y="208.856244" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="97.549287" y="216.395392" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="73.930915" y="232.900013" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="91.771092" y="277.319855" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p6772a0ed96)">
     <use xlink:href="#C1_0_ca53a4b268" x="71.041817" y="236.160184" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_5">
    <g id="xtick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="52.479366" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="124.706803" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_6">
    <g id="ytick_3">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="287.915414" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="291.714242" transform="rotate(-0 40.288281 291.714242)">0</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="247.163265" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="250.962093" transform="rotate(-0 40.288281 250.962093)">20</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="206.411115" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="210.209943" transform="rotate(-0 40.288281 210.209943)">40</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="21.160938" y="247.061384" transform="rotate(-90 21.160938 247.061384)">age</text>
    </g>
   </g>
   <g id="line2d_16"/>
   <g id="line2d_17"/>
   <g id="patch_10">
    <path d="M 47.288281 291.552544 
L 47.288281 202.570225 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 47.288281 291.552544 
L 130.547934 291.552544 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_5">
   <g id="patch_12">
    <path d="M 143.322832 291.552544 
L 226.582485 291.552544 
L 226.582485 202.570225 
L 143.322832 202.570225 
L 143.322832 291.552544 
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
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="223.323257" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="237.79027" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="266.113014" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="240.031639" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="242.884289" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="275.486009" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="222.915736" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="247.774547" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="286.69285" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="244.106854" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="270.799512" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="274.670966" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="211.505134" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="272.022076" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="279.153702" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="254.702412" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="277.727377" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="261.834039" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="273.24464" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="225.972147" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="255.924977" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="272.022076" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="280.172506" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="231.066166" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="206.614876" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="241.050442" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="271.003272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="237.994031" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="209.467527" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="274.467205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="253.072326" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="266.316775" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="275.689769" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="286.896611" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="214.765306" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="220.063085" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="249.812155" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="239.216596" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="243.08805" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="252.053523" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="274.263444" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="217.006674" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="241.865485" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="285.266525" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="236.363945" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="255.924977" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="237.58651" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="266.520536" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="265.297971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="280.783788" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="220.470607" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="279.561224" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="229.639841" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="278.134898" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="269.576947" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="267.131818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="287.507893" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="284.859003" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="233.103773" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="240.642921" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="270.39199" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="236.975227" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="216.802913" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="241.457964" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="237.994031" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="237.79027" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="241.661725" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="235.956424" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="223.93454" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="229.43608" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="226.583429" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="210.078809" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="214.765306" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="249.812155" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="254.906173" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="211.708895" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="246.144461" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="241.661725" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="256.128738" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="224.342061" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="249.608394" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="279.357463" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="266.724297" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="206.614876" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="267.53934" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="261.222756" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="214.154024" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="253.072326" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="266.113014" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="239.420356" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="254.09113" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="285.674046" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="277.116095" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="247.774547" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="236.363945" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="237.994031" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="228.213515" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="242.273007" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="282.413874" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="270.799512" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="226.583429" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="259.59267" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="213.542742" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="239.216596" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="258.166345" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="267.131818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="244.310614" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="280.376267" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="276.912334" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="248.793351" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="258.981388" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="273.855923" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="260.000192" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="279.764984" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="206.92352" y="231.066166" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="240.031639" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="221.489411" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="232.28873" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="252.664805" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="216.191631" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="226.379669" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="249.200872" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="241.050442" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="229.232319" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="224.749583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="272.633358" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="238.401553" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="274.467205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="210.078809" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="213.950263" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="230.251123" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="285.674046" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="222.100693" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="273.855923" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="251.23848" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="253.887369" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="283.636439" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="238.605313" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="220.878128" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="275.689769" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="208.856244" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="184.952659" y="216.395392" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="162.981798" y="232.900013" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="195.938089" y="277.319855" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p357400d104)">
     <use xlink:href="#C2_0_ca53a4b268" x="173.967228" y="236.160184" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_7">
    <g id="xtick_9">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m15aed4d867" x="151.996367" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_19">
      <g>
       <use xlink:href="#m15aed4d867" x="206.92352" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_8">
    <g id="ytick_6">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="287.915414" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="247.163265" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="206.411115" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="line2d_23"/>
   <g id="line2d_24"/>
   <g id="patch_13">
    <path d="M 143.322832 291.552544 
L 143.322832 202.570225 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_14">
    <path d="M 143.322832 291.552544 
L 226.582485 291.552544 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_6">
   <g id="patch_15">
    <path d="M 239.357383 291.552544 
L 322.617036 291.552544 
L 322.617036 202.570225 
L 239.357383 202.570225 
L 239.357383 291.552544 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_9">
    <g id="xtick_11">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m15aed4d867" x="258.669324" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m15aed4d867" x="314.072834" y="291.552544" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="patch_16">
    <path d="M 239.357383 291.552544 
L 322.617036 291.552544 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_7">
   <g id="patch_17">
    <path d="M 47.288281 389.237656 
L 130.547934 389.237656 
L 130.547934 300.255338 
L 47.288281 300.255338 
L 47.288281 389.237656 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_4">
    <defs>
     <path id="C3_0_ca53a4b268" d="M 0 3 
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
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.935353" y="334.140634" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="102.280184" y="324.591628" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.839819" y="350.080512" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="68.874994" y="372.038254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.698864" y="328.794185" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="73.244754" y="361.494559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="98.090992" y="327.525958" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.875933" y="352.393163" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.715171" y="341.774866" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="109.214018" y="316.38545" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.799521" y="317.00713" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="103.50805" y="320.239867" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="90.97659" y="342.147874" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="107.733355" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="67.719355" y="358.808901" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="105.458191" y="319.59332" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="83.826074" y="337.622043" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="76.964467" y="349.433965" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="90.073747" y="330.286218" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="107.87781" y="318.6981" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.261999" y="349.135559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="106.288807" y="309.323164" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="87.184649" y="338.193989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="108.852881" y="309.173961" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.041133" y="331.827984" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.871749" y="322.651986" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="82.598207" y="340.730444" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="92.385025" y="337.796113" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="77.686741" y="366.567469" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="101.594023" y="315.664301" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.120106" y="358.609964" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.068624" y="337.945317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="70.175088" y="366.542602" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="77.614514" y="360.848012" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="82.453752" y="358.535362" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="74.364279" y="364.901366" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.192333" y="360.798278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="75.664373" y="369.203393" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="68.658312" y="367.935165" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.767592" y="350.876263" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="87.220763" y="336.677089" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="85.017826" y="343.043094" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="105.891556" y="305.642818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="70.789021" y="367.114548" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="93.974029" y="335.881339" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="82.020388" y="338.840536" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="68.044378" y="359.878191" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.438384" y="334.314705" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="85.198395" y="350.130247" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="109.214018" y="311.13847" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.474498" y="311.31254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="104.591462" y="315.490231" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.446068" y="337.249035" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.623137" y="364.627827" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="103.941415" y="310.665993" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="84.837258" y="349.284762" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="104.699803" y="314.595011" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="106.505489" y="308.800953" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="82.273184" y="346.226096" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="98.343788" y="317.429873" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="102.171843" y="320.438805" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="110.152975" y="304.299989" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.751285" y="341.376991" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="75.628259" y="365.498179" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.120106" y="357.441205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="83.464936" y="352.616967" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="70.030633" y="366.144727" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.971467" y="328.620115" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="69.380586" y="365.348976" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="87.076308" y="350.130247" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="110.189088" y="310.864931" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="84.403893" y="346.599104" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="76.061624" y="363.608272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="84.620575" y="353.48732" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.264561" y="372.087989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="75.664373" y="365.324109" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.228447" y="359.53005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="80.214702" y="351.497943" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.751285" y="351.398474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="79.203518" y="369.427198" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="94.624075" y="335.682401" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="104.08587" y="324.342956" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="67.972151" y="366.119859" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="87.076308" y="353.611656" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="93.649005" y="335.284526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="87.509673" y="342.222476" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="95.563032" y="333.891962" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="75.808828" y="352.5921" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="107.444446" y="319.817124" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="110.080747" y="308.975023" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="102.858003" y="317.504474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="92.24057" y="353.03971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="103.038572" y="311.039001" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.068624" y="332.101524" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="104.447007" y="328.644982" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="88.556971" y="345.82822" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="79.167404" y="347.941933" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.084931" y="332.474532" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="88.412516" y="338.691333" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="76.02551" y="359.405714" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.104738" y="331.902586" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="98.596585" y="325.039237" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="78.372902" y="367.214016" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="74.003142" y="355.128555" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="92.132229" y="329.838608" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.823512" y="346.524502" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="98.343788" y="325.561449" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="99.174404" y="334.563377" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="67.755469" y="377.807446" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="76.061624" y="367.189149" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="104.483121" y="316.609255" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.068624" y="325.710652" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="101.160659" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="99.174404" y="322.726587" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="92.673935" y="338.044785" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="80.936976" y="353.785726" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="79.311859" y="351.721748" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="93.829574" y="331.554445" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="93.685119" y="325.785254" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="106.722171" y="310.218383" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="94.046256" y="344.908134" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.482182" y="347.469456" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="67.647127" y="378.677798" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="95.526918" y="330.659226" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="105.024826" y="320.687477" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="94.696303" y="327.650294" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="89.459814" y="344.783798" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="81.587023" y="350.403786" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="109.972406" y="313.102979" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="79.636882" y="359.157042" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="100.763408" y="317.156334" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="88.340288" y="339.536818" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.482182" y="331.753383" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="68.008265" y="385.193005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="101.774592" y="325.536581" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.354034" y="345.853088" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="107.588901" y="313.650058" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="108.383402" y="314.246871" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="106.036011" y="310.864931" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="96.61033" y="329.689405" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="74.617075" y="361.320489" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="75.556032" y="346.27583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="83.284368" y="359.629519" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="74.508734" y="367.039946" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="107.986151" y="316.410317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="86.101238" y="352.517499" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="97.549287" y="329.316397" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="73.930915" y="375.569397" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="91.771092" y="325.785254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p81824977ec)">
     <use xlink:href="#C3_0_ca53a4b268" x="71.041817" y="368.059501" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_10">
    <g id="xtick_13">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m15aed4d867" x="52.479366" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="52.479366" y="403.835312" transform="rotate(-0 52.479366 403.835312)">0</text>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m15aed4d867" x="124.706803" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="124.706803" y="403.835312" transform="rotate(-0 124.706803 403.835312)">200</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="88.918108" y="417.836094" transform="rotate(-0 88.918108 417.836094)">size</text>
    </g>
   </g>
   <g id="matplotlib.axis_11">
    <g id="ytick_9">
     <g id="line2d_29">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="389.047422" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="392.84625" transform="rotate(-0 40.288281 392.84625)">0</text>
     </g>
    </g>
    <g id="ytick_10">
     <g id="line2d_30">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="364.180217" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="367.979046" transform="rotate(-0 40.288281 367.979046)">100</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_31">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="339.313013" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="343.111841" transform="rotate(-0 40.288281 343.111841)">200</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_32">
      <g>
       <use xlink:href="#m5c8d5162d3" x="47.288281" y="314.445808" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="40.288281" y="318.244636" transform="rotate(-0 40.288281 318.244636)">300</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="344.746497" transform="rotate(-90 14.798438 344.746497)">price</text>
    </g>
   </g>
   <g id="line2d_33"/>
   <g id="line2d_34"/>
   <g id="patch_18">
    <path d="M 47.288281 389.237656 
L 47.288281 300.255338 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_19">
    <path d="M 47.288281 389.237656 
L 130.547934 389.237656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_8">
   <g id="patch_20">
    <path d="M 143.322832 389.237656 
L 226.582485 389.237656 
L 226.582485 300.255338 
L 143.322832 300.255338 
L 143.322832 389.237656 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_5">
    <defs>
     <path id="C4_0_ca53a4b268" d="M 0 3 
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
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="334.140634" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="324.591628" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="350.080512" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="372.038254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="328.794185" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="361.494559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="327.525958" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="352.393163" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="341.774866" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="316.38545" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="317.00713" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="320.239867" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="342.147874" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="358.808901" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="319.59332" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="337.622043" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="349.433965" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="330.286218" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="318.6981" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="349.135559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="309.323164" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="338.193989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="309.173961" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="331.827984" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="322.651986" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="340.730444" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="337.796113" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="366.567469" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="315.664301" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="358.609964" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="337.945317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="366.542602" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="360.848012" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="358.535362" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="364.901366" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="360.798278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="369.203393" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="367.935165" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="350.876263" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="336.677089" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="343.043094" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="305.642818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="367.114548" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="335.881339" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="338.840536" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="359.878191" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="334.314705" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="350.130247" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="311.13847" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="311.31254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="315.490231" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="337.249035" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="364.627827" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="310.665993" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="349.284762" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="314.595011" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="308.800953" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="346.226096" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="317.429873" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="320.438805" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="304.299989" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="341.376991" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="365.498179" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="357.441205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="352.616967" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="366.144727" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="328.620115" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="365.348976" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="350.130247" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="310.864931" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="346.599104" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="363.608272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="353.48732" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="372.087989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="365.324109" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="359.53005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="351.497943" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="351.398474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="369.427198" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="335.682401" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="324.342956" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="366.119859" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="353.611656" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="335.284526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="342.222476" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="333.891962" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="352.5921" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="319.817124" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="308.975023" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="317.504474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="353.03971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="311.039001" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="332.101524" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="328.644982" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="345.82822" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="347.941933" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="332.474532" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="338.691333" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="359.405714" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="331.902586" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="325.039237" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="367.214016" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="355.128555" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="329.838608" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="346.524502" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="325.561449" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="334.563377" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="377.807446" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="367.189149" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="316.609255" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="325.710652" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="322.726587" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="338.044785" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="353.785726" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="351.721748" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="331.554445" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="325.785254" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="206.92352" y="310.218383" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="344.908134" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="347.469456" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="378.677798" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="330.659226" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="320.687477" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="327.650294" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="344.783798" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="350.403786" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="313.102979" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="359.157042" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="317.156334" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="339.536818" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="331.753383" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="385.193005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="325.536581" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="345.853088" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="313.650058" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="314.246871" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="310.864931" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="329.689405" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="361.320489" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="346.27583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="359.629519" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="367.039946" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="316.410317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="352.517499" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="184.952659" y="329.316397" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="162.981798" y="375.569397" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="195.938089" y="325.785254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#p8e9919d5b5)">
     <use xlink:href="#C4_0_ca53a4b268" x="173.967228" y="368.059501" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_12">
    <g id="xtick_15">
     <g id="line2d_35">
      <g>
       <use xlink:href="#m15aed4d867" x="151.996367" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="151.996367" y="403.835312" transform="rotate(-0 151.996367 403.835312)">0</text>
     </g>
    </g>
    <g id="xtick_16">
     <g id="line2d_36">
      <g>
       <use xlink:href="#m15aed4d867" x="206.92352" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="206.92352" y="403.835312" transform="rotate(-0 206.92352 403.835312)">5</text>
     </g>
    </g>
    <g id="text_18">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="184.952659" y="417.835312" transform="rotate(-0 184.952659 417.835312)">rooms</text>
    </g>
   </g>
   <g id="matplotlib.axis_13">
    <g id="ytick_13">
     <g id="line2d_37">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="389.047422" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_38">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="364.180217" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_15">
     <g id="line2d_39">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="339.313013" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_16">
     <g id="line2d_40">
      <g>
       <use xlink:href="#m5c8d5162d3" x="143.322832" y="314.445808" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="line2d_41"/>
   <g id="line2d_42"/>
   <g id="patch_21">
    <path d="M 143.322832 389.237656 
L 143.322832 300.255338 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_22">
    <path d="M 143.322832 389.237656 
L 226.582485 389.237656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_9">
   <g id="patch_23">
    <path d="M 239.357383 389.237656 
L 322.617036 389.237656 
L 322.617036 300.255338 
L 239.357383 300.255338 
L 239.357383 389.237656 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_6">
    <defs>
     <path id="C5_0_ca53a4b268" d="M 0 3 
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
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="293.79515" y="334.140634" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.927851" y="324.591628" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.525675" y="350.080512" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="284.708974" y="372.038254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.157676" y="328.794185" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.428553" y="361.494559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="294.016764" y="327.525958" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="280.498307" y="352.393163" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="259.334166" y="341.774866" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="282.492834" y="316.38545" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="267.977114" y="317.00713" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.871781" y="320.239867" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="300.221957" y="342.147874" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="267.312272" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="263.434026" y="358.808901" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="276.730869" y="319.59332" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="264.209675" y="337.622043" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="272.852623" y="349.433965" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="266.64743" y="330.286218" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="292.354658" y="318.6981" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="276.066026" y="349.135559" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="267.312272" y="309.323164" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="262.879991" y="338.193989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="289.584483" y="309.173961" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="302.881325" y="331.827984" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="284.154939" y="322.651986" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="267.866307" y="340.730444" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.817044" y="337.796113" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="301.330027" y="366.567469" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.982588" y="315.664301" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="277.617325" y="358.609964" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.414868" y="337.945317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.317746" y="366.542602" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.925114" y="360.848012" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.925114" y="358.535362" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="259.223359" y="364.901366" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="298.449045" y="360.798278" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="295.568062" y="369.203393" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="279.390237" y="367.935165" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.152202" y="350.876263" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.046869" y="336.677089" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="278.17136" y="343.043094" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="266.093395" y="305.642818" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="297.230167" y="367.114548" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.711711" y="335.881339" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.109816" y="338.840536" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.996272" y="359.878191" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.7035" y="334.314705" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="276.066026" y="350.130247" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.038658" y="311.13847" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.304061" y="311.31254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.968904" y="315.490231" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="262.54757" y="337.249035" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="295.346448" y="364.627827" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="263.212412" y="310.665993" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="290.360132" y="349.284762" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="263.988061" y="314.595011" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="268.641956" y="308.800953" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.996272" y="346.226096" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="269.97164" y="317.429873" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="258.890938" y="320.438805" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.33143" y="304.299989" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="288.476413" y="341.376991" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="284.376553" y="365.498179" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="268.198728" y="357.441205" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.371079" y="352.616967" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="297.340974" y="366.144727" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.933325" y="328.620115" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.817044" y="365.348976" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.927851" y="350.130247" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.822518" y="310.864931" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.925114" y="346.599104" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="293.462729" y="363.608272" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="290.470939" y="353.48732" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="292.022237" y="372.087989" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="300.997606" y="365.324109" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="298.449045" y="359.53005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="279.390237" y="351.497943" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="276.620062" y="351.398474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="300.11115" y="369.427198" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="281.384763" y="335.682401" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.822518" y="324.342956" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="275.955219" y="366.119859" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="293.241115" y="353.611656" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="279.501044" y="335.284526" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.996272" y="342.222476" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="263.323219" y="333.891962" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.193254" y="352.5921" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="302.881325" y="319.817124" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="269.750026" y="308.975023" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="273.185044" y="317.504474" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="298.781466" y="353.03971" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="277.617325" y="311.039001" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="270.525675" y="332.101524" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.041395" y="328.644982" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="277.06329" y="345.82822" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="259.888202" y="347.941933" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="264.542096" y="332.474532" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="280.498307" y="338.691333" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.7035" y="359.405714" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.817044" y="331.902586" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="291.135781" y="325.039237" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="283.490097" y="367.214016" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="261.661114" y="355.128555" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="267.977114" y="329.838608" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="292.022237" y="346.524502" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="274.0715" y="325.561449" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="299.113887" y="334.563377" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.152202" y="377.807446" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="274.847149" y="367.189149" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="269.97164" y="316.609255" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="282.382027" y="325.710652" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="262.769184" y="309.546969" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="264.652903" y="322.726587" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="279.944272" y="338.044785" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="274.403921" y="353.785726" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="266.315009" y="351.721748" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="273.849886" y="331.554445" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="263.101605" y="325.785254" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="289.584483" y="310.218383" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="284.708974" y="344.908134" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="294.792413" y="347.469456" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="288.919641" y="378.677798" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="277.838939" y="330.659226" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="297.673395" y="320.687477" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="292.133044" y="327.650294" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="279.722658" y="344.783798" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="284.154939" y="350.403786" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="290.581746" y="313.102979" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="293.019501" y="359.157042" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="266.979851" y="317.156334" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.59543" y="339.536818" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.982588" y="331.753383" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="300.997606" y="385.193005" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="298.892273" y="325.536581" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="290.027711" y="345.853088" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="259.888202" y="313.650058" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="294.459992" y="314.246871" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="266.315009" y="310.864931" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="278.614588" y="329.689405" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="277.174097" y="361.320489" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="260.996272" y="346.27583" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="285.484623" y="359.629519" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="295.124834" y="367.039946" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="265.317746" y="316.410317" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="301.662448" y="352.517499" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="297.562588" y="329.316397" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="288.58722" y="375.569397" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="264.431289" y="325.785254" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
    <g clip-path="url(#pd97e1f90e5)">
     <use xlink:href="#C5_0_ca53a4b268" x="286.814307" y="368.059501" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="matplotlib.axis_14">
    <g id="xtick_17">
     <g id="line2d_43">
      <g>
       <use xlink:href="#m15aed4d867" x="258.669324" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_19">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="258.669324" y="403.835312" transform="rotate(-0 258.669324 403.835312)">0</text>
     </g>
    </g>
    <g id="xtick_18">
     <g id="line2d_44">
      <g>
       <use xlink:href="#m15aed4d867" x="314.072834" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="314.072834" y="403.835312" transform="rotate(-0 314.072834 403.835312)">50</text>
     </g>
    </g>
    <g id="text_21">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="280.98721" y="417.835312" transform="rotate(-0 280.98721 417.835312)">age</text>
    </g>
   </g>
   <g id="matplotlib.axis_15">
    <g id="ytick_17">
     <g id="line2d_45">
      <g>
       <use xlink:href="#m5c8d5162d3" x="239.357383" y="389.047422" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_18">
     <g id="line2d_46">
      <g>
       <use xlink:href="#m5c8d5162d3" x="239.357383" y="364.180217" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_19">
     <g id="line2d_47">
      <g>
       <use xlink:href="#m5c8d5162d3" x="239.357383" y="339.313013" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
    <g id="ytick_20">
     <g id="line2d_48">
      <g>
       <use xlink:href="#m5c8d5162d3" x="239.357383" y="314.445808" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
    </g>
   </g>
   <g id="line2d_49"/>
   <g id="line2d_50"/>
   <g id="patch_24">
    <path d="M 239.357383 389.237656 
L 239.357383 300.255338 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 239.357383 389.237656 
L 322.617036 389.237656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_10">
   <g id="patch_26">
    <path d="M 335.391934 389.237656 
L 418.651587 389.237656 
L 418.651587 300.255338 
L 335.391934 300.255338 
L 335.391934 389.237656 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_16">
    <g id="xtick_19">
     <g id="line2d_51">
      <g>
       <use xlink:href="#m15aed4d867" x="350.352176" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.352176" y="403.835312" transform="rotate(-0 350.352176 403.835312)">0</text>
     </g>
    </g>
    <g id="xtick_20">
     <g id="line2d_52">
      <g>
       <use xlink:href="#m15aed4d867" x="386.366166" y="389.237656" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="386.366166" y="403.835312" transform="rotate(-0 386.366166 403.835312)">250</text>
     </g>
    </g>
    <g id="text_24">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="377.021761" y="417.836094" transform="rotate(-0 377.021761 417.836094)">price</text>
    </g>
   </g>
   <g id="patch_27">
    <path d="M 335.391934 389.237656 
L 418.651587 389.237656 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
  <g id="axes_11">
   <g id="FillBetweenPolyCollection_1">
    <defs>
     <path id="m64c99cd6ec" d="M 51.072811 -331.348895 
L 51.072811 -331.256119 
L 51.453166 -331.256119 
L 51.83352 -331.256119 
L 52.213875 -331.256119 
L 52.59423 -331.256119 
L 52.974585 -331.256119 
L 53.354939 -331.256119 
L 53.735294 -331.256119 
L 54.115649 -331.256119 
L 54.496004 -331.256119 
L 54.876358 -331.256119 
L 55.256713 -331.256119 
L 55.637068 -331.256119 
L 56.017423 -331.256119 
L 56.397777 -331.256119 
L 56.778132 -331.256119 
L 57.158487 -331.256119 
L 57.538842 -331.256119 
L 57.919196 -331.256119 
L 58.299551 -331.256119 
L 58.679906 -331.256119 
L 59.060261 -331.256119 
L 59.440615 -331.256119 
L 59.82097 -331.256119 
L 60.201325 -331.256119 
L 60.58168 -331.256119 
L 60.962034 -331.256119 
L 61.342389 -331.256119 
L 61.722744 -331.256119 
L 62.103098 -331.256119 
L 62.483453 -331.256119 
L 62.863808 -331.256119 
L 63.244163 -331.256119 
L 63.624517 -331.256119 
L 64.004872 -331.256119 
L 64.385227 -331.256119 
L 64.765582 -331.256119 
L 65.145936 -331.256119 
L 65.526291 -331.256119 
L 65.906646 -331.256119 
L 66.287001 -331.256119 
L 66.667355 -331.256119 
L 67.04771 -331.256119 
L 67.428065 -331.256119 
L 67.80842 -331.256119 
L 68.188774 -331.256119 
L 68.569129 -331.256119 
L 68.949484 -331.256119 
L 69.329839 -331.256119 
L 69.710193 -331.256119 
L 70.090548 -331.256119 
L 70.470903 -331.256119 
L 70.851258 -331.256119 
L 71.231612 -331.256119 
L 71.611967 -331.256119 
L 71.992322 -331.256119 
L 72.372677 -331.256119 
L 72.753031 -331.256119 
L 73.133386 -331.256119 
L 73.513741 -331.256119 
L 73.894096 -331.256119 
L 74.27445 -331.256119 
L 74.654805 -331.256119 
L 75.03516 -331.256119 
L 75.415514 -331.256119 
L 75.795869 -331.256119 
L 76.176224 -331.256119 
L 76.556579 -331.256119 
L 76.936933 -331.256119 
L 77.317288 -331.256119 
L 77.697643 -331.256119 
L 78.077998 -331.256119 
L 78.458352 -331.256119 
L 78.838707 -331.256119 
L 79.219062 -331.256119 
L 79.599417 -331.256119 
L 79.979771 -331.256119 
L 80.360126 -331.256119 
L 80.740481 -331.256119 
L 81.120836 -331.256119 
L 81.50119 -331.256119 
L 81.881545 -331.256119 
L 82.2619 -331.256119 
L 82.642255 -331.256119 
L 83.022609 -331.256119 
L 83.402964 -331.256119 
L 83.783319 -331.256119 
L 84.163674 -331.256119 
L 84.544028 -331.256119 
L 84.924383 -331.256119 
L 85.304738 -331.256119 
L 85.685093 -331.256119 
L 86.065447 -331.256119 
L 86.445802 -331.256119 
L 86.826157 -331.256119 
L 87.206512 -331.256119 
L 87.586866 -331.256119 
L 87.967221 -331.256119 
L 88.347576 -331.256119 
L 88.72793 -331.256119 
L 89.108285 -331.256119 
L 89.48864 -331.256119 
L 89.868995 -331.256119 
L 90.249349 -331.256119 
L 90.629704 -331.256119 
L 91.010059 -331.256119 
L 91.390414 -331.256119 
L 91.770768 -331.256119 
L 92.151123 -331.256119 
L 92.531478 -331.256119 
L 92.911833 -331.256119 
L 93.292187 -331.256119 
L 93.672542 -331.256119 
L 94.052897 -331.256119 
L 94.433252 -331.256119 
L 94.813606 -331.256119 
L 95.193961 -331.256119 
L 95.574316 -331.256119 
L 95.954671 -331.256119 
L 96.335025 -331.256119 
L 96.71538 -331.256119 
L 97.095735 -331.256119 
L 97.47609 -331.256119 
L 97.856444 -331.256119 
L 98.236799 -331.256119 
L 98.617154 -331.256119 
L 98.997509 -331.256119 
L 99.377863 -331.256119 
L 99.758218 -331.256119 
L 100.138573 -331.256119 
L 100.518928 -331.256119 
L 100.899282 -331.256119 
L 101.279637 -331.256119 
L 101.659992 -331.256119 
L 102.040347 -331.256119 
L 102.420701 -331.256119 
L 102.801056 -331.256119 
L 103.181411 -331.256119 
L 103.561765 -331.256119 
L 103.94212 -331.256119 
L 104.322475 -331.256119 
L 104.70283 -331.256119 
L 105.083184 -331.256119 
L 105.463539 -331.256119 
L 105.843894 -331.256119 
L 106.224249 -331.256119 
L 106.604603 -331.256119 
L 106.984958 -331.256119 
L 107.365313 -331.256119 
L 107.745668 -331.256119 
L 108.126022 -331.256119 
L 108.506377 -331.256119 
L 108.886732 -331.256119 
L 109.267087 -331.256119 
L 109.647441 -331.256119 
L 110.027796 -331.256119 
L 110.408151 -331.256119 
L 110.788506 -331.256119 
L 111.16886 -331.256119 
L 111.549215 -331.256119 
L 111.92957 -331.256119 
L 112.309925 -331.256119 
L 112.690279 -331.256119 
L 113.070634 -331.256119 
L 113.450989 -331.256119 
L 113.831344 -331.256119 
L 114.211698 -331.256119 
L 114.592053 -331.256119 
L 114.972408 -331.256119 
L 115.352763 -331.256119 
L 115.733117 -331.256119 
L 116.113472 -331.256119 
L 116.493827 -331.256119 
L 116.874181 -331.256119 
L 117.254536 -331.256119 
L 117.634891 -331.256119 
L 118.015246 -331.256119 
L 118.3956 -331.256119 
L 118.775955 -331.256119 
L 119.15631 -331.256119 
L 119.536665 -331.256119 
L 119.917019 -331.256119 
L 120.297374 -331.256119 
L 120.677729 -331.256119 
L 121.058084 -331.256119 
L 121.438438 -331.256119 
L 121.818793 -331.256119 
L 122.199148 -331.256119 
L 122.579503 -331.256119 
L 122.959857 -331.256119 
L 123.340212 -331.256119 
L 123.720567 -331.256119 
L 124.100922 -331.256119 
L 124.481276 -331.256119 
L 124.861631 -331.256119 
L 125.241986 -331.256119 
L 125.622341 -331.256119 
L 126.002695 -331.256119 
L 126.38305 -331.256119 
L 126.763405 -331.256119 
L 126.763405 -331.392674 
L 126.763405 -331.392674 
L 126.38305 -331.425468 
L 126.002695 -331.465206 
L 125.622341 -331.513129 
L 125.241986 -331.570644 
L 124.861631 -331.639341 
L 124.481276 -331.720998 
L 124.100922 -331.817594 
L 123.720567 -331.931315 
L 123.340212 -332.064553 
L 122.959857 -332.219908 
L 122.579503 -332.400183 
L 122.199148 -332.608372 
L 121.818793 -332.847642 
L 121.438438 -333.121318 
L 121.058084 -333.432847 
L 120.677729 -333.785766 
L 120.297374 -334.183662 
L 119.917019 -334.630122 
L 119.536665 -335.12868 
L 119.15631 -335.682759 
L 118.775955 -336.295605 
L 118.3956 -336.970225 
L 118.015246 -337.709312 
L 117.634891 -338.515183 
L 117.254536 -339.389705 
L 116.874181 -340.334234 
L 116.493827 -341.349556 
L 116.113472 -342.435829 
L 115.733117 -343.592544 
L 115.352763 -344.818487 
L 114.972408 -346.111719 
L 114.592053 -347.469563 
L 114.211698 -348.888607 
L 113.831344 -350.364724 
L 113.450989 -351.893103 
L 113.070634 -353.468289 
L 112.690279 -355.084246 
L 112.309925 -356.734424 
L 111.92957 -358.411837 
L 111.549215 -360.109151 
L 111.16886 -361.818777 
L 110.788506 -363.532968 
L 110.408151 -365.243918 
L 110.027796 -366.943856 
L 109.647441 -368.625142 
L 109.267087 -370.280358 
L 108.886732 -371.902384 
L 108.506377 -373.484473 
L 108.126022 -375.020315 
L 107.745668 -376.504087 
L 107.365313 -377.930496 
L 106.984958 -379.294809 
L 106.604603 -380.59287 
L 106.224249 -381.821116 
L 105.843894 -382.976573 
L 105.463539 -384.056851 
L 105.083184 -385.060135 
L 104.70283 -385.985159 
L 104.322475 -386.831192 
L 103.94212 -387.598008 
L 103.561765 -388.285858 
L 103.181411 -388.895447 
L 102.801056 -389.427898 
L 102.420701 -389.884726 
L 102.040347 -390.267807 
L 101.659992 -390.579347 
L 101.279637 -390.82185 
L 100.899282 -390.998084 
L 100.518928 -391.111051 
L 100.138573 -391.163947 
L 99.758218 -391.160128 
L 99.377863 -391.103067 
L 98.997509 -390.996318 
L 98.617154 -390.843472 
L 98.236799 -390.648112 
L 97.856444 -390.413776 
L 97.47609 -390.143913 
L 97.095735 -389.841845 
L 96.71538 -389.510736 
L 96.335025 -389.153557 
L 95.954671 -388.773065 
L 95.574316 -388.37179 
L 95.193961 -387.952023 
L 94.813606 -387.515816 
L 94.433252 -387.064997 
L 94.052897 -386.60118 
L 93.672542 -386.125798 
L 93.292187 -385.640135 
L 92.911833 -385.145363 
L 92.531478 -384.642589 
L 92.151123 -384.132903 
L 91.770768 -383.617419 
L 91.390414 -383.097331 
L 91.010059 -382.573943 
L 90.629704 -382.048715 
L 90.249349 -381.523284 
L 89.868995 -380.999489 
L 89.48864 -380.47937 
L 89.108285 -379.96517 
L 88.72793 -379.459313 
L 88.347576 -378.96438 
L 87.967221 -378.483059 
L 87.586866 -378.018098 
L 87.206512 -377.57224 
L 86.826157 -377.148153 
L 86.445802 -376.748351 
L 86.065447 -376.37512 
L 85.685093 -376.030434 
L 85.304738 -375.715881 
L 84.924383 -375.432589 
L 84.544028 -375.181165 
L 84.163674 -374.961641 
L 83.783319 -374.773435 
L 83.402964 -374.615323 
L 83.022609 -374.485434 
L 82.642255 -374.381254 
L 82.2619 -374.299653 
L 81.881545 -374.236922 
L 81.50119 -374.188835 
L 81.120836 -374.150717 
L 80.740481 -374.117525 
L 80.360126 -374.083948 
L 79.979771 -374.044502 
L 79.599417 -373.993636 
L 79.219062 -373.92584 
L 78.838707 -373.835745 
L 78.458352 -373.718229 
L 78.077998 -373.5685 
L 77.697643 -373.382184 
L 77.317288 -373.15539 
L 76.936933 -372.884767 
L 76.556579 -372.567544 
L 76.176224 -372.201555 
L 75.795869 -371.785249 
L 75.415514 -371.317686 
L 75.03516 -370.798516 
L 74.654805 -370.227953 
L 74.27445 -369.606736 
L 73.894096 -368.936077 
L 73.513741 -368.217613 
L 73.133386 -367.453351 
L 72.753031 -366.64561 
L 72.372677 -365.79697 
L 71.992322 -364.910218 
L 71.611967 -363.988307 
L 71.231612 -363.034313 
L 70.851258 -362.051402 
L 70.470903 -361.042807 
L 70.090548 -360.011807 
L 69.710193 -358.961711 
L 69.329839 -357.895853 
L 68.949484 -356.817586 
L 68.569129 -355.730279 
L 68.188774 -354.637316 
L 67.80842 -353.542093 
L 67.428065 -352.448017 
L 67.04771 -351.358499 
L 66.667355 -350.276941 
L 66.287001 -349.206727 
L 65.906646 -348.151201 
L 65.526291 -347.113643 
L 65.145936 -346.097248 
L 64.765582 -345.10509 
L 64.385227 -344.140093 
L 64.004872 -343.205 
L 63.624517 -342.302335 
L 63.244163 -341.434376 
L 62.863808 -340.603124 
L 62.483453 -339.810281 
L 62.103098 -339.057224 
L 61.722744 -338.344998 
L 61.342389 -337.674303 
L 60.962034 -337.045491 
L 60.58168 -336.458576 
L 60.201325 -335.913242 
L 59.82097 -335.408858 
L 59.440615 -334.944506 
L 59.060261 -334.519 
L 58.679906 -334.130926 
L 58.299551 -333.778668 
L 57.919196 -333.460446 
L 57.538842 -333.174349 
L 57.158487 -332.918376 
L 56.778132 -332.690464 
L 56.397777 -332.488522 
L 56.017423 -332.310466 
L 55.637068 -332.154236 
L 55.256713 -332.017831 
L 54.876358 -331.899319 
L 54.496004 -331.796859 
L 54.115649 -331.708715 
L 53.735294 -331.633259 
L 53.354939 -331.568984 
L 52.974585 -331.514504 
L 52.59423 -331.468555 
L 52.213875 -331.429991 
L 51.83352 -331.397786 
L 51.453166 -331.371024 
L 51.072811 -331.348895 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#pc960d48d48)">
     <use xlink:href="#m64c99cd6ec" x="0" y="427.438437" style="fill: #ff7f0e; fill-opacity: 0.25; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="FillBetweenPolyCollection_2">
    <defs>
     <path id="mb8e56ce29b" d="M 53.125038 -331.391369 
L 53.125038 -331.256119 
L 53.484041 -331.256119 
L 53.843044 -331.256119 
L 54.202048 -331.256119 
L 54.561051 -331.256119 
L 54.920055 -331.256119 
L 55.279058 -331.256119 
L 55.638062 -331.256119 
L 55.997065 -331.256119 
L 56.356069 -331.256119 
L 56.715072 -331.256119 
L 57.074075 -331.256119 
L 57.433079 -331.256119 
L 57.792082 -331.256119 
L 58.151086 -331.256119 
L 58.510089 -331.256119 
L 58.869093 -331.256119 
L 59.228096 -331.256119 
L 59.5871 -331.256119 
L 59.946103 -331.256119 
L 60.305106 -331.256119 
L 60.66411 -331.256119 
L 61.023113 -331.256119 
L 61.382117 -331.256119 
L 61.74112 -331.256119 
L 62.100124 -331.256119 
L 62.459127 -331.256119 
L 62.818131 -331.256119 
L 63.177134 -331.256119 
L 63.536137 -331.256119 
L 63.895141 -331.256119 
L 64.254144 -331.256119 
L 64.613148 -331.256119 
L 64.972151 -331.256119 
L 65.331155 -331.256119 
L 65.690158 -331.256119 
L 66.049162 -331.256119 
L 66.408165 -331.256119 
L 66.767168 -331.256119 
L 67.126172 -331.256119 
L 67.485175 -331.256119 
L 67.844179 -331.256119 
L 68.203182 -331.256119 
L 68.562186 -331.256119 
L 68.921189 -331.256119 
L 69.280193 -331.256119 
L 69.639196 -331.256119 
L 69.998199 -331.256119 
L 70.357203 -331.256119 
L 70.716206 -331.256119 
L 71.07521 -331.256119 
L 71.434213 -331.256119 
L 71.793217 -331.256119 
L 72.15222 -331.256119 
L 72.511224 -331.256119 
L 72.870227 -331.256119 
L 73.229231 -331.256119 
L 73.588234 -331.256119 
L 73.947237 -331.256119 
L 74.306241 -331.256119 
L 74.665244 -331.256119 
L 75.024248 -331.256119 
L 75.383251 -331.256119 
L 75.742255 -331.256119 
L 76.101258 -331.256119 
L 76.460262 -331.256119 
L 76.819265 -331.256119 
L 77.178268 -331.256119 
L 77.537272 -331.256119 
L 77.896275 -331.256119 
L 78.255279 -331.256119 
L 78.614282 -331.256119 
L 78.973286 -331.256119 
L 79.332289 -331.256119 
L 79.691293 -331.256119 
L 80.050296 -331.256119 
L 80.409299 -331.256119 
L 80.768303 -331.256119 
L 81.127306 -331.256119 
L 81.48631 -331.256119 
L 81.845313 -331.256119 
L 82.204317 -331.256119 
L 82.56332 -331.256119 
L 82.922324 -331.256119 
L 83.281327 -331.256119 
L 83.64033 -331.256119 
L 83.999334 -331.256119 
L 84.358337 -331.256119 
L 84.717341 -331.256119 
L 85.076344 -331.256119 
L 85.435348 -331.256119 
L 85.794351 -331.256119 
L 86.153355 -331.256119 
L 86.512358 -331.256119 
L 86.871361 -331.256119 
L 87.230365 -331.256119 
L 87.589368 -331.256119 
L 87.948372 -331.256119 
L 88.307375 -331.256119 
L 88.666379 -331.256119 
L 89.025382 -331.256119 
L 89.384386 -331.256119 
L 89.743389 -331.256119 
L 90.102392 -331.256119 
L 90.461396 -331.256119 
L 90.820399 -331.256119 
L 91.179403 -331.256119 
L 91.538406 -331.256119 
L 91.89741 -331.256119 
L 92.256413 -331.256119 
L 92.615417 -331.256119 
L 92.97442 -331.256119 
L 93.333424 -331.256119 
L 93.692427 -331.256119 
L 94.05143 -331.256119 
L 94.410434 -331.256119 
L 94.769437 -331.256119 
L 95.128441 -331.256119 
L 95.487444 -331.256119 
L 95.846448 -331.256119 
L 96.205451 -331.256119 
L 96.564455 -331.256119 
L 96.923458 -331.256119 
L 97.282461 -331.256119 
L 97.641465 -331.256119 
L 98.000468 -331.256119 
L 98.359472 -331.256119 
L 98.718475 -331.256119 
L 99.077479 -331.256119 
L 99.436482 -331.256119 
L 99.795486 -331.256119 
L 100.154489 -331.256119 
L 100.513492 -331.256119 
L 100.872496 -331.256119 
L 101.231499 -331.256119 
L 101.590503 -331.256119 
L 101.949506 -331.256119 
L 102.30851 -331.256119 
L 102.667513 -331.256119 
L 103.026517 -331.256119 
L 103.38552 -331.256119 
L 103.744523 -331.256119 
L 104.103527 -331.256119 
L 104.46253 -331.256119 
L 104.821534 -331.256119 
L 105.180537 -331.256119 
L 105.539541 -331.256119 
L 105.898544 -331.256119 
L 106.257548 -331.256119 
L 106.616551 -331.256119 
L 106.975554 -331.256119 
L 107.334558 -331.256119 
L 107.693561 -331.256119 
L 108.052565 -331.256119 
L 108.411568 -331.256119 
L 108.770572 -331.256119 
L 109.129575 -331.256119 
L 109.488579 -331.256119 
L 109.847582 -331.256119 
L 110.206585 -331.256119 
L 110.565589 -331.256119 
L 110.924592 -331.256119 
L 111.283596 -331.256119 
L 111.642599 -331.256119 
L 112.001603 -331.256119 
L 112.360606 -331.256119 
L 112.71961 -331.256119 
L 113.078613 -331.256119 
L 113.437617 -331.256119 
L 113.79662 -331.256119 
L 114.155623 -331.256119 
L 114.514627 -331.256119 
L 114.87363 -331.256119 
L 115.232634 -331.256119 
L 115.591637 -331.256119 
L 115.950641 -331.256119 
L 116.309644 -331.256119 
L 116.668648 -331.256119 
L 117.027651 -331.256119 
L 117.386654 -331.256119 
L 117.745658 -331.256119 
L 118.104661 -331.256119 
L 118.463665 -331.256119 
L 118.822668 -331.256119 
L 119.181672 -331.256119 
L 119.540675 -331.256119 
L 119.899679 -331.256119 
L 120.258682 -331.256119 
L 120.617685 -331.256119 
L 120.976689 -331.256119 
L 121.335692 -331.256119 
L 121.694696 -331.256119 
L 122.053699 -331.256119 
L 122.412703 -331.256119 
L 122.771706 -331.256119 
L 123.13071 -331.256119 
L 123.489713 -331.256119 
L 123.848716 -331.256119 
L 124.20772 -331.256119 
L 124.566723 -331.256119 
L 124.566723 -331.345942 
L 124.566723 -331.345942 
L 124.20772 -331.370192 
L 123.848716 -331.400269 
L 123.489713 -331.437373 
L 123.13071 -331.4829 
L 122.771706 -331.538461 
L 122.412703 -331.605905 
L 122.053699 -331.687333 
L 121.694696 -331.785114 
L 121.335692 -331.901904 
L 120.976689 -332.040644 
L 120.617685 -332.204572 
L 120.258682 -332.397217 
L 119.899679 -332.622386 
L 119.540675 -332.884147 
L 119.181672 -333.1868 
L 118.822668 -333.534837 
L 118.463665 -333.93289 
L 118.104661 -334.385671 
L 117.745658 -334.897898 
L 117.386654 -335.474215 
L 117.027651 -336.119093 
L 116.668648 -336.836729 
L 116.309644 -337.630944 
L 115.950641 -338.505061 
L 115.591637 -339.461797 
L 115.232634 -340.503147 
L 114.87363 -341.630278 
L 114.514627 -342.843429 
L 114.155623 -344.141822 
L 113.79662 -345.523595 
L 113.437617 -346.985747 
L 113.078613 -348.524108 
L 112.71961 -350.133337 
L 112.360606 -351.806945 
L 112.001603 -353.537343 
L 111.642599 -355.315924 
L 111.283596 -357.133168 
L 110.924592 -358.978783 
L 110.565589 -360.841857 
L 110.206585 -362.711043 
L 109.847582 -364.574755 
L 109.488579 -366.42138 
L 109.129575 -368.239491 
L 108.770572 -370.01807 
L 108.411568 -371.746723 
L 108.052565 -373.415877 
L 107.693561 -375.016972 
L 107.334558 -376.542628 
L 106.975554 -377.986776 
L 106.616551 -379.34477 
L 106.257548 -380.613458 
L 105.898544 -381.79122 
L 105.539541 -382.877958 
L 105.180537 -383.875065 
L 104.821534 -384.785339 
L 104.46253 -385.61287 
L 104.103527 -386.362901 
L 103.744523 -387.041646 
L 103.38552 -387.656104 
L 103.026517 -388.213838 
L 102.667513 -388.722763 
L 102.30851 -389.190915 
L 101.949506 -389.626238 
L 101.590503 -390.036369 
L 101.231499 -390.428455 
L 100.872496 -390.808984 
L 100.513492 -391.183652 
L 100.154489 -391.55726 
L 99.795486 -391.933652 
L 99.436482 -392.315686 
L 99.077479 -392.705256 
L 98.718475 -393.103334 
L 98.359472 -393.510067 
L 98.000468 -393.924889 
L 97.641465 -394.346666 
L 97.282461 -394.773859 
L 96.923458 -395.204699 
L 96.564455 -395.637363 
L 96.205451 -396.070147 
L 95.846448 -396.501627 
L 95.487444 -396.930798 
L 95.128441 -397.35719 
L 94.769437 -397.780949 
L 94.410434 -398.202884 
L 94.05143 -398.624476 
L 93.692427 -399.047847 
L 93.333424 -399.475692 
L 92.97442 -399.911178 
L 92.615417 -400.357811 
L 92.256413 -400.819276 
L 91.89741 -401.299268 
L 91.538406 -401.801302 
L 91.179403 -402.328527 
L 90.820399 -402.883547 
L 90.461396 -403.46825 
L 90.102392 -404.083665 
L 89.743389 -404.729835 
L 89.384386 -405.405733 
L 89.025382 -406.109207 
L 88.666379 -406.836955 
L 88.307375 -407.584553 
L 87.948372 -408.346498 
L 87.589368 -409.116303 
L 87.230365 -409.886608 
L 86.871361 -410.649322 
L 86.512358 -411.395781 
L 86.153355 -412.116921 
L 85.794351 -412.803455 
L 85.435348 -413.446058 
L 85.076344 -414.035538 
L 84.717341 -414.563009 
L 84.358337 -415.020039 
L 83.999334 -415.398791 
L 83.64033 -415.692142 
L 83.281327 -415.893781 
L 82.922324 -415.998287 
L 82.56332 -416.001184 
L 82.204317 -415.898985 
L 81.845313 -415.689203 
L 81.48631 -415.370363 
L 81.127306 -414.941985 
L 80.768303 -414.404561 
L 80.409299 -413.75952 
L 80.050296 -413.009185 
L 79.691293 -412.156717 
L 79.332289 -411.206058 
L 78.973286 -410.161861 
L 78.614282 -409.029416 
L 78.255279 -407.814572 
L 77.896275 -406.523648 
L 77.537272 -405.163339 
L 77.178268 -403.740621 
L 76.819265 -402.262642 
L 76.460262 -400.736614 
L 76.101258 -399.169703 
L 75.742255 -397.568918 
L 75.383251 -395.940996 
L 75.024248 -394.292303 
L 74.665244 -392.628731 
L 74.306241 -390.955616 
L 73.947237 -389.277666 
L 73.588234 -387.598909 
L 73.229231 -385.922661 
L 72.870227 -384.251514 
L 72.511224 -382.587358 
L 72.15222 -380.93141 
L 71.793217 -379.284286 
L 71.434213 -377.646078 
L 71.07521 -376.01646 
L 70.716206 -374.394805 
L 70.357203 -372.780309 
L 69.998199 -371.172129 
L 69.639196 -369.569507 
L 69.280193 -367.971904 
L 68.921189 -366.379104 
L 68.562186 -364.791321 
L 68.203182 -363.209268 
L 67.844179 -361.634214 
L 67.485175 -360.068011 
L 67.126172 -358.513095 
L 66.767168 -356.972458 
L 66.408165 -355.4496 
L 66.049162 -353.948455 
L 65.690158 -352.473299 
L 65.331155 -351.028644 
L 64.972151 -349.619122 
L 64.613148 -348.249363 
L 64.254144 -346.923872 
L 63.895141 -345.646914 
L 63.536137 -344.422407 
L 63.177134 -343.253824 
L 62.818131 -342.144112 
L 62.459127 -341.095636 
L 62.100124 -340.110131 
L 61.74112 -339.188681 
L 61.382117 -338.331712 
L 61.023113 -337.53901 
L 60.66411 -336.80975 
L 60.305106 -336.142538 
L 59.946103 -335.535469 
L 59.5871 -334.986192 
L 59.228096 -334.49198 
L 58.869093 -334.049805 
L 58.510089 -333.656408 
L 58.151086 -333.30838 
L 57.792082 -333.002225 
L 57.433079 -332.734424 
L 57.074075 -332.501497 
L 56.715072 -332.300046 
L 56.356069 -332.126804 
L 55.997065 -331.978662 
L 55.638062 -331.852699 
L 55.279058 -331.7462 
L 54.920055 -331.656667 
L 54.561051 -331.58182 
L 54.202048 -331.519604 
L 53.843044 -331.468179 
L 53.484041 -331.425912 
L 53.125038 -331.391369 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#pc960d48d48)">
     <use xlink:href="#mb8e56ce29b" x="0" y="427.438437" style="fill: #1f77b4; fill-opacity: 0.25; stroke: #1f77b4"/>
    </g>
   </g>
  </g>
  <g id="axes_12">
   <g id="FillBetweenPolyCollection_3">
    <defs>
     <path id="m4f357e7f5c" d="M 147.107362 -233.708168 
L 147.107362 -233.571007 
L 147.487717 -233.571007 
L 147.868071 -233.571007 
L 148.248426 -233.571007 
L 148.628781 -233.571007 
L 149.009136 -233.571007 
L 149.38949 -233.571007 
L 149.769845 -233.571007 
L 150.1502 -233.571007 
L 150.530555 -233.571007 
L 150.910909 -233.571007 
L 151.291264 -233.571007 
L 151.671619 -233.571007 
L 152.051974 -233.571007 
L 152.432328 -233.571007 
L 152.812683 -233.571007 
L 153.193038 -233.571007 
L 153.573393 -233.571007 
L 153.953747 -233.571007 
L 154.334102 -233.571007 
L 154.714457 -233.571007 
L 155.094812 -233.571007 
L 155.475166 -233.571007 
L 155.855521 -233.571007 
L 156.235876 -233.571007 
L 156.616231 -233.571007 
L 156.996585 -233.571007 
L 157.37694 -233.571007 
L 157.757295 -233.571007 
L 158.137649 -233.571007 
L 158.518004 -233.571007 
L 158.898359 -233.571007 
L 159.278714 -233.571007 
L 159.659068 -233.571007 
L 160.039423 -233.571007 
L 160.419778 -233.571007 
L 160.800133 -233.571007 
L 161.180487 -233.571007 
L 161.560842 -233.571007 
L 161.941197 -233.571007 
L 162.321552 -233.571007 
L 162.701906 -233.571007 
L 163.082261 -233.571007 
L 163.462616 -233.571007 
L 163.842971 -233.571007 
L 164.223325 -233.571007 
L 164.60368 -233.571007 
L 164.984035 -233.571007 
L 165.36439 -233.571007 
L 165.744744 -233.571007 
L 166.125099 -233.571007 
L 166.505454 -233.571007 
L 166.885809 -233.571007 
L 167.266163 -233.571007 
L 167.646518 -233.571007 
L 168.026873 -233.571007 
L 168.407228 -233.571007 
L 168.787582 -233.571007 
L 169.167937 -233.571007 
L 169.548292 -233.571007 
L 169.928647 -233.571007 
L 170.309001 -233.571007 
L 170.689356 -233.571007 
L 171.069711 -233.571007 
L 171.450065 -233.571007 
L 171.83042 -233.571007 
L 172.210775 -233.571007 
L 172.59113 -233.571007 
L 172.971484 -233.571007 
L 173.351839 -233.571007 
L 173.732194 -233.571007 
L 174.112549 -233.571007 
L 174.492903 -233.571007 
L 174.873258 -233.571007 
L 175.253613 -233.571007 
L 175.633968 -233.571007 
L 176.014322 -233.571007 
L 176.394677 -233.571007 
L 176.775032 -233.571007 
L 177.155387 -233.571007 
L 177.535741 -233.571007 
L 177.916096 -233.571007 
L 178.296451 -233.571007 
L 178.676806 -233.571007 
L 179.05716 -233.571007 
L 179.437515 -233.571007 
L 179.81787 -233.571007 
L 180.198225 -233.571007 
L 180.578579 -233.571007 
L 180.958934 -233.571007 
L 181.339289 -233.571007 
L 181.719644 -233.571007 
L 182.099998 -233.571007 
L 182.480353 -233.571007 
L 182.860708 -233.571007 
L 183.241063 -233.571007 
L 183.621417 -233.571007 
L 184.001772 -233.571007 
L 184.382127 -233.571007 
L 184.762482 -233.571007 
L 185.142836 -233.571007 
L 185.523191 -233.571007 
L 185.903546 -233.571007 
L 186.2839 -233.571007 
L 186.664255 -233.571007 
L 187.04461 -233.571007 
L 187.424965 -233.571007 
L 187.805319 -233.571007 
L 188.185674 -233.571007 
L 188.566029 -233.571007 
L 188.946384 -233.571007 
L 189.326738 -233.571007 
L 189.707093 -233.571007 
L 190.087448 -233.571007 
L 190.467803 -233.571007 
L 190.848157 -233.571007 
L 191.228512 -233.571007 
L 191.608867 -233.571007 
L 191.989222 -233.571007 
L 192.369576 -233.571007 
L 192.749931 -233.571007 
L 193.130286 -233.571007 
L 193.510641 -233.571007 
L 193.890995 -233.571007 
L 194.27135 -233.571007 
L 194.651705 -233.571007 
L 195.03206 -233.571007 
L 195.412414 -233.571007 
L 195.792769 -233.571007 
L 196.173124 -233.571007 
L 196.553479 -233.571007 
L 196.933833 -233.571007 
L 197.314188 -233.571007 
L 197.694543 -233.571007 
L 198.074898 -233.571007 
L 198.455252 -233.571007 
L 198.835607 -233.571007 
L 199.215962 -233.571007 
L 199.596316 -233.571007 
L 199.976671 -233.571007 
L 200.357026 -233.571007 
L 200.737381 -233.571007 
L 201.117735 -233.571007 
L 201.49809 -233.571007 
L 201.878445 -233.571007 
L 202.2588 -233.571007 
L 202.639154 -233.571007 
L 203.019509 -233.571007 
L 203.399864 -233.571007 
L 203.780219 -233.571007 
L 204.160573 -233.571007 
L 204.540928 -233.571007 
L 204.921283 -233.571007 
L 205.301638 -233.571007 
L 205.681992 -233.571007 
L 206.062347 -233.571007 
L 206.442702 -233.571007 
L 206.823057 -233.571007 
L 207.203411 -233.571007 
L 207.583766 -233.571007 
L 207.964121 -233.571007 
L 208.344476 -233.571007 
L 208.72483 -233.571007 
L 209.105185 -233.571007 
L 209.48554 -233.571007 
L 209.865895 -233.571007 
L 210.246249 -233.571007 
L 210.626604 -233.571007 
L 211.006959 -233.571007 
L 211.387314 -233.571007 
L 211.767668 -233.571007 
L 212.148023 -233.571007 
L 212.528378 -233.571007 
L 212.908732 -233.571007 
L 213.289087 -233.571007 
L 213.669442 -233.571007 
L 214.049797 -233.571007 
L 214.430151 -233.571007 
L 214.810506 -233.571007 
L 215.190861 -233.571007 
L 215.571216 -233.571007 
L 215.95157 -233.571007 
L 216.331925 -233.571007 
L 216.71228 -233.571007 
L 217.092635 -233.571007 
L 217.472989 -233.571007 
L 217.853344 -233.571007 
L 218.233699 -233.571007 
L 218.614054 -233.571007 
L 218.994408 -233.571007 
L 219.374763 -233.571007 
L 219.755118 -233.571007 
L 220.135473 -233.571007 
L 220.515827 -233.571007 
L 220.896182 -233.571007 
L 221.276537 -233.571007 
L 221.656892 -233.571007 
L 222.037246 -233.571007 
L 222.417601 -233.571007 
L 222.797956 -233.571007 
L 222.797956 -233.735585 
L 222.797956 -233.735585 
L 222.417601 -233.774688 
L 222.037246 -233.821787 
L 221.656892 -233.878192 
L 221.276537 -233.945353 
L 220.896182 -234.02486 
L 220.515827 -234.118434 
L 220.135473 -234.227924 
L 219.755118 -234.355283 
L 219.374763 -234.502556 
L 218.994408 -234.671846 
L 218.614054 -234.865284 
L 218.233699 -235.084989 
L 217.853344 -235.333024 
L 217.472989 -235.61134 
L 217.092635 -235.921729 
L 216.71228 -236.265762 
L 216.331925 -236.644729 
L 215.95157 -237.059585 
L 215.571216 -237.510897 
L 215.190861 -237.998792 
L 214.810506 -238.522919 
L 214.430151 -239.082426 
L 214.049797 -239.675939 
L 213.669442 -240.301574 
L 213.289087 -240.956952 
L 212.908732 -241.639243 
L 212.528378 -242.345233 
L 212.148023 -243.071403 
L 211.767668 -243.814031 
L 211.387314 -244.56932 
L 211.006959 -245.333525 
L 210.626604 -246.103106 
L 210.246249 -246.874872 
L 209.865895 -247.646136 
L 209.48554 -248.414855 
L 209.105185 -249.17976 
L 208.72483 -249.940464 
L 208.344476 -250.697537 
L 207.964121 -251.452555 
L 207.583766 -252.208106 
L 207.203411 -252.967748 
L 206.823057 -253.735931 
L 206.442702 -254.51786 
L 206.062347 -255.319328 
L 205.681992 -256.146493 
L 205.301638 -257.00563 
L 204.921283 -257.902852 
L 204.540928 -258.843813 
L 204.160573 -259.833405 
L 203.780219 -260.875462 
L 203.399864 -261.972482 
L 203.019509 -263.12538 
L 202.639154 -264.333294 
L 202.2588 -265.593437 
L 201.878445 -266.901022 
L 201.49809 -268.249262 
L 201.117735 -269.629446 
L 200.737381 -271.031096 
L 200.357026 -272.442204 
L 199.976671 -273.849542 
L 199.596316 -275.239034 
L 199.215962 -276.596181 
L 198.835607 -277.906523 
L 198.455252 -279.15612 
L 198.074898 -280.332034 
L 197.694543 -281.422789 
L 197.314188 -282.418793 
L 196.933833 -283.312701 
L 196.553479 -284.099705 
L 196.173124 -284.77773 
L 195.792769 -285.347531 
L 195.412414 -285.812688 
L 195.03206 -286.179479 
L 194.651705 -286.456663 
L 194.27135 -286.655146 
L 193.890995 -286.787571 
L 193.510641 -286.867834 
L 193.130286 -286.910538 
L 192.749931 -286.930432 
L 192.369576 -286.941827 
L 191.989222 -286.958045 
L 191.608867 -286.990894 
L 191.228512 -287.050218 
L 190.848157 -287.143532 
L 190.467803 -287.275744 
L 190.087448 -287.449007 
L 189.707093 -287.662676 
L 189.326738 -287.913395 
L 188.946384 -288.195296 
L 188.566029 -288.500314 
L 188.185674 -288.818585 
L 187.805319 -289.138938 
L 187.424965 -289.449422 
L 187.04461 -289.737884 
L 186.664255 -289.992535 
L 186.2839 -290.202507 
L 185.903546 -290.358362 
L 185.523191 -290.452526 
L 185.142836 -290.479643 
L 184.762482 -290.436821 
L 184.382127 -290.323762 
L 184.001772 -290.142775 
L 183.621417 -289.898662 
L 183.241063 -289.598492 
L 182.860708 -289.25127 
L 182.480353 -288.867516 
L 182.099998 -288.458769 
L 181.719644 -288.03705 
L 181.339289 -287.614295 
L 180.958934 -287.201795 
L 180.578579 -286.809659 
L 180.198225 -286.446332 
L 179.81787 -286.118187 
L 179.437515 -285.8292 
L 179.05716 -285.58074 
L 178.676806 -285.371467 
L 178.296451 -285.197349 
L 177.916096 -285.051795 
L 177.535741 -284.925903 
L 177.155387 -284.808795 
L 176.775032 -284.68805 
L 176.394677 -284.550191 
L 176.014322 -284.381218 
L 175.633968 -284.167158 
L 175.253613 -283.894618 
L 174.873258 -283.551306 
L 174.492903 -283.126502 
L 174.112549 -282.611468 
L 173.732194 -281.999773 
L 173.351839 -281.287521 
L 172.971484 -280.473487 
L 172.59113 -279.559138 
L 172.210775 -278.54856 
L 171.83042 -277.448284 
L 171.450065 -276.267031 
L 171.069711 -275.015379 
L 170.689356 -273.705377 
L 170.309001 -272.350113 
L 169.928647 -270.963272 
L 169.548292 -269.558679 
L 169.167937 -268.149863 
L 168.787582 -266.749659 
L 168.407228 -265.369843 
L 168.026873 -264.020836 
L 167.646518 -262.711467 
L 167.266163 -261.448814 
L 166.885809 -260.238114 
L 166.505454 -259.082746 
L 166.125099 -257.984287 
L 165.744744 -256.942625 
L 165.36439 -255.956128 
L 164.984035 -255.02186 
L 164.60368 -254.135817 
L 164.223325 -253.293197 
L 163.842971 -252.488667 
L 163.462616 -251.716632 
L 163.082261 -250.971488 
L 162.701906 -250.247854 
L 162.321552 -249.540771 
L 161.941197 -248.845868 
L 161.560842 -248.159492 
L 161.180487 -247.478788 
L 160.800133 -246.801749 
L 160.419778 -246.127222 
L 160.039423 -245.454881 
L 159.659068 -244.785167 
L 159.278714 -244.119208 
L 158.898359 -243.458708 
L 158.518004 -242.80584 
L 158.137649 -242.163113 
L 157.757295 -241.533253 
L 157.37694 -240.919073 
L 156.996585 -240.323366 
L 156.616231 -239.748794 
L 156.235876 -239.197805 
L 155.855521 -238.672554 
L 155.475166 -238.174855 
L 155.094812 -237.706134 
L 154.714457 -237.267414 
L 154.334102 -236.859306 
L 153.953747 -236.482019 
L 153.573393 -236.135378 
L 153.193038 -235.818856 
L 152.812683 -235.531612 
L 152.432328 -235.272534 
L 152.051974 -235.040284 
L 151.671619 -234.833348 
L 151.291264 -234.650079 
L 150.910909 -234.488745 
L 150.530555 -234.347569 
L 150.1502 -234.224767 
L 149.769845 -234.11858 
L 149.38949 -234.027298 
L 149.009136 -233.94929 
L 148.628781 -233.883014 
L 148.248426 -233.827031 
L 147.868071 -233.780016 
L 147.487717 -233.740759 
L 147.107362 -233.708168 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#p4df8b4f7b9)">
     <use xlink:href="#m4f357e7f5c" x="0" y="427.438437" style="fill: #ff7f0e; fill-opacity: 0.25; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="FillBetweenPolyCollection_4">
    <defs>
     <path id="m75ba730969" d="M 148.522611 -233.841915 
L 148.522611 -233.571007 
L 148.888743 -233.571007 
L 149.254874 -233.571007 
L 149.621005 -233.571007 
L 149.987136 -233.571007 
L 150.353267 -233.571007 
L 150.719398 -233.571007 
L 151.085529 -233.571007 
L 151.451661 -233.571007 
L 151.817792 -233.571007 
L 152.183923 -233.571007 
L 152.550054 -233.571007 
L 152.916185 -233.571007 
L 153.282316 -233.571007 
L 153.648447 -233.571007 
L 154.014578 -233.571007 
L 154.38071 -233.571007 
L 154.746841 -233.571007 
L 155.112972 -233.571007 
L 155.479103 -233.571007 
L 155.845234 -233.571007 
L 156.211365 -233.571007 
L 156.577496 -233.571007 
L 156.943627 -233.571007 
L 157.309759 -233.571007 
L 157.67589 -233.571007 
L 158.042021 -233.571007 
L 158.408152 -233.571007 
L 158.774283 -233.571007 
L 159.140414 -233.571007 
L 159.506545 -233.571007 
L 159.872677 -233.571007 
L 160.238808 -233.571007 
L 160.604939 -233.571007 
L 160.97107 -233.571007 
L 161.337201 -233.571007 
L 161.703332 -233.571007 
L 162.069463 -233.571007 
L 162.435594 -233.571007 
L 162.801726 -233.571007 
L 163.167857 -233.571007 
L 163.533988 -233.571007 
L 163.900119 -233.571007 
L 164.26625 -233.571007 
L 164.632381 -233.571007 
L 164.998512 -233.571007 
L 165.364643 -233.571007 
L 165.730775 -233.571007 
L 166.096906 -233.571007 
L 166.463037 -233.571007 
L 166.829168 -233.571007 
L 167.195299 -233.571007 
L 167.56143 -233.571007 
L 167.927561 -233.571007 
L 168.293692 -233.571007 
L 168.659824 -233.571007 
L 169.025955 -233.571007 
L 169.392086 -233.571007 
L 169.758217 -233.571007 
L 170.124348 -233.571007 
L 170.490479 -233.571007 
L 170.85661 -233.571007 
L 171.222742 -233.571007 
L 171.588873 -233.571007 
L 171.955004 -233.571007 
L 172.321135 -233.571007 
L 172.687266 -233.571007 
L 173.053397 -233.571007 
L 173.419528 -233.571007 
L 173.785659 -233.571007 
L 174.151791 -233.571007 
L 174.517922 -233.571007 
L 174.884053 -233.571007 
L 175.250184 -233.571007 
L 175.616315 -233.571007 
L 175.982446 -233.571007 
L 176.348577 -233.571007 
L 176.714708 -233.571007 
L 177.08084 -233.571007 
L 177.446971 -233.571007 
L 177.813102 -233.571007 
L 178.179233 -233.571007 
L 178.545364 -233.571007 
L 178.911495 -233.571007 
L 179.277626 -233.571007 
L 179.643757 -233.571007 
L 180.009889 -233.571007 
L 180.37602 -233.571007 
L 180.742151 -233.571007 
L 181.108282 -233.571007 
L 181.474413 -233.571007 
L 181.840544 -233.571007 
L 182.206675 -233.571007 
L 182.572807 -233.571007 
L 182.938938 -233.571007 
L 183.305069 -233.571007 
L 183.6712 -233.571007 
L 184.037331 -233.571007 
L 184.403462 -233.571007 
L 184.769593 -233.571007 
L 185.135724 -233.571007 
L 185.501856 -233.571007 
L 185.867987 -233.571007 
L 186.234118 -233.571007 
L 186.600249 -233.571007 
L 186.96638 -233.571007 
L 187.332511 -233.571007 
L 187.698642 -233.571007 
L 188.064773 -233.571007 
L 188.430905 -233.571007 
L 188.797036 -233.571007 
L 189.163167 -233.571007 
L 189.529298 -233.571007 
L 189.895429 -233.571007 
L 190.26156 -233.571007 
L 190.627691 -233.571007 
L 190.993823 -233.571007 
L 191.359954 -233.571007 
L 191.726085 -233.571007 
L 192.092216 -233.571007 
L 192.458347 -233.571007 
L 192.824478 -233.571007 
L 193.190609 -233.571007 
L 193.55674 -233.571007 
L 193.922872 -233.571007 
L 194.289003 -233.571007 
L 194.655134 -233.571007 
L 195.021265 -233.571007 
L 195.387396 -233.571007 
L 195.753527 -233.571007 
L 196.119658 -233.571007 
L 196.485789 -233.571007 
L 196.851921 -233.571007 
L 197.218052 -233.571007 
L 197.584183 -233.571007 
L 197.950314 -233.571007 
L 198.316445 -233.571007 
L 198.682576 -233.571007 
L 199.048707 -233.571007 
L 199.414838 -233.571007 
L 199.78097 -233.571007 
L 200.147101 -233.571007 
L 200.513232 -233.571007 
L 200.879363 -233.571007 
L 201.245494 -233.571007 
L 201.611625 -233.571007 
L 201.977756 -233.571007 
L 202.343888 -233.571007 
L 202.710019 -233.571007 
L 203.07615 -233.571007 
L 203.442281 -233.571007 
L 203.808412 -233.571007 
L 204.174543 -233.571007 
L 204.540674 -233.571007 
L 204.906805 -233.571007 
L 205.272937 -233.571007 
L 205.639068 -233.571007 
L 206.005199 -233.571007 
L 206.37133 -233.571007 
L 206.737461 -233.571007 
L 207.103592 -233.571007 
L 207.469723 -233.571007 
L 207.835854 -233.571007 
L 208.201986 -233.571007 
L 208.568117 -233.571007 
L 208.934248 -233.571007 
L 209.300379 -233.571007 
L 209.66651 -233.571007 
L 210.032641 -233.571007 
L 210.398772 -233.571007 
L 210.764904 -233.571007 
L 211.131035 -233.571007 
L 211.497166 -233.571007 
L 211.863297 -233.571007 
L 212.229428 -233.571007 
L 212.595559 -233.571007 
L 212.96169 -233.571007 
L 213.327821 -233.571007 
L 213.693953 -233.571007 
L 214.060084 -233.571007 
L 214.426215 -233.571007 
L 214.792346 -233.571007 
L 215.158477 -233.571007 
L 215.524608 -233.571007 
L 215.890739 -233.571007 
L 216.25687 -233.571007 
L 216.623002 -233.571007 
L 216.989133 -233.571007 
L 217.355264 -233.571007 
L 217.721395 -233.571007 
L 218.087526 -233.571007 
L 218.453657 -233.571007 
L 218.819788 -233.571007 
L 219.185919 -233.571007 
L 219.552051 -233.571007 
L 219.918182 -233.571007 
L 220.284313 -233.571007 
L 220.650444 -233.571007 
L 221.016575 -233.571007 
L 221.382706 -233.571007 
L 221.382706 -233.721517 
L 221.382706 -233.721517 
L 221.016575 -233.759506 
L 220.650444 -233.805727 
L 220.284313 -233.861603 
L 219.918182 -233.928716 
L 219.552051 -234.008801 
L 219.185919 -234.103744 
L 218.819788 -234.215561 
L 218.453657 -234.346382 
L 218.087526 -234.498417 
L 217.721395 -234.673923 
L 217.355264 -234.875155 
L 216.989133 -235.104314 
L 216.623002 -235.363482 
L 216.25687 -235.654559 
L 215.890739 -235.979188 
L 215.524608 -236.338682 
L 215.158477 -236.733947 
L 214.792346 -237.165414 
L 214.426215 -237.632973 
L 214.060084 -238.135924 
L 213.693953 -238.672936 
L 213.327821 -239.242031 
L 212.96169 -239.840587 
L 212.595559 -240.465365 
L 212.229428 -241.112572 
L 211.863297 -241.77794 
L 211.497166 -242.456849 
L 211.131035 -243.144465 
L 210.764904 -243.835912 
L 210.398772 -244.52646 
L 210.032641 -245.211732 
L 209.66651 -245.887915 
L 209.300379 -246.551973 
L 208.934248 -247.201851 
L 208.568117 -247.836654 
L 208.201986 -248.456803 
L 207.835854 -249.064146 
L 207.469723 -249.662019 
L 207.103592 -250.255257 
L 206.737461 -250.850132 
L 206.37133 -251.454235 
L 206.005199 -252.076279 
L 205.639068 -252.725851 
L 205.272937 -253.413087 
L 204.906805 -254.148311 
L 204.540674 -254.941617 
L 204.174543 -255.802441 
L 203.808412 -256.739111 
L 203.442281 -257.758409 
L 203.07615 -258.865165 
L 202.710019 -260.061893 
L 202.343888 -261.348498 
L 201.977756 -262.722069 
L 201.611625 -264.176768 
L 201.245494 -265.703836 
L 200.879363 -267.291715 
L 200.513232 -268.926299 
L 200.147101 -270.591298 
L 199.78097 -272.268725 
L 199.414838 -273.939473 
L 199.048707 -275.583975 
L 198.682576 -277.182933 
L 198.316445 -278.71806 
L 197.950314 -280.17283 
L 197.584183 -281.533201 
L 197.218052 -282.788262 
L 196.851921 -283.93079 
L 196.485789 -284.95768 
L 196.119658 -285.870227 
L 195.753527 -286.674231 
L 195.387396 -287.379929 
L 195.021265 -288.001732 
L 194.655134 -288.557781 
L 194.289003 -289.069323 
L 193.922872 -289.559933 
L 193.55674 -290.054614 
L 193.190609 -290.578786 
L 192.824478 -291.157235 
L 192.458347 -291.813032 
L 192.092216 -292.566494 
L 191.726085 -293.434215 
L 191.359954 -294.428218 
L 190.993823 -295.555269 
L 190.627691 -296.81638 
L 190.26156 -298.206539 
L 189.895429 -299.714678 
L 189.529298 -301.323885 
L 189.163167 -303.011869 
L 188.797036 -304.751656 
L 188.430905 -306.512498 
L 188.064773 -308.260955 
L 187.698642 -309.962124 
L 187.332511 -311.580945 
L 186.96638 -313.083556 
L 186.600249 -314.438618 
L 186.234118 -315.618565 
L 185.867987 -316.600733 
L 185.501856 -317.368297 
L 185.135724 -317.910995 
L 184.769593 -318.225593 
L 184.403462 -318.316072 
L 184.037331 -318.193522 
L 183.6712 -317.875755 
L 183.305069 -317.386633 
L 182.938938 -316.755151 
L 182.572807 -316.014302 
L 182.206675 -315.19978 
L 181.840544 -314.348558 
L 181.474413 -313.497417 
L 181.108282 -312.681472 
L 180.742151 -311.932772 
L 180.37602 -311.279012 
L 180.009889 -310.742425 
L 179.643757 -310.338903 
L 179.277626 -310.07736 
L 178.911495 -309.959393 
L 178.545364 -309.979232 
L 178.179233 -310.123982 
L 177.813102 -310.374161 
L 177.446971 -310.704488 
L 177.08084 -311.084901 
L 176.714708 -311.481763 
L 176.348577 -311.85919 
L 175.982446 -312.18046 
L 175.616315 -312.409443 
L 175.250184 -312.511985 
L 174.884053 -312.457196 
L 174.517922 -312.218598 
L 174.151791 -311.775074 
L 173.785659 -311.111596 
L 173.419528 -310.219708 
L 173.053397 -309.097743 
L 172.687266 -307.75077 
L 172.321135 -306.190298 
L 171.955004 -304.43373 
L 171.588873 -302.503621 
L 171.222742 -300.42676 
L 170.85661 -298.233124 
L 170.490479 -295.954752 
L 170.124348 -293.624581 
L 169.758217 -291.275304 
L 169.392086 -288.938275 
L 169.025955 -286.642521 
L 168.659824 -284.413889 
L 168.293692 -282.274344 
L 167.927561 -280.241459 
L 167.56143 -278.328089 
L 167.195299 -276.542245 
L 166.829168 -274.887151 
L 166.463037 -273.361477 
L 166.096906 -271.959736 
L 165.730775 -270.672797 
L 165.364643 -269.488519 
L 164.998512 -268.392439 
L 164.632381 -267.368512 
L 164.26625 -266.399852 
L 163.900119 -265.469454 
L 163.533988 -264.560865 
L 163.167857 -263.658786 
L 162.801726 -262.74958 
L 162.435594 -261.821681 
L 162.069463 -260.865889 
L 161.703332 -259.875547 
L 161.337201 -258.846616 
L 160.97107 -257.777632 
L 160.604939 -256.669575 
L 160.238808 -255.525654 
L 159.872677 -254.351026 
L 159.506545 -253.152466 
L 159.140414 -251.938002 
L 158.774283 -250.716541 
L 158.408152 -249.497493 
L 158.042021 -248.290407 
L 157.67589 -247.104647 
L 157.309759 -245.949093 
L 156.943627 -244.831896 
L 156.577496 -243.760281 
L 156.211365 -242.740403 
L 155.845234 -241.777247 
L 155.479103 -240.874595 
L 155.112972 -240.035015 
L 154.746841 -239.259911 
L 154.38071 -238.549591 
L 154.014578 -237.903367 
L 153.648447 -237.319677 
L 153.282316 -236.796214 
L 152.916185 -236.330061 
L 152.550054 -235.917832 
L 152.183923 -235.555799 
L 151.817792 -235.240022 
L 151.451661 -234.966455 
L 151.085529 -234.731046 
L 150.719398 -234.529824 
L 150.353267 -234.358961 
L 149.987136 -234.214831 
L 149.621005 -234.094045 
L 149.254874 -233.993479 
L 148.888743 -233.910289 
L 148.522611 -233.841915 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#p4df8b4f7b9)">
     <use xlink:href="#m75ba730969" x="0" y="427.438437" style="fill: #1f77b4; fill-opacity: 0.25; stroke: #1f77b4"/>
    </g>
   </g>
  </g>
  <g id="axes_13">
   <g id="FillBetweenPolyCollection_5">
    <defs>
     <path id="m1e1bdc6b3e" d="M 243.272178 -136.034046 
L 243.272178 -135.885894 
L 243.651878 -135.885894 
L 244.031578 -135.885894 
L 244.411278 -135.885894 
L 244.790979 -135.885894 
L 245.170679 -135.885894 
L 245.550379 -135.885894 
L 245.930079 -135.885894 
L 246.309779 -135.885894 
L 246.689479 -135.885894 
L 247.069179 -135.885894 
L 247.44888 -135.885894 
L 247.82858 -135.885894 
L 248.20828 -135.885894 
L 248.58798 -135.885894 
L 248.96768 -135.885894 
L 249.34738 -135.885894 
L 249.72708 -135.885894 
L 250.106781 -135.885894 
L 250.486481 -135.885894 
L 250.866181 -135.885894 
L 251.245881 -135.885894 
L 251.625581 -135.885894 
L 252.005281 -135.885894 
L 252.384981 -135.885894 
L 252.764682 -135.885894 
L 253.144382 -135.885894 
L 253.524082 -135.885894 
L 253.903782 -135.885894 
L 254.283482 -135.885894 
L 254.663182 -135.885894 
L 255.042882 -135.885894 
L 255.422583 -135.885894 
L 255.802283 -135.885894 
L 256.181983 -135.885894 
L 256.561683 -135.885894 
L 256.941383 -135.885894 
L 257.321083 -135.885894 
L 257.700783 -135.885894 
L 258.080484 -135.885894 
L 258.460184 -135.885894 
L 258.839884 -135.885894 
L 259.219584 -135.885894 
L 259.599284 -135.885894 
L 259.978984 -135.885894 
L 260.358684 -135.885894 
L 260.738385 -135.885894 
L 261.118085 -135.885894 
L 261.497785 -135.885894 
L 261.877485 -135.885894 
L 262.257185 -135.885894 
L 262.636885 -135.885894 
L 263.016585 -135.885894 
L 263.396286 -135.885894 
L 263.775986 -135.885894 
L 264.155686 -135.885894 
L 264.535386 -135.885894 
L 264.915086 -135.885894 
L 265.294786 -135.885894 
L 265.674487 -135.885894 
L 266.054187 -135.885894 
L 266.433887 -135.885894 
L 266.813587 -135.885894 
L 267.193287 -135.885894 
L 267.572987 -135.885894 
L 267.952687 -135.885894 
L 268.332388 -135.885894 
L 268.712088 -135.885894 
L 269.091788 -135.885894 
L 269.471488 -135.885894 
L 269.851188 -135.885894 
L 270.230888 -135.885894 
L 270.610588 -135.885894 
L 270.990289 -135.885894 
L 271.369989 -135.885894 
L 271.749689 -135.885894 
L 272.129389 -135.885894 
L 272.509089 -135.885894 
L 272.888789 -135.885894 
L 273.268489 -135.885894 
L 273.64819 -135.885894 
L 274.02789 -135.885894 
L 274.40759 -135.885894 
L 274.78729 -135.885894 
L 275.16699 -135.885894 
L 275.54669 -135.885894 
L 275.92639 -135.885894 
L 276.306091 -135.885894 
L 276.685791 -135.885894 
L 277.065491 -135.885894 
L 277.445191 -135.885894 
L 277.824891 -135.885894 
L 278.204591 -135.885894 
L 278.584291 -135.885894 
L 278.963992 -135.885894 
L 279.343692 -135.885894 
L 279.723392 -135.885894 
L 280.103092 -135.885894 
L 280.482792 -135.885894 
L 280.862492 -135.885894 
L 281.242192 -135.885894 
L 281.621893 -135.885894 
L 282.001593 -135.885894 
L 282.381293 -135.885894 
L 282.760993 -135.885894 
L 283.140693 -135.885894 
L 283.520393 -135.885894 
L 283.900093 -135.885894 
L 284.279794 -135.885894 
L 284.659494 -135.885894 
L 285.039194 -135.885894 
L 285.418894 -135.885894 
L 285.798594 -135.885894 
L 286.178294 -135.885894 
L 286.557994 -135.885894 
L 286.937695 -135.885894 
L 287.317395 -135.885894 
L 287.697095 -135.885894 
L 288.076795 -135.885894 
L 288.456495 -135.885894 
L 288.836195 -135.885894 
L 289.215895 -135.885894 
L 289.595596 -135.885894 
L 289.975296 -135.885894 
L 290.354996 -135.885894 
L 290.734696 -135.885894 
L 291.114396 -135.885894 
L 291.494096 -135.885894 
L 291.873797 -135.885894 
L 292.253497 -135.885894 
L 292.633197 -135.885894 
L 293.012897 -135.885894 
L 293.392597 -135.885894 
L 293.772297 -135.885894 
L 294.151997 -135.885894 
L 294.531698 -135.885894 
L 294.911398 -135.885894 
L 295.291098 -135.885894 
L 295.670798 -135.885894 
L 296.050498 -135.885894 
L 296.430198 -135.885894 
L 296.809898 -135.885894 
L 297.189599 -135.885894 
L 297.569299 -135.885894 
L 297.948999 -135.885894 
L 298.328699 -135.885894 
L 298.708399 -135.885894 
L 299.088099 -135.885894 
L 299.467799 -135.885894 
L 299.8475 -135.885894 
L 300.2272 -135.885894 
L 300.6069 -135.885894 
L 300.9866 -135.885894 
L 301.3663 -135.885894 
L 301.746 -135.885894 
L 302.1257 -135.885894 
L 302.505401 -135.885894 
L 302.885101 -135.885894 
L 303.264801 -135.885894 
L 303.644501 -135.885894 
L 304.024201 -135.885894 
L 304.403901 -135.885894 
L 304.783601 -135.885894 
L 305.163302 -135.885894 
L 305.543002 -135.885894 
L 305.922702 -135.885894 
L 306.302402 -135.885894 
L 306.682102 -135.885894 
L 307.061802 -135.885894 
L 307.441502 -135.885894 
L 307.821203 -135.885894 
L 308.200903 -135.885894 
L 308.580603 -135.885894 
L 308.960303 -135.885894 
L 309.340003 -135.885894 
L 309.719703 -135.885894 
L 310.099403 -135.885894 
L 310.479104 -135.885894 
L 310.858804 -135.885894 
L 311.238504 -135.885894 
L 311.618204 -135.885894 
L 311.997904 -135.885894 
L 312.377604 -135.885894 
L 312.757304 -135.885894 
L 313.137005 -135.885894 
L 313.516705 -135.885894 
L 313.896405 -135.885894 
L 314.276105 -135.885894 
L 314.655805 -135.885894 
L 315.035505 -135.885894 
L 315.415205 -135.885894 
L 315.794906 -135.885894 
L 316.174606 -135.885894 
L 316.554306 -135.885894 
L 316.934006 -135.885894 
L 317.313706 -135.885894 
L 317.693406 -135.885894 
L 318.073107 -135.885894 
L 318.452807 -135.885894 
L 318.832507 -135.885894 
L 318.832507 -135.937631 
L 318.832507 -135.937631 
L 318.452807 -135.950867 
L 318.073107 -135.967112 
L 317.693406 -135.986954 
L 317.313706 -136.011068 
L 316.934006 -136.040229 
L 316.554306 -136.075319 
L 316.174606 -136.117334 
L 315.794906 -136.167393 
L 315.415205 -136.226742 
L 315.035505 -136.296759 
L 314.655805 -136.378953 
L 314.276105 -136.474969 
L 313.896405 -136.586578 
L 313.516705 -136.715678 
L 313.137005 -136.864275 
L 312.757304 -137.034476 
L 312.377604 -137.228469 
L 311.997904 -137.448498 
L 311.618204 -137.696839 
L 311.238504 -137.975767 
L 310.858804 -138.287527 
L 310.479104 -138.634286 
L 310.099403 -139.018105 
L 309.719703 -139.440886 
L 309.340003 -139.904333 
L 308.960303 -140.409909 
L 308.580603 -140.958789 
L 308.200903 -141.551827 
L 307.821203 -142.18951 
L 307.441502 -142.871933 
L 307.061802 -143.598769 
L 306.682102 -144.36925 
L 306.302402 -145.182159 
L 305.922702 -146.035822 
L 305.543002 -146.928119 
L 305.163302 -147.856499 
L 304.783601 -148.818007 
L 304.403901 -149.809318 
L 304.024201 -150.826784 
L 303.644501 -151.866486 
L 303.264801 -152.924294 
L 302.885101 -153.995933 
L 302.505401 -155.077055 
L 302.1257 -156.163311 
L 301.746 -157.250427 
L 301.3663 -158.334277 
L 300.9866 -159.410956 
L 300.6069 -160.476846 
L 300.2272 -161.528679 
L 299.8475 -162.56359 
L 299.467799 -163.579167 
L 299.088099 -164.573481 
L 298.708399 -165.545117 
L 298.328699 -166.493189 
L 297.948999 -167.417339 
L 297.569299 -168.317731 
L 297.189599 -169.195032 
L 296.809898 -170.050381 
L 296.430198 -170.885346 
L 296.050498 -171.701876 
L 295.670798 -172.502242 
L 295.291098 -173.28897 
L 294.911398 -174.064773 
L 294.531698 -174.832474 
L 294.151997 -175.594931 
L 293.772297 -176.354959 
L 293.392597 -177.115257 
L 293.012897 -177.878335 
L 292.633197 -178.646446 
L 292.253497 -179.42153 
L 291.873797 -180.205156 
L 291.494096 -180.998485 
L 291.114396 -181.802232 
L 290.734696 -182.616647 
L 290.354996 -183.441498 
L 289.975296 -184.276077 
L 289.595596 -185.1192 
L 289.215895 -185.969232 
L 288.836195 -186.824108 
L 288.456495 -187.681367 
L 288.076795 -188.538194 
L 287.697095 -189.391457 
L 287.317395 -190.237754 
L 286.937695 -191.07346 
L 286.557994 -191.89477 
L 286.178294 -192.697742 
L 285.798594 -193.478343 
L 285.418894 -194.232484 
L 285.039194 -194.95606 
L 284.659494 -195.644983 
L 284.279794 -196.295215 
L 283.900093 -196.902802 
L 283.520393 -197.463906 
L 283.140693 -197.974842 
L 282.760993 -198.432115 
L 282.381293 -198.832459 
L 282.001593 -199.172891 
L 281.621893 -199.450753 
L 281.242192 -199.663776 
L 280.862492 -199.810134 
L 280.482792 -199.88851 
L 280.103092 -199.898159 
L 279.723392 -199.838965 
L 279.343692 -199.711505 
L 278.963992 -199.517089 
L 278.584291 -199.257807 
L 278.204591 -198.936544 
L 277.824891 -198.556992 
L 277.445191 -198.123636 
L 277.065491 -197.641715 
L 276.685791 -197.117168 
L 276.306091 -196.55655 
L 275.92639 -195.966929 
L 275.54669 -195.35576 
L 275.16699 -194.730744 
L 274.78729 -194.09967 
L 274.40759 -193.470245 
L 274.02789 -192.849921 
L 273.64819 -192.245725 
L 273.268489 -191.664086 
L 272.888789 -191.110679 
L 272.509089 -190.590287 
L 272.129389 -190.106673 
L 271.749689 -189.662489 
L 271.369989 -189.2592 
L 270.990289 -188.89705 
L 270.610588 -188.575044 
L 270.230888 -188.290972 
L 269.851188 -188.041454 
L 269.471488 -187.822015 
L 269.091788 -187.627187 
L 268.712088 -187.450624 
L 268.332388 -187.285243 
L 267.952687 -187.123369 
L 267.572987 -186.956899 
L 267.193287 -186.77746 
L 266.813587 -186.576577 
L 266.433887 -186.345832 
L 266.054187 -186.07702 
L 265.674487 -185.762298 
L 265.294786 -185.394322 
L 264.915086 -184.966371 
L 264.535386 -184.472457 
L 264.155686 -183.907427 
L 263.775986 -183.267042 
L 263.396286 -182.548047 
L 263.016585 -181.74822 
L 262.636885 -180.866409 
L 262.257185 -179.902554 
L 261.877485 -178.857691 
L 261.497785 -177.733938 
L 261.118085 -176.534473 
L 260.738385 -175.263487 
L 260.358684 -173.92613 
L 259.978984 -172.528433 
L 259.599284 -171.077227 
L 259.219584 -169.580039 
L 258.839884 -168.04498 
L 258.460184 -166.480625 
L 258.080484 -164.895882 
L 257.700783 -163.299858 
L 257.321083 -161.701716 
L 256.941383 -160.110543 
L 256.561683 -158.535208 
L 256.181983 -156.984237 
L 255.802283 -155.465688 
L 255.422583 -153.987045 
L 255.042882 -152.555121 
L 254.663182 -151.175977 
L 254.283482 -149.854862 
L 253.903782 -148.596168 
L 253.524082 -147.403406 
L 253.144382 -146.279198 
L 252.764682 -145.225291 
L 252.384981 -144.242585 
L 252.005281 -143.331175 
L 251.625581 -142.49041 
L 251.245881 -141.718959 
L 250.866181 -141.014889 
L 250.486481 -140.375744 
L 250.106781 -139.798632 
L 249.72708 -139.280312 
L 249.34738 -138.817274 
L 248.96768 -138.405827 
L 248.58798 -138.042168 
L 248.20828 -137.722457 
L 247.82858 -137.442879 
L 247.44888 -137.199696 
L 247.069179 -136.989293 
L 246.689479 -136.808218 
L 246.309779 -136.653212 
L 245.930079 -136.521224 
L 245.550379 -136.409432 
L 245.170679 -136.315248 
L 244.790979 -136.236318 
L 244.411278 -136.170522 
L 244.031578 -136.115965 
L 243.651878 -136.070966 
L 243.272178 -136.034046 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#p1d86597a8a)">
     <use xlink:href="#m1e1bdc6b3e" x="0" y="427.438437" style="fill: #ff7f0e; fill-opacity: 0.25; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="FillBetweenPolyCollection_6">
    <defs>
     <path id="m6f0b375746" d="M 243.141913 -135.965569 
L 243.141913 -135.885894 
L 243.521252 -135.885894 
L 243.900591 -135.885894 
L 244.27993 -135.885894 
L 244.659268 -135.885894 
L 245.038607 -135.885894 
L 245.417946 -135.885894 
L 245.797285 -135.885894 
L 246.176624 -135.885894 
L 246.555963 -135.885894 
L 246.935302 -135.885894 
L 247.314641 -135.885894 
L 247.69398 -135.885894 
L 248.073318 -135.885894 
L 248.452657 -135.885894 
L 248.831996 -135.885894 
L 249.211335 -135.885894 
L 249.590674 -135.885894 
L 249.970013 -135.885894 
L 250.349352 -135.885894 
L 250.728691 -135.885894 
L 251.10803 -135.885894 
L 251.487368 -135.885894 
L 251.866707 -135.885894 
L 252.246046 -135.885894 
L 252.625385 -135.885894 
L 253.004724 -135.885894 
L 253.384063 -135.885894 
L 253.763402 -135.885894 
L 254.142741 -135.885894 
L 254.522079 -135.885894 
L 254.901418 -135.885894 
L 255.280757 -135.885894 
L 255.660096 -135.885894 
L 256.039435 -135.885894 
L 256.418774 -135.885894 
L 256.798113 -135.885894 
L 257.177452 -135.885894 
L 257.556791 -135.885894 
L 257.936129 -135.885894 
L 258.315468 -135.885894 
L 258.694807 -135.885894 
L 259.074146 -135.885894 
L 259.453485 -135.885894 
L 259.832824 -135.885894 
L 260.212163 -135.885894 
L 260.591502 -135.885894 
L 260.97084 -135.885894 
L 261.350179 -135.885894 
L 261.729518 -135.885894 
L 262.108857 -135.885894 
L 262.488196 -135.885894 
L 262.867535 -135.885894 
L 263.246874 -135.885894 
L 263.626213 -135.885894 
L 264.005552 -135.885894 
L 264.38489 -135.885894 
L 264.764229 -135.885894 
L 265.143568 -135.885894 
L 265.522907 -135.885894 
L 265.902246 -135.885894 
L 266.281585 -135.885894 
L 266.660924 -135.885894 
L 267.040263 -135.885894 
L 267.419601 -135.885894 
L 267.79894 -135.885894 
L 268.178279 -135.885894 
L 268.557618 -135.885894 
L 268.936957 -135.885894 
L 269.316296 -135.885894 
L 269.695635 -135.885894 
L 270.074974 -135.885894 
L 270.454313 -135.885894 
L 270.833651 -135.885894 
L 271.21299 -135.885894 
L 271.592329 -135.885894 
L 271.971668 -135.885894 
L 272.351007 -135.885894 
L 272.730346 -135.885894 
L 273.109685 -135.885894 
L 273.489024 -135.885894 
L 273.868363 -135.885894 
L 274.247701 -135.885894 
L 274.62704 -135.885894 
L 275.006379 -135.885894 
L 275.385718 -135.885894 
L 275.765057 -135.885894 
L 276.144396 -135.885894 
L 276.523735 -135.885894 
L 276.903074 -135.885894 
L 277.282412 -135.885894 
L 277.661751 -135.885894 
L 278.04109 -135.885894 
L 278.420429 -135.885894 
L 278.799768 -135.885894 
L 279.179107 -135.885894 
L 279.558446 -135.885894 
L 279.937785 -135.885894 
L 280.317124 -135.885894 
L 280.696462 -135.885894 
L 281.075801 -135.885894 
L 281.45514 -135.885894 
L 281.834479 -135.885894 
L 282.213818 -135.885894 
L 282.593157 -135.885894 
L 282.972496 -135.885894 
L 283.351835 -135.885894 
L 283.731173 -135.885894 
L 284.110512 -135.885894 
L 284.489851 -135.885894 
L 284.86919 -135.885894 
L 285.248529 -135.885894 
L 285.627868 -135.885894 
L 286.007207 -135.885894 
L 286.386546 -135.885894 
L 286.765885 -135.885894 
L 287.145223 -135.885894 
L 287.524562 -135.885894 
L 287.903901 -135.885894 
L 288.28324 -135.885894 
L 288.662579 -135.885894 
L 289.041918 -135.885894 
L 289.421257 -135.885894 
L 289.800596 -135.885894 
L 290.179934 -135.885894 
L 290.559273 -135.885894 
L 290.938612 -135.885894 
L 291.317951 -135.885894 
L 291.69729 -135.885894 
L 292.076629 -135.885894 
L 292.455968 -135.885894 
L 292.835307 -135.885894 
L 293.214646 -135.885894 
L 293.593984 -135.885894 
L 293.973323 -135.885894 
L 294.352662 -135.885894 
L 294.732001 -135.885894 
L 295.11134 -135.885894 
L 295.490679 -135.885894 
L 295.870018 -135.885894 
L 296.249357 -135.885894 
L 296.628696 -135.885894 
L 297.008034 -135.885894 
L 297.387373 -135.885894 
L 297.766712 -135.885894 
L 298.146051 -135.885894 
L 298.52539 -135.885894 
L 298.904729 -135.885894 
L 299.284068 -135.885894 
L 299.663407 -135.885894 
L 300.042745 -135.885894 
L 300.422084 -135.885894 
L 300.801423 -135.885894 
L 301.180762 -135.885894 
L 301.560101 -135.885894 
L 301.93944 -135.885894 
L 302.318779 -135.885894 
L 302.698118 -135.885894 
L 303.077457 -135.885894 
L 303.456795 -135.885894 
L 303.836134 -135.885894 
L 304.215473 -135.885894 
L 304.594812 -135.885894 
L 304.974151 -135.885894 
L 305.35349 -135.885894 
L 305.732829 -135.885894 
L 306.112168 -135.885894 
L 306.491506 -135.885894 
L 306.870845 -135.885894 
L 307.250184 -135.885894 
L 307.629523 -135.885894 
L 308.008862 -135.885894 
L 308.388201 -135.885894 
L 308.76754 -135.885894 
L 309.146879 -135.885894 
L 309.526218 -135.885894 
L 309.905556 -135.885894 
L 310.284895 -135.885894 
L 310.664234 -135.885894 
L 311.043573 -135.885894 
L 311.422912 -135.885894 
L 311.802251 -135.885894 
L 312.18159 -135.885894 
L 312.560929 -135.885894 
L 312.940268 -135.885894 
L 313.319606 -135.885894 
L 313.698945 -135.885894 
L 314.078284 -135.885894 
L 314.457623 -135.885894 
L 314.836962 -135.885894 
L 315.216301 -135.885894 
L 315.59564 -135.885894 
L 315.974979 -135.885894 
L 316.354317 -135.885894 
L 316.733656 -135.885894 
L 317.112995 -135.885894 
L 317.492334 -135.885894 
L 317.871673 -135.885894 
L 318.251012 -135.885894 
L 318.630351 -135.885894 
L 318.630351 -135.967203 
L 318.630351 -135.967203 
L 318.251012 -135.988563 
L 317.871673 -136.014914 
L 317.492334 -136.047255 
L 317.112995 -136.086741 
L 316.733656 -136.134704 
L 316.354317 -136.192663 
L 315.974979 -136.262338 
L 315.59564 -136.345668 
L 315.216301 -136.444814 
L 314.836962 -136.562168 
L 314.457623 -136.700359 
L 314.078284 -136.862247 
L 313.698945 -137.050916 
L 313.319606 -137.269664 
L 312.940268 -137.521978 
L 312.560929 -137.811506 
L 312.18159 -138.142024 
L 311.802251 -138.517391 
L 311.422912 -138.941495 
L 311.043573 -139.418195 
L 310.664234 -139.951254 
L 310.284895 -140.544268 
L 309.905556 -141.200587 
L 309.526218 -141.923237 
L 309.146879 -142.714842 
L 308.76754 -143.577537 
L 308.388201 -144.512901 
L 308.008862 -145.521884 
L 307.629523 -146.604746 
L 307.250184 -147.76101 
L 306.870845 -148.989423 
L 306.491506 -150.287943 
L 306.112168 -151.653731 
L 305.732829 -153.083168 
L 305.35349 -154.571897 
L 304.974151 -156.114873 
L 304.594812 -157.706438 
L 304.215473 -159.340418 
L 303.836134 -161.010229 
L 303.456795 -162.708998 
L 303.077457 -164.429698 
L 302.698118 -166.165287 
L 302.318779 -167.908849 
L 301.93944 -169.653736 
L 301.560101 -171.393706 
L 301.180762 -173.123048 
L 300.801423 -174.836694 
L 300.422084 -176.530319 
L 300.042745 -178.20041 
L 299.663407 -179.844326 
L 299.284068 -181.460322 
L 298.904729 -183.047548 
L 298.52539 -184.606027 
L 298.146051 -186.136603 
L 297.766712 -187.640856 
L 297.387373 -189.121004 
L 297.008034 -190.579775 
L 296.628696 -192.02026 
L 296.249357 -193.445755 
L 295.870018 -194.859581 
L 295.490679 -196.264906 
L 295.11134 -197.664554 
L 294.732001 -199.060822 
L 294.352662 -200.455302 
L 293.973323 -201.848708 
L 293.593984 -203.240729 
L 293.214646 -204.629895 
L 292.835307 -206.013476 
L 292.455968 -207.387407 
L 292.076629 -208.746249 
L 291.69729 -210.083194 
L 291.317951 -211.390098 
L 290.938612 -212.657574 
L 290.559273 -213.875111 
L 290.179934 -215.031244 
L 289.800596 -216.113765 
L 289.421257 -217.109968 
L 289.041918 -218.006921 
L 288.662579 -218.791775 
L 288.28324 -219.452075 
L 287.903901 -219.976097 
L 287.524562 -220.353169 
L 287.145223 -220.573997 
L 286.765885 -220.630959 
L 286.386546 -220.518378 
L 286.007207 -220.232755 
L 285.627868 -219.772953 
L 285.248529 -219.140334 
L 284.86919 -218.338835 
L 284.489851 -217.374987 
L 284.110512 -216.257869 
L 283.731173 -214.999002 
L 283.351835 -213.612194 
L 282.972496 -212.113317 
L 282.593157 -210.520054 
L 282.213818 -208.851595 
L 281.834479 -207.128311 
L 281.45514 -205.371401 
L 281.075801 -203.602535 
L 280.696462 -201.843484 
L 280.317124 -200.11577 
L 279.937785 -198.440321 
L 279.558446 -196.837152 
L 279.179107 -195.325072 
L 278.799768 -193.921423 
L 278.420429 -192.641857 
L 278.04109 -191.500147 
L 277.661751 -190.508034 
L 277.282412 -189.675117 
L 276.903074 -189.008775 
L 276.523735 -188.514121 
L 276.144396 -188.193989 
L 275.765057 -188.04895 
L 275.385718 -188.077352 
L 275.006379 -188.275379 
L 274.62704 -188.637137 
L 274.247701 -189.154745 
L 273.868363 -189.818453 
L 273.489024 -190.616765 
L 273.109685 -191.536573 
L 272.730346 -192.563306 
L 272.351007 -193.681083 
L 271.971668 -194.872884 
L 271.592329 -196.120718 
L 271.21299 -197.40581 
L 270.833651 -198.708788 
L 270.454313 -200.009887 
L 270.074974 -201.289151 
L 269.695635 -202.526644 
L 269.316296 -203.702674 
L 268.936957 -204.798004 
L 268.557618 -205.794083 
L 268.178279 -206.67326 
L 267.79894 -207.419003 
L 267.419601 -208.016109 
L 267.040263 -208.450901 
L 266.660924 -208.711414 
L 266.281585 -208.787561 
L 265.902246 -208.671277 
L 265.522907 -208.35664 
L 265.143568 -207.839962 
L 264.764229 -207.119852 
L 264.38489 -206.197237 
L 264.005552 -205.075356 
L 263.626213 -203.759718 
L 263.246874 -202.258017 
L 262.867535 -200.580016 
L 262.488196 -198.737395 
L 262.108857 -196.743571 
L 261.729518 -194.613484 
L 261.350179 -192.363362 
L 260.97084 -190.010466 
L 260.591502 -187.57282 
L 260.212163 -185.068937 
L 259.832824 -182.517532 
L 259.453485 -179.937249 
L 259.074146 -177.346391 
L 258.694807 -174.762667 
L 258.315468 -172.20296 
L 257.936129 -169.683113 
L 257.556791 -167.217752 
L 257.177452 -164.820129 
L 256.798113 -162.502011 
L 256.418774 -160.273591 
L 256.039435 -158.143436 
L 255.660096 -156.118473 
L 255.280757 -154.204001 
L 254.901418 -152.403735 
L 254.522079 -150.719872 
L 254.142741 -149.153188 
L 253.763402 -147.703143 
L 253.384063 -146.368013 
L 253.004724 -145.14502 
L 252.625385 -144.03048 
L 252.246046 -143.019945 
L 251.866707 -142.108353 
L 251.487368 -141.290166 
L 251.10803 -140.559504 
L 250.728691 -139.910275 
L 250.349352 -139.336285 
L 249.970013 -138.831346 
L 249.590674 -138.389359 
L 249.211335 -138.004397 
L 248.831996 -137.670766 
L 248.452657 -137.383051 
L 248.073318 -137.136162 
L 247.69398 -136.925352 
L 247.314641 -136.746236 
L 246.935302 -136.594802 
L 246.555963 -136.467402 
L 246.176624 -136.36075 
L 245.797285 -136.271907 
L 245.417946 -136.198264 
L 245.038607 -136.137522 
L 244.659268 -136.087668 
L 244.27993 -136.046951 
L 243.900591 -136.013861 
L 243.521252 -135.987102 
L 243.141913 -135.965569 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#p1d86597a8a)">
     <use xlink:href="#m6f0b375746" x="0" y="427.438437" style="fill: #1f77b4; fill-opacity: 0.25; stroke: #1f77b4"/>
    </g>
   </g>
  </g>
  <g id="axes_14">
   <g id="FillBetweenPolyCollection_7">
    <defs>
     <path id="mb07e0989af" d="M 340.938699 -38.241931 
L 340.938699 -38.200781 
L 341.310199 -38.200781 
L 341.681698 -38.200781 
L 342.053197 -38.200781 
L 342.424697 -38.200781 
L 342.796196 -38.200781 
L 343.167695 -38.200781 
L 343.539194 -38.200781 
L 343.910694 -38.200781 
L 344.282193 -38.200781 
L 344.653692 -38.200781 
L 345.025192 -38.200781 
L 345.396691 -38.200781 
L 345.76819 -38.200781 
L 346.139689 -38.200781 
L 346.511189 -38.200781 
L 346.882688 -38.200781 
L 347.254187 -38.200781 
L 347.625687 -38.200781 
L 347.997186 -38.200781 
L 348.368685 -38.200781 
L 348.740185 -38.200781 
L 349.111684 -38.200781 
L 349.483183 -38.200781 
L 349.854682 -38.200781 
L 350.226182 -38.200781 
L 350.597681 -38.200781 
L 350.96918 -38.200781 
L 351.34068 -38.200781 
L 351.712179 -38.200781 
L 352.083678 -38.200781 
L 352.455177 -38.200781 
L 352.826677 -38.200781 
L 353.198176 -38.200781 
L 353.569675 -38.200781 
L 353.941175 -38.200781 
L 354.312674 -38.200781 
L 354.684173 -38.200781 
L 355.055672 -38.200781 
L 355.427172 -38.200781 
L 355.798671 -38.200781 
L 356.17017 -38.200781 
L 356.54167 -38.200781 
L 356.913169 -38.200781 
L 357.284668 -38.200781 
L 357.656167 -38.200781 
L 358.027667 -38.200781 
L 358.399166 -38.200781 
L 358.770665 -38.200781 
L 359.142165 -38.200781 
L 359.513664 -38.200781 
L 359.885163 -38.200781 
L 360.256662 -38.200781 
L 360.628162 -38.200781 
L 360.999661 -38.200781 
L 361.37116 -38.200781 
L 361.74266 -38.200781 
L 362.114159 -38.200781 
L 362.485658 -38.200781 
L 362.857157 -38.200781 
L 363.228657 -38.200781 
L 363.600156 -38.200781 
L 363.971655 -38.200781 
L 364.343155 -38.200781 
L 364.714654 -38.200781 
L 365.086153 -38.200781 
L 365.457652 -38.200781 
L 365.829152 -38.200781 
L 366.200651 -38.200781 
L 366.57215 -38.200781 
L 366.94365 -38.200781 
L 367.315149 -38.200781 
L 367.686648 -38.200781 
L 368.058147 -38.200781 
L 368.429647 -38.200781 
L 368.801146 -38.200781 
L 369.172645 -38.200781 
L 369.544145 -38.200781 
L 369.915644 -38.200781 
L 370.287143 -38.200781 
L 370.658643 -38.200781 
L 371.030142 -38.200781 
L 371.401641 -38.200781 
L 371.77314 -38.200781 
L 372.14464 -38.200781 
L 372.516139 -38.200781 
L 372.887638 -38.200781 
L 373.259138 -38.200781 
L 373.630637 -38.200781 
L 374.002136 -38.200781 
L 374.373635 -38.200781 
L 374.745135 -38.200781 
L 375.116634 -38.200781 
L 375.488133 -38.200781 
L 375.859633 -38.200781 
L 376.231132 -38.200781 
L 376.602631 -38.200781 
L 376.97413 -38.200781 
L 377.34563 -38.200781 
L 377.717129 -38.200781 
L 378.088628 -38.200781 
L 378.460128 -38.200781 
L 378.831627 -38.200781 
L 379.203126 -38.200781 
L 379.574625 -38.200781 
L 379.946125 -38.200781 
L 380.317624 -38.200781 
L 380.689123 -38.200781 
L 381.060623 -38.200781 
L 381.432122 -38.200781 
L 381.803621 -38.200781 
L 382.17512 -38.200781 
L 382.54662 -38.200781 
L 382.918119 -38.200781 
L 383.289618 -38.200781 
L 383.661118 -38.200781 
L 384.032617 -38.200781 
L 384.404116 -38.200781 
L 384.775615 -38.200781 
L 385.147115 -38.200781 
L 385.518614 -38.200781 
L 385.890113 -38.200781 
L 386.261613 -38.200781 
L 386.633112 -38.200781 
L 387.004611 -38.200781 
L 387.37611 -38.200781 
L 387.74761 -38.200781 
L 388.119109 -38.200781 
L 388.490608 -38.200781 
L 388.862108 -38.200781 
L 389.233607 -38.200781 
L 389.605106 -38.200781 
L 389.976606 -38.200781 
L 390.348105 -38.200781 
L 390.719604 -38.200781 
L 391.091103 -38.200781 
L 391.462603 -38.200781 
L 391.834102 -38.200781 
L 392.205601 -38.200781 
L 392.577101 -38.200781 
L 392.9486 -38.200781 
L 393.320099 -38.200781 
L 393.691598 -38.200781 
L 394.063098 -38.200781 
L 394.434597 -38.200781 
L 394.806096 -38.200781 
L 395.177596 -38.200781 
L 395.549095 -38.200781 
L 395.920594 -38.200781 
L 396.292093 -38.200781 
L 396.663593 -38.200781 
L 397.035092 -38.200781 
L 397.406591 -38.200781 
L 397.778091 -38.200781 
L 398.14959 -38.200781 
L 398.521089 -38.200781 
L 398.892588 -38.200781 
L 399.264088 -38.200781 
L 399.635587 -38.200781 
L 400.007086 -38.200781 
L 400.378586 -38.200781 
L 400.750085 -38.200781 
L 401.121584 -38.200781 
L 401.493083 -38.200781 
L 401.864583 -38.200781 
L 402.236082 -38.200781 
L 402.607581 -38.200781 
L 402.979081 -38.200781 
L 403.35058 -38.200781 
L 403.722079 -38.200781 
L 404.093578 -38.200781 
L 404.465078 -38.200781 
L 404.836577 -38.200781 
L 405.208076 -38.200781 
L 405.579576 -38.200781 
L 405.951075 -38.200781 
L 406.322574 -38.200781 
L 406.694073 -38.200781 
L 407.065573 -38.200781 
L 407.437072 -38.200781 
L 407.808571 -38.200781 
L 408.180071 -38.200781 
L 408.55157 -38.200781 
L 408.923069 -38.200781 
L 409.294568 -38.200781 
L 409.666068 -38.200781 
L 410.037567 -38.200781 
L 410.409066 -38.200781 
L 410.780566 -38.200781 
L 411.152065 -38.200781 
L 411.523564 -38.200781 
L 411.895064 -38.200781 
L 412.266563 -38.200781 
L 412.638062 -38.200781 
L 413.009561 -38.200781 
L 413.381061 -38.200781 
L 413.75256 -38.200781 
L 414.124059 -38.200781 
L 414.495559 -38.200781 
L 414.867058 -38.200781 
L 414.867058 -38.267881 
L 414.867058 -38.267881 
L 414.495559 -38.285539 
L 414.124059 -38.307349 
L 413.75256 -38.334154 
L 413.381061 -38.366936 
L 413.009561 -38.40683 
L 412.638062 -38.455141 
L 412.266563 -38.513359 
L 411.895064 -38.58317 
L 411.523564 -38.666475 
L 411.152065 -38.765397 
L 410.780566 -38.882292 
L 410.409066 -39.019753 
L 410.037567 -39.180614 
L 409.666068 -39.367945 
L 409.294568 -39.585046 
L 408.923069 -39.835432 
L 408.55157 -40.122811 
L 408.180071 -40.451056 
L 407.808571 -40.824173 
L 407.437072 -41.246253 
L 407.065573 -41.721423 
L 406.694073 -42.253789 
L 406.322574 -42.847369 
L 405.951075 -43.50602 
L 405.579576 -44.233364 
L 405.208076 -45.032704 
L 404.836577 -45.906942 
L 404.465078 -46.858499 
L 404.093578 -47.889224 
L 403.722079 -49.000324 
L 403.35058 -50.192284 
L 402.979081 -51.464809 
L 402.607581 -52.816761 
L 402.236082 -54.246125 
L 401.864583 -55.749976 
L 401.493083 -57.324467 
L 401.121584 -58.964838 
L 400.750085 -60.665433 
L 400.378586 -62.419746 
L 400.007086 -64.22048 
L 399.635587 -66.05962 
L 399.264088 -67.92853 
L 398.892588 -69.818056 
L 398.521089 -71.71865 
L 398.14959 -73.620494 
L 397.778091 -75.513637 
L 397.406591 -77.388133 
L 397.035092 -79.234176 
L 396.663593 -81.042237 
L 396.292093 -82.80319 
L 395.920594 -84.508426 
L 395.549095 -86.149957 
L 395.177596 -87.720508 
L 394.806096 -89.213581 
L 394.434597 -90.623517 
L 394.063098 -91.945522 
L 393.691598 -93.175688 
L 393.320099 -94.31099 
L 392.9486 -95.349267 
L 392.577101 -96.289187 
L 392.205601 -97.130207 
L 391.834102 -97.872513 
L 391.462603 -98.516957 
L 391.091103 -99.064996 
L 390.719604 -99.518621 
L 390.348105 -99.880288 
L 389.976606 -100.152856 
L 389.605106 -100.339529 
L 389.233607 -100.443801 
L 388.862108 -100.469409 
L 388.490608 -100.420297 
L 388.119109 -100.300578 
L 387.74761 -100.114513 
L 387.37611 -99.866484 
L 387.004611 -99.560979 
L 386.633112 -99.202575 
L 386.261613 -98.795921 
L 385.890113 -98.345725 
L 385.518614 -97.856729 
L 385.147115 -97.333695 
L 384.775615 -96.781375 
L 384.404116 -96.204481 
L 384.032617 -95.607657 
L 383.661118 -94.99544 
L 383.289618 -94.37222 
L 382.918119 -93.742207 
L 382.54662 -93.109386 
L 382.17512 -92.477485 
L 381.803621 -91.84994 
L 381.432122 -91.229867 
L 381.060623 -90.62004 
L 380.689123 -90.022876 
L 380.317624 -89.440427 
L 379.946125 -88.874382 
L 379.574625 -88.326075 
L 379.203126 -87.796502 
L 378.831627 -87.286345 
L 378.460128 -86.795999 
L 378.088628 -86.32561 
L 377.717129 -85.875107 
L 377.34563 -85.444244 
L 376.97413 -85.032636 
L 376.602631 -84.639798 
L 376.231132 -84.265174 
L 375.859633 -83.908171 
L 375.488133 -83.568174 
L 375.116634 -83.244571 
L 374.745135 -82.936754 
L 374.373635 -82.644123 
L 374.002136 -82.366081 
L 373.630637 -82.102013 
L 373.259138 -81.851274 
L 372.887638 -81.613154 
L 372.516139 -81.386851 
L 372.14464 -81.171432 
L 371.77314 -80.965801 
L 371.401641 -80.768659 
L 371.030142 -80.578469 
L 370.658643 -80.39343 
L 370.287143 -80.211449 
L 369.915644 -80.030125 
L 369.544145 -79.846744 
L 369.172645 -79.658279 
L 368.801146 -79.461412 
L 368.429647 -79.252555 
L 368.058147 -79.027895 
L 367.686648 -78.783445 
L 367.315149 -78.515108 
L 366.94365 -78.21875 
L 366.57215 -77.890282 
L 366.200651 -77.525746 
L 365.829152 -77.121407 
L 365.457652 -76.673842 
L 365.086153 -76.180024 
L 364.714654 -75.637411 
L 364.343155 -75.044012 
L 363.971655 -74.398453 
L 363.600156 -73.700025 
L 363.228657 -72.948718 
L 362.857157 -72.145237 
L 362.485658 -71.291007 
L 362.114159 -70.388153 
L 361.74266 -69.439471 
L 361.37116 -68.448383 
L 360.999661 -67.418872 
L 360.628162 -66.355419 
L 360.256662 -65.262914 
L 359.885163 -64.146577 
L 359.513664 -63.011865 
L 359.142165 -61.86438 
L 358.770665 -60.709781 
L 358.399166 -59.553698 
L 358.027667 -58.401648 
L 357.656167 -57.258966 
L 357.284668 -56.130734 
L 356.913169 -55.021728 
L 356.54167 -53.936371 
L 356.17017 -52.878694 
L 355.798671 -51.85231 
L 355.427172 -50.860395 
L 355.055672 -49.905678 
L 354.684173 -48.99044 
L 354.312674 -48.116517 
L 353.941175 -47.285311 
L 353.569675 -46.497809 
L 353.198176 -45.754598 
L 352.826677 -45.055893 
L 352.455177 -44.40156 
L 352.083678 -43.791145 
L 351.712179 -43.223906 
L 351.34068 -42.698839 
L 350.96918 -42.214711 
L 350.597681 -41.770092 
L 350.226182 -41.363384 
L 349.854682 -40.992849 
L 349.483183 -40.656642 
L 349.111684 -40.352837 
L 348.740185 -40.079451 
L 348.368685 -39.834473 
L 347.997186 -39.615887 
L 347.625687 -39.421689 
L 347.254187 -39.24991 
L 346.882688 -39.098631 
L 346.511189 -38.966 
L 346.139689 -38.850242 
L 345.76819 -38.749671 
L 345.396691 -38.662695 
L 345.025192 -38.587827 
L 344.653692 -38.523682 
L 344.282193 -38.468985 
L 343.910694 -38.422565 
L 343.539194 -38.38336 
L 343.167695 -38.350408 
L 342.796196 -38.322846 
L 342.424697 -38.299906 
L 342.053197 -38.280906 
L 341.681698 -38.265248 
L 341.310199 -38.252408 
L 340.938699 -38.241931 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#pf421431600)">
     <use xlink:href="#mb07e0989af" x="0" y="427.438437" style="fill: #ff7f0e; fill-opacity: 0.25; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="FillBetweenPolyCollection_8">
    <defs>
     <path id="m0d48a5ddb8" d="M 339.176464 -38.234202 
L 339.176464 -38.200781 
L 339.533605 -38.200781 
L 339.890747 -38.200781 
L 340.247888 -38.200781 
L 340.60503 -38.200781 
L 340.962171 -38.200781 
L 341.319313 -38.200781 
L 341.676454 -38.200781 
L 342.033596 -38.200781 
L 342.390737 -38.200781 
L 342.747879 -38.200781 
L 343.10502 -38.200781 
L 343.462161 -38.200781 
L 343.819303 -38.200781 
L 344.176444 -38.200781 
L 344.533586 -38.200781 
L 344.890727 -38.200781 
L 345.247869 -38.200781 
L 345.60501 -38.200781 
L 345.962152 -38.200781 
L 346.319293 -38.200781 
L 346.676435 -38.200781 
L 347.033576 -38.200781 
L 347.390718 -38.200781 
L 347.747859 -38.200781 
L 348.105 -38.200781 
L 348.462142 -38.200781 
L 348.819283 -38.200781 
L 349.176425 -38.200781 
L 349.533566 -38.200781 
L 349.890708 -38.200781 
L 350.247849 -38.200781 
L 350.604991 -38.200781 
L 350.962132 -38.200781 
L 351.319274 -38.200781 
L 351.676415 -38.200781 
L 352.033556 -38.200781 
L 352.390698 -38.200781 
L 352.747839 -38.200781 
L 353.104981 -38.200781 
L 353.462122 -38.200781 
L 353.819264 -38.200781 
L 354.176405 -38.200781 
L 354.533547 -38.200781 
L 354.890688 -38.200781 
L 355.24783 -38.200781 
L 355.604971 -38.200781 
L 355.962113 -38.200781 
L 356.319254 -38.200781 
L 356.676395 -38.200781 
L 357.033537 -38.200781 
L 357.390678 -38.200781 
L 357.74782 -38.200781 
L 358.104961 -38.200781 
L 358.462103 -38.200781 
L 358.819244 -38.200781 
L 359.176386 -38.200781 
L 359.533527 -38.200781 
L 359.890669 -38.200781 
L 360.24781 -38.200781 
L 360.604951 -38.200781 
L 360.962093 -38.200781 
L 361.319234 -38.200781 
L 361.676376 -38.200781 
L 362.033517 -38.200781 
L 362.390659 -38.200781 
L 362.7478 -38.200781 
L 363.104942 -38.200781 
L 363.462083 -38.200781 
L 363.819225 -38.200781 
L 364.176366 -38.200781 
L 364.533508 -38.200781 
L 364.890649 -38.200781 
L 365.24779 -38.200781 
L 365.604932 -38.200781 
L 365.962073 -38.200781 
L 366.319215 -38.200781 
L 366.676356 -38.200781 
L 367.033498 -38.200781 
L 367.390639 -38.200781 
L 367.747781 -38.200781 
L 368.104922 -38.200781 
L 368.462064 -38.200781 
L 368.819205 -38.200781 
L 369.176346 -38.200781 
L 369.533488 -38.200781 
L 369.890629 -38.200781 
L 370.247771 -38.200781 
L 370.604912 -38.200781 
L 370.962054 -38.200781 
L 371.319195 -38.200781 
L 371.676337 -38.200781 
L 372.033478 -38.200781 
L 372.39062 -38.200781 
L 372.747761 -38.200781 
L 373.104903 -38.200781 
L 373.462044 -38.200781 
L 373.819185 -38.200781 
L 374.176327 -38.200781 
L 374.533468 -38.200781 
L 374.89061 -38.200781 
L 375.247751 -38.200781 
L 375.604893 -38.200781 
L 375.962034 -38.200781 
L 376.319176 -38.200781 
L 376.676317 -38.200781 
L 377.033459 -38.200781 
L 377.3906 -38.200781 
L 377.747741 -38.200781 
L 378.104883 -38.200781 
L 378.462024 -38.200781 
L 378.819166 -38.200781 
L 379.176307 -38.200781 
L 379.533449 -38.200781 
L 379.89059 -38.200781 
L 380.247732 -38.200781 
L 380.604873 -38.200781 
L 380.962015 -38.200781 
L 381.319156 -38.200781 
L 381.676298 -38.200781 
L 382.033439 -38.200781 
L 382.39058 -38.200781 
L 382.747722 -38.200781 
L 383.104863 -38.200781 
L 383.462005 -38.200781 
L 383.819146 -38.200781 
L 384.176288 -38.200781 
L 384.533429 -38.200781 
L 384.890571 -38.200781 
L 385.247712 -38.200781 
L 385.604854 -38.200781 
L 385.961995 -38.200781 
L 386.319137 -38.200781 
L 386.676278 -38.200781 
L 387.033419 -38.200781 
L 387.390561 -38.200781 
L 387.747702 -38.200781 
L 388.104844 -38.200781 
L 388.461985 -38.200781 
L 388.819127 -38.200781 
L 389.176268 -38.200781 
L 389.53341 -38.200781 
L 389.890551 -38.200781 
L 390.247693 -38.200781 
L 390.604834 -38.200781 
L 390.961975 -38.200781 
L 391.319117 -38.200781 
L 391.676258 -38.200781 
L 392.0334 -38.200781 
L 392.390541 -38.200781 
L 392.747683 -38.200781 
L 393.104824 -38.200781 
L 393.461966 -38.200781 
L 393.819107 -38.200781 
L 394.176249 -38.200781 
L 394.53339 -38.200781 
L 394.890532 -38.200781 
L 395.247673 -38.200781 
L 395.604814 -38.200781 
L 395.961956 -38.200781 
L 396.319097 -38.200781 
L 396.676239 -38.200781 
L 397.03338 -38.200781 
L 397.390522 -38.200781 
L 397.747663 -38.200781 
L 398.104805 -38.200781 
L 398.461946 -38.200781 
L 398.819088 -38.200781 
L 399.176229 -38.200781 
L 399.53337 -38.200781 
L 399.890512 -38.200781 
L 400.247653 -38.200781 
L 400.604795 -38.200781 
L 400.961936 -38.200781 
L 401.319078 -38.200781 
L 401.676219 -38.200781 
L 402.033361 -38.200781 
L 402.390502 -38.200781 
L 402.747644 -38.200781 
L 403.104785 -38.200781 
L 403.461927 -38.200781 
L 403.819068 -38.200781 
L 404.176209 -38.200781 
L 404.533351 -38.200781 
L 404.890492 -38.200781 
L 405.247634 -38.200781 
L 405.604775 -38.200781 
L 405.961917 -38.200781 
L 406.319058 -38.200781 
L 406.6762 -38.200781 
L 407.033341 -38.200781 
L 407.390483 -38.200781 
L 407.747624 -38.200781 
L 408.104765 -38.200781 
L 408.461907 -38.200781 
L 408.819048 -38.200781 
L 409.17619 -38.200781 
L 409.533331 -38.200781 
L 409.890473 -38.200781 
L 410.247614 -38.200781 
L 410.247614 -38.359145 
L 410.247614 -38.359145 
L 409.890473 -38.404049 
L 409.533331 -38.460093 
L 409.17619 -38.529578 
L 408.819048 -38.61515 
L 408.461907 -38.719832 
L 408.104765 -38.847033 
L 407.747624 -39.00056 
L 407.390483 -39.184616 
L 407.033341 -39.403784 
L 406.6762 -39.663001 
L 406.319058 -39.967508 
L 405.961917 -40.32279 
L 405.604775 -40.734489 
L 405.247634 -41.208305 
L 404.890492 -41.749873 
L 404.533351 -42.364622 
L 404.176209 -43.057624 
L 403.819068 -43.833422 
L 403.461927 -44.695859 
L 403.104785 -45.647904 
L 402.747644 -46.691475 
L 402.390502 -47.827281 
L 402.033361 -49.054682 
L 401.676219 -50.371571 
L 401.319078 -51.774289 
L 400.961936 -53.257588 
L 400.604795 -54.814624 
L 400.247653 -56.437015 
L 399.890512 -58.114937 
L 399.53337 -59.837277 
L 399.176229 -61.591835 
L 398.819088 -63.365572 
L 398.461946 -65.144894 
L 398.104805 -66.915969 
L 397.747663 -68.665067 
L 397.390522 -70.378909 
L 397.03338 -72.045014 
L 396.676239 -73.652031 
L 396.319097 -75.190055 
L 395.961956 -76.650892 
L 395.604814 -78.028291 
L 395.247673 -79.318112 
L 394.890532 -80.518435 
L 394.53339 -81.629607 
L 394.176249 -82.654217 
L 393.819107 -83.597002 
L 393.461966 -84.464698 
L 393.104824 -85.265817 
L 392.747683 -86.010387 
L 392.390541 -86.709633 
L 392.0334 -87.375636 
L 391.676258 -88.020961 
L 391.319117 -88.658275 
L 390.961975 -89.299965 
L 390.604834 -89.957767 
L 390.247693 -90.642416 
L 389.890551 -91.36333 
L 389.53341 -92.128334 
L 389.176268 -92.943435 
L 388.819127 -93.812656 
L 388.461985 -94.737924 
L 388.104844 -95.719035 
L 387.747702 -96.753672 
L 387.390561 -97.837504 
L 387.033419 -98.964334 
L 386.676278 -100.126318 
L 386.319137 -101.314234 
L 385.961995 -102.517788 
L 385.604854 -103.725973 
L 385.247712 -104.927432 
L 384.890571 -106.110844 
L 384.533429 -107.265306 
L 384.176288 -108.3807 
L 383.819146 -109.448022 
L 383.462005 -110.459683 
L 383.104863 -111.409741 
L 382.747722 -112.294079 
L 382.39058 -113.110505 
L 382.033439 -113.858774 
L 381.676298 -114.540539 
L 381.319156 -115.159209 
L 380.962015 -115.719751 
L 380.604873 -116.22841 
L 380.247732 -116.692393 
L 379.89059 -117.119498 
L 379.533449 -117.517728 
L 379.176307 -117.894902 
L 378.819166 -118.258266 
L 378.462024 -118.614153 
L 378.104883 -118.96767 
L 377.747741 -119.322463 
L 377.3906 -119.680539 
L 377.033459 -120.042185 
L 376.676317 -120.405951 
L 376.319176 -120.768732 
L 375.962034 -121.12592 
L 375.604893 -121.471623 
L 375.247751 -121.798942 
L 374.89061 -122.100289 
L 374.533468 -122.367724 
L 374.176327 -122.593297 
L 373.819185 -122.769378 
L 373.462044 -122.888947 
L 373.104903 -122.945846 
L 372.747761 -122.934967 
L 372.39062 -122.852371 
L 372.033478 -122.695334 
L 371.676337 -122.462327 
L 371.319195 -122.15292 
L 370.962054 -121.767631 
L 370.604912 -121.30772 
L 370.247771 -120.774959 
L 369.890629 -120.171371 
L 369.533488 -119.49898 
L 369.176346 -118.759563 
L 368.819205 -117.954446 
L 368.462064 -117.084327 
L 368.104922 -116.149174 
L 367.747781 -115.148166 
L 367.390639 -114.079713 
L 367.033498 -112.941531 
L 366.676356 -111.730789 
L 366.319215 -110.444301 
L 365.962073 -109.078767 
L 365.604932 -107.631041 
L 365.24779 -106.098419 
L 364.890649 -104.478925 
L 364.533508 -102.771583 
L 364.176366 -100.976658 
L 363.819225 -99.09586 
L 363.462083 -97.132486 
L 363.104942 -95.091511 
L 362.7478 -92.979601 
L 362.390659 -90.80507 
L 362.033517 -88.577763 
L 361.676376 -86.308876 
L 361.319234 -84.010731 
L 360.962093 -81.696497 
L 360.604951 -79.379883 
L 360.24781 -77.074815 
L 359.890669 -74.7951 
L 359.533527 -72.554102 
L 359.176386 -70.364437 
L 358.819244 -68.237699 
L 358.462103 -66.184226 
L 358.104961 -64.21291 
L 357.74782 -62.331065 
L 357.390678 -60.544345 
L 357.033537 -58.856715 
L 356.676395 -57.270481 
L 356.319254 -55.786357 
L 355.962113 -54.403582 
L 355.604971 -53.120066 
L 355.24783 -51.932569 
L 354.890688 -50.836889 
L 354.533547 -49.828066 
L 354.176405 -48.900587 
L 353.819264 -48.048585 
L 353.462122 -47.266023 
L 353.104981 -46.546862 
L 352.747839 -45.885214 
L 352.390698 -45.275462 
L 352.033556 -44.712357 
L 351.676415 -44.191091 
L 351.319274 -43.707345 
L 350.962132 -43.257309 
L 350.604991 -42.837688 
L 350.247849 -42.445678 
L 349.890708 -42.078941 
L 349.533566 -41.735559 
L 349.176425 -41.41398 
L 348.819283 -41.112962 
L 348.462142 -40.831518 
L 348.105 -40.568855 
L 347.747859 -40.324319 
L 347.390718 -40.097349 
L 347.033576 -39.887433 
L 346.676435 -39.69407 
L 346.319293 -39.516746 
L 345.962152 -39.354912 
L 345.60501 -39.207969 
L 345.247869 -39.075266 
L 344.890727 -38.956093 
L 344.533586 -38.849693 
L 344.176444 -38.755263 
L 343.819303 -38.671966 
L 343.462161 -38.598947 
L 343.10502 -38.535341 
L 342.747879 -38.480288 
L 342.390737 -38.432945 
L 342.033596 -38.392496 
L 341.676454 -38.358164 
L 341.319313 -38.329215 
L 340.962171 -38.304967 
L 340.60503 -38.28479 
L 340.247888 -38.268112 
L 339.890747 -38.254419 
L 339.533605 -38.24325 
L 339.176464 -38.234202 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#pf421431600)">
     <use xlink:href="#m0d48a5ddb8" x="0" y="427.438437" style="fill: #1f77b4; fill-opacity: 0.25; stroke: #1f77b4"/>
    </g>
   </g>
  </g>
  <g id="legend_1">
   <g id="text_25">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="439.328919" y="201.316484" transform="rotate(-0 439.328919 201.316484)">garden</text>
   </g>
   <g id="line2d_53">
    <defs>
     <path id="m337eb76d3d" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #ffffff; stroke-width: 0.48"/>
    </defs>
    <g>
     <use xlink:href="#m337eb76d3d" x="440.403137" y="212.817266" style="fill: #1f77b4; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="text_26">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="458.403137" y="216.317266" transform="rotate(-0 458.403137 216.317266)">False</text>
   </g>
   <g id="line2d_54">
    <defs>
     <path id="maa3836e418" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #ffffff; stroke-width: 0.48"/>
    </defs>
    <g>
     <use xlink:href="#maa3836e418" x="440.403137" y="227.818047" style="fill: #ff7f0e; stroke: #ffffff; stroke-width: 0.48"/>
    </g>
   </g>
   <g id="text_27">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="458.403137" y="231.318047" transform="rotate(-0 458.403137 231.318047)">True</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p6b281bf15b">
   <rect x="47.288281" y="104.885113" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p6772a0ed96">
   <rect x="47.288281" y="202.570225" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p357400d104">
   <rect x="143.322832" y="202.570225" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p81824977ec">
   <rect x="47.288281" y="300.255338" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p8e9919d5b5">
   <rect x="143.322832" y="300.255338" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="pd97e1f90e5">
   <rect x="239.357383" y="300.255338" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="pc960d48d48">
   <rect x="47.288281" y="7.2" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p4df8b4f7b9">
   <rect x="143.322832" y="104.885113" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="p1d86597a8a">
   <rect x="239.357383" y="202.570225" width="83.259653" height="88.982318"/>
  </clipPath>
  <clipPath id="pf421431600">
   <rect x="335.391934" y="300.255338" width="83.259653" height="88.982318"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Distributions on the diagonal, pairwise relationships below.</figcaption>
</figure>

## How to read it

- Four numeric columns give a 4 × 4 grid; `corner=True` drops the symmetric
  upper half (a mirror of the same charts).
- In the `price` row there is a clearly rising band with `size` (correlation
  0.95) and a slightly falling trend with `age` (−0.32). `rooms` also looks
  related to price, but the real cause is the size of the home; rooms are a
  consequence of it.
- `hue="garden"` colours the points by a category; if the groups form
  separate clusters, it shows at a glance.

## When, and when not?

- A first look for exploration: in a few minutes it catches outliers, skewed
  distributions and strong relationships.
- The grid grows with the square of the column count: 20 columns means 400
  cells, unreadable and slow. Then pick the relevant columns with `corr()`
  first (`vars=[...]`).
- It is a chart for you, not for a report. When presenting, a chart that
  clearly shows a single relationship is better.
