import math


def days_needed(n_per_group, daily_visitors):
    return math.ceil(2 * n_per_group / daily_visitors)


print(days_needed(6562, 1500))
print(days_needed(1000, 300))
