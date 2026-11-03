def ratio_of_sums(clicks, views):
    return round(sum(clicks) / sum(views), 4)


print(ratio_of_sums([1, 1, 2, 4, 0], [1, 2, 10, 40, 3]))
