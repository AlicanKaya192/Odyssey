"""A small churn model with fixed weights. It stands in for the registered model file."""
import math

VERSION = 3


def churn_probability(row):
    """Return the probability that this customer cancels (between 0 and 1)."""
    score = (0.3 - 0.06 * row["tenure"] + 0.04 * (row["monthly_fee"] - 30)
             + 0.9 * row["support_calls"] - 0.09 * (row["usage_hours"] - 30))
    return 1 / (1 + math.exp(-score))
