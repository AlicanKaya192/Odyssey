## Splitters

| Code | When |
|---|---|
| `KFold(5, shuffle=True, random_state=0)` | regression, independent rows |
| `StratifiedKFold(5, shuffle=True, random_state=0)` | classification (class ratio kept) |
| `GroupKFold(5)` + `groups=` | the same person/device in several rows |
| `StratifiedGroupKFold(5)` | group + class ratio |
| `TimeSeriesSplit(n_splits=5, test_size=, gap=)` | time order |
| `RepeatedStratifiedKFold(n_splits=5, n_repeats=10)` | a steadier mean on small data |
| `ShuffleSplit(n_splits=10, test_size=0.2)` | random splits that may overlap |
| `LeaveOneOut()` | very small data; each row tested once |

## Tools

| Code | Gives |
|---|---|
| `cross_val_score(m, X, y, cv=cv, scoring="f1")` | fold scores of one measure |
| `cross_validate(m, X, y, cv=cv, scoring=[...], return_train_score=True)` | a dictionary: `test_*`, `train_*`, times |
| `cross_val_predict(m, X, y, cv=cv)` | for each row, the prediction of a model that never saw it |
| `learning_curve(m, X, y, train_sizes=[...])` | training/test score by data size |
| `validation_curve(m, X, y, param_name=, param_range=)` | training/test score by one setting |

## Rules

- The number `cv=5`: `StratifiedKFold` for a classifier, `KFold` for
  regression; neither **shuffles**.
- Build the splitter object once and pass the same one everywhere: the
  models are then compared on the same folds.
- Validation should imitate what the model will face tomorrow: a new
  customer → group, the future → time.
- Only group splitters use `groups=`; plain `KFold` ignores it with a
  warning.
