def subsets(items):
    result, path = [], []

    def backtrack(start):
        result.append(path[:])
        for i in range(start, len(items)):
            path.append(items[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result


for subset in subsets([1, 2, 3]):
    print(subset)
print(len(subsets(list(range(10)))))
