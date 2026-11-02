import math


def weeks_needed(n_per_group, daily_users, traffic=1.0):
    days = 2 * n_per_group / daily_users
    return math.ceil(days / 7)


print(weeks_needed(47209, 3000))
print(weeks_needed(47209, 3000, traffic=0.5))
