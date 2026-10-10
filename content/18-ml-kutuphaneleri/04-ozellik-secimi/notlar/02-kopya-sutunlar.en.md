A situation common in real data: two columns carry almost the same
information (net and gross square metres, Celsius and Fahrenheit, a total and
an average). The three selection methods do **three different** things here.

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(9)
signal = rng.normal(size=400)
other = rng.normal(size=400)
X = np.column_stack([signal, signal + rng.normal(0, 0.05, 400), other,
                     rng.normal(size=(400, 3))])
y = (signal + 0.5 * other + rng.normal(0, 0.5, 400) > 0).astype(int)
print(round(float(np.corrcoef(X[:, 0], X[:, 1])[0, 1]), 3))
print(SelectKBest(f_classif, k=2).fit(X, y).get_support(indices=True).tolist())
l1 = LogisticRegression(penalty="l1", C=0.05, solver="liblinear").fit(X, y)
print(l1.coef_.round(2).tolist()[0])
forest = RandomForestClassifier(n_estimators=200, random_state=9).fit(X, y)
print(forest.feature_importances_.round(2).tolist())
```

```text
0.999
[0, 1]
[0.0, 1.73, 0.63, 0.0, 0.0, 0.0]
[0.31, 0.32, 0.16, 0.08, 0.06, 0.07]
```

## Three methods, three behaviours

- Columns 0 and 1 copy each other (correlation 0.999). Column 2 is related to
  the target too, but weaker; 3–5 are noise.
- The **filter** (`SelectKBest`, k=2) chose both copies: each looks strong on
  its own. Column 2, which carries truly new information, was left out.
- **L1** zeroed one of the copies (0 for column 0, 1.73 for column 1) and kept
  column 2: it does not pay for the same information twice. Which copy gets
  chosen can come down to chance.
- The **forest** **split** the importance between the copies (0.31 and 0.32).
  Someone looking at them alone would think "both are moderately important";
  in fact each is half of the same feature.

## What to do?

- Before selecting, look at highly correlated pairs (`df.corr()`, a heat map);
  if they mean the same thing, drop one by hand.
- When reading importance scores, think of copies together: they matter as a
  group (the Explaining Models section).
- Do not read meaning into which copy L1 picked; swap the two copies and the
  result may change.
