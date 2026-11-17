def naive_mae(series, split, lag):
    errors = [abs(series[t] - series[t - lag]) for t in range(split, len(series))]
    return round(sum(errors) / len(errors), 3)

series = [10, 12, 11, 13, 12, 14, 13, 15]
print(naive_mae(series, 4, 1))
print(naive_mae(series, 4, 2))
