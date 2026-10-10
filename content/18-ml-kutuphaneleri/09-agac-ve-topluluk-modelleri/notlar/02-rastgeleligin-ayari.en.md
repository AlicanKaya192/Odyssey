A random forest's strength comes from its trees being **different from one
another**. Two settings decide how different: how many columns each split
looks at (`max_features`) and whether the cut point is searched for (in
ExtraTrees it is chosen at random). They can be compared with the
out-of-bag score, without setting up a separate validation:

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
for features in ["sqrt", 0.5, None]:
    rf = RandomForestClassifier(n_estimators=200, max_features=features,
                                oob_score=True, random_state=0)
    print(features, round(rf.fit(X_train, y_train).oob_score_, 3))
extra = ExtraTreesClassifier(n_estimators=300, bootstrap=True, oob_score=True,
                             random_state=0).fit(X_train, y_train)
print(round(extra.oob_score_, 3), round(extra.score(X_test, y_test), 3))
```

```text
sqrt 0.916
0.5 0.904
None 0.907
0.918 0.893
```

## What we see

- `max_features="sqrt"` (3 of 10 columns) is the best. `None` looks at all
  columns at every split; the trees become alike and voting gains less. That
  is plain bagging.
- ExtraTrees also picks the cut points at random: its out-of-bag score is
  close to the forest's (0.918), its test score a little lower (0.893). On
  this data it is not better than the forest; which one wins depends on the
  data.
- ExtraTrees does not bootstrap by default; `bootstrap=True` is needed for an
  out-of-bag score.

## When

- Compare the forest and ExtraTrees on the same validation; neither always
  wins.
- `max_features` is one of the forest's most effective settings; put
  `"sqrt"`, `"log2"` and fractions between 0.3 and 0.7 into the search.
