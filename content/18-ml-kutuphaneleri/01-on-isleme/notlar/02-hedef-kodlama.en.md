For a category with very many distinct values (400 shops, thousands of
products), one-hot opens hundreds of columns. A common shortcut: replace each
category with **the target's mean within that category** (target encoding).
But done by hand, it leaks the target into the feature.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import TargetEncoder

rng = np.random.default_rng(4)
df = pd.DataFrame({"shop": rng.integers(0, 400, 2000).astype(str),
                   "bought": rng.integers(0, 2, 2000)})
train, test = train_test_split(df, test_size=0.5, random_state=4)
means = train.groupby("shop")["bought"].mean()
naive_train = train["shop"].map(means).to_frame()
naive_test = test["shop"].map(means).fillna(train["bought"].mean()).to_frame()
model = LogisticRegression().fit(naive_train, train["bought"])
print(round(model.score(naive_train, train["bought"]), 3),
      round(model.score(naive_test, test["bought"]), 3))
enc = TargetEncoder(random_state=4)
safe_train = enc.fit_transform(train[["shop"]], train["bought"])
safe_test = enc.transform(test[["shop"]])
model = LogisticRegression().fit(safe_train, train["bought"])
print(round(model.score(safe_train, train["bought"]), 3),
      round(model.score(safe_test, test["bought"]), 3))
```

```text
0.734 0.484
0.492 0.497
```

## What happened?

- There is **no relationship** in the data: shop and purchase were generated
  at random, independently. The true success should be around 50%.
- Hand encoding gave **73.4%** accuracy in training, 48.4% in testing. Each
  shop's mean was computed from the targets of that shop's own rows; with 2–3
  rows per shop, the mean carries the row's own answer. The model read the
  target from inside the feature.
- `TargetEncoder` does **cross fitting** on the training data: each row's
  code is computed from folds the row is not in. The training score is 49.2%,
  that is honest: there is nothing to learn and the model shows it.
- A category with few records has an unreliable mean; `TargetEncoder` pulls
  it towards the overall mean (smoothing, `smooth`).

## The rule

Any feature derived from the target (a target mean, a ranking by the target)
must be computed without seeing the training row's **own** answer. Instead of
doing it by hand, `TargetEncoder`; `fit_transform` in training, `transform`
in testing.
