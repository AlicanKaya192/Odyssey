## Methods

| Kind | Code | When |
|---|---|---|
| Constant column | `VarianceThreshold(threshold=0)` | always first |
| Filter | `SelectKBest(f_classif, k=10)` | a fast first cut (classification) |
| Filter | `SelectKBest(f_regression, k=10)` | regression |
| Filter | `SelectKBest(mutual_info_classif, k=10)` | non-linear relationships |
| Filter | `SelectPercentile(f_classif, percentile=20)` | by percentage |
| Embedded | `SelectFromModel(LogisticRegression(penalty="l1", solver="liblinear"))` | sparse linear |
| Embedded | `SelectFromModel(RandomForestClassifier(), max_features=10, threshold=-np.inf)` | tree importance |
| Wrapper | `RFECV(model, cv=5)` | judges columns together, expensive |
| Wrapper | `SequentialFeatureSelector(model, n_features_to_select=5)` | forward / backward addition |

## Reading

| Code | Gives |
|---|---|
| `sel.get_support()` | the selected ones (True/False) |
| `sel.get_support(indices=True)` | the positions of the selected ones |
| `sel.get_feature_names_out(names)` | the selected names |
| `kb.scores_`, `kb.pvalues_` | filter scores |
| `rfe.ranking_`, `rfe.n_features_` | elimination order, number selected |

## Rules

- Selection inside the pipeline; otherwise cross-validation shows a fake
  success.
- `k` is a hyperparameter: `selectkbest__k` with `GridSearchCV`.
- Copy columns: the filter picks both, L1 one, a forest splits the importance.
- Dropping a column drops information; drop it if the score does not fall and
  the model gets simpler.
