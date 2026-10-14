def combinations(matrix):
    # Tek bir bos birlesimle basla.
    combos = [{}]
    return combos


matrix = {"os": ["ubuntu-latest", "windows-latest"], "python": ["3.12", "3.13"]}
for combo in combinations(matrix):
    print(combo)
print(len(combinations({"a": [1, 2, 3], "b": [1, 2], "c": [1, 2]})))
