import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(7)
X = pd.DataFrame(rng.normal(size=(80, 300)),
                 columns=[f"c{i}" for i in range(300)])
y = pd.Series(rng.normal(size=80))

correlations = X.apply(lambda c: abs(c.corr(y)))
chosen = correlations.sort_values(ascending=False).head(5).index.tolist()
A_train, A_test, ay_train, ay_test = train_test_split(
    X[chosen], y, test_size=0.25, random_state=42)
leaky = LinearRegression().fit(A_train, ay_train)
print(round(r2_score(ay_test, leaky.predict(A_test)), 3))

B_train, B_test, by_train, by_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
train_correlations = B_train.apply(lambda c: abs(c.corr(by_train)))
clean_choice = train_correlations.sort_values(ascending=False).head(5).index.tolist()
clean = LinearRegression().fit(B_train[clean_choice], by_train)
print(round(r2_score(by_test, clean.predict(B_test[clean_choice])), 3))
