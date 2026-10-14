def cart_total(prices, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
