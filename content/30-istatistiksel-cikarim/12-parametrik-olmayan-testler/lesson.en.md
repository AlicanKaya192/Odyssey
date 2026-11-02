# Non-Parametric Tests

The t-test and ANOVA look at means and assume that means are distributed in a
bell shape. With large samples the central limit theorem ensures that. But
if the sample is small, the data very skewed or there are a few huge
outliers, the mean becomes fragile and the test stumbles with it. For these
situations there are tests that look at the **ranks** of the values instead
of the values themselves. Because they assume no distribution shape
(parameter), they are called **non-parametric** tests.

## What is a rank?

The values are put in order from smallest to largest and each takes its
place in that order:

```python
from scipy import stats

print(stats.rankdata([42, 900, 55, 61]))
```

```text
[1. 4. 2. 3.]
```

Whether 900 is 70 or 90,000, its rank is still 4. However extreme an outlier
is, in ranks it is only "the largest". The robustness of non-parametric
tests comes from here.

## How a single outlier breaks the t-test

In two small groups B is clearly larger. Then let us add a single huge order
(900) to B:

```python
from scipy import stats

a = [42, 55, 61, 48, 70, 52, 66, 58]
b = [68, 75, 81, 72, 90, 77, 85, 79]
print(f"{stats.ttest_ind(b, a, equal_var=False).pvalue:.1e}",
      f"{stats.mannwhitneyu(b, a).pvalue:.1e}")
b_big = b + [900]
print(round(stats.ttest_ind(b_big, a, equal_var=False).pvalue, 3),
      f"{stats.mannwhitneyu(b_big, a).pvalue:.1e}")
```

```text
1.4e-04 3.1e-04
0.251 1.6e-04
```

- On the first line both tests see the difference very clearly.
- The huge order **raised** B's mean, so the difference grew. Yet the
  t-test's p became 0.251: "not significant". The outlier inflated
  B's deviation so much that the difference got lost in the noise.
- The **Mann–Whitney U test** (`mannwhitneyu`) looks at ranks, so it was not
  affected: p is still very small.

## The Mann–Whitney U test

It compares two independent groups. Its question is not about means: "How
inclined is a random B value to be larger than a random A value?" Under
$H_0$ this probability is 0.5. Real, very skewed data: basket values.

```python
import numpy as np
from scipy import stats
from ab_data import make_basket_test

test = make_basket_test(n=60)
a = test.loc[test["group"] == "A", "basket"].to_numpy()
b = test.loc[test["group"] == "B", "basket"].to_numpy()
print(round(a.mean(), 1), round(b.mean(), 1))
print(round(np.median(a), 1), round(np.median(b), 1))
u = stats.mannwhitneyu(b, a)
p_t = stats.ttest_ind(b, a, equal_var=False).pvalue
print(round(p_t, 3), round(u.pvalue, 3))
print(round(u.statistic / (len(a) * len(b)), 3))
```

```text
118.7 132.4
99.0 122.0
0.428 0.213
0.566
```

- The means are 118.7 and 132.4, the medians 99.0
  and 122.0.
- In this single dataset neither test is significant (60 orders per group
  is few).
- The last line is $U / (n_A n_B)$: an estimate of the probability that a
  random B order is larger than a random A order, 0.566. This is
  called the **common language effect size**; we will see it again in the
  next section.

From one dataset we cannot tell which test is better. Let us ask a
simulation where the truth is known: what do the two tests do when B really
is 30% larger (power) and when there is no difference (false alarm)?

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(201)
for n in [25, 60, 150]:
    a = rng.lognormal(4.6, 0.9, size=(3000, n))
    b = rng.lognormal(4.6 + np.log(1.3), 0.9, size=(3000, n))
    same = rng.lognormal(4.6, 0.9, size=(3000, n))
    t = stats.ttest_ind(b, a, axis=1, equal_var=False).pvalue < 0.05
    u = stats.mannwhitneyu(b, a, axis=1).pvalue < 0.05
    t0 = stats.ttest_ind(same, a, axis=1, equal_var=False).pvalue < 0.05
    u0 = stats.mannwhitneyu(same, a, axis=1).pvalue < 0.05
    shares = [round(x.mean(), 3) for x in (t, u, t0, u0)]
    print(n, *shares)
