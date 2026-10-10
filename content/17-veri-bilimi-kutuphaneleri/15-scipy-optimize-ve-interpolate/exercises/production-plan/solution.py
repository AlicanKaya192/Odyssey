from scipy import optimize


def plan(profits, hours, limits):
    cost = [-p for p in profits]
    free = [(0, None)] * len(profits)
    res = optimize.linprog(cost, A_ub=hours, b_ub=limits, bounds=free)
    return {"units": res.x.round(2).tolist(), "profit": round(float(-res.fun), 1)}

result = plan([30, 50], [[2, 4], [3, 2]], [80, 90])
print(result["units"], result["profit"])
