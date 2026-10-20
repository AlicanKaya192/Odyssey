def join_outcomes(log, outcomes, threshold):
    # Sonucu olanlari birlestir, dogrulari say.
    pass


log = [
    {"id": "C1", "churn_probability": 0.9},
    {"id": "C2", "churn_probability": 0.2},
    {"id": "C3", "churn_probability": 0.6},
    {"id": "C4", "churn_probability": 0.1},
]
outcomes = {"C1": 1, "C2": 0, "C3": 0}
print(join_outcomes(log, outcomes, 0.5))
