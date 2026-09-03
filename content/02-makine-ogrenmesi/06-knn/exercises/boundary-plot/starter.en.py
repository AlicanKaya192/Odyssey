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

# Open two panels side by side.


# For the left panel k=1 and the right panel k=15:
# train the model, predict for the grid and reshape it to grid_x's shape,
# colour the regions with contourf, put the training points on top,
# write the title and axis labels, print the test accuracy.


# Call tight_layout and save as chart.png.
