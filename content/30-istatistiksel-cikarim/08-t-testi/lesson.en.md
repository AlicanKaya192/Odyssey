# The t-Test

In the previous two sections we saw the logic of testing and the p-value.
Now we learn the most widely used test in detail: the **t-test**. It has
three kinds, and each answers a different question:

| Kind | Question | scipy |
|---|---|---|
| One-sample | Is this group's mean different from a given value? | `ttest_1samp` |
| Two independent samples | Are the means of two separate groups different? | `ttest_ind` |
| Paired (dependent) samples | Are the before/after measurements of the same units different? | `ttest_rel` |

We used the one-sample t-test in The Logic of Hypothesis Testing. This
section focuses on the other two and on when to choose which; picking the
wrong kind is the easiest way to get a wrong result from the right data.

## Two independent groups: a design test

A new page design was tried: half of the users saw the old one (A), half the
new one (B). The question: did the new design make sessions longer?

```python
from scipy import stats
from ab_data import make_design_test

test = make_design_test()
a = test.loc[test["group"] == "A", "minutes"]
b = test.loc[test["group"] == "B", "minutes"]
result = stats.ttest_ind(b, a, equal_var=False)
low, high = result.confidence_interval(0.95)
print(len(a), round(a.mean(), 2), round(b.mean(), 2))
print(round(result.statistic, 3), f"{result.pvalue:.4f}")
print(round(b.mean() - a.mean(), 2), round(low, 2), round(high, 2))
```

```text
500 8.47 9.79
3.644 0.0003
1.32 0.61 2.03
```

- Each group has 500 users. B's mean is 9.79, A's 8.47
  minutes.
- p = 0.0003: with no difference, seeing a difference this large is very
  unlikely.
- The 95% confidence interval of the difference is 0.61 to
  2.03 minutes. This line says more than p: the new design very
  likely makes sessions longer, but by how much is still a wide range.
- We generated the data: the true effect is 10%, about 0.9 minutes. The
  interval contains it; the observed difference (1.32) came out a bit
  large by chance.

## Inside the formula: Welch's test

The difference between the two means is divided by the standard error of
the difference. Since the difference comes from two independent means,
their variances add up:

$$t = \dfrac{\bar{x}_B - \bar{x}_A}{\sqrt{\dfrac{s_A^2}{n_A} + \dfrac{s_B^2}{n_B}}}$$

```python
import numpy as np
from ab_data import make_design_test

test = make_design_test()
a = test.loc[test["group"] == "A", "minutes"]
b = test.loc[test["group"] == "B", "minutes"]
se = np.sqrt(a.var() / len(a) + b.var() / len(b))
print(round((b.mean() - a.mean()) / se, 3))
print(round(a.std(), 2), round(b.std(), 2))
```

```text
3.644
5.29 6.15
```

The t we found by hand is the same as the one from `ttest_ind`. This formula
accepts that the two groups' deviations may **differ**; it is called
**Welch's t-test**. In scipy it is chosen with `equal_var=False`.

## Student or Welch?

By default (`equal_var=True`) `ttest_ind` runs **Student's t-test**: it
assumes the two groups have equal deviations and pools them. When the
deviations and group sizes differ, that assumption costs dearly. Let us
measure in a world where the true difference is **zero**: the small group
(20 people) is very scattered, the large group (80 people) very consistent.

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(111)
small = rng.normal(10, 6, size=(5000, 20))
large = rng.normal(10, 2, size=(5000, 80))
student = stats.ttest_ind(small, large, axis=1).pvalue
welch = stats.ttest_ind(small, large, axis=1, equal_var=False).pvalue
print(round((student < 0.05).mean(), 3), round((welch < 0.05).mean(), 3))
```

```text
0.259 0.056
```

- With no difference Student's test said "significant" 25.9% of the
  time: five times the promised 5%.
- Welch: 5.6%; it keeps its promise.
- If the deviations really are equal, Welch loses almost nothing. That is why
  the default choice when comparing two groups is **Welch**
  (`equal_var=False`).

## Paired measurements: the same page, before and after

A team compressed images and measured the load time of the same 25 pages
before and after. The pages differ a lot from each other (some light, some
heavy), but each page can be compared with its own earlier self.

```python
from scipy import stats
from ab_data import make_paired_speed

