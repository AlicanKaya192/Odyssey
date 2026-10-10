# Overall Review

You have reached the end of the ML Libraries module. From scikit-learn's
common interface to preprocessing and pipelines, from model selection to
metrics, from linear models to boosting libraries, from statsmodels'
inference tools to saving and explaining a model, you have seen a model's
whole path from start to finish. This section walks the path once more; at
the end there is an example where all of it works together.

<figure class="fig">
  <div class="flow">
    <span class="node">Preparation<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Evaluation<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Models<br><small>08–10, 14</small></span><span class="arrow">→</span>
    <span class="node">Statistics<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Saving and explaining<br><small>11, 15</small></span>
  </div>
  <figcaption>The module's path: prepare the data, measure honestly, choose the model, test the effect, save and explain.</figcaption>
</figure>

## 1. Preparation (Sections 0–4)

| Task | Tool |
|---|---|
| Common interface | build → `fit` → `predict` / `transform`; learned `coef_`, `mean_`; `clone` |
| Scale | `StandardScaler`, `RobustScaler` with outliers; unnecessary for trees |
| Missing and categories | `SimpleImputer(add_indicator=True)`, `OneHotEncoder(handle_unknown="ignore")`, `OrdinalEncoder` |
| Column groups | `ColumnTransformer`, `remainder`, `make_column_selector`, `set_output(transform="pandas")` |
| Flow | `make_pipeline`, `step__setting`, your own transformer, `FunctionTransformer` |
| Selecting columns | `VarianceThreshold`, `SelectKBest`, `SelectFromModel`, `RFECV` |

Every step that learns from data goes **inside** the pipeline; left outside,
cross-validation shows fake success. The default `remainder="drop"` silently
drops columns.

## 2. Evaluation (Sections 5–7)

| Task | Tool |
|---|---|
| Search | `GridSearchCV`, `RandomizedSearchCV(loguniform, randint)`, `cv_results_` |
| An honest score | nested validation, a held-out test; `best_score_` is optimistic |
| Splitter | `StratifiedKFold`, `KFold(shuffle=True)`, `GroupKFold`, `TimeSeriesSplit` |
| Several measures | `cross_validate(scoring=[...], return_train_score=True)` |
| Curves | `learning_curve`, `validation_curve` |
| Measure | `scoring="neg_..."`, `average="macro"`, AUC with probabilities, `make_scorer` |
| Threshold | `TunedThresholdClassifierCV`, `FixedThresholdClassifier` |

Shuffle sorted data, keep the same person off both sides, train on the past
in time. Do not choose the threshold by looking at the test data.

## 3. Models (Sections 8–10 and 14)

| Task | Tool |
|---|---|
| Linear | `RidgeCV`, `LassoCV`, `LogisticRegression(l1_ratio=1, solver="saga")`, `C=np.inf` |
| Curved relationship | `PolynomialFeatures` + a penalised model |
| Tree | `ccp_alpha`, `min_samples_leaf`, accepts `NaN` |
| Ensemble | `RandomForest`, `ExtraTrees`, `VotingClassifier`, `StackingClassifier` |
| Clustering | `KMeans`, `HDBSCAN`; ARI, silhouette |
| Dimensions | `PCA(n_components=0.95)`, `TSNE` for drawing only |
| Boosting | `HistGradientBoostingClassifier`, `LGBMClassifier`; `eval_X`, `eval_y`, `early_stopping` |

A `ConvergenceWarning` is usually missing scaling; `feature_importances_`
favours many-valued columns; combining gains only with models that make
different errors.

## 4. Statistics (Sections 12–13)

| Task | Tool |
|---|---|
| OLS | `sm.OLS(y, sm.add_constant(X))`, `summary().tables[1]`, `conf_int` |
| Diagnostics | `variance_inflation_factor`, `het_breuschpagan`, `cov_type="HC3"` |
| Prediction interval | `get_prediction(...).summary_frame()`: `mean_ci`, `obs_ci` |
| Formula | `smf.ols("y ~ a + C(c)")`, `Treatment('...')`, `a * C(c)`, `I(a ** 2)` |
| GLM | `smf.logit` (odds ratio), `Poisson` + `offset`, negative binomial |

