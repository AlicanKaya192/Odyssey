def abstain_scores(results):
    said = sum(nf for _, nf in results)
    no_answer = sum(not has for has, _ in results)
    right = sum(nf and not has for has, nf in results)
    precision = round(right / said, 2) if said else 0.0
    recall = round(right / no_answer, 2) if no_answer else 0.0
    return [precision, recall]


results = [[False, True], [False, True], [True, True], [True, False], [False, False]]
print(abstain_scores(results))
