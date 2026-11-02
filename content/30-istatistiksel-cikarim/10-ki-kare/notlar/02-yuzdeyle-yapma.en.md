Feeding percentages to a chi-square test is a common mistake that silently
gives a wrong result: the code runs, a p-value comes out, but that p belongs
to the wrong sample size.

## The same rates, different evidence

Let the buying rate be 12% and 20% in two groups. Seeing this with 100
people per group is not the same evidence as seeing it with 1000:

```python
from scipy import stats

small = [[12, 88], [20, 80]]
large = [[120, 880], [200, 800]]
print(round(stats.chi2_contingency(small).pvalue, 4))
print(f"{stats.chi2_contingency(large).pvalue:.1e}")
```

```text
0.177
1.4e-06
```

With 100 per group the difference is not significant; with 1000 it is very
strong. The rates are the same; only the counts differ.

## Why does a table of percentages mislead?

If you write the percentages into the table as `[[12, 88], [20, 80]]`, the
test takes them as **counts of 100 people**. If there really are 1000 people
per group, you find p much larger than it is and miss a real difference. If
there really are 30 per group, the opposite: you find p smaller than it is
and raise a false alarm.

## The right way

- Always build from raw counts: `pd.crosstab(data["group"], data["outcome"])`.
- Compute and report the rates separately; give the test the counts.
- If you only have percentages and group sizes, recover the counts:
  `rate × group size`, to the nearest whole number.
