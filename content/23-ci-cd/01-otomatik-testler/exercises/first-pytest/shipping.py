def shipping_cost(weight_kg):
    if weight_kg <= 1:
        return 5
    if weight_kg <= 5:
        return 9
    return 9 + (weight_kg - 5) * 2
