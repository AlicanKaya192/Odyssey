from scipy import optimize


def plan(profits, hours, limits):
    return {"units": [], "profit": 0.0}

result = plan([30, 50], [[2, 4], [3, 2]], [80, 90])
print(result["units"], result["profit"])
