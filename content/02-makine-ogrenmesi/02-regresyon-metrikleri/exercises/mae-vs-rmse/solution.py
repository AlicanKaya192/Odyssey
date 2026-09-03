truth = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
model_a = [110, 90, 110, 90, 110, 90, 110, 90, 110, 90]
model_b = [100, 100, 100, 100, 100, 100, 100, 100, 100, 200]

from sklearn.metrics import mean_absolute_error, mean_squared_error

for name, guess in (("a", model_a), ("b", model_b)):
    mae = mean_absolute_error(truth, guess)
    rmse = mean_squared_error(truth, guess) ** 0.5
    print(name, round(mae, 2), round(rmse, 2))
