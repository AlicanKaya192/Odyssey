`ColumnTransformer` shows its real strength when combined with a model **in a
single object**: a raw DataFrame goes in, a prediction comes out. Filling,
encoding and the model are learned with the same `fit`; it works even when new
data has a missing value or an unknown city.

```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

rng = np.random.default_rng(5)
n = 200
homes = pd.DataFrame({"size": rng.uniform(50, 200, n).round(),
                      "city": rng.choice(["Izmir", "Ankara", "Bursa"], n)})
bonus = homes["city"].map({"Izmir": 300, "Ankara": 200, "Bursa": 100})
price = homes["size"] * 20 + bonus + rng.normal(0, 50, n)
homes.loc[homes.sample(10, random_state=5).index, "size"] = np.nan
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), ["size"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
model = make_pipeline(prep, LinearRegression()).fit(homes, price)
new = pd.DataFrame({"size": [100.0, np.nan], "city": ["Izmir", "Van"]})
print(model.predict(new).round(0).tolist())
print(round(model.score(homes, price), 3))
print(model[0].named_transformers_["num"].statistics_.tolist())
```

```text
[2327.0, 2679.0]
0.953
[122.5]
```

## What happened?

- `make_pipeline(prep, LinearRegression())` applies the preparation first,
  then the model. The model was trained on the raw `homes` table and predicted
  on the raw `new` table; no step by hand in between.
- The second new home has both an unknown size and an unseen city (Van). The
  size was filled with the training median (122.5); all the city columns
  became 0. No error, but this prediction was made **with assumptions**: for
  Van the model used no city's effect. In production such rows should be
  counted and watched.
- `model[0]` gives the first step (the preparation), `named_transformers_["num"]`
  its part; the learned median is read from there.

## Why one object?

- **The same** steps, with the same learned values, are applied to test and
  production data; forgetting one is impossible.
- In cross-validation the preparation is learned in each fold from that fold's
  training data only: leakage is prevented by itself (the Pipeline section).
- A single saved file carries everything (the Saving Models section).
