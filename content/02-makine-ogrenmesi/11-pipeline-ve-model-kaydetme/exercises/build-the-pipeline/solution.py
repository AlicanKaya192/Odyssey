import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("subscribers.csv")
print(df.isna().sum().to_dict())

X = df.drop(columns="churn")
y = df["churn"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

numeric = ["tenure", "monthly", "support"]
text = ["city", "plan"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ]), text),
])

pipe = Pipeline([
    ("prepare", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)

baseline = accuracy_score(y_test, [y_train.mode()[0]] * len(y_test))
print(round(baseline, 3),
      round(accuracy_score(y_test, pipe.predict(X_test)), 3))

names = [str(name) for name
         in pipe.named_steps["prepare"].get_feature_names_out()]
print(len(names))
print(names)
