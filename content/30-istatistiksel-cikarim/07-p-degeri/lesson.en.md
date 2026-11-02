# The p-Value and Its Misreadings

The p-value is the most used and most misread number in statistics. Its
definition is one sentence: **the probability of a result at least this
extreme if $H_0$ were true**. The trouble is that this sentence sounds like
other things: "the probability that the result is due to chance", "the
probability that $H_0$ is true", "the size of the effect". It is none of
them. In this section we will refute each misreading by simulation, because
the best way to understand what a p-value is, is to look at thousands of
them.

The examples compare two groups: we draw two separate groups from the
session lengths and test their means with a **two-sample t-test**
(`stats.ttest_ind`). The details of the test come in the next section; here
we only look at the p-value it gives.

## How are p-values distributed when there is no difference?

Draw both groups from the same population: the true difference is zero.
10,000 times:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(91)
a = rng.choice(x, size=(10000, 100))
b = rng.choice(x, size=(10000, 100))
p = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
print(round((p < 0.05).mean(), 3), round((p < 0.5).mean(), 3))
print(np.histogram(p, bins=5, range=(0, 1))[0])
```

```text
0.055 0.507
[2090 2007 2006 1980 1917]
```

- With no difference the p-value is **uniformly** distributed between 0 and
  1: about 2000 tests fall into each fifth.
- About 5.5% of tests fell below 0.05, half below 0.5. So seeing a
  "significant" result with no difference is not surprising at all: it
  happens once every twenty tries.

## How are p-values distributed when there is a difference?

Now let the second group's sessions be truly 10% longer:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(91)
a = rng.choice(x, size=(10000, 100))
b = rng.choice(x, size=(10000, 100)) * 1.10
p = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue
print(round((p < 0.05).mean(), 3))
print(np.round(np.percentile(p, [10, 50, 90]), 3))
```

```text
0.174
[0.022 0.28  0.836]
```

- There is a real effect, but with 100 people per group only 17.4% of
  tests found it "significant" (the power).
- Over repeats of the same experiment the p-value wandered between
  0.022 and 0.836 (the 10th and 90th percentiles). Someone who
  sees p = 0.02 in one experiment and repeats it may see p = 0.6 the second
  time. **The p-value is not a measure of reproducibility.**

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="483.12pt" height="225.319219pt" viewBox="0 0 483.12 225.319219" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 225.319219 
L 483.12 225.319219 
L 483.12 0 
L 0 0 
L 0 225.319219 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 187.118437 
L 220.254545 187.118437 
L 220.254545 20.798437 
L 7.2 20.798437 
L 7.2 187.118437 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 16.884298 187.118437 
L 26.568595 187.118437 
L 26.568595 136.925097 
L 16.884298 136.925097 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_4">
    <path d="M 26.568595 187.118437 
L 36.252893 187.118437 
L 36.252893 143.017404 
L 26.568595 143.017404 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_5">
    <path d="M 36.252893 187.118437 
L 45.93719 187.118437 
L 45.93719 136.743237 
L 36.252893 136.743237 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_6">
    <path d="M 45.93719 187.118437 
L 55.621488 187.118437 
L 55.621488 141.744385 
L 45.93719 141.744385 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_7">
    <path d="M 55.621488 187.118437 
L 65.305785 187.118437 
L 65.305785 141.198805 
L 55.621488 141.198805 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_8">
    <path d="M 65.305785 187.118437 
L 74.990083 187.118437 
L 74.990083 139.743925 
L 65.305785 139.743925 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_9">
    <path d="M 74.990083 187.118437 
L 84.67438 187.118437 
L 84.67438 141.835315 
L 74.990083 141.835315 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_10">
    <path d="M 84.67438 187.118437 
L 94.358678 187.118437 
L 94.358678 143.199264 
L 84.67438 143.199264 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_11">
    <path d="M 94.358678 187.118437 
L 104.042975 187.118437 
L 104.042975 140.198575 
L 94.358678 140.198575 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_12">
    <path d="M 104.042975 187.118437 
L 113.727273 187.118437 
L 113.727273 145.654373 
L 104.042975 145.654373 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_13">
    <path d="M 113.727273 187.118437 
