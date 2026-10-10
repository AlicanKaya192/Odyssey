PCA reduces data to fewer columns; `inverse_transform` goes back from those
few columns to the original size. The more the returned data differs from
the original, the more information was lost. Let us see it with digit
images:

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

X, y = load_digits(return_X_y=True)      # pixel values 0–16
fig, axes = plt.subplots(1, 5, figsize=(7, 1.8))
axes[0].imshow(X[0].reshape(8, 8), cmap="gray_r")
axes[0].set_title("64")
for ax, n in zip(axes[1:], [5, 10, 20, 40]):
    pca = PCA(n_components=n).fit(X)
    back = pca.inverse_transform(pca.transform(X))
    kept = pca.explained_variance_ratio_.sum()
    print(n, round(kept, 3), round(np.abs(back - X).mean(), 2))
    ax.imshow(back[0].reshape(8, 8), cmap="gray_r")
    ax.set_title(str(n))
for ax in axes:
    ax.axis("off")
```

```text
5 0.545 1.95
10 0.738 1.47
20 0.894 0.95
40 0.988 0.27
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="405pt" height="96.862015pt" viewBox="0 0 405 96.862015" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 96.862015 
L 405 96.862015 
L 405 0 
L 0 0 
L 0 96.862015 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g clip-path="url(#peef0d0a10f)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAF4AAABeCAYAAACq0qNuAAABsUlEQVR4nO3cUY3CQBRA0WGzBiqhIKGVgAUs1AIWwAISqASwAA6KhFZCNzjgkby9dPee72ECN/P1Msxqnue5JDmdTqH1h8MhtL5t25fXns/n8km+6C/wXxkeYniI4SGGhxgeYniI4SGGhxgeYnjIKjqreTweL69tmiZ1ttP3/ctrh2EI7X273UomTzzE8BDDQwwPMTzE8BDDQwwPMTzE8JDv6AciI4PI9Yun3W5XIrbbbcrap+PxGFq/3+9D6z3xEMNDDA8xPMTwEMNDDA8xPMTwEMNDDL+UWc00TWnXO6KqqkqbG0V+5zs88RDDQwwPMTzE8BDDQwwPMTzE8BDDQwy/lFlNZD5yuVxSn03J+t6/wRMPMTzE8BDDQwwPMTzE8BDDQwwPMfxfHBnc7/e0v/k8rdfrkvUaR/bVFE88xPAQw0MMDzE8xPAQw0MMDzE8xPAQwy9lVhOZYdR1Hdp7s9mkPbNyvV5De3ddVzJ54iGGhxgeYniI4SGGhxgeYniI4SGGhxh+KbOaT3omtgrc8RnHMW3vd3jiIYaHGB5ieIjhIYaHGB5ieIjhIYaHGL4wfgCctUNU8TOa8QAAAABJRU5ErkJggg==" id="imageaa6ec10497" transform="scale(1 -1) translate(0 -67.68)" x="7.2" y="-21.982015" width="67.68" height="67.68"/>
   </g>
   <g id="text_1">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="40.872414" y="16.317188" transform="rotate(-0 40.872414 16.317188)">64</text>
   </g>
  </g>
  <g id="axes_2">
   <g clip-path="url(#pc2406ca5e2)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAF4AAABeCAYAAACq0qNuAAACF0lEQVR4nO3dvYlqURhG4ePVEQ0UQQQxMdJIDAQ7EIwGG5hUsAADaxFswUSbsARTEyP/AsFIL7eD/cE9LAbWE79uhsVOlNFTuN1unyzg/X5H5tl2u03eLpfL0NnD4TC0XywWydvv7+/Q2eVyObT/E1rrvzE8xPAQw0MMDzE8xPAQw0MMDzE8xPCQ0ucT+qgmezweof16vU7e/vz8hM7udruh/WazSd622+3Q2ePxOLT3xkMMDzE8xPAQw0MMDzE8xPAQw0MMDylFX3A8HkP7YrGYvJ3P56Gzm81maL/b7ZK3h8MhdPZoNArtvfEQw0MMDzE8xPAQw0MMDzE8xPAQw0MMDykVCoXQC06nU2hfqVSSt4Xg33K/30P76/WavH0+n1mevPEQw0MMDzE8xPAQw0MMDzE8xPAQw0MM/1v+r6ZarYb25/M5edtqtUJnXy6X0P7r6yt5W6/Xszx54yGGhxgeYniI4SGGhxgeYniI4SGG/y0fGUTfSke+ulMMfG3nn8FgENq/Xq/kba/XC50d/RUUbzzE8BDDQwwPMTzE8BDDQwwPMTzE8BDD/5bPavr9fm5Pi5nNZqGzJ5NJaF+r1ZK3nU4ny/NpQd54iOEhhocYHmJ4iOEhhocYHmJ4iOEhhocU8n6C8X6/T96uVqvQ2Y1GI7cnGE+n01x/btcbDzE8xPAQw0MMDzE8xPAQw0MMDzE8xPAZ4y/sQU/PIJRiwAAAAABJRU5ErkJggg==" id="image2a9cc2c43c" transform="scale(1 -1) translate(0 -67.68)" x="87.84" y="-21.982015" width="67.68" height="67.68"/>
   </g>
   <g id="text_2">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="121.686207" y="16.317188" transform="rotate(-0 121.686207 16.317188)">5</text>
   </g>
  </g>
  <g id="axes_3">
   <g clip-path="url(#p686ff36b1c)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAF4AAABeCAYAAACq0qNuAAACDklEQVR4nO3bMc5pURhGYedGoxMUCgURnZiCVikmoWIKWpVGbwjGYAwiGlQOepEoJNzcGewvubIiWU/9/tuflRPFzpFdLpdPIeD1ekXmhdVqFdrP5/PkbavVCp29WCxC+36/n7x9Pp+hs/+E1vpvDA8xPMTwEMNDDA8xPMTwEMNDDA8xPCTL8zx0V3O9XkMfMBgMQvvRaJS8PZ1OobNvt1tov16vk7e1Wi10tk88xPAQw0MMDzE8xPAQw0MMDzE8xPCQYvQPttttaF+tVkP7yWSSvH08HqGzx+NxaL/ZbJK3w+EwdLZPPMTwEMNDDA8xPMTwEMNDDA8xPMTwEMNDilmWffUViUajEdr3er3Ct1QqldD+cDgkbz+f0FsyPvEUv2oghocYHmJ4iOEhhocYHmJ4iOEhhv+V92qi9x3n8zm0z/M8eVssxv79+/0e2kfvsSJ84iGGhxgeYniI4SGGhxgeYniI4SGG/5Urg+hPa47HY2i/3++Tt81m86tXBt1uN3nr6x0/wq8aiOEhhocYHmJ4iOEhhocYHmJ4iOF/5a4mej8SfQVjOp0mbzudTujsUqkU2rfb7eTt+/0One0TDzE8xPAQw0MMDzE8xPAQw0MMDzE8xPC/cldTr9dD+9lsFtovl8vk7W63+9o90D/lcrnwLT7xEMNDDA8xPMTwEMNDDA8xPMTwEMNDDF9g/AUcilZiyEsizwAAAABJRU5ErkJggg==" id="image2bd8ee50e5" transform="scale(1 -1) translate(0 -67.68)" x="168.48" y="-21.982015" width="67.68" height="67.68"/>
   </g>
   <g id="text_3">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="16.317188" transform="rotate(-0 202.5 16.317188)">10</text>
   </g>
  </g>
  <g id="axes_4">
   <g clip-path="url(#pf375ddb09e)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAF0AAABeCAYAAABB5RhtAAACIUlEQVR4nO3csaqBcRzG8fc9nWIiCyWRWbkAF6HMBovYLO7B4AasLsLqAoyK5VWUQVHKTDidO/g/dZznHb6f+ek3fHszvL3nxLvd7h0Fer1ekWKxWEj78XgcvG02m9Lt2Wwm7VutlrQ/nU7B2y/pMv4E0Q2IbkB0A6IbEN2A6AZENyC6AdENiG4QJ0kS/O7lfD5LxzudjrQfDofB2+PxKN3ebDbSfj6fS/t8Ph+85Uk3ILoB0Q2IbkB0A6IbEN2A6AZENyC6wXccx8Hjw+EgHa9Wq9J+NBoFb5MkkW4PBgNpv1wupX273Q7e8qQbEN2A6AZENyC6AdENiG5AdAOiGxDdgOgG38r4crlIx2u1mrR/PB7B22KxKN1uNBrS/nq9Svv3O/hLFp50B35eDIhuQHQDohsQ3YDoBkQ3ILoB0Q2InvZ3L4VCQTq+3++l/f1+/9i7F+X7nl+3203a8+4l5fh5MSC6AdENiG5AdAOiGxDdgOgGRE/7a4BKpSIdX6/X0n673QZvS6WSdHu1Wkn7brcr7Z/PZ/CWJ92A6AZENyC6AdENiG5AdAOiGxDdgOgGRE/7u5dyuSwdz2az0r7f7wdv6/W6dDuXy0WffM+kfD7Ck25AdAOiGxDdgOgGRDcgugHRDYhuQHQDoqf93Usmk5GOTyYTaT+dTj/2b016vV70Sfz5S8rx82JAdAOiGxDdgOgGRDcgugHRDYhuQPTo//0AedNcpFdHY+kAAAAASUVORK5CYII=" id="imageb21ff64fc1" transform="scale(1 -1) translate(0 -67.68)" x="249.84" y="-21.982015" width="66.96" height="67.68"/>
   </g>
   <g id="text_4">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="283.313793" y="16.317188" transform="rotate(-0 283.313793 16.317188)">20</text>
   </g>
  </g>
  <g id="axes_5">
   <g clip-path="url(#p89a0b75e73)">
    <image xlink:href="data:image/png;base64,
