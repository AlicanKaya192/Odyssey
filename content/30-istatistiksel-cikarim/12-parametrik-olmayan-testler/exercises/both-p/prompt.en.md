`both_p(a, b)` should return two ps for "is b larger than a": Welch's t-test
(`ttest_ind(b, a, equal_var=False)`) and Mann–Whitney (`mannwhitneyu(b, a)`),
4 places. The starter code returns the t p twice. Look at how the huge
value in the example affects the two tests.

**Expected output:**

```text
[0.2506, 0.0002]
```