Do not forget the constant; a large p is not "no effect"; `obs_ci` for one
house.

## 5. Saving and explaining (Sections 11 and 15)

| Task | Tool |
|---|---|
| Saving | `joblib.dump({...}, compress=3)`; version, columns, threshold together |
| Safe loading | turn `InconsistentVersionWarning` into an error; do not open untrusted files |
| Importance | `permutation_importance(model, X_test, y_test)` |
| Shape of an effect | `partial_dependence`, `PartialDependenceDisplay(kind="both")` |

## All together

```python
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import (GridSearchCV, StratifiedKFold,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

rng = np.random.default_rng(16)
df = pd.DataFrame({
    "tenure": rng.integers(1, 72, 1500).astype(float),
    "monthly": rng.uniform(20, 120, 1500).round(2),
    "plan": rng.choice(["basic", "plus", "pro"], 1500),
    "support": rng.poisson(1.5, 1500).astype(float),
})
plan_effect = df["plan"].map({"basic": 0.6, "plus": 0.0, "pro": -0.6})
logit = (-0.04 * df["tenure"] + 0.02 * df["monthly"] + 0.5 * df["support"]
         + plan_effect - 0.5)
df["churn"] = (rng.random(1500) < 1 / (1 + np.exp(-logit))).astype(int)
df.loc[rng.random(1500) < 0.08, "monthly"] = np.nan
print(round(df["churn"].mean(), 3), int(df["monthly"].isna().sum()))

X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,
                                                    random_state=0)
numeric = ["tenure", "monthly", "support"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
     numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["plan"]),
])
pipe = make_pipeline(prep, LogisticRegression())
cv = StratifiedKFold(5, shuffle=True, random_state=0)
search = GridSearchCV(pipe, {"logisticregression__C": [0.01, 0.1, 1, 10]},
                      cv=cv, scoring="roc_auc").fit(X_train, y_train)
print(search.best_params_, round(search.best_score_, 3))

boost = make_pipeline(
    ColumnTransformer([("cat", OrdinalEncoder(), ["plan"])],
                      remainder="passthrough"),
    HistGradientBoostingClassifier(random_state=0))
boost_auc = cross_val_score(boost, X_train, y_train, cv=cv, scoring="roc_auc")
print(round(boost_auc.mean(), 3))

best = search.best_estimator_
print(round(roc_auc_score(y_test, best.predict_proba(X_test)[:, 1]), 3))
perm = permutation_importance(best, X_test, y_test, scoring="roc_auc",
                              n_repeats=10, random_state=0)
order = perm.importances_mean.argsort()[::-1]
print([X.columns[i] for i in order])
joblib.dump({"model": best, "columns": list(X.columns)}, "churn.joblib")
loaded = joblib.load("churn.joblib")
print(bool((loaded["model"].predict(X_test) == best.predict(X_test)).all()))
```

```text
0.553 123
{'logisticregression__C': 0.1} 0.777
0.72
0.814
['tenure', 'support', 'monthly', 'plan']
True
```

- **Data:** 1500 subscribers; a churn rate of 55.3%; 123 cells of the monthly
  fee are missing. The rule that made churn is linear (logistic): short
  tenure, many support requests and the `basic` plan mean more churn.
- **Preparation:** `ColumnTransformer` applies median filling + scaling to the
  numbers and one-hot to the plan; all inside the pipeline, no leakage.
- **Evaluation:** `C` was searched with a shuffled `StratifiedKFold` and AUC:
  the best is 0.1, cross-validated AUC 0.777.
- **Comparing models:** on the same folds boosting gets 0.72. Since the data
  was made by a linear rule, the linear model leads; "the strongest model"
  is not the best on every dataset; it is measured.
- **Test:** the chosen model was measured once on the test data: AUC 0.814.
- **Explanation:** the permutation importance order is `tenure`, `support`,
  `monthly`, `plan`; the rule's largest effect was tenure.
- **Saving:** the model and column list in one file; the loaded model gives
  the same predictions.

## Next

The notes hold a one-page summary of the whole module and where to go from
here. The four modules of the Core Libraries track end here: Python Libraries
(Beginner and Advanced), Data Science Libraries and ML Libraries.
