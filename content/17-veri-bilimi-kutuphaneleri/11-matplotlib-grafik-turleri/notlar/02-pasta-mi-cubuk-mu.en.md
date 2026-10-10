The pie chart is the best known and the hardest to read. The eye is poor at
comparing angles and areas and good at comparing lengths. Let us draw the
same data both ways: five channels' shares of sales, close to each other.

```python
import matplotlib.pyplot as plt

channels = ["web", "store", "phone", "partner", "other"]
share = [23, 21, 20, 19, 17]
fig, (left, right) = plt.subplots(1, 2, figsize=(7.5, 3), layout="constrained")
left.pie(share, labels=channels)
left.set_title("Pie")
order = sorted(range(len(share)), key=lambda i: share[i])
right.barh([channels[i] for i in order], [share[i] for i in order])
right.set_title("Sorted bars")
right.set_xlabel("share (%)")
print(sum(share), max(share) - min(share))
print([channels[i] for i in order][::-1])
```

```text
100 6
['web', 'store', 'phone', 'partner', 'other']
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="528.564498pt" height="224.39952pt" viewBox="0 0 528.564498 224.39952" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 224.39952 
L 528.564498 224.39952 
L 528.564498 -0 
L 0 -0 
L 0 224.39952 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 173.889639 104.258432 
C 173.889639 88.300176 168.062243 72.878419 157.508859 60.907954 
C 146.955475 48.937489 132.385689 41.223185 116.553269 39.223085 
L 108.337394 104.258432 
z
" style="fill: #1f77b4"/>
   </g>
   <g id="patch_3">
    <path d="M 116.553269 39.223085 
C 102.122866 37.400102 87.48816 40.430804 74.968586 47.834859 
C 62.449012 55.238915 52.742864 66.603354 47.388457 80.127041 
L 108.337394 104.258432 
z
" style="fill: #ff7f0e"/>
   </g>
   <g id="patch_4">
    <path d="M 47.388457 80.127041 
C 42.2932 92.996192 41.402445 107.154333 44.844593 120.560612 
C 48.28674 133.966892 55.888051 145.944641 66.55282 154.767305 
L 108.337394 104.258432 
z
" style="fill: #2ca02c"/>
   </g>
   <g id="patch_5">
    <path d="M 66.55282 154.767305 
C 76.676434 163.142287 89.0879 168.283285 102.168383 169.519754 
C 115.248865 170.756224 128.403817 168.031964 139.917429 161.702302 
L 108.337394 104.258432 
z
" style="fill: #d62728"/>
   </g>
   <g id="patch_6">
    <path d="M 139.917429 161.702302 
C 150.204168 156.04712 158.78546 147.731269 164.760966 137.62724 
C 170.736473 127.52321 173.889639 115.997175 173.889639 104.258432 
L 108.337394 104.258432 
z
" style="fill: #9467bd"/>
   </g>
   <g id="matplotlib.axis_1"/>
   <g id="matplotlib.axis_2"/>
   <g id="text_1">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="162.426005" y="59.170953" transform="rotate(-0 162.426005 59.170953)">web</text>
   </g>
   <g id="text_2">
    <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="71.631705" y="44.790158" transform="rotate(-0 71.631705 44.790158)">store</text>
   </g>
   <g id="text_3">
    <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="38.495313" y="124.788877" transform="rotate(-0 38.495313 124.788877)">phone</text>
   </g>
   <g id="text_4">
    <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="101.551481" y="178.643543" transform="rotate(-0 101.551481 178.643543)">partner</text>
   </g>
   <g id="text_5">
    <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="170.403324" y="143.562167" transform="rotate(-0 170.403324 143.562167)">other</text>
   </g>
   <g id="text_6">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="108.337394" y="16.318125" transform="rotate(-0 108.337394 16.318125)">Pie</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 279.419665 186.198739 
L 521.364498 186.198739 
L 521.364498 22.318125 
L 279.419665 22.318125 
L 279.419665 186.198739 
z
" style="fill: none"/>
   </g>
   <g id="patch_8">
    <path d="M 279.419665 178.74962 
L 449.732798 178.74962 
L 449.732798 153.919224 
L 279.419665 153.919224 
z
" clip-path="url(#pce7007e1f8)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_9">
    <path d="M 279.419665 147.711625 
L 469.769637 147.711625 
L 469.769637 122.881229 
L 279.419665 122.881229 
z
" clip-path="url(#pce7007e1f8)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_10">
    <path d="M 279.419665 116.67363 
L 479.788056 116.67363 
L 479.788056 91.843234 
L 279.419665 91.843234 
z
" clip-path="url(#pce7007e1f8)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_11">
    <path d="M 279.419665 85.635635 
L 489.806476 85.635635 
L 489.806476 60.805239 
L 279.419665 60.805239 
z
" clip-path="url(#pce7007e1f8)" style="fill: #1f77b4"/>
   </g>
   <g id="patch_12">
    <path d="M 279.419665 54.59764 
L 509.843315 54.59764 
L 509.843315 29.767244 
L 279.419665 29.767244 
z
" clip-path="url(#pce7007e1f8)" style="fill: #1f77b4"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="279.419665" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="279.419665" y="200.796395" transform="rotate(-0 279.419665 200.796395)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="329.511763" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="329.511763" y="200.796395" transform="rotate(-0 329.511763 200.796395)">5</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="379.603861" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="379.603861" y="200.796395" transform="rotate(-0 379.603861 200.796395)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="429.695959" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="429.695959" y="200.796395" transform="rotate(-0 429.695959 200.796395)">15</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="479.788056" y="186.198739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="479.788056" y="200.796395" transform="rotate(-0 479.788056 200.796395)">20</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="400.392081" y="214.797176" transform="rotate(-0 400.392081 214.797176)">share (%)</text>
    </g>
   </g>
   <g id="matplotlib.axis_4">
    <g id="ytick_1">
     <g id="line2d_6">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="279.419665" y="166.334422" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="272.419665" y="170.133641" transform="rotate(-0 272.419665 170.133641)">other</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="279.419665" y="135.296427" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="272.419665" y="139.095255" transform="rotate(-0 272.419665 139.095255)">partner</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="279.419665" y="104.258432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_15">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="272.419665" y="108.057651" transform="rotate(-0 272.419665 108.057651)">phone</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="279.419665" y="73.220437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_16">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="272.419665" y="77.019265" transform="rotate(-0 272.419665 77.019265)">store</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="279.419665" y="42.182442" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_17">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="272.419665" y="45.981661" transform="rotate(-0 272.419665 45.981661)">web</text>
     </g>
    </g>
   </g>
   <g id="patch_13">
    <path d="M 279.419665 186.198739 
L 279.419665 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_14">
    <path d="M 521.364498 186.198739 
L 521.364498 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_15">
    <path d="M 279.419665 186.198739 
L 521.364498 186.198739 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_16">
    <path d="M 279.419665 22.318125 
L 521.364498 22.318125 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_18">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="400.392081" y="16.318125" transform="rotate(-0 400.392081 16.318125)">Sorted bars</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pce7007e1f8">
   <rect x="279.419665" y="22.318125" width="241.944833" height="163.880614"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The same shares: the order does not read in the pie, it does at a glance in sorted bars.</figcaption>
</figure>

## What do we see?

- In the pie it is almost impossible to say whether web or store is larger;
  the slices differ by only 2 points. In the bars the ranking reads at a
  glance.
- **Sorting** is the cheapest improvement to a bar chart: the largest on
  top, the eye moves down. If category names are long, horizontal bars
  (`barh`) make room for the labels.

## When is a pie fine?

- Only with **two or three** parts and a message resting on a rough ratio
  like "more than half".
- When the parts really add up to a whole (100 percent). Putting values whose
  sum means nothing (like average scores) in a pie is wrong.
- Otherwise bars almost always read better.