```

```text
25 0.134 0.168 0.041 0.052
60 0.271 0.34 0.044 0.049
150 0.559 0.697 0.05 0.053
```

Columns: the group size, the t-test's power, Mann–Whitney's power, the
t-test's false alarm rate, Mann–Whitney's false alarm rate.

- With no difference both tests stay around 5%.
- On this skewed data Mann–Whitney is more powerful at every size: with 150
  orders per group 69.7%, the t-test 55.9%.
- Both tests have low power with 60 orders per group. That is why the single
  dataset above coming out "not significant" was no surprise.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="386.103125pt" height="226.607609pt" viewBox="0 0 386.103125 226.607609" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 226.607609 
L 386.103125 226.607609 
L 386.103125 0 
L 0 0 
L 0 226.607609 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 44.103125 188.406828 
L 378.903125 188.406828 
L 378.903125 10.998828 
L 44.103125 10.998828 
L 44.103125 188.406828 
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
       <use xlink:href="#m15aed4d867" x="47.146761" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="47.146761" y="203.004484" transform="rotate(-0 47.146761 203.004484)">20</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="95.844943" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="95.844943" y="203.004484" transform="rotate(-0 95.844943 203.004484)">40</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="144.543125" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="144.543125" y="203.004484" transform="rotate(-0 144.543125 203.004484)">60</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="193.241307" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="193.241307" y="203.004484" transform="rotate(-0 193.241307 203.004484)">80</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="241.939489" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="241.939489" y="203.004484" transform="rotate(-0 241.939489 203.004484)">100</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="290.63767" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="290.63767" y="203.004484" transform="rotate(-0 290.63767 203.004484)">120</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="339.335852" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="339.335852" y="203.004484" transform="rotate(-0 339.335852 203.004484)">140</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="211.503125" y="217.005266" transform="rotate(-0 211.503125 217.005266)">Orders per group</text>
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
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="192.205656" transform="rotate(-0 37.103125 192.205656)">0.0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="152.925228" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="156.724056" transform="rotate(-0 37.103125 156.724056)">0.2</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="117.443628" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="121.242456" transform="rotate(-0 37.103125 121.242456)">0.4</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="81.962028" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="85.760856" transform="rotate(-0 37.103125 85.760856)">0.6</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="46.480428" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="50.279256" transform="rotate(-0 37.103125 50.279256)">0.8</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103125" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103125" y="14.797656" transform="rotate(-0 37.103125 14.797656)">1.0</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.797656" y="99.702828" transform="rotate(-90 14.797656 99.702828)">Power</text>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 59.321307 164.57502 
L 144.543125 140.388396 
L 363.684943 89.294892 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
    <defs>
     <path id="mf12848e078" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#p80e0e5b987)">
     <use xlink:href="#mf12848e078" x="59.321307" y="164.57502" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#mf12848e078" x="144.543125" y="140.388396" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     <use xlink:href="#mf12848e078" x="363.684943" y="89.294892" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_15">
    <path d="M 59.321307 158.602284 
L 144.543125 128.028972 
L 363.684943 64.694316 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    <defs>
     <path id="maa4a6bf018" d="M 0 3 
C 0.795609 3 1.55874 2.683901 2.12132 2.12132 
C 2.683901 1.55874 3 0.795609 3 0 
C 3 -0.795609 2.683901 -1.55874 2.12132 -2.12132 
C 1.55874 -2.683901 0.795609 -3 0 -3 
C -0.795609 -3 -1.55874 -2.683901 -2.12132 -2.12132 
C -2.683901 -1.55874 -3 -0.795609 -3 0 
C -3 0.795609 -2.683901 1.55874 -2.12132 2.12132 
C -1.55874 2.683901 -0.795609 3 0 3 
z
" style="stroke: #f97316"/>
    </defs>
    <g clip-path="url(#p80e0e5b987)">
     <use xlink:href="#maa4a6bf018" x="59.321307" y="158.602284" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#maa4a6bf018" x="144.543125" y="128.028972" style="fill: #f97316; stroke: #f97316"/>
     <use xlink:href="#maa4a6bf018" x="363.684943" y="64.694316" style="fill: #f97316; stroke: #f97316"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 44.103125 188.406828 
L 44.103125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 378.903125 188.406828 
L 378.903125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 44.103125 188.406828 
L 378.903125 188.406828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 44.103125 10.998828 
L 378.903125 10.998828 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="line2d_16">
     <path d="M 269.935937 24.097266 
L 279.935937 24.097266 
L 289.935937 24.097266 
" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
     <g>
      <use xlink:href="#mf12848e078" x="279.935937" y="24.097266" style="fill: #8b5cf6; stroke: #8b5cf6"/>
     </g>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="297.935937" y="27.597266" transform="rotate(-0 297.935937 27.597266)">t</text>
    </g>
    <g id="line2d_17">
     <path d="M 269.935937 39.098047 
L 279.935937 39.098047 
L 289.935937 39.098047 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
     <g>
      <use xlink:href="#maa4a6bf018" x="279.935937" y="39.098047" style="fill: #f97316; stroke: #f97316"/>
     </g>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="297.935937" y="42.598047" transform="rotate(-0 297.935937 42.598047)">Mann-Whitney</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p80e0e5b987">
   <rect x="44.103125" y="10.998828" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The rate of catching a real 30% difference on skewed basket data. The rank-based test leads at every size.</figcaption>
</figure>

## Paired data: the Wilcoxon signed-rank test

The rank-based counterpart of the paired t-test is the **Wilcoxon
signed-rank test**: it takes the differences, ranks their absolute values
and looks at the signs of the ranks.

```python
from scipy import stats
from ab_data import make_paired_speed

