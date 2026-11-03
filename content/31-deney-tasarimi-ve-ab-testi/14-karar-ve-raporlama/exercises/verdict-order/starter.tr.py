def verdict(low, high, threshold=0.003):
    if high < threshold:
        return "not worth it"
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    return "inconclusive"


print(verdict(-0.0295, -0.0154))
print(verdict(0.0010, 0.0022))
