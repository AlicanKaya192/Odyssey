# Power Analysis

A test's **power** is the probability of catching an effect that really
exists: $1 - \beta$, the probability of "not making a Type II error". When
power is low, a real improvement comes out "not significant" and gets thrown
away. **Power analysis** answers the question "how many people do I need?"
**before** the test starts.

## Four numbers, one unknown

In power analysis four numbers are tied together:

- **Effect size:** the smallest difference you want to catch (d or h).
- **Significance level** $\alpha$: the false alarm rate, usually 0.05.
- **Power** $1 - \beta$: usually 0.8.
- **Sample size** n: people per group.

You give three and the fourth is computed. `statsmodels` does this with
`solve_power`; you leave the unknown out. For means, `TTestIndPower`:

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

for d in [0.8, 0.5, 0.2, 0.1]:
    n = TTestIndPower().solve_power(effect_size=d, power=0.8, alpha=0.05)
    print(d, int(np.ceil(n)))
```

```text
0.8 26
0.5 64
0.2 394
0.1 1571
```

The number of people is rounded up (`ceil`): there is no such thing as 25.5
people. Notice: **when the effect halves, the people needed roughly
quadruple** (394 at 0.2, 1,571 at 0.1). n grows with
$1 / d^2$. Catching small effects is expensive.

## For rates: how many visitors?

In the checkout button test the true rates were 11.4% and 13.0% (we
generated the data, so we know). How many people per group are needed to
catch this difference with 80% power? First `proportion_effectsize` turns
the difference into Cohen's h, then `NormalIndPower` (based on the z-test)
solves it:

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

h = proportion_effectsize(0.130, 0.114)
n = NormalIndPower().solve_power(effect_size=h, power=0.8, alpha=0.05)
print(round(h, 4), int(np.ceil(n)))
```

```text
0.0489 6562
```

6,562 people per group, 13,124 in total. A 1.6-point
difference needs this many people because h is very small.

## Checking by simulation

Let's try what the calculation says ourselves: run 2000 tests of this size
and count in how many the difference comes out significant.

```python
from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(401)
n_group = int(np.ceil(n))
hits = 0
for _ in range(2000):
    buy_a = rng.binomial(n_group, 0.114)
    buy_b = rng.binomial(n_group, 0.130)
    p = proportions_ztest([buy_b, buy_a], [n_group, n_group])[1]
    hits += p < 0.05
print(hits / 2000)
```

```text
0.804
```

About 80% of the tests caught the difference: the calculation
holds. `rng.binomial(n, p)` produces "how many of n people bought" in one
go; there is no need to generate each person separately.

## The power of the test we had

The checkout test we used in earlier sections had 4000 people in each
group. What was its power? This time the unknown is `power`. The same
function also finds the **minimum detectable effect** (MDE): the smallest h
that can be caught with 80% power.

```python
power = NormalIndPower().power(effect_size=h, nobs1=4000, alpha=0.05)
mde = NormalIndPower().solve_power(nobs1=4000, power=0.8, alpha=0.05)
rate_b = np.sin(np.arcsin(np.sqrt(0.114)) + mde / 2) ** 2
print(round(power, 3))
print(round(mde, 4), round(rate_b, 4))
```

```text
0.59
0.0626 0.1347
```

- With 4000 per group the chance of catching the real difference is only
  59%. In that test the difference came out significant, but that
  was partly luck.
