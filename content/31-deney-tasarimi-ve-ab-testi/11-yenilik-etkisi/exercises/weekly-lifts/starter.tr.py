def weekly_lifts(daily_a, daily_b):
    lifts = []
    for start in range(0, len(daily_a), 7):
        lifts.append(round(daily_b[start] / daily_a[start] - 1, 3))
    return lifts


a = [10, 11, 12, 10, 11, 12, 10, 10, 10, 11, 10, 11, 10, 10]
b = [13, 13, 13, 12, 12, 12, 12, 11, 10, 11, 11, 11, 10, 11]
print(weekly_lifts(a, b))