iVBORw0KGgoAAAANSUhEUgAAAF4AAABeCAYAAACq0qNuAAACJklEQVR4nO3cP65pYRyF4b0vGtH4E5VCoxSikBiBQmIESolhEAMQk1BoFdQmQKMSCqVGR4jg5s7gW8mVFcn71MsvJ292TrFznPh6vX4iwfv9Dt7OZjPldDSdTqV9uVwO3i4WC+l2KpWS9pfLRdr/kdb4bwhvQngTwpsQ3oTwJoQ3IbwJ4U0Ib0J4k1h9V3M+n4O3jUZD+mEmk4m0Xy6Xwdvj8SjdXq1W0j6dTkt7nngTwpsQ3oTwJoQ3IbwJ4U0Ib0J4E8KbJNUPbLfb4G21WpVu93o9ad9ut4O3nU5Huj2fz6V9v9+X9jzxJoQ3IbwJ4U0Ib0J4E8KbEN6E8CaENyH8r7yrud1uwdtWqyXdvt/v0j6XywVv6/W6dPtwOETfxBNvQngTwpsQ3oTwJoQ3IbwJ4U0Ib0J4E8KbJOM4lj5QKBS+8lWZf8bjcaR4vV7B22w2K91OJBLRN/HEmxDehPAmhDchvAnhTQhvQngTwpsQ/lf+vCOTyQRvd7uddHu/30v7SqUSvN1sNtJt9T+PPJ9Pac8Tb0J4E8KbEN6E8CaENyG8CeFNCG9CeBPC/8q7mmazGbwtlUrS7VqtJu273W7wdr1eS7cHg4G0513Nj+BXjQnhTQhvQngTwpsQ3oTwJoQ3IbwJ4U2Sn8/na19/GQ6H0u3RaCTt8/l88PZ0Okm3i8WitH88HtKeJ96E8CaENyG8CeFNCG9CeBPCmxDehPAmhI88/gIgBV2OY38G1AAAAABJRU5ErkJggg==" id="imagef32ec50e6c" transform="scale(1 -1) translate(0 -67.68)" x="330.48" y="-21.982015" width="67.68" height="67.68"/>
   </g>
   <g id="text_5">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="364.127586" y="16.317187" transform="rotate(-0 364.127586 16.317187)">40</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="peef0d0a10f">
   <rect x="7.2" y="22.317188" width="67.344828" height="67.344828"/>
  </clipPath>
  <clipPath id="pc2406ca5e2">
   <rect x="88.013793" y="22.317188" width="67.344828" height="67.344828"/>
  </clipPath>
  <clipPath id="p686ff36b1c">
   <rect x="168.827586" y="22.317188" width="67.344828" height="67.344828"/>
  </clipPath>
  <clipPath id="pf375ddb09e">
   <rect x="249.641379" y="22.317188" width="67.344828" height="67.344828"/>
  </clipPath>
  <clipPath id="p89a0b75e73">
   <rect x="330.455172" y="22.317187" width="67.344828" height="67.344828"/>
  </clipPath>
 </defs>
</svg>
<figcaption>From the left: the original (64 columns), then the image back from 5, 10, 20 and 40 components.</figcaption>
</figure>

## What we see

- Each line: the number of components, the variance kept, the mean error per
  pixel.
- 5 components keep only 54.5% of the variance; the overall shape of the
  zero remains but the pixel shades are off: the error per pixel is 1.95 (on
  a 0–16 scale).
- The error falls as components are added: 0.95 at 20 (89.4%), 0.27 at 40
  (98.8%); the 40-component picture is hard to tell from the original.

## When

- Shrinking data to store or send it (20 numbers instead of 64).
- Removing noise: small components are often noise; going back with few
  components drops it.
- In a pipeline, the number of components to keep is chosen by measuring the
  **model's score**, not the error.
