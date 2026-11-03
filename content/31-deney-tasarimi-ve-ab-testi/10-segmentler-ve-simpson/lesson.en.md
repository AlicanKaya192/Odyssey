# Segments and Simpson's Paradox

When a test ends, the first question is usually "who did it work for?":
mobile or desktop, which country? Looking at segments is valuable but it
has two traps. First, if the make-up of the groups changes from segment to
segment, the total result can say the **opposite** of what the segments
say: **Simpson's paradox**. Second, whoever looks at enough segments finds
a striking one by chance.

## Losing in total, winning in every week

In a test that ran for two weeks, B's share of the traffic was 10% in the
first week and 50% in the second (a slow opening, a ramp-up). The first
week had a sale and everyone bought more. We made the data: in both weeks
B truly raises buying by 5%.

```python
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_ramp_test, make_segment_test

ramp = make_ramp_test()
print(ramp.groupby("group")["bought"].agg(["mean", "size"]).round(4))
k = ramp.groupby("group")["bought"].sum()
n = ramp.groupby("group").size()
p = proportions_ztest([k["B"], k["A"]], [n["B"], n["A"]])[1]
print(f"{p:.1e}")
```

```text
         mean   size
group               
A      0.0952  28059
B      0.0642  11941
5.0e-24
```

In total, B's buying rate is 6.4% and A's 9.5%; the
p-value is tiny. The report looks set to say "B clearly lowers buying".
Let us split by week:

```python
by_week = ramp.groupby(["week", "group"])["bought"].mean().unstack()
print(by_week.round(4))
print(ramp.groupby(["week", "group"]).size().unstack())
```

```text
group       A       B
week                 
1      0.1198  0.1215
2      0.0514  0.0525
group      A     B
week              
1      17976  2024
2      10083  9917
```

In both weeks B is slightly **ahead** of A. The reversed total comes from
the weights: most of B's users come from the second week, when buying was
low, and most of A's users from the first week with the sale. The total
rate is an average of "mostly the second week" for B and "mostly the first
week" for A; the two groups are not compared with the same mix.

That is why in an experiment whose assignment ratio was changed mid-test
the totals are not compared. Had the SRM check from the A/A Tests and
Sample Ratio Mismatch section been run for each week separately, the
difference would have shown at once.

## The right comparison: within strata

The fix is to compare each week within itself and combine the differences
**with the same weights** (a stratified estimate). The weight is each
week's share of all users; it is the same for both groups:

```python
weights = ramp.groupby("week").size() / len(ramp)
print(round(((by_week["B"] - by_week["A"]) * weights).sum(), 4))
```

```text
0.0015
```

The stratified difference is positive: the sign flipped. Let us not tie
this to one data set; let us build the same design with 100 different
seeds:

```python
pooled_worse, strat = 0, []
for s in range(100):
    t = make_ramp_test(seed=1000 + s)
    w = t.groupby(["week", "group"])["bought"].mean().unstack()
    m = t.groupby("group")["bought"].mean()
    pooled_worse += m["B"] < m["A"]
    share = t.groupby("week").size() / len(t)
    strat.append(((w["B"] - w["A"]) * share).sum())
print(pooled_worse, round(float(np.mean(strat)), 4))
```

```text
100 0.0043
```

The total rate shows B behind in 100 of the 100 tests. The
average of the stratified estimate (0.0043) is close to the
true difference (0.0042). There is also a simpler way: analyse
only the period with a fixed assignment ratio (the second week).

## Segment hunting

The second trap is drilling down. Let us split a test with 40,000 people
into 8 countries × 2 platforms = 16 segments. In this data B raises buying
by the same 8% in **every segment**:

```python
seg = make_segment_test()
cells = seg.groupby(["country", "platform", "group"])["bought"].mean().unstack()
lift = (cells["B"] / cells["A"] - 1).sort_values()
print(lift.round(3).iloc[[0, 1, -2, -1]].to_string())
overall = seg.groupby("group")["bought"].mean()
print(round(overall["B"] / overall["A"] - 1, 3))
```

```text
country  platform
TR       desktop    -0.179
BR       desktop    -0.163
TR       mobile      0.415
US       mobile      0.535
0.115
```

Although the effect is the same everywhere, the segment estimates spread
between -17.9% and 53.5%. A segment is about 2,500
people; in groups this small a rate difference is very noisy. Writing in
the report "B lowers sales on desktop in this country and doubles them on
mobile in that one" turns noise into a story.

How misleading is the most striking segment? Let us build the same test
100 times and take the **largest** segment lift each time:

```python
best = []
for s in range(100):
    t = make_segment_test(seed=2000 + s)
    c = t.groupby(["country", "platform", "group"])["bought"].mean().unstack()
    best.append((c["B"] / c["A"] - 1).max())
print(round(float(np.mean(best)), 3))
```

```text
0.515
```

While the true effect is 8%, the "best segment" shows 51.5%
on average. The winner's curse from the Power Analysis section works here
too: picking the largest of 16 estimates picks the one chance helped most.

## How to read segments

- The decision follows the **total** result (if the make-up is the same);
  segments are for explaining.
- Segment analysis is written in advance and kept to a few segments; the
  corrections from the Multiple Comparisons section apply.
- If a segment really looks different, that is the **question** of a new
  test.
- If the assignment ratio changed between segments or over time, the
  within-stratum differences are compared, not the totals.

## Summary

- Simpson's paradox: if the groups' make-up differs, the total result can
  be the opposite of the one in every stratum.
- If the assignment ratio changes mid-test, use a stratified estimate or
  only the period with a fixed ratio.
- Small segments' estimates are very noisy; the most striking segment
  greatly exaggerates the effect.
- Segments explain, they do not decide.
