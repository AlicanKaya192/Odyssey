import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split

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
X, y = df.drop(columns="churn"), df["churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,
                                                    random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = ["tenure", "monthly", "support"]
prep = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
     numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["plan"]),
])
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OrdinalEncoder


def model_auc(kind):
    if kind == "linear":
        model = make_pipeline(prep, LogisticRegression(C=0.1))
    else:
        model = make_pipeline(prep, LogisticRegression(C=0.1))
    scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")
    return round(float(scores.mean()), 3)

print(model_auc("linear"))
print(model_auc("boosting"))