pages = make_paired_speed()
print(round(stats.ttest_rel(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.wilcoxon(pages["before"], pages["after"]).pvalue, 4))
```

```text
0.0211
0.0346
```

In this data the differences are bell-shaped, so the two tests give similar
results; the paired t-test is a little more powerful. If the differences
contain outliers, the picture turns around.

## Many groups: Kruskal–Wallis

The rank-based counterpart of ANOVA is the **Kruskal–Wallis test**:

```python
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
groups = [g["minutes"] for _, g in test.groupby("layout")]
print(f"{stats.kruskal(*groups).pvalue:.1e}")
print(f"{stats.f_oneway(*groups).pvalue:.1e}")
```

```text
5.9e-05
4.8e-05
```

On this bell-shaped data the two tests give almost the same p.

## Which one when?

| Situation | Parametric | Non-parametric |
|---|---|---|
| Two independent groups | Welch's t-test | Mann–Whitney U |
| Paired measurements | paired t-test | Wilcoxon signed-rank |
| Many groups | ANOVA | Kruskal–Wallis |

- If the data is bell-shaped, parametric tests are a little more powerful and
  talk about the mean.
- If the data is very skewed, the sample small or there are outliers,
  rank-based tests are more reliable and often more powerful.
- Careful: Mann–Whitney does not test means but the question "which one tends
  to be larger". If the question really is about the **mean** (like total
  revenue), with large samples the t-test or the bootstrap (second module)
  is the right tool.

## Summary

- Non-parametric tests look at the ranks of the values; they are robust to
  outliers.
- A single huge value can move the t-test's p from significant to not
  significant; Mann–Whitney is not affected.
- On skewed data Mann–Whitney is more powerful; both tests keep the false
  alarm rate at 5%.
- The counterparts: Mann–Whitney U, Wilcoxon signed-rank, Kruskal–Wallis.
