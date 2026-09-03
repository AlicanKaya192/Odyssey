from sklearn.linear_model import LinearRegression

areas = [50, 60, 70, 80, 90, 100, 110, 120]
prices = [155, 178, 205, 228, 250, 278, 300, 325]

X = [[a] for a in areas]

model = LinearRegression()
model.fit(X, prices)

print(round(model.coef_[0], 2))
print(round(model.intercept_, 2))
print(round(model.predict([[95]])[0], 2))
