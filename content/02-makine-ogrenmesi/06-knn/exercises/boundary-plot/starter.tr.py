import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("customers.csv")
X = df[["income", "visits"]]
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

grid_x, grid_y = np.meshgrid(np.linspace(-2.5, 2.5, 200),
                             np.linspace(-2.5, 2.5, 200))
grid = np.c_[grid_x.ravel(), grid_y.ravel()]

# Yan yana iki panel ac.


# Sol panel k=1, sag panel k=15 icin:
# modeli egit, grid icin tahmin uret ve grid_x sekline getir,
# bolgeleri contourf ile boya, egitim noktalarini scatter ile ustune koy,
# baslik ve eksen adlarini yaz, test dogrulugunu yazdir.


# tight_layout cagir ve chart.png olarak kaydet.
