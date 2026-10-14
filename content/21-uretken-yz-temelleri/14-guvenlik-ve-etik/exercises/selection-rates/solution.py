def rates(chosen, group):
    result = []
    for k in (0, 1):
        picks = [c for c, g in zip(chosen, group) if g == k]
        result.append(round(sum(picks) / len(picks), 2))
    return result


print(rates([1, 0, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1]))
