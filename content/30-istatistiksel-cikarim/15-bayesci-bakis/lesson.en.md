# An Introduction to the Bayesian View

Throughout this module we used **frequentist** statistics: we asked "if H₀
were true, how surprising would this data be?" and computed p-values and
confidence intervals. Teams, however, often ask something else: "what is the
**probability** that B is better than A?" The approach that answers this
question directly is **Bayesian** statistics. This section shows its core
idea and its use in A/B testing.

## Bayes' theorem: updating a belief with new information

$$P(H \mid D) = \frac{P(D \mid H) \, P(H)}{P(D)}$$

- $P(H)$: the belief **before** the data, the **prior**.
- $P(D \mid H)$: the probability of this data if H is true, the
  **likelihood**.
- $P(H \mid D)$: the belief **after** seeing the data, the **posterior**.

In the p-Value and Its Misreadings section we saw something by simulation: if most ideas do not
work, a large share of "significant" results are false alarms. That is Bayes'
theorem itself. When the data "it came out significant" arrives, the
probability that the idea really works:

```python
def real_given_significant(prior, power, alpha=0.05):
    hit = prior * power
    false_alarm = (1 - prior) * alpha
    return hit / (hit + false_alarm)


for prior in [0.1, 0.5]:
    for power in [0.2, 0.8]:
        print(prior, power, round(real_given_significant(prior, power), 3))
```

```text
0.1 0.2 0.308
0.1 0.8 0.64
0.5 0.2 0.8
0.5 0.8 0.941
```

- If only 10% of ideas work and the tests have power 0.2, only
  31% of significant results are real.
- With power 0.8 this becomes 64%. That is one more reason
  for the calculation in the Power Analysis section.
- When the prior belief changes, the same "significant" result means
  something very different.

## Prior and posterior for rates: the Beta distribution

We express our belief about a buying rate with a distribution between 0 and
1. The **Beta distribution** is made for this: start with a Beta(a, b) prior,
see that k of n people bought, and the posterior is Beta(a + k, b + n − k).
That is the whole calculation: add the successes and failures to the prior.
Beta(1, 1) is the "flat" prior that treats every rate as equally likely.

In the checkout button test (4000 per group):

```python
import numpy as np
from scipy import stats
from ab_data import make_checkout_test

shop = make_checkout_test()
k = shop.groupby("group")["bought"].sum()
n = shop.groupby("group")["bought"].size()
for g in ["A", "B"]:
    post = stats.beta(1 + k[g], 1 + n[g] - k[g])
    low, high = post.ppf([0.025, 0.975])
    print(g, k[g], round(post.mean(), 4), round(low, 4), round(high, 4))
```

```text
A 472 0.1182 0.1084 0.1284
B 560 0.1402 0.1296 0.1511
```

On each line: the number who bought, the posterior mean and the 95%
**credible interval**. A credible interval is read the way a confidence
interval is wrongly read, and here it is right: "with this data, the
probability that the rate is in this interval is 95%."

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="494.252812pt" height="215.749969pt" viewBox="0 0 494.252812 215.749969" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 215.749969 
L 494.252812 215.749969 
L 494.252812 0 
L 0 0 
L 0 215.749969 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 177.549187 
L 220.254545 177.549187 
L 220.254545 22.317187 
L 7.2 22.317187 
L 7.2 177.549187 
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
       <use xlink:href="#m15aed4d867" x="16.884298" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="16.884298" y="192.146844" transform="rotate(-0 16.884298 192.146844)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="72.22314" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="72.22314" y="192.146844" transform="rotate(-0 72.22314 192.146844)">0.1</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="127.561983" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="127.561983" y="192.146844" transform="rotate(-0 127.561983 192.146844)">0.2</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="182.900826" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="182.900826" y="192.146844" transform="rotate(-0 182.900826 192.146844)">0.3</text>
     </g>
    </g>
    <g id="text_5">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="206.147625" transform="rotate(-0 113.727273 206.147625)">Buying rate</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_5">
    <path d="M 16.884298 170.493187 
