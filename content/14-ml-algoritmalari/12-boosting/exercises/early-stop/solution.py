def early_stop(val_errors, patience):
    best, best_round, waited = float("inf"), 0, 0
    for n, err in enumerate(val_errors, 1):
        if err < best:
            best, best_round, waited = err, n, 0
        else:
            waited += 1
        if waited == patience:
            return best_round, n
    return best_round, len(val_errors)

errors = [5.0, 4.0, 3.5, 3.6, 3.4, 3.45, 3.5, 3.55, 3.6]
print(early_stop(errors, 3))
print(early_stop([3.0, 2.0, 1.0], 5))