L 123.41157 187.118437 
L 123.41157 138.198116 
L 113.727273 138.198116 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_14">
    <path d="M 123.41157 187.118437 
L 133.095868 187.118437 
L 133.095868 142.017175 
L 123.41157 142.017175 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_15">
    <path d="M 133.095868 187.118437 
L 142.780165 187.118437 
L 142.780165 145.654373 
L 133.095868 145.654373 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_16">
    <path d="M 142.780165 187.118437 
L 152.464463 187.118437 
L 152.464463 143.017404 
L 142.780165 143.017404 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_17">
    <path d="M 152.464463 187.118437 
L 162.14876 187.118437 
L 162.14876 141.289735 
L 152.464463 141.289735 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_18">
    <path d="M 162.14876 187.118437 
L 171.833058 187.118437 
L 171.833058 138.470906 
L 162.14876 138.470906 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_19">
    <path d="M 171.833058 187.118437 
L 181.517355 187.118437 
L 181.517355 140.653225 
L 171.833058 140.653225 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_20">
    <path d="M 181.517355 187.118437 
L 191.201653 187.118437 
L 191.201653 143.653914 
L 181.517355 143.653914 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_21">
    <path d="M 191.201653 187.118437 
L 200.88595 187.118437 
L 200.88595 144.745074 
L 191.201653 144.745074 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_22">
    <path d="M 200.88595 187.118437 
