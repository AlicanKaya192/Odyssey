def has_duplicate(items):
    comparisons = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            comparisons += 1
            if items[i] == items[j]:
                return True, comparisons
    return False, comparisons


print(has_duplicate([4, 4, 1, 2]))
print(has_duplicate([1, 2, 3, 2]))
print(has_duplicate(list(range(100))))
