We cannot see 20-dimensional vectors directly. But we can project them onto
the two directions in which they spread most (the same idea as PCA: subtract
the mean, take SVD's first two directions). With the lesson's `E`, `index`
and `vocab`, let us draw the words of five classes:

```python
import matplotlib.pyplot as plt
import numpy as np
from corpus_data import WORD_CLASSES

groups = ["animal", "food", "vehicle", "city", "country"]
words = [w for g in groups for w in WORD_CLASSES[g]]
X = E[[index[w] for w in words]]
X = X - X.mean(axis=0)
_, _, Vt2 = np.linalg.svd(X, full_matrices=False)
xy = X @ Vt2[:2].T
fig, ax = plt.subplots(figsize=(6, 4))
for g in groups:
    rows = [i for i, w in enumerate(words) if w in WORD_CLASSES[g]]
    ax.scatter(xy[rows, 0], xy[rows, 1], s=22, label=g)
    ax.annotate(words[rows[0]], xy[rows[0]], fontsize=8,
                xytext=(4, 4), textcoords="offset points")
ax.set(xticks=[], yticks=[])
ax.legend(fontsize=8)
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="360.988408pt" height="236.16pt" viewBox="0 0 360.988408 236.16" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 236.16 
L 360.988408 236.16 
L 360.988408 0 
L 0 0 
L 0 236.16 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 228.96 
L 342 228.96 
L 342 7.2 
L 7.2 7.2 
L 7.2 228.96 
z
" style="fill: none"/>
   </g>
   <g id="PathCollection_1">
    <defs>
     <path id="m259ceb098f" d="M 0 2.345208 
C 0.621956 2.345208 1.218523 2.098102 1.658312 1.658312 
C 2.098102 1.218523 2.345208 0.621956 2.345208 0 
C 2.345208 -0.621956 2.098102 -1.218523 1.658312 -1.658312 
C 1.218523 -2.098102 0.621956 -2.345208 0 -2.345208 
C -0.621956 -2.345208 -1.218523 -2.098102 -1.658312 -1.658312 
C -2.098102 -1.218523 -2.345208 -0.621956 -2.345208 0 
C -2.345208 0.621956 -2.098102 1.218523 -1.658312 1.658312 
C -1.218523 2.098102 -0.621956 2.345208 0 2.345208 
z
" style="stroke: #1f77b4"/>
    </defs>
    <g clip-path="url(#p8bdb9df806)">
     <use xlink:href="#m259ceb098f" x="289.175505" y="218.705921" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="290.591402" y="218.439465" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="288.910812" y="218.88" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="289.503779" y="218.614812" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="288.990819" y="218.729383" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="290.679158" y="218.42778" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="290.921219" y="218.294542" style="fill: #1f77b4; stroke: #1f77b4"/>
     <use xlink:href="#m259ceb098f" x="289.374114" y="218.723032" style="fill: #1f77b4; stroke: #1f77b4"/>
    </g>
   </g>
   <g id="PathCollection_2">
    <defs>
     <path id="mbeaf97b1dd" d="M 0 2.345208 
C 0.621956 2.345208 1.218523 2.098102 1.658312 1.658312 
C 2.098102 1.218523 2.345208 0.621956 2.345208 0 
C 2.345208 -0.621956 2.098102 -1.218523 1.658312 -1.658312 
C 1.218523 -2.098102 0.621956 -2.345208 0 -2.345208 
C -0.621956 -2.345208 -1.218523 -2.098102 -1.658312 -1.658312 
C -2.098102 -1.218523 -2.345208 -0.621956 -2.345208 0 
C -2.345208 0.621956 -2.098102 1.218523 -1.658312 1.658312 
C -1.218523 2.098102 -0.621956 2.345208 0 2.345208 
z
" style="stroke: #ff7f0e"/>
    </defs>
    <g clip-path="url(#p8bdb9df806)">
     <use xlink:href="#mbeaf97b1dd" x="326.693408" y="117.409563" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.598067" y="117.575027" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.158982" y="117.367792" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.660243" y="117.513054" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.1612" y="117.530187" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.222347" y="117.713696" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="326.781818" y="118.211981" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     <use xlink:href="#mbeaf97b1dd" x="325.945872" y="117.34722" style="fill: #ff7f0e; stroke: #ff7f0e"/>
    </g>
   </g>
   <g id="PathCollection_3">
    <defs>
     <path id="m31be2f78a3" d="M 0 2.345208 
C 0.621956 2.345208 1.218523 2.098102 1.658312 1.658312 
C 2.098102 1.218523 2.345208 0.621956 2.345208 0 
C 2.345208 -0.621956 2.098102 -1.218523 1.658312 -1.658312 
C 1.218523 -2.098102 0.621956 -2.345208 0 -2.345208 
C -0.621956 -2.345208 -1.218523 -2.098102 -1.658312 -1.658312 
C -2.098102 -1.218523 -2.345208 -0.621956 -2.345208 0 
C -2.345208 0.621956 -2.098102 1.218523 -1.658312 1.658312 
C -1.218523 2.098102 -0.621956 2.345208 0 2.345208 
z
" style="stroke: #2ca02c"/>
    </defs>
    <g clip-path="url(#p8bdb9df806)">
     <use xlink:href="#m31be2f78a3" x="210.150221" y="17.700425" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="211.759784" y="17.46947" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="212.009594" y="17.557756" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="212.499364" y="17.460369" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="209.760532" y="17.957827" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="212.271137" y="17.474057" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="212.48959" y="17.28" style="fill: #2ca02c; stroke: #2ca02c"/>
     <use xlink:href="#m31be2f78a3" x="211.615013" y="17.481872" style="fill: #2ca02c; stroke: #2ca02c"/>
    </g>
   </g>
   <g id="PathCollection_4">
    <defs>
     <path id="m140e9540c5" d="M 0 2.345208 
C 0.621956 2.345208 1.218523 2.098102 1.658312 1.658312 
C 2.098102 1.218523 2.345208 0.621956 2.345208 0 
C 2.345208 -0.621956 2.098102 -1.218523 1.658312 -1.658312 
C 1.218523 -2.098102 0.621956 -2.345208 0 -2.345208 
C -0.621956 -2.345208 -1.218523 -2.098102 -1.658312 -1.658312 
C -2.098102 -1.218523 -2.345208 -0.621956 -2.345208 0 
C -2.345208 0.621956 -2.098102 1.218523 -1.658312 1.658312 
C -1.218523 2.098102 -0.621956 2.345208 0 2.345208 
z
" style="stroke: #d62728"/>
    </defs>
    <g clip-path="url(#p8bdb9df806)">
     <use xlink:href="#m140e9540c5" x="23.323094" y="136.054089" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="25.148124" y="135.663987" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="26.639452" y="135.404814" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="22.832177" y="136.540928" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="23.522483" y="135.776665" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="25.065102" y="135.224284" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="24.02914" y="135.778074" style="fill: #d62728; stroke: #d62728"/>
     <use xlink:href="#m140e9540c5" x="22.447127" y="135.95291" style="fill: #d62728; stroke: #d62728"/>
    </g>
   </g>
   <g id="PathCollection_5">
    <defs>
     <path id="m51ab09817d" d="M 0 2.345208 
C 0.621956 2.345208 1.218523 2.098102 1.658312 1.658312 
C 2.098102 1.218523 2.345208 0.621956 2.345208 0 
C 2.345208 -0.621956 2.098102 -1.218523 1.658312 -1.658312 
C 1.218523 -2.098102 0.621956 -2.345208 0 -2.345208 
C -0.621956 -2.345208 -1.218523 -2.098102 -1.658312 -1.658312 
C -2.098102 -1.218523 -2.345208 -0.621956 -2.345208 0 
C -2.345208 0.621956 -2.098102 1.218523 -1.658312 1.658312 
C -1.218523 2.098102 -0.621956 2.345208 0 2.345208 
z
" style="stroke: #9467bd"/>
    </defs>
    <g clip-path="url(#p8bdb9df806)">
     <use xlink:href="#m51ab09817d" x="25.486216" y="152.50073" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="25.552143" y="151.675618" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="27.283006" y="150.851607" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="26.322721" y="154.583617" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="24.124146" y="151.643311" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="22.418182" y="151.602128" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="24.92014" y="151.599596" style="fill: #9467bd; stroke: #9467bd"/>
     <use xlink:href="#m51ab09817d" x="23.482954" y="151.710082" style="fill: #9467bd; stroke: #9467bd"/>
    </g>
   </g>
   <g id="matplotlib.axis_1"/>
   <g id="matplotlib.axis_2"/>
   <g id="patch_3">
    <path d="M 7.2 228.96 
L 7.2 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 342 228.96 
L 342 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 7.2 228.96 
L 342 228.96 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 7.2 7.2 
L 342 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_1">
    <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="293.175505" y="214.705921" transform="rotate(-0 293.175505 214.705921)">cat</text>
   </g>
   <g id="text_2">
    <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="330.693408" y="113.409563" transform="rotate(-0 330.693408 113.409563)">bread</text>
   </g>
   <g id="text_3">
    <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="214.150221" y="13.700425" transform="rotate(-0 214.150221 13.700425)">car</text>
   </g>
   <g id="text_4">
    <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="27.323094" y="132.054089" transform="rotate(-0 27.323094 132.054089)">paris</text>
   </g>
   <g id="text_5">
    <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="29.486216" y="148.50073" transform="rotate(-0 29.486216 148.50073)">france</text>
   </g>
   <g id="legend_1">
    <g id="patch_7">
     <path d="M 280.20625 73.603125 
L 336.4 73.603125 
Q 338 73.603125 338 72.003125 
L 338 12.8 
Q 338 11.2 336.4 11.2 
L 280.20625 11.2 
Q 278.60625 11.2 278.60625 12.8 
L 278.60625 72.003125 
Q 278.60625 73.603125 280.20625 73.603125 
L 280.20625 73.603125 
z
" style="fill: none; opacity: 0.8; stroke: currentColor; stroke-linejoin: miter"/>
    </g>
    <g id="PathCollection_6">
     <g>
      <use xlink:href="#m259ceb098f" x="289.80625" y="18.37875" style="fill: #1f77b4; stroke: #1f77b4"/>
     </g>
    </g>
    <g id="text_6">
     <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="304.20625" y="20.47875" transform="rotate(-0 304.20625 20.47875)">animal</text>
    </g>
    <g id="PathCollection_7">
     <g>
      <use xlink:href="#mbeaf97b1dd" x="289.80625" y="30.379375" style="fill: #ff7f0e; stroke: #ff7f0e"/>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="304.20625" y="32.479375" transform="rotate(-0 304.20625 32.479375)">food</text>
    </g>
    <g id="PathCollection_8">
     <g>
      <use xlink:href="#m31be2f78a3" x="289.80625" y="42.38" style="fill: #2ca02c; stroke: #2ca02c"/>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="304.20625" y="44.48" transform="rotate(-0 304.20625 44.48)">vehicle</text>
    </g>
    <g id="PathCollection_9">
     <g>
      <use xlink:href="#m140e9540c5" x="289.80625" y="54.380625" style="fill: #d62728; stroke: #d62728"/>
     </g>
    </g>
    <g id="text_9">
     <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="304.20625" y="56.480625" transform="rotate(-0 304.20625 56.480625)">city</text>
    </g>
    <g id="PathCollection_10">
     <g>
      <use xlink:href="#m51ab09817d" x="289.80625" y="66.38125" style="fill: #9467bd; stroke: #9467bd"/>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 8px; font-family:inherit; text-anchor: start; fill: currentColor" x="304.20625" y="68.48125" transform="rotate(-0 304.20625 68.48125)">country</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p8bdb9df806">
   <rect x="7.2" y="7.2" width="334.8" height="221.76"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The PPMI + SVD vectors projected onto two dimensions. Each point is a word; words of the same class sit together.</figcaption>
</figure>

- Each class gathers in its own region, with wide gaps between the classes.
  The eight words of each class land almost on top of each other (only the
  first word is labelled): in our small world the words of a class are used
  in exactly the same sentences. In real embeddings clusters are not this
  tight, and they overlap.
- Cities and countries form two separate clusters close to each other: they
  appear in the same sentences ("paris is the capital of france") but take
  different places.
- Two dimensions are a very rough shadow of 20. Two points that look close
  may actually be far apart; to decide, measure similarity in all
  dimensions.
