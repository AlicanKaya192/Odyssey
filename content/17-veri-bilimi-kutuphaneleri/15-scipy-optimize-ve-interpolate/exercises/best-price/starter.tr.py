from scipy import optimize


def best_price(cost, max_price):
    def profit(price):
        return (price - cost) * (1000 - 8 * price)

    res = optimize.minimize_scalar(profit, bounds=(cost, max_price), method="bounded")
    return [round(float(res.x), 2), round(float(res.fun), 1)]

print(best_price(20, 125))
print(best_price(40, 125))
