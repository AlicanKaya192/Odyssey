# ANOVA: Comparing Many Groups

This time not two but four page layouts (A, B, C, D) were tried; 150 users
saw each. The question: does the layout change the time spent on the page?
The first idea is to compare every pair with a t-test: A–B, A–C, A–D, B–C,
B–D, C–D, six tests. This section shows by measurement why that is a bad
idea and introduces the right tool: **analysis of variance (ANOVA)**.

## The data

```python
from ab_data import make_layout_test

test = make_layout_test()
summary = test.groupby("layout")["minutes"].agg(["count", "mean", "std"])
print(summary.round(2).to_string())
```

```text
        count  mean   std
layout                   
A         150  7.73  2.93
B         150  7.84  2.80
C         150  9.17  3.26
D         150  8.60  3.01
```

The four means differ from each other. But each group has 150 people and
the deviations are around 3 minutes: how much of these differences is real,
how much chance?

## The trouble with six t-tests

In a world where all groups are **truly the same**, let us make six
pairwise comparisons and count how often at least one is "significant":

```python
import itertools
import numpy as np
from scipy import stats

rng = np.random.default_rng(171)
hits = 0
for _ in range(4000):
    groups = rng.normal(8, 3, size=(4, 150))
    pairs = itertools.combinations(range(4), 2)
    p = [stats.ttest_ind(groups[i], groups[j]).pvalue for i, j in pairs]
    hits += min(p) < 0.05
print(round(hits / 4000, 3), round(1 - 0.95 ** 6, 3))
```

```text
0.19 0.265
```

- With no difference at all, at least one pair came out "significant" in
  19.0% of the experiments: about four times the promised 5%.
- With six independent tests the rate would be $1 - 0.95^6 \approx$
  0.265. The real rate is a bit lower because the tests share groups
  and are not independent. Still, the chance of a false alarm multiplies.
- The probability of "at least one false alarm" is called the
  **family-wise error rate**. The number of pairs grows fast with the number
  of groups: 45 pairs for 10 groups.

## The idea of ANOVA: two kinds of wobble

ANOVA asks a single question: "Are all the group means the same?" $H_0$:
$\mu_A = \mu_B = \mu_C = \mu_D$. It answers by comparing two kinds of
wobble:

- **Between groups**: how far are the group means from the overall mean?
- **Within groups**: inside each group, how far are users from their own
  group mean?

If the groups really are the same, the group means wobble only by chance and
the two wobbles come out close. If the groups differ, the between-group
wobble grows. Their ratio is called the **F statistic**:

$$F = \dfrac{\text{between-group sum of squares} / (k - 1)}{\text{within-group sum of squares} / (N - k)}$$

$k$ is the number of groups, $N$ the total number of people. The divisors
in the numerator and denominator are degrees of freedom.

```python
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
groups = [g["minutes"].to_numpy() for _, g in test.groupby("layout")]
values = test["minutes"].to_numpy()
grand = values.mean()
between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
within = sum(((g - g.mean()) ** 2).sum() for g in groups)
k, n = len(groups), len(values)
f = (between / (k - 1)) / (within / (n - k))
print(round(between, 1), round(within, 1), round(f, 3))
print(f"{stats.f.sf(f, k - 1, n - k):.1e}")
result = stats.f_oneway(*groups)
print(round(result.statistic, 3), f"{result.pvalue:.1e}")
```

```text
208.2 5378.4 7.692
4.8e-05
7.692 4.8e-05
```

- The between-group sum of squares is 208.2, the within-group one
  5378.4. Turned into mean squares, F = 7.692: the between-group
  wobble is about 7.7 times what chance would explain.
- p comes from the **F distribution** (`stats.f.sf`), with two degrees of
  freedom (3 and 596). `stats.f_oneway` does the same calculation in one
  line.
- p is tiny: the layouts are not all the same. But **which** ones differ?
  ANOVA does not say.

## Effect size: η²

How much of the total wobble comes from the groups? **Eta squared**
($\eta^2$):

$$\eta^2 = \dfrac{\text{between groups}}{\text{between groups} + \text{within groups}}$$

Here $\eta^2$ = 0.037: only about 4% of the differences in time come
from the layout; the rest is the natural difference between users. There may
be an important layout difference, but users' behaviour is mostly decided by
other things.

## Which groups differ? Tukey's test

After ANOVA says "at least one differs", a **post-hoc** test that accounts
for multiple comparisons is used to look at the pairs. The most common is
**Tukey HSD** (honestly significant difference): it judges the six pairs
together and keeps the family-wise error rate at 5%.

```python
import itertools
from scipy import stats
from ab_data import make_layout_test

test = make_layout_test()
names = sorted(test["layout"].unique())
groups = [test.loc[test["layout"] == n, "minutes"] for n in names]
res = stats.tukey_hsd(*groups)
for i, j in itertools.combinations(range(4), 2):
    diff = float(res.statistic[i, j])
    p = float(res.pvalue[i, j])
    print(names[i], names[j], round(diff, 2), round(p, 4))
```

```text
A B -0.1 0.9911
A C -1.44 0.0002
A D -0.87 0.0609
B C -1.34 0.0007
B D -0.77 0.1229
C D 0.57 0.3475
```

- `res.statistic[i, j]` is the mean of the first group minus the second.
- C differs clearly from A and from B (p-values 0.0002 and
  0.0007).
