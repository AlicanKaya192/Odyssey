def summary(log):
    tokens = sum(entry["tokens"] for entry in log)
    cost = sum(entry["cost"] for entry in log)
    return [len(log), tokens, round(cost, 6)]


log = [{"tokens": 150, "cost": 0.0001}, {"tokens": 90, "cost": 0.00006}]
print(summary(log))
