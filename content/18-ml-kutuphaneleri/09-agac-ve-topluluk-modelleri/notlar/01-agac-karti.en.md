## Classes

| Class | Idea | `NaN` |
|---|---|---|
| `DecisionTreeClassifier` / `Regressor` | one tree, readable | accepted |
| `RandomForestClassifier` / `Regressor` | bootstrap + random columns, voting | accepted |
| `ExtraTreesClassifier` / `Regressor` | the cut points are random too | accepted |
| `GradientBoostingClassifier` / `Regressor` | trees in sequence on residuals | not accepted |
| `HistGradientBoostingClassifier` / `Regressor` | fast boosting, large data | accepted |
| `BaggingClassifier(estimator)` | bags any model | depends on the model |
| `VotingClassifier(list, voting="soft")` | mean of probabilities | depends on the models |
| `StackingClassifier(list, final_estimator)` | a model on top of predictions | depends on the models |

## Settings that limit a tree

| Setting | Effect |
|---|---|
| `max_depth` | at most how many questions in a row |
| `min_samples_leaf` | at least how many rows in a leaf |
| `max_leaf_nodes` | at most how many leaves |
| `ccp_alpha` | the pruning price; `cost_complexity_pruning_path` gives candidates |

## Forest settings

| Setting | Effect |
|---|---|
| `n_estimators` | number of trees; many trees do not overfit, they only slow down |
| `max_features` | columns looked at in each split (`"sqrt"` by default) |
| `oob_score=True` | out-of-bag accuracy, `oob_score_` |
| `n_jobs=-1` | all cores |
| `class_weight="balanced"` | imbalanced classes |

## Attributes to read

| Attribute | What |
|---|---|
| `get_n_leaves()`, `get_depth()` | the size of the tree |
| `feature_importances_` | purity gain (from training, biased) |
| `estimators_` | the trees in the forest |
| `export_text(tree)`, `plot_tree(tree)` | writing / drawing the tree |
