def lift(rate_a, rate_b):
    relative = (rate_b - rate_a) / rate_a
    return [round(relative * 100, 1), round(relative * 100, 1)]


print(lift(0.117, 0.122))
print(lift(0.30, 0.27))
