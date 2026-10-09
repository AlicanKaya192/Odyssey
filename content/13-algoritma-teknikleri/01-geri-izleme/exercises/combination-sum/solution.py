def combination_sum(candidates, target):
    values = sorted(candidates)
    result, path = [], []

    def backtrack(start, total):
        if total == target:
            result.append(path[:])
            return
        for i in range(start, len(values)):
            if total + values[i] > target:
                break
            path.append(values[i])
            backtrack(i + 1, total + values[i])
            path.pop()

    backtrack(0, 0)
    return result


print(combination_sum([10, 1, 2, 7, 6, 5], 8))
print(len(combination_sum(list(range(1, 41)), 30)))
