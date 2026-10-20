from scorer import VERSION, churn_probability


def score_batch(rows):
    # Her musteri icin [id, olasilik, surum].
    pass


customers = [
    {"id": "C1", "tenure": 2, "monthly_fee": 45.0, "support_calls": 6, "usage_hours": 5.0},
    {"id": "C2", "tenure": 60, "monthly_fee": 20.0, "support_calls": 0, "usage_hours": 40.0},
    {"id": "C3", "tenure": 12, "monthly_fee": 30.0, "support_calls": 1, "usage_hours": 30.0},
]
for line in score_batch(customers):
    print(line)
