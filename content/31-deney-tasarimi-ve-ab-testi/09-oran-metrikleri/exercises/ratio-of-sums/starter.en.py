def ratio_of_sums(clicks, views):
    rates = [c / v for c, v in zip(clicks, views)]
    return round(sum(rates) / len(rates), 4)


print(ratio_of_sums([1, 1, 2, 4, 0], [1, 2, 10, 40, 3]))
