def mrr(ranks):
    return round(sum(1 / r for r in ranks if r) / len(ranks), 3)


print(mrr([1, None, 2, 1, 4]))
print(mrr([None, None]))
