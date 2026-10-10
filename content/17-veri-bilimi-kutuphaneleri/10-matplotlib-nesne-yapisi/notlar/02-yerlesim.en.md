`plt.subplots(2, 3)` opens all areas at the same size. In a report, though,
there is often one large **main** chart with smaller ones beside it. The most
readable way to do this is `subplot_mosaic`: you write the layout **like a
picture**.

```python
import matplotlib.pyplot as plt

layout = [["main", "main", "side"],
          ["main", "main", "low"]]
fig, axd = plt.subplot_mosaic(layout, figsize=(7, 3.2), layout="constrained")
axd["main"].plot([1, 2, 3, 4, 5], [3, 5, 4, 7, 6], marker="o")
axd["main"].set_title("Daily visitors")
axd["side"].bar(["A", "B"], [4, 7])
axd["side"].set_title("By channel")
axd["low"].hist([1, 2, 2, 3, 3, 3, 4], bins=4)
axd["low"].set_title("Distribution")
print(sorted(axd), len(fig.axes))
print(axd["main"].get_subplotspec().rowspan, axd["main"].get_subplotspec().colspan)
```

```text
['low', 'main', 'side'] 3
range(0, 2) range(0, 2)
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="512.39952pt" height="238.79952pt" viewBox="0 0 512.39952 238.79952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 238.79952 
L 512.39952 238.79952 
L 512.39952 0 
L 0 0 
L 0 238.79952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 30.103125 214.59952 
L 327.564985 214.59952 
L 327.564985 22.318125 
L 30.103125 22.318125 
L 30.103125 214.59952 
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
       <use xlink:href="#m15aed4d867" x="43.624119" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="43.624119" y="229.197176" transform="rotate(-0 43.624119 229.197176)">1.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="77.426603" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="77.426603" y="229.197176" transform="rotate(-0 77.426603 229.197176)">1.5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="111.229087" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="111.229087" y="229.197176" transform="rotate(-0 111.229087 229.197176)">2.0</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="145.031571" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="145.031571" y="229.197176" transform="rotate(-0 145.031571 229.197176)">2.5</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="178.834055" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="178.834055" y="229.197176" transform="rotate(-0 178.834055 229.197176)">3.0</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="212.636539" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="212.636539" y="229.197176" transform="rotate(-0 212.636539 229.197176)">3.5</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="246.439023" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="246.439023" y="229.197176" transform="rotate(-0 246.439023 229.197176)">4.0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="280.241507" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="280.241507" y="229.197176" transform="rotate(-0 280.241507 229.197176)">4.5</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="314.043991" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="314.043991" y="229.197176" transform="rotate(-0 314.043991 229.197176)">5.0</text>
     </g>
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
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="205.859457" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="209.658285" transform="rotate(-0 23.103125 209.658285)">3.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="184.009298" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="187.808126" transform="rotate(-0 23.103125 187.808126)">3.5</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="162.15914" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="165.957968" transform="rotate(-0 23.103125 165.957968)">4.0</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="140.308981" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="144.107809" transform="rotate(-0 23.103125 144.107809)">4.5</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="118.458822" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="122.257651" transform="rotate(-0 23.103125 122.257651)">5.0</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_15">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="96.608664" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="100.407492" transform="rotate(-0 23.103125 100.407492)">5.5</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_16">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="74.758505" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="78.557334" transform="rotate(-0 23.103125 78.557334)">6.0</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_17">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="52.908347" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="56.707175" transform="rotate(-0 23.103125 56.707175)">6.5</text>
     </g>
    </g>
    <g id="ytick_9">
     <g id="line2d_18">
      <g>
       <use xlink:href="#m5c8d5162d3" x="30.103125" y="31.058188" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_18">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="23.103125" y="34.857017" transform="rotate(-0 23.103125 34.857017)">7.0</text>
     </g>
    </g>
   </g>
   <g id="line2d_19">
    <path d="M 43.624119 205.859457 
L 111.229087 118.458822 
L 178.834055 162.15914 
L 246.439023 31.058188 
L 314.043991 74.758505 
" clip-path="url(#p0187f0c997)" style="fill: none; stroke: #1f77b4; stroke-width: 1.5; stroke-linecap: square"/>
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
    <g clip-path="url(#p0187f0c997)">
     <use xlink:href="#m98ae7f93d8" x="43.624119" y="205.859457" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="111.229087" y="118.458822" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="178.834055" y="162.15914" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="246.439023" y="31.058188" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m98ae7f93d8" x="314.043991" y="74.758505" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 30.103125 214.59952 
L 30.103125 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 327.564985 214.59952 
L 327.564985 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 30.103125 214.59952 
L 327.564985 214.59952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 30.103125 22.318125 
L 327.564985 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_19">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="178.834055" y="16.318125" transform="rotate(-0 178.834055 16.318125)">Daily visitors</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 356.46859 99.39952 
L 505.19952 99.39952 
L 505.19952 22.318125 
L 356.46859 22.318125 
L 356.46859 99.39952 
z
" style="fill: none"/>
   </g>
   <g id="patch_8">
    <path d="M 363.229087 99.39952 
L 423.322392 99.39952 
L 423.322392 57.450461 
L 363.229087 57.450461 
z
" clip-path="url(#pa4eb8babdb)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_9">
    <path d="M 438.345718 99.39952 
L 498.439023 99.39952 
L 498.439023 25.988668 
L 438.345718 25.988668 
z
" clip-path="url(#pa4eb8babdb)" style="fill: #1f77b4"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_10">
     <g id="line2d_20">
      <g>
       <use xlink:href="#m15aed4d867" x="393.275739" y="99.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_20">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="393.275739" y="113.997176" transform="rotate(-0 393.275739 113.997176)">A</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_21">
      <g>
       <use xlink:href="#m15aed4d867" x="468.392371" y="99.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_21">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="468.392371" y="113.997176" transform="rotate(-0 468.392371 113.997176)">B</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_10">
     <g id="line2d_22">
      <g>
       <use xlink:href="#m5c8d5162d3" x="356.46859" y="99.39952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_22">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="349.46859" y="103.198348" transform="rotate(-0 349.46859 103.198348)">0.0</text>
     </g>
    </g>
    <g id="ytick_11">
     <g id="line2d_23">
      <g>
       <use xlink:href="#m5c8d5162d3" x="356.46859" y="73.181358" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_23">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="349.46859" y="76.980187" transform="rotate(-0 349.46859 76.980187)">2.5</text>
     </g>
    </g>
    <g id="ytick_12">
     <g id="line2d_24">
      <g>
       <use xlink:href="#m5c8d5162d3" x="356.46859" y="46.963197" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_24">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="349.46859" y="50.762025" transform="rotate(-0 349.46859 50.762025)">5.0</text>
     </g>
    </g>
   </g>
   <g id="patch_10">
    <path d="M 356.46859 99.39952 
L 356.46859 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 505.19952 99.39952 
L 505.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_12">
    <path d="M 356.46859 99.39952 
L 505.19952 99.39952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_13">
    <path d="M 356.46859 22.318125 
L 505.19952 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_25">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="430.834055" y="16.318125" transform="rotate(-0 430.834055 16.318125)">By channel</text>
   </g>
  </g>
  <g id="axes_3">
   <g id="patch_14">
    <path d="M 356.46859 214.59952 
L 505.19952 214.59952 
L 505.19952 137.518125 
L 356.46859 137.518125 
L 356.46859 214.59952 
z
" style="fill: none"/>
   </g>
   <g id="patch_15">
    <path d="M 363.229087 214.59952 
L 397.031571 214.59952 
L 397.031571 190.129236 
L 363.229087 190.129236 
z
" clip-path="url(#pd7aec4cf05)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_16">
    <path d="M 397.031571 214.59952 
L 430.834055 214.59952 
L 430.834055 165.658952 
L 397.031571 165.658952 
z
" clip-path="url(#pd7aec4cf05)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_17">
    <path d="M 430.834055 214.59952 
L 464.636539 214.59952 
L 464.636539 141.188668 
L 430.834055 141.188668 
z
" clip-path="url(#pd7aec4cf05)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_18">
    <path d="M 464.636539 214.59952 
L 498.439023 214.59952 
L 498.439023 190.129236 
L 464.636539 190.129236 
z
" clip-path="url(#pd7aec4cf05)" style="fill: #1f77b4"/>
   </g>
   <g id="matplotlib.axis_5">
    <g id="xtick_12">
     <g id="line2d_25">
      <g>
       <use xlink:href="#m15aed4d867" x="363.229087" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_26">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="363.229087" y="229.197176" transform="rotate(-0 363.229087 229.197176)">1</text>
     </g>
    </g>
    <g id="xtick_13">
     <g id="line2d_26">
      <g>
       <use xlink:href="#m15aed4d867" x="408.299066" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_27">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="408.299066" y="229.197176" transform="rotate(-0 408.299066 229.197176)">2</text>
     </g>
    </g>
    <g id="xtick_14">
     <g id="line2d_27">
      <g>
       <use xlink:href="#m15aed4d867" x="453.369044" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_28">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="453.369044" y="229.197176" transform="rotate(-0 453.369044 229.197176)">3</text>
     </g>
    </g>
    <g id="xtick_15">
     <g id="line2d_28">
      <g>
       <use xlink:href="#m15aed4d867" x="498.439023" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_29">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="498.439023" y="229.197176" transform="rotate(-0 498.439023 229.197176)">4</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_6">
    <g id="ytick_13">
     <g id="line2d_29">
      <g>
       <use xlink:href="#m5c8d5162d3" x="356.46859" y="214.59952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_30">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="349.46859" y="218.398348" transform="rotate(-0 349.46859 218.398348)">0</text>
     </g>
    </g>
    <g id="ytick_14">
     <g id="line2d_30">
      <g>
       <use xlink:href="#m5c8d5162d3" x="356.46859" y="165.658952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_31">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="349.46859" y="169.45778" transform="rotate(-0 349.46859 169.45778)">2</text>
     </g>
    </g>
   </g>
   <g id="patch_19">
    <path d="M 356.46859 214.59952 
L 356.46859 137.518125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_20">
    <path d="M 505.19952 214.59952 
L 505.19952 137.518125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_21">
    <path d="M 356.46859 214.59952 
L 505.19952 214.59952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_22">
    <path d="M 356.46859 137.518125 
L 505.19952 137.518125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_32">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="430.834055" y="131.518125" transform="rotate(-0 430.834055 131.518125)">Distribution</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p0187f0c997">
   <rect x="30.103125" y="22.318125" width="297.46186" height="192.281395"/>
  </clipPath>
  <clipPath id="pa4eb8babdb">
   <rect x="356.46859" y="22.318125" width="148.73093" height="77.081395"/>
  </clipPath>
  <clipPath id="pd7aec4cf05">
   <rect x="356.46859" y="137.518125" width="148.73093" height="77.081395"/>
  </clipPath>
 </defs>
</svg>
<figcaption>One large and two small areas: <code>main</code> covers four cells.</figcaption>
</figure>

## How to read it

- The list is a grid: 2 rows, 3 columns. Cells with the same name merge into
  **one area**. `main` covers four cells: rows 0–1, columns 0–1
  (`range(0, 2)`).
- The returned `axd` is a **dictionary**: areas are reached by name
  (`axd["main"]`). More readable than remembering positions like
  `axes[1, 2]`.
- A cell to leave empty is written `"."`.

## layout="constrained"

If titles, axis labels and tick labels do not fit between the areas, they
overlap. `layout="constrained"` measures each area's text and sets the
spacing itself. Older examples call `fig.tight_layout()` after drawing for
the same job; in new code `layout="constrained"` is given when building the
figure and also accounts for text added later.

## Finer control: GridSpec

If the **ratio** of rows and columns needs adjusting (`width_ratios=[3, 1]`),
both `plt.subplots` and `subplot_mosaic` take it directly:
`plt.subplots(1, 2, width_ratios=[3, 1])`. The structure working behind them
is `GridSpec`; building the same thing by hand by slicing cells (`gs[0, :2]`)
is also possible, but the two ways above cover most needs.
