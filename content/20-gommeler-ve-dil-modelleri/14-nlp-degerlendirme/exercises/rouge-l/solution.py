def rouge_l(candidate, reference):
    a, b = candidate.split(), reference.split()
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                table[i + 1][j + 1] = table[i][j] + 1
            else:
                table[i + 1][j + 1] = max(table[i][j + 1], table[i + 1][j])
    return round(table[-1][-1] / len(b), 3)

ref = "the parcel arrived damaged and the customer wants a refund"
print(rouge_l("the customer wants a refund", ref))
print(rouge_l("refund wants customer the", ref))
