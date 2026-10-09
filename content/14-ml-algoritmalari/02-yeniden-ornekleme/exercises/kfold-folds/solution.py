def kfold_folds(n, k):
    folds = []
    start = 0
    for i in range(k):
        size = n // k + (1 if i < n % k else 0)
        folds.append(list(range(start, start + size)))
        start += size
    return folds

for test in kfold_folds(11, 3):
    print(test)
