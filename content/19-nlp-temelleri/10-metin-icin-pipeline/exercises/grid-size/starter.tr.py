def count_fits(grid, folds):
    return 0


def step_names(grid):
    return []

grid = {
    "tfidf__ngram_range": [[1, 1], [1, 2]],
    "tfidf__sublinear_tf": [False, True],
    "model__C": [0.1, 1, 10],
}
print(count_fits(grid, 5))
print(step_names(grid))
