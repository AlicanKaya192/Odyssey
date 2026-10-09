def rank(records):
    ordered = sorted(records, key=lambda r: (-r[1], r[0]))
    return [r[0] for r in ordered]


print(rank([["Cem", 80], ["Ada", 92], ["Bora", 80]]))
print(rank([["Zeki", 70], ["Mert", 70], ["Lale", 70]]))
