Every step carries the same shape: **learn on training, apply to both.**

## Missing values

**Seeing them:**

```python
print(df.isna().sum())                    # count per column
print(df.isna().sum().sum())              # the total
print(df[df.isna().any(axis=1)])          # the rows with gaps
```

**Filling them (by hand):**

```python
fill_value = X_train["engine"].mean()     # or .median()
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})
```

**Filling them (with sklearn):**

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="mean")
imputer.fit(X_train)
X_train = imputer.transform(X_train)
X_test = imputer.transform(X_test)
```

| `strategy` | What it does | When |
|---|---|---|
| `mean` | Fills with the mean | Numeric, no outliers |
| `median` | Fills with the median | Numeric, with outliers |
| `most_frequent` | Fills with the commonest value | Categorical |
| `constant` | Fills with a fixed `fill_value` | When the absence itself is meaningful |

**Dropping them:**

```python
df = df.dropna()                          # drop rows with any gap
df = df.dropna(subset=["engine"])         # look at this column only
df = df.drop(columns=["engine"])          # drop the whole column
```

If more than half a column is missing, filling becomes invention; dropping
the column is more honest.

## Categorical columns

**Finding them:**

```python
text_columns = df.select_dtypes(exclude="number").columns.tolist()
print(df["fuel"].unique())
print(df["fuel"].value_counts())
```

**A pandas 3 warning:** the `df.dtypes == "object"` check found in older
sources no longer **finds** text columns; use
`select_dtypes(exclude="number")`.

**One-hot (pandas):**

```python
encoded = pd.get_dummies(df, columns=["fuel", "gearbox"])
encoded = pd.get_dummies(df, columns=["fuel"], drop_first=True)
```

`drop_first=True` drops one column per group: three categories can be
described with two columns (if both are 0, it is the third). Preferred for
linear models, unnecessary for trees.

**One-hot (sklearn):**

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
encoder.fit(X_train[["fuel"]])
train_encoded = encoder.transform(X_train[["fuel"]])
test_encoded = encoder.transform(X_test[["fuel"]])
```

**When `OneHotEncoder` instead of `get_dummies`:** when the test set may
contain a category not seen in training. `get_dummies` produces **different
columns** for the two sets and the model breaks; `OneHotEncoder` remembers
the training categories and, with `handle_unknown="ignore"`, drops new ones
quietly.

**Ordinal encoding:**

```python
order = {"low": 0, "medium": 1, "high": 2}
df["level"] = df["level"].map(order)
```

Only when the categories really do have **an order**.

## Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

| Scaler | Result | To outliers |
|---|---|---|
| `StandardScaler` | Mean 0, standard deviation 1 | Sensitive |
| `MinMaxScaler` | Between 0 and 1 | Very sensitive |
| `RobustScaler` | Median and quartiles | Robust |

**When to use `fit_transform`:** on the training set only.

```python
X_train_scaled = scaler.fit_transform(X_train)   # correct
X_test_scaled = scaler.transform(X_test)         # correct
X_test_scaled = scaler.fit_transform(X_test)     # LEAKAGE
```

The last line re-teaches the scaler on the test data: leakage, and on top of
that the two sets end up on different scales.

**Which models want it:**

| Want it | Do not |
|---|---|
| KNN | Decision tree |
| SVM | Random forest |
| Linear models (regularised) | Gradient boosting |
| Clustering (KMeans) | Naive Bayes |
| Neural networks | |

## The order

```python
# 1. read
df = pd.read_csv("cars.csv")

# 2. SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# 3. fill the gaps (learn from training)
fill_value = X_train["engine"].mean()
X_train = X_train.fillna({"engine": fill_value})
X_test = X_test.fillna({"engine": fill_value})

# 4. encode the categories
# 5. scale (fit on training, transform on both)
# 6. train and measure
```

## Common mistakes

- **Preparing before splitting.** The most common and the sneakiest.
- **Calling `fit_transform` on the test set.** Leakage.
- **Computing the fill value over all the data.** Leakage.
- **Inventing an order for unordered categories.** `petrol=0, diesel=1,
  lpg=2`.
- **Applying `get_dummies` to the two sets separately.** The columns will
  not match.
- **Scaling the target (`y`) too.** Unnecessary, and it makes the results
  harder to interpret.
- **Spending time scaling for a tree model.** It does no harm and no good.