- A–D (p = 0.0609) is borderline, C–D (p = 0.3475) is not.
- The true means were A 8.0, B 8.0, C 8.8, D 8.2. Tukey correctly found that
  C stands out; the real 0.6-minute difference between C and D it could not
  tell apart with 150 people each. "Not significant" still does not mean
  "no difference".

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="386.103906pt" height="208.808pt" viewBox="0 0 386.103906 208.808" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 208.808 
L 386.103906 208.808 
L 386.103906 0 
L 0 0 
L 0 208.808 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 44.103906 184.608 
L 378.903906 184.608 
L 378.903906 7.2 
L 44.103906 7.2 
L 44.103906 184.608 
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
       <use xlink:href="#m15aed4d867" x="91.932478" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="91.932478" y="199.205656" transform="rotate(-0 91.932478 199.205656)">A</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="171.646763" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="171.646763" y="199.205656" transform="rotate(-0 171.646763 199.205656)">B</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="251.361049" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="251.361049" y="199.205656" transform="rotate(-0 251.361049 199.205656)">C</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="331.075335" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="331.075335" y="199.205656" transform="rotate(-0 331.075335 199.205656)">D</text>
     </g>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_5">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="160.722691" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="164.521519" transform="rotate(-0 37.103906 164.521519)">7.5</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="127.67383" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="131.472658" transform="rotate(-0 37.103906 131.472658)">8.0</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="94.62497" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="98.423798" transform="rotate(-0 37.103906 98.423798)">8.5</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="61.576109" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="65.374937" transform="rotate(-0 37.103906 65.374937)">9.0</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="44.103906" y="28.527248" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="37.103906" y="32.326077" transform="rotate(-0 37.103906 32.326077)">9.5</text>
     </g>
    </g>
    <g id="text_10">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="95.904" transform="rotate(-90 14.798438 95.904)">Mean time (minutes)</text>
    </g>
   </g>
   <g id="LineCollection_1">
    <path d="M 91.932478 176.544 
L 91.932478 114.108656 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_10">
    <defs>
     <path id="mef9653b673" d="M 6 0 
L -6 -0 
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="91.932478" y="176.544" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_11">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="91.932478" y="114.108656" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_2">
    <path d="M 171.646763 168.463991 
L 171.646763 108.687104 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_12">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="171.646763" y="168.463991" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_13">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="171.646763" y="108.687104" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_3">
    <path d="M 251.361049 84.762829 
L 251.361049 15.264 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_14">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="251.361049" y="84.762829" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_15">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="251.361049" y="15.264" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="LineCollection_4">
    <path d="M 331.075335 120.096131 
L 331.075335 55.916637 
" clip-path="url(#p8aac6f4af8)" style="fill: none; stroke: #8b5cf6; stroke-width: 2"/>
   </g>
   <g id="line2d_16">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="331.075335" y="120.096131" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_17">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mef9653b673" x="331.075335" y="55.916637" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_18">
    <defs>
     <path id="mee854baf65" d="M 0 3.5 
C 0.928211 3.5 1.81853 3.131218 2.474874 2.474874 
C 3.131218 1.81853 3.5 0.928211 3.5 0 
C 3.5 -0.928211 3.131218 -1.81853 2.474874 -2.474874 
C 1.81853 -3.131218 0.928211 -3.5 0 -3.5 
C -0.928211 -3.5 -1.81853 -3.131218 -2.474874 -2.474874 
C -3.131218 -1.81853 -3.5 -0.928211 -3.5 0 
C -3.5 0.928211 -3.131218 1.81853 -2.474874 2.474874 
C -1.81853 3.131218 -0.928211 3.5 0 3.5 
z
" style="stroke: #8b5cf6"/>
    </defs>
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="91.932478" y="145.326328" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_19">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="171.646763" y="138.575548" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_20">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="251.361049" y="50.013414" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="line2d_21">
    <g clip-path="url(#p8aac6f4af8)">
     <use xlink:href="#mee854baf65" x="331.075335" y="88.006384" style="fill: #8b5cf6; stroke: #8b5cf6"/>
    </g>
   </g>
   <g id="patch_3">
    <path d="M 44.103906 184.608 
L 44.103906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_4">
    <path d="M 378.903906 184.608 
L 378.903906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_5">
    <path d="M 44.103906 184.608 
L 378.903906 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_6">
    <path d="M 44.103906 7.2 
L 378.903906 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p8aac6f4af8">
   <rect x="44.103906" y="7.2" width="334.8" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The mean and 95% confidence interval of the four layouts. C stands out; A and B are almost the same, D is in between.</figcaption>
</figure>

## Assumptions

- **Independence:** each user is in one group.
- **Normality:** the group means should be bell-shaped; with large groups the
  central limit theorem ensures it.
- **Equal variances:** classical ANOVA, like Student's t-test, assumes the
  groups' deviations are equal. If they differ clearly, **Welch's ANOVA** is
  used (`statsmodels.stats.oneway.anova_oneway(..., use_var="unequal")`).

## Summary

- Comparing many groups pair by pair with t-tests multiplies false alarms
  (the family-wise error rate).
- ANOVA asks "are they all the same?" in one test: F = between-group wobble
  / within-group wobble (`stats.f_oneway`).
- A post-hoc test such as Tukey HSD says which groups differ
  (`stats.tukey_hsd`).
- $\eta^2$ measures how much of the difference comes from the groups; put it
  next to p.
