def first_warning(signals):
    months = max((len(values) for values in signals.values()), default=0)
    for month in range(months):
        fired = sorted(name for name, values in signals.items()
                       if month < len(values) and values[month])
        if fired:
            return [month, fired]
    return None


signals = {
    "accuracy": [False, False, False, False, True, True],
    "predicted_rate": [False, False, True, True, True, True],
    "usage_mean": [False, False, True, True, True, True],
}
print(first_warning(signals))
print(first_warning({"accuracy": [False, False]}))
