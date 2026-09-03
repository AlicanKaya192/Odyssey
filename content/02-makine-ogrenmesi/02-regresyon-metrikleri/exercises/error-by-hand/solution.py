actual = [210, 185, 340, 275, 190, 410, 260, 320]
predicted = [198, 192, 355, 260, 205, 380, 268, 310]

errors = [a - p for a, p in zip(actual, predicted)]
n = len(errors)

mae = sum(abs(e) for e in errors) / n
mse = sum(e ** 2 for e in errors) / n
rmse = mse ** 0.5

print(errors)
print(round(mae, 2))
print(round(mse, 2), round(rmse, 2))
