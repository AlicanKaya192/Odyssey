def offer_value(churned, saved, cost):
    if churned == 1:
        return saved - cost
    return -cost


print(offer_value(1, 18, 5))
print(offer_value(0, 18, 5))
print(offer_value(1, 4, 5))
