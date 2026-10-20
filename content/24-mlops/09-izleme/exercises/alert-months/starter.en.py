def alert_months(values, reference, limit, patience):
    # Count consecutive crossings; add the month when patience runs out.
    pass


rates = [0.20, 0.29, 0.34, 0.39, 0.50, 0.51, 0.59, 0.59]
print(alert_months(rates, rates[0], 0.1, 2))
print(alert_months(rates, rates[0], 0.1, 3))
print(alert_months([0.2, 0.35, 0.2, 0.35], 0.2, 0.1, 2))
