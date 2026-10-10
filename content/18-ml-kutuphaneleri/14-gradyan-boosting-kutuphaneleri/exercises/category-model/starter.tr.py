import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(2)
names = [f"c{i}" for i in range(30)]
effect = dict(zip(names, rng.normal(0, 1, 30)))
city = rng.choice(names, 6000)
x1 = rng.normal(0, 1, 6000)
chance = 1 / (1 + np.exp(-(1.5 * pd.Series(city).map(effect) + x1)))
target = (rng.random(6000) < chance).astype(int)
df = pd.DataFrame({"city": pd.Categorical(city), "x1": x1})
df.loc[rng.random(6000) < 0.1, "x1"] = np.nan
d_train, d_test, t_train, t_test = train_test_split(df, target, random_state=2)
from sklearn.ensemble import HistGradientBoostingClassifier


def category_model(min_leaf):
    model = HistGradientBoostingClassifier(min_samples_leaf=min_leaf, random_state=0)
    model.fit(d_train[["x1"]], t_train)
    score = model.score(d_test[["x1"]], t_test)
    return [model.is_categorical_.tolist(), round(float(score), 3)]

print(category_model(20))