L 17.854344 170.390786 
L 18.501042 170.049726 
L 19.147739 169.355011 
L 19.794437 168.230741 
L 20.441135 166.63014 
L 21.087832 164.530405 
L 22.057879 160.442059 
L 23.027925 155.27811 
L 24.321321 146.909022 
L 25.938065 134.560048 
L 28.201507 115.148528 
L 32.081693 81.505209 
L 34.021786 66.6287 
L 35.63853 55.895075 
L 36.931925 48.563676 
L 38.22532 42.419394 
L 39.518716 37.487261 
L 40.488762 34.580399 
L 41.458809 32.338891 
L 42.428855 30.742655 
L 43.075553 30.024386 
L 43.722251 29.572591 
L 44.368948 29.377594 
L 45.015646 29.42906 
L 45.662344 29.716116 
L 46.309041 30.227469 
L 47.279088 31.389585 
L 48.249134 32.990144 
L 49.219181 34.988626 
L 50.512576 38.202433 
L 52.12932 42.97041 
L 54.069413 49.562069 
L 56.332855 58.099765 
L 60.213041 73.805545 
L 65.386622 94.642723 
L 68.296762 105.513498 
L 70.883552 114.409174 
L 73.470343 122.49299 
L 75.733785 128.873192 
L 77.997227 134.608126 
L 80.260669 139.717088 
L 82.52411 144.231515 
L 84.787552 148.190976 
L 86.727645 151.176699 
L 88.991087 154.225194 
L 91.254529 156.850251 
L 93.517971 159.097996 
L 95.781413 161.012489 
L 98.044854 162.63499 
L 100.308296 164.003509 
L 102.895087 165.300686 
L 105.481878 166.357071 
L 108.392017 167.307384 
L 111.625505 168.124258 
L 115.182342 168.795542 
L 119.385877 169.35899 
L 124.559459 169.812168 
L 131.026435 170.140536 
L 140.080203 170.357913 
L 155.277598 170.468502 
L 203.456574 170.493134 
L 210.570248 170.493168 
L 210.570248 170.493168 
" clip-path="url(#pb10c4c7451)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_6">
    <path d="M 16.884298 170.493187 
L 27.878158 170.393199 
L 30.464948 170.152541 
L 32.405041 169.77643 
L 34.021786 169.270477 
L 35.63853 168.534849 
L 37.255274 167.517657 
L 38.548669 166.46803 
L 39.842065 165.184218 
L 41.458809 163.221546 
L 43.075553 160.83595 
L 44.692297 158.012145 
L 46.309041 154.748372 
L 48.249134 150.269332 
L 50.189227 145.22242 
L 52.452669 138.716128 
L 55.362809 129.617014 
L 65.063273 98.519034 
L 67.326715 92.260261 
L 69.266808 87.477274 
L 71.206901 83.313579 
L 72.823645 80.359914 
L 74.44039 77.901547 
L 75.733785 76.301879 
L 77.02718 75.032704 
L 78.320576 74.094336 
L 79.613971 73.483904 
L 80.584017 73.237893 
L 81.554064 73.169669 
L 82.52411 73.274988 
L 83.817506 73.676697 
L 85.110901 74.364503 
L 86.404296 75.323128 
L 87.697692 76.535836 
L 89.314436 78.381652 
L 90.93118 80.559561 
L 92.871273 83.557525 
L 95.134715 87.50036 
L 97.721506 92.464179 
L 101.278343 99.820198 
L 113.242249 125.047538 
L 116.475738 131.192042 
L 119.709226 136.846439 
L 122.619366 141.477212 
L 125.529505 145.658728 
L 128.116296 148.999095 
L 130.703086 151.994068 
L 133.289877 154.658293 
L 135.876668 157.010668 
L 138.463458 159.072989 
L 141.050249 160.868787 
L 143.960389 162.600743 
L 146.870528 164.060655 
L 149.780668 165.281949 
L 153.014156 166.397388 
L 156.570993 167.37645 
L 160.451179 168.201848 
L 164.654714 168.869466 
L 169.504946 169.417225 
L 175.325225 169.849249 
L 182.762248 170.16905 
L 193.109411 170.375231 
L 210.570248 170.474658 
L 210.570248 170.474658 
" clip-path="url(#pb10c4c7451)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_3">
    <path d="M 7.2 177.549187 
L 7.2 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 220.254545 177.549187 
L 220.254545 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 7.2 177.549187 
L 220.254545 177.549187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 7.2 22.317187 
L 220.254545 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_6">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="16.317187" transform="rotate(-0 113.727273 16.317187)">60 per group</text>
   </g>
   <g id="legend_1">
    <g id="line2d_7">
     <path d="M 176.393608 35.415625 
L 186.393608 35.415625 
L 196.393608 35.415625 
" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="204.393608" y="38.915625" transform="rotate(-0 204.393608 38.915625)">A</text>
    </g>
    <g id="line2d_8">
     <path d="M 176.393608 50.416406 
L 186.393608 50.416406 
L 196.393608 50.416406 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="204.393608" y="53.916406" transform="rotate(-0 204.393608 53.916406)">B</text>
    </g>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_7">
    <path d="M 262.865455 177.549187 
L 475.92 177.549187 
L 475.92 22.317187 
L 262.865455 22.317187 
L 262.865455 177.549187 
z
" style="fill: none"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="262.865455" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="262.865455" y="192.146844" transform="rotate(-0 262.865455 192.146844)">0.08</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="305.476364" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="305.476364" y="192.146844" transform="rotate(-0 305.476364 192.146844)">0.10</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="348.087273" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="348.087273" y="192.146844" transform="rotate(-0 348.087273 192.146844)">0.12</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="390.698182" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="390.698182" y="192.146844" transform="rotate(-0 390.698182 192.146844)">0.14</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="433.309091" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="433.309091" y="192.146844" transform="rotate(-0 433.309091 192.146844)">0.16</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_14">
      <g>
       <use xlink:href="#m15aed4d867" x="475.92" y="177.549187" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="475.92" y="192.146844" transform="rotate(-0 475.92 192.146844)">0.18</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="206.147625" transform="rotate(-0 369.392727 206.147625)">Buying rate</text>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_15">
    <path d="M 92.421818 170.493187 
L 304.053629 170.406357 
L 307.788308 170.146759 
L 310.278094 169.694043 
L 311.522987 169.309931 
L 312.76788 168.770269 
L 314.012773 168.025689 
L 315.257666 167.016804 
L 316.502559 165.674285 
L 317.747452 163.919812 
L 318.992345 161.668131 
L 320.237238 158.830385 
L 321.482131 155.318794 
L 322.727024 151.052649 
L 323.971917 145.965413 
L 325.21681 140.012533 
L 326.461703 133.179422 
L 327.706596 125.488908 
L 330.196382 107.848594 
L 337.66574 50.594651 
L 338.910633 43.241953 
L 340.155526 37.260008 
L 341.400419 32.862088 
L 342.645312 30.203641 
L 343.890205 29.373187 
L 345.135098 30.387563 
L 346.379991 33.191839 
L 347.624884 37.663846 
L 348.869777 43.622801 
L 350.11467 50.841209 
L 352.604456 67.998533 
L 358.828921 114.336157 
L 361.318707 129.897827 
L 362.5636 136.579552 
L 363.808493 142.488353 
L 365.053386 147.632394 
L 366.298279 152.043559 
L 367.543172 155.771425 
L 368.788065 158.877493 
L 370.032958 161.430009 
L 371.277851 163.499566 
L 372.522744 165.15559 
L 373.767637 166.463727 
L 375.01253 167.484063 
L 376.257423 168.270083 
L 377.502316 168.868237 
L 379.992102 169.652151 
L 382.481888 170.075716 
L 386.216567 170.358028 
L 392.441032 170.476312 
L 418.583785 170.493187 
L 495.252812 170.493187 
L 495.252812 170.493187 
" clip-path="url(#p6dda9b9836)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 92.421818 170.493187 
L 347.624884 170.413454 
L 351.359563 170.206913 
L 353.849349 169.868912 
L 356.339135 169.207138 
L 357.584028 168.685765 
L 358.828921 167.988028 
L 360.073814 167.068395 
L 361.318707 165.874649 
L 362.5636 164.348581 
L 363.808493 162.427345 
L 365.053386 160.045553 
L 366.298279 157.138167 
L 367.543172 153.644172 
L 368.788065 149.510921 
L 370.032958 144.698991 
L 371.277851 139.187257 
L 372.522744 132.977849 
L 375.01253 118.616278 
L 377.502316 102.236131 
L 382.481888 68.400474 
L 383.726781 60.920314 
L 384.971674 54.272012 
L 386.216567 48.65647 
L 387.46146 44.247038 
L 388.706353 41.180555 
L 389.951246 39.550271 
L 391.196139 39.401177 
L 392.441032 40.728038 
L 393.685925 43.476268 
L 394.930818 47.545507 
L 396.175711 52.79561 
L 397.420604 59.054529 
L 399.91039 73.806872 
L 407.379748 121.634605 
L 409.869534 134.699988 
L 411.114427 140.324995 
L 412.35932 145.323272 
L 413.604213 149.704563 
L 414.849106 153.494758 
L 416.093999 156.731931 
L 417.338892 159.462554 
L 418.583785 161.73806 
L 419.828678 163.61189 
L 421.073571 165.137071 
L 422.318464 166.364358 
L 423.563357 167.340894 
L 424.80825 168.109365 
L 426.053143 168.707548 
L 428.542929 169.519213 
L 431.032715 169.981411 
L 434.767394 170.31127 
L 439.746966 170.452835 
L 453.440789 170.492876 
L 495.252812 170.493187 
L 495.252812 170.493187 
" clip-path="url(#p6dda9b9836)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_8">
    <path d="M 262.865455 177.549187 
L 262.865455 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_9">
    <path d="M 475.92 177.549187 
L 475.92 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_10">
    <path d="M 262.865455 177.549187 
L 475.92 177.549187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_11">
    <path d="M 262.865455 22.317187 
L 475.92 22.317187 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 12px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="16.317187" transform="rotate(-0 369.392727 16.317187)">4000 per group</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pb10c4c7451">
   <rect x="7.2" y="22.317187" width="213.054545" height="155.232"/>
  </clipPath>
  <clipPath id="p6dda9b9836">
   <rect x="262.865455" y="22.317187" width="213.054545" height="155.232"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Posterior distributions with a flat prior. With little data the two curves are wide and overlap a lot; with much data they are narrow and almost separate (the right axis is zoomed).</figcaption>
</figure>

## The probability that B is better

If we draw many samples from the two posteriors and compare them, we answer
every question by counting:

```python
rng = np.random.default_rng(502)
draw_a = rng.beta(1 + k["A"], 1 + n["A"] - k["A"], 200_000)
draw_b = rng.beta(1 + k["B"], 1 + n["B"] - k["B"], 200_000)
lift = draw_b - draw_a
print(round((draw_b > draw_a).mean(), 4))
print(np.round(np.percentile(lift, [2.5, 97.5]), 4))
loss_b = np.maximum(-lift, 0).mean()
loss_a = np.maximum(lift, 0).mean()
print(f"{loss_b:.1e}", round(loss_a, 4))
```

```text
0.9985
[0.0073 0.0367]
3.4e-06 0.022
```

- **P(B > A)** = 0.999: "the probability that B is better". This is
  the question the team was really asking.
- The difference's credible interval is almost the same as the confidence
  interval in the Effect Size section (0.0073 – 0.0367). With a large sample
  and a flat prior the two approaches meet in the numbers; their **readings**
  differ.
- The last line is the **expected loss**: if we choose B and are wrong, how
  much do we lose on average? The loss of choosing B is tiny, the loss of
  staying with A about 0.022 (in buying rate). Many teams decide
  with the rule "choose once the loss drops below a threshold".

## Are p and P(B > A) the same thing?

```python
from statsmodels.stats.proportion import proportions_ztest

p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]],
                      alternative="larger")[1]
print(round(p, 4), round(1 - (draw_b > draw_a).mean(), 4))
```

```text
0.0017 0.0015
```

The one-sided p and $1 - P(B > A)$ are very close here. That is a result of
the flat prior and the large sample, not a rule. Their meanings still differ:
p asks "if there were no difference, how surprising would this data be?",
$P(B > A)$ asks "with this data, what is the probability B is better?". The
second also depends on the prior.

## The effect of the prior

In a small test (60 per group) the prior changes the result noticeably. If
we know from past data that the buying rate is about 11.4%, we can write it
as a prior worth 100 people of information: Beta(11.4, 88.6).

```python
small = make_checkout_test(n=60, seed=503)
k_s = small.groupby("group")["bought"].sum()
for a0, b0 in [(1, 1), (11.4, 88.6)]:
    s_a = rng.beta(a0 + k_s["A"], b0 + 60 - k_s["A"], 200_000)
    s_b = rng.beta(a0 + k_s["B"], b0 + 60 - k_s["B"], 200_000)
    print(a0, b0, round(s_a.mean(), 3), round(s_b.mean(), 3),
          round((s_b > s_a).mean(), 3))
```

```text
1 1 0.065 0.129 0.897
11.4 88.6 0.09 0.115 0.773
```

- In the small sample A saw 3 purchases and B 7. The
  flat prior believes these small numbers completely; the informed prior
  pulls both rates toward the known 11.4% (**shrinkage**).
- P(B > A) is 0.897 with the flat prior and 0.773 with
  the informed one. A result that looks "very promising" on small data is
  more measured with an informed prior.
- With 4000 per group the two priors give almost the same result: as the
  data grows, the prior's weight melts away.

The prior is written before looking at the data, with a justification.
Choosing the prior after seeing the result is as wrong as choosing the
threshold afterwards.

## When to use which?

- **Frequentist:** fixes and controls the false alarm rate in advance;
  common in teams, little to argue about.
- **Bayesian:** gives numbers a decision maker understands, like "the
  probability B is better" and "the expected loss"; brings in past
  knowledge through the prior.
- The Bayesian method does not magically solve the problem of stopping the
  test whenever you like either; the rules are still written in advance.

## Summary

- Bayes' theorem updates a prior belief with data into a posterior belief.
- For rates, a Beta(a, b) prior with k successes in n becomes a
  Beta(a + k, b + n − k) posterior.
- A credible interval is read "the rate is in this interval with 95%
  probability".
- Drawing samples from the posteriors gives P(B > A) and the expected loss.
- The prior changes the result noticeably on small data and melts away on
  large data; it is chosen in advance with a justification.
