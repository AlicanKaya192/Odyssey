Why are many trees better than one? Imagine `n` models, each 60% accurate, with
errors **completely independent** of each other. The majority vote is right if
more than half of the models are right; this is a binomial probability:

```python
from math import comb

for n in (1, 5, 25, 101):
    wins = range(n // 2 + 1, n + 1)
    acc = sum(comb(n, k) * 0.6 ** k * 0.4 ** (n - k) for k in wins)
    print(n, round(acc, 3))
```

```text
1 0.6
5 0.683
25 0.846
101 0.979
```

The vote of 101 models that are 60% accurate on their own is 97.9% accurate.
This is the best-case calculation: real trees' errors are not independent;
because they learn from the same data, most of them err on the same samples. In
the lesson, bagging with 100 trees took a single tree only from 0.738 to 0.80.

The whole craft of ensemble methods is making the errors **as independent as
possible**: different bootstrap samples (bagging), different feature subsets
(random forest), or, as in the next section, focusing each new model on the
errors of the previous ones (boosting).