pages = make_paired_speed()
diff = pages["before"] - pages["after"]
print(round(diff.mean(), 1), round(diff.std(), 1))
print(round(pages["before"].std(), 1))
print(round(stats.ttest_rel(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.ttest_ind(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.ttest_1samp(diff, 0).pvalue, 4))
```

```text
17.2 34.9
153.4
0.0211
0.7022
0.0211
```

- The average saving per page is 17.2 ms. The deviation of the
  differences is only 34.9 ms, while the pages' own deviation is
  153.4 ms.
- The **paired t-test** (`ttest_rel`) gives p = 0.0211: the saving is
  significant.
- Applying an independent-groups test to the same data gives p =
  0.7022: nothing shows. The large differences between pages (light
  and heavy ones) bury the 20 ms saving in noise.
- The last line: the paired test is really a one-sample t-test of **the
  differences**; p is exactly the same.

Is that the luck of one dataset? Let us repeat the same experiment with 500
different groups of pages:

```python
import numpy as np
from scipy import stats
from ab_data import make_paired_speed

paired, unpaired = [], []
for seed in range(1000, 1500):
    pages = make_paired_speed(seed=seed)
    before, after = pages["before"], pages["after"]
    paired.append(stats.ttest_rel(before, after).pvalue < 0.05)
    unpaired.append(stats.ttest_ind(before, after).pvalue < 0.05)
print(round(np.mean(paired), 3), round(np.mean(unpaired), 3))
```

```text
0.782 0.0
```

The paired test caught the real 20 ms saving in 78.2% of the
repeats, the independent-groups test in 0.0%. If the data is
paired by structure, use the paired test; it gets much more information out
of the same data.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="373.330781pt" height="230.984781pt" viewBox="0 0 373.330781 230.984781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 230.984781 
L 373.330781 230.984781 
L 373.330781 -0 
L 0 -0 
L 0 230.984781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 53.650781 206.784 
L 366.130781 206.784 
L 366.130781 7.2 
L 53.650781 7.2 
L 53.650781 206.784 
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
       <use xlink:href="#m15aed4d867" x="112.240781" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="112.240781" y="221.382438" transform="rotate(-0 112.240781 221.382438)">before</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="307.540781" y="206.784" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="307.540781" y="221.382438" transform="rotate(-0 307.540781 221.382438)">after</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_3">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="189.823304" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="193.622132" transform="rotate(-0 46.650781 193.622132)">600</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="163.527652" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="167.32648" transform="rotate(-0 46.650781 167.32648)">700</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="137.232" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="141.030828" transform="rotate(-0 46.650781 141.030828)">800</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="110.936348" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="114.735176" transform="rotate(-0 46.650781 114.735176)">900</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="84.640696" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="88.439524" transform="rotate(-0 46.650781 88.439524)">1000</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="58.345043" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="62.143872" transform="rotate(-0 46.650781 62.143872)">1100</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="53.650781" y="32.049391" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="46.650781" y="35.848219" transform="rotate(-0 46.650781 35.848219)">1200</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="106.992" transform="rotate(-90 14.798438 106.992)">Load time (ms)</text>
    </g>
   </g>
   <g id="line2d_10">
    <path d="M 112.240781 76.226087 
L 307.540781 84.903652 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <defs>
     <path id="m0653a46230" d="M 0 1.5 
C 0.397805 1.5 0.77937 1.341951 1.06066 1.06066 
C 1.341951 0.77937 1.5 0.397805 1.5 0 
C 1.5 -0.397805 1.341951 -0.77937 1.06066 -1.06066 
C 0.77937 -1.341951 0.397805 -1.5 0 -1.5 
C -0.397805 -1.5 -0.77937 -1.341951 -1.06066 -1.06066 
C -1.341951 -0.77937 -1.5 -0.397805 -1.5 0 
C -1.5 0.397805 -1.341951 0.77937 -1.06066 1.06066 
C -0.77937 1.341951 -0.397805 1.5 0 1.5 
z
" style="stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </defs>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="76.226087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="84.903652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 112.240781 23.10887 
L 307.540781 22.057043 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="23.10887" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="22.057043" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_12">
    <path d="M 112.240781 164.842435 
L 307.540781 185.878957 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="164.842435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="185.878957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_13">
    <path d="M 112.240781 107.254957 
L 307.540781 128.554435 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="107.254957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="128.554435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 112.240781 57.293217 
L 307.540781 65.970783 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="57.293217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 112.240781 63.078261 
L 307.540781 71.49287 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="63.078261" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="71.49287" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_16">
    <path d="M 112.240781 55.715478 
L 307.540781 55.978435 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="55.715478" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="55.978435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_17">
    <path d="M 112.240781 111.199304 
L 307.540781 101.995826 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="111.199304" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="101.995826" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_18">
    <path d="M 112.240781 65.970783 
L 307.540781 58.345043 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="58.345043" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_19">
    <path d="M 112.240781 20.216348 
L 307.540781 16.272 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="20.216348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="16.272" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_20">
    <path d="M 112.240781 67.285565 
L 307.540781 78.592696 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="67.285565" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="78.592696" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_21">
    <path d="M 112.240781 64.130087 
L 307.540781 65.970783 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="64.130087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="65.970783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_22">
    <path d="M 112.240781 134.076522 
L 307.540781 129.869217 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="134.076522" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="129.869217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_23">
    <path d="M 112.240781 184.301217 
L 307.540781 197.712 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="184.301217" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="197.712" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_24">
    <path d="M 112.240781 131.446957 
L 307.540781 128.291478 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="131.446957" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="128.291478" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_25">
    <path d="M 112.240781 115.406609 
L 307.540781 114.354783 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="115.406609" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="114.354783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_26">
    <path d="M 112.240781 64.130087 
L 307.540781 75.96313 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="64.130087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="75.96313" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_27">
    <path d="M 112.240781 116.458435 
L 307.540781 111.199304 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="116.458435" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="111.199304" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_28">
    <path d="M 112.240781 110.936348 
L 307.540781 103.310609 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="110.936348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="103.310609" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_29">
    <path d="M 112.240781 103.573565 
L 307.540781 114.354783 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="103.573565" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="114.354783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_30">
    <path d="M 112.240781 42.041739 
L 307.540781 54.663652 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="42.041739" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="54.663652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_31">
    <path d="M 112.240781 104.888348 
L 307.540781 107.78087 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="104.888348" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="107.78087" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_32">
    <path d="M 112.240781 115.143652 
L 307.540781 125.661913 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="115.143652" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="125.661913" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_33">
    <path d="M 112.240781 100.15513 
L 307.540781 116.721391 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="100.15513" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="116.721391" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="line2d_34">
    <path d="M 112.240781 100.15513 
L 307.540781 96.210783 
" clip-path="url(#pf1403c5586)" style="fill: none; stroke: #8b5cf6; stroke-opacity: 0.6; stroke-width: 1.5; stroke-linecap: square"/>
    <g clip-path="url(#pf1403c5586)">
     <use xlink:href="#m0653a46230" x="112.240781" y="100.15513" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
     <use xlink:href="#m0653a46230" x="307.540781" y="96.210783" style="fill: #8b5cf6; fill-opacity: 0.6; stroke: #8b5cf6; stroke-opacity: 0.6"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 53.650781 206.784 
L 53.650781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 366.130781 206.784 
L 366.130781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 53.650781 206.784 
L 366.130781 206.784 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 53.650781 7.2 
L 366.130781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pf1403c5586">
   <rect x="53.650781" y="7.2" width="312.48" height="199.584"/>
  </clipPath>
 </defs>
</svg>
<figcaption>Each line is one page. Pages differ from each other by hundreds of milliseconds; the drop within each page is small but goes the same way for almost all. The paired test looks at the latter.</figcaption>
</figure>

## Assumptions

- **Independence:** the measurements in a group must be independent of each
  other (the same user must not be counted twice). In a paired test it is
  **the pairs** that are independent.
- **Normality:** with small samples the means need to be bell-shaped. Thanks
  to the central limit theorem, with large samples (500 per group here)
  skewed data is not a problem. With small, very skewed samples look at
  non-parametric tests or the bootstrap.
- **Equal deviations:** only Student's test needs it; Welch's does not.

## Summary

- Two independent groups → `ttest_ind(..., equal_var=False)` (Welch). The
  default Student's test produces false alarms when deviations and group
  sizes differ.
- Before/after measurements of the same units → `ttest_rel`. It equals the
  one-sample test of the differences, and because it removes the
  differences between units it is much more powerful.
- Put the difference and its confidence interval (`confidence_interval`)
  next to p.
