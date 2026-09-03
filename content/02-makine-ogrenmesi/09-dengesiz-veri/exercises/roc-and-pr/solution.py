import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("transactions.csv")
X = df[["amount", "hour", "attempts"]]
y = df["fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, precision_recall_curve,
                             roc_auc_score, roc_curve)

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train_scaled, y_train)
logreg_probability = logreg.predict_proba(X_test_scaled)[:, 1]

forest = RandomForestClassifier(n_estimators=200, random_state=42)
forest.fit(X_train, y_train)
forest_probability = forest.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, logreg_probability)
average = average_precision_score(y_test, logreg_probability)
print("logreg", round(auc, 3), round(average, 3))
print("forest", round(roc_auc_score(y_test, forest_probability), 3),
      round(average_precision_score(y_test, forest_probability), 3))
print(round(float(y_test.mean()), 3))

fpr, tpr, _ = roc_curve(y_test, logreg_probability)
precision, recall, _ = precision_recall_curve(y_test, logreg_probability)

figure, axes = plt.subplots(1, 2)
axes[0].plot(fpr, tpr)
axes[0].set_xlabel("fpr")
axes[0].set_ylabel("tpr")
axes[0].set_title("ROC")
axes[1].plot(recall, precision)
axes[1].set_xlabel("recall")
axes[1].set_ylabel("precision")
axes[1].set_title("PR")
figure.tight_layout()
figure.savefig("chart.png")

print(round(auc - average, 3))
