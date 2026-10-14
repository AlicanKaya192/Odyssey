def opportunity_gap(chosen, group, suitable):
    result = []
    for k in (0, 1):
        picks = [c for c, g, s in zip(chosen, group, suitable) if g == k and s == 1]
        result.append(sum(picks) / len(picks))
    return [round(result[0], 2), round(result[1], 2), round(result[0] - result[1], 2)]


print(opportunity_gap([1, 0, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1], [1, 1, 0, 1, 1, 0]))