- MDE: h = 0.063. Turning h back (solving h's formula for $p_B$),
  the 11.4% base rate is caught with 80% power only if it rises to
  13.5%. The true rate is 13.0%, so smaller than what this test
  can reliably see.

The question to ask when designing a test: "With this traffic, is the
smallest effect I can see smaller than the effect I hope for?" If not, the
test has failed before it starts.

## The power curve

How does power grow as the sample grows? For two different true effects:

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="386.791193pt" height="226.607609pt" viewBox="0 0 386.791193 226.607609" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 226.607609 
L 386.791193 226.607609 
L 386.791193 0 
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
       <use xlink:href="#m15aed4d867" x="57.278598" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="57.278598" y="203.004484" transform="rotate(-0 57.278598 203.004484)">0</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="108.346322" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="108.346322" y="203.004484" transform="rotate(-0 108.346322 203.004484)">5000</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="159.414046" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="159.414046" y="203.004484" transform="rotate(-0 159.414046 203.004484)">10000</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="210.481771" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="210.481771" y="203.004484" transform="rotate(-0 210.481771 203.004484)">15000</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="261.549495" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="261.549495" y="203.004484" transform="rotate(-0 261.549495 203.004484)">20000</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="312.617219" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="312.617219" y="203.004484" transform="rotate(-0 312.617219 203.004484)">25000</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="363.684943" y="188.406828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="363.684943" y="203.004484" transform="rotate(-0 363.684943 203.004484)">30000</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="211.503125" y="217.005266" transform="rotate(-0 211.503125 217.005266)">People per group</text>
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
    <path d="M 59.321307 174.599716 
L 65.449434 159.176147 
L 75.662979 133.154185 
L 81.791105 118.261009 
L 85.876523 108.855287 
L 89.961941 99.943332 
L 94.047359 91.564889 
L 98.132777 83.741936 
L 102.218195 76.482087 
L 106.303613 69.781563 
L 110.389031 63.627743 
L 114.474449 58.001338 
L 118.559867 52.878217 
L 122.645285 48.230921 
L 126.730703 44.029909 
L 130.816121 40.244559 
L 134.901539 36.84397 
L 138.986957 33.797586 
L 143.072375 31.075666 
L 147.157792 28.64964 
L 151.24321 26.492356 
L 155.328628 24.578242 
L 159.414046 22.883402 
L 163.499464 21.385662 
L 167.584882 20.064565 
L 173.713009 18.373522 
L 179.841136 16.981544 
L 185.969263 15.839759 
L 192.09739 14.906271 
L 200.268226 13.924834 
L 208.439062 13.181394 
L 218.652606 12.504081 
L 230.90886 11.955915 
L 245.207823 11.55817 
L 263.592204 11.275672 
L 292.190129 11.089229 
L 347.343271 11.008542 
L 363.684943 11.003767 
L 363.684943 11.003767 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_15">
    <path d="M 59.321307 178.281137 
L 71.577561 170.559626 
L 85.876523 161.267359 
L 130.816121 131.851956 
L 145.115084 122.855804 
L 157.371337 115.397268 
L 169.627591 108.208913 
L 181.883845 101.316827 
L 192.09739 95.81332 
L 202.310935 90.535797 
L 212.524479 85.488772 
L 222.738024 80.674385 
L 232.951569 76.092727 
L 243.165114 71.742137 
L 253.378659 67.619477 
L 263.592204 63.720369 
L 273.805749 60.039415 
L 284.019293 56.570392 
L 294.232838 53.306423 
L 304.446383 50.240128 
L 316.702637 46.810576 
L 328.958891 43.640657 
L 341.215145 40.716245 
L 353.471398 38.023145 
L 363.684943 35.945415 
L 363.684943 35.945415 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
   </g>
   <g id="line2d_16">
    <path d="M 44.103125 46.480428 
L 378.903125 46.480428 
" clip-path="url(#p80e0e5b987)" style="fill: none; stroke-dasharray: 3.7,1.6; stroke-dashoffset: 0; stroke: currentColor"/>
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
    <g id="line2d_17">
     <path d="M 263.632812 158.503703 
L 273.632812 158.503703 
L 283.632812 158.503703 
" style="fill: none; stroke: #8b5cf6; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="291.632812" y="162.003703" transform="rotate(-0 291.632812 162.003703)">11.4% → 13.0%</text>
    </g>
    <g id="line2d_18">
     <path d="M 263.632812 173.504484 
L 273.632812 173.504484 
L 283.632812 173.504484 
" style="fill: none; stroke: #f97316; stroke-width: 2; stroke-linecap: square"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="291.632812" y="177.004484" transform="rotate(-0 291.632812 177.004484)">11.4% → 12.2%</text>
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
<figcaption>The dashed line is 80% power. The orange curve is a difference half as large; it reaches the same power much further right.</figcaption>
</figure>

When the effect halves, reaching the same power needs about four times the
people; the curve shifts to the right.

## The winner's curse: low power exaggerates the effect

In a low-power test the results that come out "significant" are
systematically **larger than the true effect**. The reason: with a small
sample the true effect stays under the noise; only results that luck has
also inflated clear the bar. This is called the **winner's curse** or a
**Type M error** (magnitude error). Let's see it by simulation; the true
difference is 0.016:

```python
def curse(n_group, reps=2000):
    lifts, hits = [], 0
    for _ in range(reps):
        buy_a = rng.binomial(n_group, 0.114)
        buy_b = rng.binomial(n_group, 0.130)
        p = proportions_ztest([buy_b, buy_a], [n_group, n_group])[1]
        if p < 0.05 and buy_b > buy_a:
            hits += 1
            lifts.append((buy_b - buy_a) / n_group)
    return round(hits / reps, 2), round(float(np.mean(lifts)) / 0.016, 2)


for n_group in [1000, 4000, 6562]:
    print(n_group, *curse(n_group))
```

```text
1000 0.2 2.27
4000 0.59 1.3
6562 0.79 1.12
```

The second column is the power, the third the ratio of the average
difference in significant tests to the true difference.

- With 1000 per group the power is only 20%; the tests that come
  out significant show the difference 2.3 times larger on
  average.
- As power grows the exaggeration shrinks; at 80% power the ratio is close
  to 1.
- In the 4000-per-group checkout test, too, the difference we found (2.2
  points) was larger than the true difference (1.6 points). That is exactly
  the winner's curse.

This is why news of "a big effect in a small test" is met with suspicion. A
result not repeated with enough power is very likely exaggerated.

## Summary

- Power is the probability of catching a real effect; 0.8 is the usual
  target.
- Given three of effect, $\alpha$, power and n, the fourth is found with
  `solve_power`; n grows inversely with the square of the effect.
- For rates, first h with `proportion_effectsize`, then `NormalIndPower`.
- The calculation can be checked by simulation.
- With the available traffic the minimum detectable effect (MDE) is
  computed; if it is larger than the hoped-for effect, the test has failed
  before it starts.
- Results that come out significant at low power exaggerate the effect.
