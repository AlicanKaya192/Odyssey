def skewed_columns(names, trained, live, tolerance):
    flagged = []
    for name, old, new in zip(names, trained, live):
        if old == 0:
            if new != 0:
                flagged.append(name)
        elif abs(new - old) > tolerance * abs(old):
            flagged.append(name)
    return flagged


names = ["tenure", "monthly_fee", "support_calls", "is_pro"]
trained = [36.7, 30.2, 0.74, 0.4]
live = [36.1, 0.75, 30.1, 0.0]
print(skewed_columns(names, trained, live, 0.5))
print(skewed_columns(names, trained, trained, 0.5))
