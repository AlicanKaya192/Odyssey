def combination_sum(candidates, target):
    values = sorted(candidates)
    result, path = [], []

    def backtrack(start, total):
        # Hedef tuttu mu? Sonra sec - devam et - geri al; gecince break.
        pass

    backtrack(0, 0)
    return result


print(combination_sum([10, 1, 2, 7, 6, 5], 8))
print(len(combination_sum(list(range(1, 41)), 30)))
