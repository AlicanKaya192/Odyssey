## Methods

| Method | Idea | Where |
|---|---|---|
| AdaBoost | weigh misclassified samples up, let stumps vote | `AdaBoostClassifier` |
| Gradient boosting | each round a tree on the loss gradient (the residual in regression) | `GradientBoostingRegressor` |
| Histogram-based GB | bins the features and searches splits very fast | `HistGradientBoostingClassifier` |
| XGBoost, LightGBM, CatBoost | the same idea, sped up for regularisation and big data | separate libraries |

## Settings

| Setting | Effect |
|---|---|
| `n_estimators` | the number of trees; **can overfit**, choose with early stopping |
| `learning_rate` | each tree's contribution; small → more trees, usually better |
| `max_depth` | the trees' depth; shallow trees (2–6) in boosting |
| `subsample` | each tree with part of the data (stochastic GB) |

## Compared with bagging

| | Bagging / random forest | Boosting |
|---|---|---|
| Trees | independent, parallel | sequential, depending on the previous |
| Tree type | deep (low bias) | shallow (weak learner) |
| As the number of trees grows | does not overfit | can overfit |
| What goes down | variance | bias (and variance) |

## Common mistakes

- Choosing the number of trees by training error: it always says "more".
- A large learning rate: memorisation within a few trees.
- AdaBoost on noisy labels: it piles weight onto the wrong labels.
