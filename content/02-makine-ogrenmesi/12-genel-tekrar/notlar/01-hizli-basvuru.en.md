## The skeleton

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("data.csv")
X = df.drop(columns="target")
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

numeric = ["a", "b"]
text = ["c", "d"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler())]), numeric),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                      ("encode", OneHotEncoder(handle_unknown="ignore"))]), text),
])

pipe = Pipeline([("prepare", preprocessor), ("model", model)])
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipe, X_train, y_train, cv=folds)

pipe.fit(X_train, y_train)
print(accuracy_score(y_test, pipe.predict(X_test)))
```

`stratify=y` is for classification only; regression uses `KFold`.

## The baseline

```python
# classification: the most frequent class
baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))

# regression: the training mean
baseline = mean_absolute_error(y_test, [y_train.mean()] * len(y_test))
```

This line is written in every project. Without it no score can be read.

## Models

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                              GradientBoostingClassifier)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
```

| Model | When | Scaling | Main setting |
|---|---|---|---|
| `LinearRegression` | The relationship is linear | Not needed | — |
| `LogisticRegression` | Binary classification, a fast baseline | Useful | `C`, `class_weight` |
| `KNeighbors*` | Small data, local patterns | **Mandatory** | `n_neighbors` |
| `DecisionTree*` | Interpretability is essential | Not needed | `max_depth` |
| `RandomForest*` | General purpose, stable | Not needed | `n_estimators` |
| `GradientBoosting*` | Reducing bias | Not needed | `learning_rate` |
| `KMeans` | No labels, looking for groups | **Mandatory** | `n_clusters` |
| `PCA` | Dimension reduction, drawing | **Mandatory** | `n_components` |

## Metrics

```python
# regression
from sklearn.metrics import (mean_absolute_error, root_mean_squared_error,
                             r2_score)

# classification
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix,
                             classification_report, roc_auc_score,
                             average_precision_score)

# clustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
```

| Metric | What it says | Its baseline |
|---|---|---|
| MAE | Mean absolute error, same units | The mean's MAE |
| RMSE | Punishes large errors | The mean's RMSE |
| R² | How much of the variance is explained | 0 |
| Accuracy | The share got right | The most frequent class's share |
| Precision | How much of what it called positive is right | — |
| Recall | How many real positives were caught | — |
| F1 | The harmonic mean of the two | — |
| ROC AUC | Ranking ability | 0.5 |
| Average precision | The area under the PR curve | **The positive rate** |
| Silhouette | How tidy the clusters are | Its value on noise |

The last column is often skipped and is where most misreadings come from.

## Cross validation

```python
scores = cross_val_score(pipe, X_train, y_train, cv=folds,
                         scoring="average_precision")
print(round(float(scores.mean()), 3), round(float(scores.std()), 3))
```

**The mean is never read alone; the spread is written too.** If the gap
between two models' means is smaller than the spreads, there is no gap.

Common `scoring` values: `"accuracy"`, `"precision"`, `"recall"`, `"f1"`,
`"roc_auc"`, `"average_precision"`, `"r2"`, `"neg_mean_absolute_error"`.

## Tuning

```python
from sklearn.model_selection import GridSearchCV

grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
search = GridSearchCV(pipe, grid, cv=folds, scoring="accuracy")
search.fit(X_train, y_train)
print(search.best_params_, round(float(search.best_score_), 3))
```

The step names and the parameter are joined by **two underscores**.
`best_score_` is not the final report — it comes from the training side and
is optimistic.

## Imbalanced data

```python
model = LogisticRegression(max_iter=1000, class_weight="balanced")

probability = pipe.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

`predict()` always uses 0.5. The threshold is a business decision and is
chosen **on the training side**.

## Saving

```python
import joblib
joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

The **whole** model is saved. A text file beside it records the library
versions, the threshold and the scores you measured.

## Four rules that never change

1. **Measure the baseline.** Without it no score can be read.
2. **Split first, touch afterwards.** A pipeline guarantees it.
3. **Look at the test set once.** A second look makes the score optimistic.
4. **Never trust one number.** Read the spread, the confusion matrix and
   the baseline together.
