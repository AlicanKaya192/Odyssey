def combinations(matrix):
    combos = [{}]
    for key, values in matrix.items():
        grown = []
        for combo in combos:
            for value in values:
                new = combo.copy()
                new[key] = value
                grown.append(new)
        combos = grown
    return combos


matrix = {"os": ["ubuntu-latest", "windows-latest"], "python": ["3.12", "3.13"]}
for combo in combinations(matrix):
    print(combo)
print(len(combinations({"a": [1, 2, 3], "b": [1, 2], "c": [1, 2]})))
