def join_outcomes(log, outcomes, threshold):
    correct = 0
    total = 0
    for entry in log:
        if entry["id"] not in outcomes:
            continue
        predicted = 1 if entry["churn_probability"] >= threshold else 0
        correct += predicted == outcomes[entry["id"]]
        total += 1
    return [correct, total]


log = [
    {"id": "C1", "churn_probability": 0.9},
    {"id": "C2", "churn_probability": 0.2},
    {"id": "C3", "churn_probability": 0.6},
    {"id": "C4", "churn_probability": 0.1},
]
outcomes = {"C1": 1, "C2": 0, "C3": 0}
print(join_outcomes(log, outcomes, 0.5))
