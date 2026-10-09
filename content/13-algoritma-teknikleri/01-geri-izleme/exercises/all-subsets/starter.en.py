def subsets(items):
    result, path = [], []

    def backtrack(start):
        # Add the current path (a copy!), then choose - continue - undo.
        pass

    backtrack(0)
    return result


for subset in subsets([1, 2, 3]):
    print(subset)
print(len(subsets(list(range(10)))))
