train_prices = [250, 310, 180, 420, 275, 350]
test_prices = [300, 200, 380]

baseline = sum(train_prices) / len(train_prices)
errors = [abs(p - baseline) for p in test_prices]

print(round(baseline, 2))
print([round(e, 2) for e in errors])
print(round(sum(errors) / len(errors), 2))
