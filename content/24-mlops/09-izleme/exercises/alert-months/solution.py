def alert_months(values, reference, limit, patience):
    alerts = []
    streak = 0
    for month, value in enumerate(values):
        if abs(value - reference) > limit:
            streak += 1
        else:
            streak = 0
        if streak >= patience:
            alerts.append(month)
    return alerts


rates = [0.20, 0.29, 0.34, 0.39, 0.50, 0.51, 0.59, 0.59]
print(alert_months(rates, rates[0], 0.1, 2))
print(alert_months(rates, rates[0], 0.1, 3))
print(alert_months([0.2, 0.35, 0.2, 0.35], 0.2, 0.1, 2))
