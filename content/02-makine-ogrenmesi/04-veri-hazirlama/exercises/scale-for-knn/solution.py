import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("cars.csv").dropna()
X = df[["age", "km", "engine"]]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_raw = KNeighborsRegressor(n_neighbors=5).fit(X_train, y_train)
knn_scaled = KNeighborsRegressor(n_neighbors=5).fit(X_train_scaled, y_train)
raw_mae = mean_absolute_error(y_test, knn_raw.predict(X_test))
scaled_mae = mean_absolute_error(y_test, knn_scaled.predict(X_test_scaled))
print(round(raw_mae, 2), round(scaled_mae, 2))

lin_raw = LinearRegression().fit(X_train, y_train)
lin_scaled = LinearRegression().fit(X_train_scaled, y_train)
lin_raw_mae = mean_absolute_error(y_test, lin_raw.predict(X_test))
lin_scaled_mae = mean_absolute_error(y_test, lin_scaled.predict(X_test_scaled))
print(round(lin_raw_mae, 2), round(lin_scaled_mae, 2))

print("same" if round(lin_raw_mae, 2) == round(lin_scaled_mae, 2) else "different")