L 210.570248 187.118437 
L 210.570248 145.108793 
L 200.88595 145.108793 
z
" clip-path="url(#p578913c353)" style="fill: #8b5cf6; opacity: 0.8"/>
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
       <use xlink:href="#m15aed4d867" x="16.884298" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="16.884298" y="201.716094" transform="rotate(-0 16.884298 201.716094)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="55.621488" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="55.621488" y="201.716094" transform="rotate(-0 55.621488 201.716094)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="94.358678" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="94.358678" y="201.716094" transform="rotate(-0 94.358678 201.716094)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="133.095868" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="133.095868" y="201.716094" transform="rotate(-0 133.095868 201.716094)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="171.833058" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="171.833058" y="201.716094" transform="rotate(-0 171.833058 201.716094)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="210.570248" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.570248" y="201.716094" transform="rotate(-0 210.570248 201.716094)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="215.716875" transform="rotate(-0 113.727273 215.716875)">p-value</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_7">
    <path d="M 26.568595 187.118437 
L 26.568595 20.798437 
" clip-path="url(#p578913c353)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_23">
    <path d="M 7.2 187.118437 
L 7.2 20.798438 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 220.254545 187.118437 
L 220.254545 20.798438 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 7.2 187.118437 
L 220.254545 187.118437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 7.2 20.798437 
L 220.254545 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_8">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="113.727273" y="14.798437" transform="rotate(-0 113.727273 14.798437)">No difference</text>
   </g>
  </g>
  <g id="axes_2">
   <g id="patch_27">
    <path d="M 262.865455 187.118437 
L 475.92 187.118437 
L 475.92 20.798437 
L 262.865455 20.798437 
L 262.865455 187.118437 
z
" style="fill: none"/>
   </g>
   <g id="patch_28">
    <path d="M 272.549752 187.118437 
L 282.23405 187.118437 
L 282.23405 28.718437 
L 272.549752 28.718437 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_29">
    <path d="M 282.23405 187.118437 
L 291.918347 187.118437 
L 291.918347 97.097772 
L 282.23405 97.097772 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_30">
    <path d="M 291.918347 187.118437 
L 301.602645 187.118437 
L 301.602645 123.012812 
L 291.918347 123.012812 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_31">
    <path d="M 301.602645 187.118437 
L 311.286942 187.118437 
L 311.286942 128.7414 
L 301.602645 128.7414 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_32">
    <path d="M 311.286942 187.118437 
L 320.97124 187.118437 
L 320.97124 138.379976 
L 311.286942 138.379976 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_33">
    <path d="M 320.97124 187.118437 
L 330.655537 187.118437 
L 330.655537 141.289735 
L 320.97124 141.289735 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_34">
    <path d="M 330.655537 187.118437 
L 340.339835 187.118437 
L 340.339835 144.381354 
L 330.655537 144.381354 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_35">
    <path d="M 340.339835 187.118437 
L 350.024132 187.118437 
L 350.024132 150.382731 
L 340.339835 150.382731 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_36">
    <path d="M 350.024132 187.118437 
L 359.70843 187.118437 
L 359.70843 149.928082 
L 350.024132 149.928082 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_37">
    <path d="M 359.70843 187.118437 
L 369.392727 187.118437 
L 369.392727 153.65621 
L 359.70843 153.65621 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_38">
    <path d="M 369.392727 187.118437 
L 379.077025 187.118437 
L 379.077025 154.20179 
L 369.392727 154.20179 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_39">
    <path d="M 379.077025 187.118437 
L 388.761322 187.118437 
L 388.761322 155.20202 
L 379.077025 155.20202 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_40">
    <path d="M 388.761322 187.118437 
L 398.44562 187.118437 
L 398.44562 156.929689 
L 388.761322 156.929689 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_41">
    <path d="M 398.44562 187.118437 
L 408.129917 187.118437 
L 408.129917 157.566199 
L 398.44562 157.566199 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_42">
    <path d="M 408.129917 187.118437 
L 417.814215 187.118437 
L 417.814215 155.838529 
L 408.129917 155.838529 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_43">
    <path d="M 417.814215 187.118437 
L 427.498512 187.118437 
L 427.498512 159.475728 
L 417.814215 159.475728 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_44">
    <path d="M 427.498512 187.118437 
L 437.18281 187.118437 
L 437.18281 156.838759 
L 427.498512 156.838759 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_45">
    <path d="M 437.18281 187.118437 
L 446.867107 187.118437 
L 446.867107 160.021308 
L 437.18281 160.021308 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_46">
    <path d="M 446.867107 187.118437 
L 456.551405 187.118437 
L 456.551405 161.112467 
L 446.867107 161.112467 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_47">
    <path d="M 456.551405 187.118437 
L 466.235702 187.118437 
L 466.235702 160.294098 
L 456.551405 160.294098 
z
" clip-path="url(#peb0d66ab89)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="matplotlib.axis_3">
    <g id="xtick_7">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m15aed4d867" x="272.549752" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="272.549752" y="201.716094" transform="rotate(-0 272.549752 201.716094)">0.0</text>
     </g>
    </g>
    <g id="xtick_8">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m15aed4d867" x="311.286942" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="311.286942" y="201.716094" transform="rotate(-0 311.286942 201.716094)">0.2</text>
     </g>
    </g>
    <g id="xtick_9">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m15aed4d867" x="350.024132" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.024132" y="201.716094" transform="rotate(-0 350.024132 201.716094)">0.4</text>
     </g>
    </g>
    <g id="xtick_10">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m15aed4d867" x="388.761322" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="388.761322" y="201.716094" transform="rotate(-0 388.761322 201.716094)">0.6</text>
     </g>
    </g>
    <g id="xtick_11">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m15aed4d867" x="427.498512" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="427.498512" y="201.716094" transform="rotate(-0 427.498512 201.716094)">0.8</text>
     </g>
    </g>
    <g id="xtick_12">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m15aed4d867" x="466.235702" y="187.118437" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="466.235702" y="201.716094" transform="rotate(-0 466.235702 201.716094)">1.0</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="215.716875" transform="rotate(-0 369.392727 215.716875)">p-value</text>
    </g>
   </g>
   <g id="matplotlib.axis_4"/>
   <g id="line2d_14">
    <path d="M 282.23405 187.118437 
L 282.23405 20.798437 
" clip-path="url(#peb0d66ab89)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="patch_48">
    <path d="M 262.865455 187.118437 
L 262.865455 20.798438 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_49">
    <path d="M 475.92 187.118437 
L 475.92 20.798438 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_50">
    <path d="M 262.865455 187.118437 
L 475.92 187.118437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_51">
    <path d="M 262.865455 20.798437 
L 475.92 20.798437 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="text_16">
    <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="369.392727" y="14.798437" transform="rotate(-0 369.392727 14.798437)">A real difference: 10%</text>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p578913c353">
   <rect x="7.2" y="20.798437" width="213.054545" height="166.32"/>
  </clipPath>
  <clipPath id="peb0d66ab89">
   <rect x="262.865455" y="20.798437" width="213.054545" height="166.32"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The p-values of 10,000 tests each. The orange line is 0.05. With no difference p is uniform; with a difference it piles up on the left but still spreads everywhere.</figcaption>
</figure>

## Misreading 1: "p is the probability that H₀ is true"

A team tries 2000 ideas. In truth only one in ten works (adds 10%); the rest
change nothing. Each idea is tested with 100 people per group. How many of
the "significant" results are ideas that really work?

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(92)
for n in [100, 400]:
    works = rng.random(2000) < 0.10
    lift = np.where(works, 1.10, 1.0)[:, None]
    a = rng.choice(x, size=(2000, n))
    b = rng.choice(x, size=(2000, n)) * lift
    sig = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue < 0.05
    false_hits = (sig & ~works).sum()
    print(n, works.sum(), sig.sum(), false_hits, round(false_hits / sig.sum(), 2))
```

```text
100 212 113 80 0.71
400 195 212 102 0.48
```

Columns: people per group, ideas that really work, significant results,
how many of those do not work, and their share.

- With 100-person tests there were 113 significant results; 80
  of them were ideas that **do nothing**: a share of 71%. Each one
  had p < 0.05.
- With 400 people power grew and the share of wrong results became
  48%; lower, but still not small.
- Lesson: p < 0.05 does **not** mean "this result has a 5% chance of being
  wrong". That chance depends on two more things besides p: how many of the
  tried ideas really work, and the power of the test. If both are low, most
  "significant" results are false alarms.

## Misreading 2: "A small p means a big effect"

In a very large sample even a tiny difference becomes "highly significant":

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(93)
a = rng.choice(x, size=100000)
b = rng.choice(x, size=100000) * 1.01
result = stats.ttest_ind(b, a, equal_var=False)
print(f"{result.pvalue:.1e}", round(b.mean() - a.mean(), 3))
```

```text
1.0e-07 0.146
```

p is about one in ten million; the difference is 0.146 minutes per
session, less than 10 seconds. Statistically certain, practically perhaps
trivial. p answers "is the difference zero?", not "does the difference
matter?". The **effect size** answers that; it has its own section.

## Misreading 3: "I looked at 20 things and one was significant"

Imagine an experiment where 20 different metrics (session length, clicks,
basket, ...) are examined; none has a real difference. What is the chance
that at least one has p < 0.05?

```python
import numpy as np
from scipy import stats
from ab_data import make_population

x = make_population()["minutes"].to_numpy()
rng = np.random.default_rng(94)
hits = 0
for _ in range(2000):
    a = rng.choice(x, size=(20, 50))
    b = rng.choice(x, size=(20, 50))
    p = stats.ttest_ind(a, b, axis=1, equal_var=False).pvalue
    hits += (p < 0.05).any()
print(round(hits / 2000, 3), round(1 - 0.95 ** 20, 3))
```

```text
0.626 0.642
```

- In 62.6% of 2000 experiments at least one of the 20 metrics came
  out "significant". The formula $1 - 0.95^{20} \approx 0.64$ says the same.
- Reporting only that metric afterwards, or slicing the data in different
  ways until something is significant, is known as **p-hacking**, and it is
  the shortest way to produce wrong results. The cure: write down in advance
  which metric will be examined, or use a multiple comparison correction (in
  the second module).

## Reading it correctly

On its own, a p-value says: "How surprising would this data be if there
were no difference?" In a report, always put next to it:

- the difference itself and its confidence interval (how much?),
- the sample size and the power (what was the chance of missing?),
- how many things were examined (how many tries?).

And avoid reading p = 0.049 as "certainly there" and p = 0.051 as
"certainly not". They are almost the same evidence; 0.05 is a decision
threshold, not a boundary of nature.

## Summary

- With no difference p is uniformly distributed; one test in twenty comes
  out "significant".
- p is not the probability that $H_0$ is true; how many "significant"
  results are right depends on power and on how good the tried ideas are.
- A small p does not mean a big effect; in a large sample a trivial
  difference is significant too.
- p does not measure reproducibility; the same experiment can give very
  different p-values.
- Looking at many things and picking the significant one multiplies false
  alarms.
