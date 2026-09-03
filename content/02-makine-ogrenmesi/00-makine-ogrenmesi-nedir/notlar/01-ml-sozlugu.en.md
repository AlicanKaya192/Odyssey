The words in this field are new names for familiar things. Here they are.

## Data

| Term | What it means |
|---|---|
| Sample (instance) | A **row** in the table: one house, one patient |
| Feature (variable) | A **column** used to predict |
| Target (label) | The column you want to predict |
| Independent variable | Another name for a feature — `X` |
| Dependent variable | Another name for the target — `y` |
| Dimension | The number of features |

`X` is capital and `y` lowercase: `X` is a table, `y` a single column.

## Kinds of learning

| Kind | What you have | Example |
|---|---|---|
| Supervised | Features **and** the right answers | Price prediction, spam detection |
| Unsupervised | Features only | Customer clustering, dimension reduction |
| Reinforcement | Rewards and penalties | Systems that play games |

## Kinds of problem

| Target | Problem | Measure |
|---|---|---|
| A number | Regression | MAE, RMSE, R² |
| Two categories | Binary classification | Accuracy, precision, recall, AUC |
| Many categories | Multiclass classification | Accuracy, macro F1 |
| No label | Clustering | Silhouette, elbow |

## The process

| Term | What it means |
|---|---|
| Training set | The data the model learns from |
| Test set | Data the model **never sees**, kept for measuring |
| Validation set | A third piece kept aside for trying settings |
| Fit | Deriving the rule from data |
| Predict | Applying the rule to a new row |
| Baseline | The simplest prediction that learns nothing; the yardstick |

## How a model behaves

| Term | What it means |
|---|---|
| Overfitting | Excellent on training, poor on test — it memorised |
| Underfitting | Poor on both — the rule stayed too simple |
| Generalisation | Working on data it has not seen |
| Bias | The model being wrong systematically |
| Variance | The result changing a lot when the data changes a little |

## Parameter and hyperparameter

| Term | Who decides it |
|---|---|
| Parameter | The **model**, during training (the slope in linear regression) |
| Hyperparameter | **You**, before training (the `k` in KNN, a tree's depth) |

The distinction is practical: you never set a parameter by hand, and you
choose a hyperparameter by trying.

## In sklearn every model has the same three steps

```python
model = SomeModel()          # build
model.fit(X_train, y_train)  # learn
prediction = model.predict(X_test)
```

Linear regression, decision tree, KNN — all of them carry the same three
calls. Changing model usually means changing one line. That design is what
makes trying different methods cheap.

## Common abbreviations

| Abbreviation | What it stands for |
|---|---|
| MAE | Mean Absolute Error |
| MSE / RMSE | Mean Squared Error / its square root |
| R² | The share of variance explained |
| TP / TN / FP / FN | True positive / true negative / false positive / false negative |
| ROC-AUC | Area under the curve |
| CV | Cross validation |
| KNN | K-Nearest Neighbors |
| CART | Classification and Regression Tree |
| RF | Random Forest |
| GBM | Gradient Boosting Machine |
