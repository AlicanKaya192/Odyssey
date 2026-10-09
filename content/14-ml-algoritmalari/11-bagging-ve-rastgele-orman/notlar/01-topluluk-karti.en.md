## Methods

| Method | Where does variety come from? | scikit-learn |
|---|---|---|
| Bagging | bootstrap samples | `BaggingClassifier` |
| Random forest | bootstrap + a random feature subset per split | `RandomForestClassifier` |
| Extremely randomised trees | random thresholds too | `ExtraTreesClassifier` |

## Settings

| Setting | Effect |
|---|---|
| `n_estimators` | the number of trees; many does no harm, it slows down |
| `max_features` | features looked at per split; `"sqrt"` in classification |
| `max_depth`, `min_samples_leaf` | the complexity of individual trees |
| `oob_score=True` | out-of-bag validation |

## When?

- When a strong model that works well with few settings is needed on tabular
  data.
- No scaling needed; it learns non-linear relations and interactions.
- Minuses: a single tree's readability is lost; many trees need memory and
  prediction time.

## Common mistakes

- Taking a tree's own `feature_importances_` as certain: it can favour
  features with many values (continuous ones); permutation importance is more
  reliable.
- Mixing up OOB and the test result: OOB comes from the training data; the
  final measurement is still made on a separate test set.
- Leaving `max_features=None` in a random forest: it turns into bagging and the
  trees become alike.
