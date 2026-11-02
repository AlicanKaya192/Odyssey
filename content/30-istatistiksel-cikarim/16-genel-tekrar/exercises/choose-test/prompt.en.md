`choose_test(outcome, groups, paired, skewed)` should return the name of
the right test. `outcome` is `"mean"` or `"rate"`. For rates two groups
are `"z-test"`, more are `"chi-square"`. For means: more than two groups
`"anova"` (`"kruskal"` if skewed); two paired groups `"paired-t"`
(`"wilcoxon"` if skewed); two independent groups `"welch"`
(`"mann-whitney"` if skewed). The starter code always says `"welch"`.

**Expected output:**

```text
welch
wilcoxon
chi-square
```
