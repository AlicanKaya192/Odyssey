# Tree and Ensemble Models

You saw how a decision tree splits, random forests, out-of-bag (OOB)
validation and the idea of boosting in the Machine Learning track and the ML
Algorithms module. This section looks at the tools that help when working
with trees in scikit-learn: **pruning** a tree, training directly with
missing values, why `feature_importances_` can mislead, and
`VotingClassifier` / `StackingClassifier`, which combine several models.

## Pruning: ccp_alpha

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

X, y = make_classification(n_samples=600, n_features=10, n_informative=4,
                           flip_y=0.1, random_state=8)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=8)
full = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)
print(full.get_n_leaves(), full.get_depth(), round(full.score(X_test, y_test), 3))
path = full.cost_complexity_pruning_path(X_train, y_train)
print(len(path.ccp_alphas))
search = GridSearchCV(DecisionTreeClassifier(random_state=0),
                      {"ccp_alpha": path.ccp_alphas}, cv=5).fit(X_train, y_train)
pruned = search.best_estimator_
print(round(search.best_params_["ccp_alpha"], 4), pruned.get_n_leaves(),
      pruned.get_depth(), round(pruned.score(X_test, y_test), 3))
print(export_text(pruned, max_depth=1))
```

```text
48 12 0.84
29
0.0062 12 5 0.9
|--- feature_2 <= 0.20
|   |--- feature_3 <= 0.81
|   |   |--- truncated branch of depth 3
|   |--- feature_3 >  0.81
|   |   |--- truncated branch of depth 4
|--- feature_2 >  0.20
|   |--- feature_6 <= 0.95
|   |   |--- truncated branch of depth 2
|   |--- feature_6 >  0.95
|   |   |--- truncated branch of depth 2
```

- The unlimited tree has 48 leaves and depth 12; 10% of the labels are noise
  (`flip_y=0.1`) and the tree memorises them too. Test 0.84.
- **Pruning** means growing first and cutting afterwards: `ccp_alpha` puts a
  price on each leaf, and branches that do less work than their price are
  cut. `cost_complexity_pruning_path` gives the tree's meaningful pruning
  points (29 of them); cross-validation picks the good one.
- The chosen tree has 12 leaves and depth 5; test 0.9. Both better and
  readable. `export_text` writes the tree as text; `max_depth=1` shows the
  first two levels, the rest is a "truncated branch".

## Stopping early: min_samples_leaf

```python
from sklearn.model_selection import cross_val_score

for leaf in [1, 5, 20, 50]:
    model = DecisionTreeClassifier(min_samples_leaf=leaf, random_state=0)
    score = cross_val_score(model, X_train, y_train, cv=5).mean()
    print(leaf, model.fit(X_train, y_train).get_n_leaves(), round(score, 3))
```

```text
1 48 0.82
5 30 0.862
20 14 0.842
50 7 0.798
```

- The opposite of pruning: the tree is stopped while growing.
  `min_samples_leaf=5` asks for at least 5 rows in each leaf; 48 leaves drop
  to 30 and accuracy rises from 0.82 to 0.862.
- A very large value (50) oversimplifies the tree: 7 leaves, 0.798.
- Similar knobs: `max_depth`, `max_leaf_nodes`, `min_samples_split`. They all
  ask the same question: how much detail may the tree go into?

## Directly with missing values

```python
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

X_nan = X_train.copy()
rng = np.random.default_rng(0)
X_nan[rng.random(X_nan.shape) < 0.1] = np.nan    # 10% of cells empty
print(int(np.isnan(X_nan).sum()))
for model in [DecisionTreeClassifier(random_state=0),
              RandomForestClassifier(random_state=0),
              GradientBoostingClassifier(random_state=0)]:
    try:
        model.fit(X_nan, y_train)
        print(type(model).__name__, round(model.score(X_test, y_test), 3))
    except ValueError as err:
        print(type(model).__name__, str(err).splitlines()[0])
```

```text
470
DecisionTreeClassifier 0.82
RandomForestClassifier 0.9
GradientBoostingClassifier Input X contains NaN.
```

- `DecisionTreeClassifier` and `RandomForestClassifier` accept `NaN`
  directly: at each split they also learn which side the missing values go
  to. No imputer step is needed.
- The older `GradientBoostingClassifier` does not. The boosting class that
  takes missing values directly is `HistGradientBoostingClassifier`; it is in
  the Gradient Boosting Libraries section.
- If missingness carries information (a form left empty), learning it can be
  better than filling it in; measure case by case.

## feature_importances_ can mislead

```python
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer(as_frame=True)
X = data.data.iloc[:, :5].copy()
y = data.target
rng = np.random.default_rng(0)
X["row_id"] = rng.permutation(len(X))    # meaningless, 569 distinct values
X["coin"] = rng.integers(0, 2, len(X))   # meaningless, 2 distinct values
rf = RandomForestClassifier(n_estimators=200, random_state=0).fit(X, y)
for name, value in zip(X.columns, rf.feature_importances_):
    print(f"{name:16} {value:.3f}")
```

```text
mean radius      0.209
mean texture     0.115
mean perimeter   0.280
mean area        0.256
mean smoothness  0.102
row_id           0.031
coin             0.006
```

- `feature_importances_` is the total **gain in purity** each column gave in
  the trees. Fast and free, but biased.
- `row_id` and `coin` are both entirely random; they have nothing to do with
  the target. Still `row_id` got 0.031, five times `coin`. In a column with
  many distinct values the tree always finds a cut point that "seems to
  help"; it fits the noise in the training data.
- These importances are computed **from the training data**. Whether a
  column really helps on unseen data is measured by permutation importance
  (the Explaining Models section).

## Combining models

```python
from sklearn.ensemble import (RandomForestClassifier, StackingClassifier,
                              VotingClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

base = [("lr", make_pipeline(StandardScaler(), LogisticRegression())),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier(15))),
        ("rf", RandomForestClassifier(n_estimators=200, random_state=0))]
vote = VotingClassifier(base, voting="soft")
stack = StackingClassifier(base, final_estimator=LogisticRegression())
for name, model in base + [("vote", vote), ("stack", stack)]:
    print(name, round(cross_val_score(model, X_train, y_train, cv=5).mean(), 3))
```

```text
lr 0.896
knn 0.898
rf 0.911
vote 0.907
stack 0.904
```

- `VotingClassifier(voting="soft")` averages the models' probabilities.
  `StackingClassifier` makes each model's (cross-validated) predictions into
  new columns and trains one more model on top.
- On this data neither **beat** the random forest (0.907 and 0.904; the
  forest alone 0.911). Combining gains when the models make **different**
  errors; if the best model is already strong, the weaker ones can pull it
  down.
- The price: training three models, and for stacking an inner
  cross-validation too. Always compare with the single best model.

## Summary

- Limit the tree: `ccp_alpha` (pruning, with cross-validation) or
  `min_samples_leaf` / `max_depth`.
- Trees and random forests accept `NaN`; the older gradient boosting does
  not.
- `feature_importances_` favours many-valued columns and comes from the
  training data; look at permutation importance before deciding.
- Voting / stacking gains only with models that make different errors.
