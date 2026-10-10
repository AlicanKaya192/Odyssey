Instead of writing the same settings into every chart one by one, you can use
matplotlib's ready-made **styles**. A style is a bundle of `rcParams`: the
colour cycle, font size, grid, background.

```python
import matplotlib.pyplot as plt
import numpy as np

print(len(plt.style.available), "tableau-colorblind10" in plt.style.available)
x = np.arange(10)
with plt.style.context("tableau-colorblind10"):
    fig, ax = plt.subplots(figsize=(6, 2.8), layout="constrained")
    for k, name in enumerate(["web", "store", "phone"]):
        ax.plot(x, x * (k + 1), marker="osd"[k], label=name)
    ax.legend()
    print(plt.rcParams["axes.prop_cycle"].by_key()["color"][:3])
```

```text
28 True
['#006BA4', '#FF800E', '#ABABAB']
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="440.39952pt" height="209.99952pt" viewBox="0 0 440.39952 209.99952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 209.99952 
L 440.39952 209.99952 
L 440.39952 0 
L 0 0 
L 0 209.99952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 26.925 185.79952 
L 433.19952 185.79952 
L 433.19952 7.2 
L 26.925 7.2 
L 26.925 185.79952 
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
       <use xlink:href="#m15aed4d867" x="45.392024" y="185.79952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="45.392024" y="200.397176" transform="rotate(-0 45.392024 200.397176)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="127.467684" y="185.79952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="127.467684" y="200.397176" transform="rotate(-0 127.467684 200.397176)">2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="209.543345" y="185.79952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="209.543345" y="200.397176" transform="rotate(-0 209.543345 200.397176)">4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="291.619005" y="185.79952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="291.619005" y="200.397176" transform="rotate(-0 291.619005 200.397176)">6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="373.694666" y="185.79952" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="373.694666" y="200.397176" transform="rotate(-0 373.694666 200.397176)">8</text>
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
       <use xlink:href="#m5c8d5162d3" x="26.925" y="177.68136" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="181.480188" transform="rotate(-0 19.925 181.480188)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="26.925" y="147.614101" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="151.412929" transform="rotate(-0 19.925 151.412929)">5</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="26.925" y="117.546841" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="121.34567" transform="rotate(-0 19.925 121.34567)">10</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="26.925" y="87.479582" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="91.27841" transform="rotate(-0 19.925 91.27841)">15</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="26.925" y="57.412323" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="61.211151" transform="rotate(-0 19.925 61.211151)">20</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="26.925" y="27.345064" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="19.925" y="31.143892" transform="rotate(-0 19.925 31.143892)">25</text>
     </g>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 45.392024 177.68136 
L 86.429854 171.667908 
L 127.467684 165.654456 
L 168.505515 159.641004 
L 209.543345 153.627553 
L 250.581175 147.614101 
L 291.619005 141.600649 
L 332.656836 135.587197 
L 373.694666 129.573745 
L 414.732496 123.560293 
" clip-path="url(#pc0edb8f9f3)" style="fill: none; stroke: #006ba4; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="md6202af5a0" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #006ba4"/>
    </defs>
    <g clip-path="url(#pc0edb8f9f3)">
     <use xlink:href="#md6202af5a0" x="45.392024" y="177.68136" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="86.429854" y="171.667908" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="127.467684" y="165.654456" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="168.505515" y="159.641004" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="209.543345" y="153.627553" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="250.581175" y="147.614101" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="291.619005" y="141.600649" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="332.656836" y="135.587197" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="373.694666" y="129.573745" style="fill: #006ba4; stroke: #006ba4"/>
     <use xlink:href="#md6202af5a0" x="414.732496" y="123.560293" style="fill: #006ba4; stroke: #006ba4"/>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 45.392024 177.68136 
L 86.429854 165.654456 
L 127.467684 153.627553 
L 168.505515 141.600649 
L 209.543345 129.573745 
L 250.581175 117.546841 
L 291.619005 105.519938 
L 332.656836 93.493034 
L 373.694666 81.46613 
L 414.732496 69.439227 
" clip-path="url(#pc0edb8f9f3)" style="fill: none; stroke: #ff800e; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m4d612a3d16" d="M -3 3 
L 3 3 
L 3 -3 
L -3 -3 
z
" style="stroke: #ff800e; stroke-linejoin: miter"/>
    </defs>
    <g clip-path="url(#pc0edb8f9f3)">
     <use xlink:href="#m4d612a3d16" x="45.392024" y="177.68136" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="86.429854" y="165.654456" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="127.467684" y="153.627553" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="168.505515" y="141.600649" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="209.543345" y="129.573745" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="250.581175" y="117.546841" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="291.619005" y="105.519938" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="332.656836" y="93.493034" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="373.694666" y="81.46613" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     <use xlink:href="#m4d612a3d16" x="414.732496" y="69.439227" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 45.392024 177.68136 
L 86.429854 159.641004 
L 127.467684 141.600649 
L 168.505515 123.560293 
L 209.543345 105.519938 
L 250.581175 87.479582 
L 291.619005 69.439227 
L 332.656836 51.398871 
L 373.694666 33.358516 
L 414.732496 15.31816 
" clip-path="url(#pc0edb8f9f3)" style="fill: none; stroke: #ababab; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m991d2a7f53" d="M 0 4.242641 
L 2.545584 0 
L 0 -4.242641 
L -2.545584 0 
z
" style="stroke: #ababab; stroke-linejoin: miter"/>
    </defs>
    <g clip-path="url(#pc0edb8f9f3)">
     <use xlink:href="#m991d2a7f53" x="45.392024" y="177.68136" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="86.429854" y="159.641004" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="127.467684" y="141.600649" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="168.505515" y="123.560293" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="209.543345" y="105.519938" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="250.581175" y="87.479582" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="291.619005" y="69.439227" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="332.656836" y="51.398871" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="373.694666" y="33.358516" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     <use xlink:href="#m991d2a7f53" x="414.732496" y="15.31816" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 26.925 185.79952 
L 26.925 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 433.19952 185.79952 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 26.925 185.79952 
L 433.19952 185.79952 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 26.925 7.2 
L 433.19952 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 33.925 60.202344 
L 97.220312 60.202344 
Q 99.220312 60.202344 99.220312 58.202344 
L 99.220312 14.2 
Q 99.220312 12.2 97.220312 12.2 
L 33.925 12.2 
Q 31.925 12.2 31.925 14.2 
L 31.925 58.202344 
Q 31.925 60.202344 33.925 60.202344 
L 33.925 60.202344 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="line2d_15">
     <path d="M 35.925 20.298438 
L 45.925 20.298438 
L 55.925 20.298438 
" style="fill: none; stroke: #006ba4; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#md6202af5a0" x="45.925" y="20.298438" style="fill: #006ba4; stroke: #006ba4"/>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="63.925" y="23.798438" transform="rotate(-0 63.925 23.798438)">web</text>
    </g>
    <g id="line2d_16">
     <path d="M 35.925 35.299219 
L 45.925 35.299219 
L 55.925 35.299219 
" style="fill: none; stroke: #ff800e; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m4d612a3d16" x="45.925" y="35.299219" style="fill: #ff800e; stroke: #ff800e; stroke-linejoin: miter"/>
     </g>
    </g>
    <g id="text_13">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="63.925" y="38.799219" transform="rotate(-0 63.925 38.799219)">store</text>
    </g>
    <g id="line2d_17">
     <path d="M 35.925 50.3 
L 45.925 50.3 
L 55.925 50.3 
" style="fill: none; stroke: #ababab; stroke-width: 1.5; stroke-linecap: square"/>
     <g>
      <use xlink:href="#m991d2a7f53" x="45.925" y="50.3" style="fill: #ababab; stroke: #ababab; stroke-linejoin: miter"/>
     </g>
    </g>
    <g id="text_14">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="63.925" y="53.8" transform="rotate(-0 63.925 53.8)">phone</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pc0edb8f9f3">
   <rect x="26.925" y="7.2" width="406.27452" height="178.59952"/>
  </clipPath>
 </defs>
</svg>
<figcaption>A colour-blind-friendly cycle and a different marker on each line.</figcaption>
</figure>

## Styles

- `plt.style.available` lists the ready-made styles (28 in this
  installation: `ggplot`, `bmh`, `fivethirtyeight`, the `seaborn-v0_8`
  family...).
- `plt.style.use("ggplot")` changes the rest of the script;
  `plt.style.context(...)` only the `with` block.
- You can write your own style into a `.mplstyle` file (lines like
  `axes.spines.top: False`) and set up the same look in every project with
  `plt.style.use("file.mplstyle")`.

## Colour blindness

About 8% of men have some form of colour vision difference; the most common
is not telling red from green apart. If a chart's meaning rests only on a
red / green distinction, the chart is empty for these readers.

- The `tableau-colorblind10` style gives a colour cycle that stays distinct
  under colour blindness too (blue, orange, grey...). For continuous values
  the `viridis` and `cividis` scales are designed for the same purpose.
- Add a **second cue** to colour: the lines above also have different markers
  (`o`, `s`, `d`). They stay distinct when printed in black and white too.
- Writing each line's name at its end (`ax.text`) instead of a legend box
  frees the eye from colour.
