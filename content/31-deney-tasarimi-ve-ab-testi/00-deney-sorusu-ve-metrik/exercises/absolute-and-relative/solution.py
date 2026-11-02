def lift(rate_a, rate_b):
    points = (rate_b - rate_a) * 100
    relative = (rate_b - rate_a) / rate_a * 100
    return [round(points, 2), round(relative, 1)]


print(lift(0.117, 0.122))
print(lift(0.30, 0.27))
