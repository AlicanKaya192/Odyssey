def count_fits(grid, folds):
    total = folds
    for values in grid.values():
        total *= len(values)
    return total


def step_names(grid):
    return sorted({name.split("__")[0] for name in grid})

grid = {
    "tfidf__ngram_range": [[1, 1], [1, 2]],
    "tfidf__sublinear_tf": [False, True],
    "model__C": [0.1, 1, 10],
}
print(count_fits(grid, 5))
print(step_names(grid))
