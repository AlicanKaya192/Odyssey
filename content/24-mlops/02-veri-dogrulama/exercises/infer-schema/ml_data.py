"""Customer data for the MLOps exercises.

A subscription service wants to know which customers will cancel
(churn). Every call with the same arguments returns the same customers
on every computer: the data comes from a seeded `random.Random`, not
from a file.

    make_customers(n, seed=7, month=0)

`month` moves the data forward in time. From month 1 on, the
customers slowly change (data drift): they use the service less and pay
a little more. From month 4 on, the reason people leave changes too
(concept drift): support calls matter less and the price matters more.
"""
import csv
import math
import random

FEATURES = ["tenure", "monthly_fee", "support_calls", "usage_hours", "plan"]
NUMERIC = ["tenure", "monthly_fee", "support_calls", "usage_hours"]
PLANS = ["basic", "pro"]
TARGET = "churned"
CONCEPT_MONTH = 4


def _churn_chance(row, month):
    fee_weight, calls_weight = (0.04, 0.9) if month < CONCEPT_MONTH else (0.15, 0.1)
    score = (0.3 - 0.06 * row["tenure"] + fee_weight * (row["monthly_fee"] - 30)
             + calls_weight * row["support_calls"] - 0.09 * (row["usage_hours"] - 30))
    return 1 / (1 + math.exp(-score))


def make_customers(n, seed=7, month=0):
    """Return `n` customers as dictionaries (id, the five features, churned)."""
    rng = random.Random(f"{seed}-{month}")
    shift = min(month, 6) / 6
    rows = []
    for i in range(n):
        plan = "pro" if rng.random() < 0.4 else "basic"
        base_fee = 45.0 if plan == "pro" else 20.0
        row = {
            "id": f"C{month:02d}-{i + 1:05d}",
            "tenure": rng.randint(1, 72),
            "monthly_fee": round(max(5.0, rng.gauss(base_fee + 6 * shift, 4)), 2),
            "support_calls": min(10, int(rng.expovariate(1 / (1.2 + shift)))),
            "usage_hours": round(max(0.0, rng.gauss(32 - 10 * shift, 9)), 1),
            "plan": plan,
        }
        row[TARGET] = 1 if rng.random() < _churn_chance(row, month) else 0
        rows.append(row)
    return rows


def write_customers_csv(path, n, seed=7, month=0):
    """Write `make_customers(n, seed, month)` to a CSV file."""
    rows = make_customers(n, seed, month)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", *FEATURES, TARGET], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
