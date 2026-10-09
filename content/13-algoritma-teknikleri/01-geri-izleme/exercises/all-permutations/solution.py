def permutations(items):
    result, path, used = [], [], [False] * len(items)

    def backtrack():
        if len(path) == len(items):
            result.append(path[:])
            return
        for i, x in enumerate(items):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return result


for order in permutations([1, 2, 3]):
    print(order)
print(len(permutations(list(range(7)))))
