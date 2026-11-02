# A/A Tests and Sample Ratio Mismatch

Before trusting an experiment system's result, you need to trust the
system itself: is the assignment really random, are the logs complete,
does the test keep its promise? This section shows two tools for checking
that: the **A/A test** and the **sample ratio mismatch** (SRM) check.

## The A/A test: when both groups see the same thing

In an A/A test both groups are shown the **same** version. The true
difference is zero; so the test should give false alarms only at the rate
α, and the p-values should be spread evenly, as we saw in The p-Value and
Its Misreadings section. Let's run 1000 A/A tests on the shop's log
(revenue, Welch's t-test):

```python
import numpy as np
from scipy import stats
from ab_data import make_user_log

users = make_user_log()
rng = np.random.default_rng(91)
revenue = users["revenue"]
p_values = []
for _ in range(1000):
    in_b = rng.random(len(users)) < 0.5
    test = stats.ttest_ind(revenue[in_b], revenue[~in_b], equal_var=False)
    p_values.append(test.pvalue)
p_values = np.array(p_values)
print(round(float((p_values < 0.05).mean()), 3))
print(np.histogram(p_values, bins=10, range=(0, 1))[0])
```

```text
0.051
[ 96  76  93  78 114 116  93 114 118 102]
```

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="382.925781pt" height="200.632781pt" viewBox="0 0 382.925781 200.632781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 200.632781 
L 382.925781 200.632781 
L 382.925781 -0 
L 0 -0 
L 0 200.632781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 40.925781 162.432 
L 375.725781 162.432 
L 375.725781 7.2 
L 40.925781 7.2 
L 40.925781 162.432 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 56.143963 162.432 
L 71.362145 162.432 
L 71.362145 49.897075 
L 56.143963 49.897075 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_4">
    <path d="M 71.362145 162.432 
L 86.580327 162.432 
L 86.580327 63.136478 
L 71.362145 63.136478 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_5">
    <path d="M 86.580327 162.432 
L 101.798509 162.432 
L 101.798509 89.615284 
L 86.580327 89.615284 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_6">
    <path d="M 101.798509 162.432 
L 117.01669 162.432 
L 117.01669 67.549612 
L 101.798509 67.549612 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_7">
    <path d="M 117.01669 162.432 
L 132.234872 162.432 
L 132.234872 74.169313 
L 117.01669 74.169313 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_8">
    <path d="M 132.234872 162.432 
L 147.453054 162.432 
L 147.453054 45.48394 
L 132.234872 45.48394 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_9">
    <path d="M 147.453054 162.432 
L 162.671236 162.432 
L 162.671236 94.028418 
L 147.453054 94.028418 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_10">
    <path d="M 162.671236 162.432 
L 177.889418 162.432 
L 177.889418 58.723343 
L 162.671236 58.723343 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_11">
    <path d="M 177.889418 162.432 
L 193.107599 162.432 
L 193.107599 38.864239 
L 177.889418 38.864239 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_12">
    <path d="M 193.107599 162.432 
L 208.325781 162.432 
L 208.325781 34.451104 
L 193.107599 34.451104 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_13">
    <path d="M 208.325781 162.432 
L 223.543963 162.432 
L 223.543963 49.897075 
L 208.325781 49.897075 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_14">
    <path d="M 223.543963 162.432 
L 238.762145 162.432 
L 238.762145 19.005134 
L 223.543963 19.005134 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_15">
    <path d="M 238.762145 162.432 
L 253.980327 162.432 
L 253.980327 76.375881 
L 238.762145 76.375881 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_16">
    <path d="M 253.980327 162.432 
L 269.198509 162.432 
L 269.198509 43.277373 
L 253.980327 43.277373 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_17">
    <path d="M 269.198509 162.432 
L 284.41669 162.432 
L 284.41669 43.277373 
L 269.198509 43.277373 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_18">
    <path d="M 284.41669 162.432 
L 299.634872 162.432 
L 299.634872 30.03797 
L 284.41669 30.03797 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_19">
    <path d="M 299.634872 162.432 
L 314.853054 162.432 
L 314.853054 14.592 
L 299.634872 14.592 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_20">
    <path d="M 314.853054 162.432 
L 330.071236 162.432 
L 330.071236 49.897075 
L 314.853054 49.897075 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_21">
    <path d="M 330.071236 162.432 
L 345.289418 162.432 
L 345.289418 45.48394 
L 330.071236 45.48394 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
   </g>
   <g id="patch_22">
    <path d="M 345.289418 162.432 
L 360.507599 162.432 
L 360.507599 54.310209 
L 345.289418 54.310209 
z
" clip-path="url(#pe124e62095)" style="fill: #8b5cf6; opacity: 0.8"/>
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
       <use xlink:href="#m15aed4d867" x="56.143963" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="56.143963" y="177.029656" transform="rotate(-0 56.143963 177.029656)">0.0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="117.01669" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="117.01669" y="177.029656" transform="rotate(-0 117.01669 177.029656)">0.2</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="177.889418" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="177.889418" y="177.029656" transform="rotate(-0 177.889418 177.029656)">0.4</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="238.762145" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="238.762145" y="177.029656" transform="rotate(-0 238.762145 177.029656)">0.6</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="299.634872" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="299.634872" y="177.029656" transform="rotate(-0 299.634872 177.029656)">0.8</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="360.507599" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="360.507599" y="177.029656" transform="rotate(-0 360.507599 177.029656)">1.0</text>
     </g>
    </g>
    <g id="text_7">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="208.325781" y="191.030437" transform="rotate(-0 208.325781 191.030437)">p-value</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_7">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="162.432" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="166.230828" transform="rotate(-0 33.925781 166.230828)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="118.300657" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="122.099485" transform="rotate(-0 33.925781 122.099485)">20</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="74.169313" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="77.968142" transform="rotate(-0 33.925781 77.968142)">40</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="30.03797" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="33.836798" transform="rotate(-0 33.925781 33.836798)">60</text>
     </g>
    </g>
    <g id="text_12">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="84.816" transform="rotate(-90 14.798438 84.816)">Number of tests</text>
    </g>
   </g>
   <g id="line2d_11">
    <path d="M 40.925781 52.103642 
L 375.725781 52.103642 
" clip-path="url(#pe124e62095)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: #f97316; stroke-width: 1.5"/>
   </g>
   <g id="patch_23">
    <path d="M 40.925781 162.432 
L 40.925781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_24">
    <path d="M 375.725781 162.432 
L 375.725781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_25">
    <path d="M 40.925781 162.432 
L 375.725781 162.432 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_26">
    <path d="M 40.925781 7.2 
L 375.725781 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pe124e62095">
   <rect x="40.925781" y="7.2" width="334.8" height="155.232"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The p-values of 1000 A/A tests. The dashed line is the 50 tests expected in each slice: the distribution is flat.</figcaption>
</figure>

- 5.1% of the tests came out "significant": close to the
  promised 5%. Revenue is very skewed, but with 10,000 per group the
  central limit theorem works.
- The p-values are spread roughly evenly over the ten slices.

In a real system an A/A test is run with the same code, the same
assignment and the same logging path. If the false alarm rate comes out
clearly above 5% (or the p-values pile up at one end), something is wrong
in the system: counting page views instead of users as observations, the
two groups going through different logging code, or a wrong test.

A single A/A test coming out "significant" is not a problem; one in twenty
does. The problem is when it happens more often than 5%. That is why A/A
tests are judged over many repeats, not one at a time.

## SRM: when the group sizes do not match the design

In a 50/50 test the groups never come out exactly equal, but how big a
difference counts as chance? This is the **goodness of fit** question from
the Chi-Square Tests section. In the experiment below B has no effect at
all; but B's logging code has a bug and some mobile users who did not buy
never reach the log:

```python
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_assignment_log

log = make_assignment_log(lost_b=0.08)
counts = log["group"].value_counts().sort_index()
print(counts.to_dict())
print(f"{stats.chisquare(counts).pvalue:.1e}")
k = log.groupby("group")["bought"].sum()
print(log.groupby("group")["bought"].mean().round(4).to_dict())
p = proportions_ztest([k["B"], k["A"]], [counts["B"], counts["A"]])[1]
print(round(p, 4))
```

```text
{'A': 24976, 'B': 23973}
5.8e-06
{'A': 0.1104, 'B': 0.1181}
0.0074
```

- B has 1,003 fewer people than A. The chi-square test's p is
  5.8e-06: a difference this large hardly ever comes from chance in
  a 50/50 assignment.
- The buying rate looks higher in B and the z-test finds it "significant"
  (p = 0.0074). But B does nothing: because the lost users were
  the **ones who did not buy**, B's rate got inflated.

SRM is an alarm not about the result **itself** but about how far the
result can be trusted. With SRM, not only the size but also the
**contents** of the groups may be damaged, and no test can fix that. The
rule: if SRM is seen, the result is not read; first the cause is found.

## Finding where the loss is

The cause of SRM is often in one segment. Let's look segment by segment:

```python
for platform, part in log.groupby("platform"):
    c = part["group"].value_counts().sort_index()
    print(platform, c.to_dict(), f"{stats.chisquare(c).pvalue:.1e}")
```

```text
desktop {'A': 10055, 'B': 10180} 3.8e-01
mobile {'A': 14921, 'B': 13793} 2.8e-11
```

On desktop the groups are balanced; the problem is on mobile. In real life
this points to the next step: does the logging code work on B's mobile
page? Common causes:

- Version B loads slowly or crashes on some devices, so no log is sent.
- The bot filter works differently in the two groups.
- Users are redirected from B to A (or the other way).
- One group of the experiment is restarted in the middle of the test.

## Small losses are invisible

If the loss is small, the SRM test may not catch it, but the result is
still damaged:

```python
small = make_assignment_log(lost_b=0.02)
c = small["group"].value_counts().sort_index()
print(c.to_dict(), round(stats.chisquare(c).pvalue, 3))
print(small.groupby("group")["bought"].mean().round(4).to_dict())
```

```text
{'A': 24976, 'B': 24781} 0.382
{'A': 0.1104, 'B': 0.1142}
```

The SRM p is 0.382: no alarm. Still, B's buying rate rose only
because of the loss. The SRM check is necessary but not sufficient; the
logging path being the same in both groups is ensured by design.

## The SRM threshold

The SRM check runs on every experiment, automatically and continuously. So
its threshold is usually kept much stricter than α = 0.05 (e.g. 0.001):
alarming at 5% across hundreds of experiments would flood the system with
needless alarms. A real loss usually makes p much smaller.

## Summary

- An A/A test measures the system's false alarm rate when there is no real
  difference; over many repeats it should be about 5%.
- SRM is when group sizes do not match the designed split; it is tested
  with a chi-square goodness of fit test.
- With SRM the result is not read: the loss is usually not random and
  creates a fake effect.
- The cause is searched segment by segment (platform, browser, country,
  day).
- Small losses may not trip the SRM test; equal logging paths are ensured
  by design.
