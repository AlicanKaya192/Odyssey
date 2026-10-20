def selection_gap(scores):
    best_val, its_test = scores[0]
    for val, test in scores:
        if val > best_val:
            best_val, its_test = val, test
    val_mean = sum(val for val, _ in scores) / len(scores)
    test_mean = sum(test for _, test in scores) / len(scores)
    return {"val_lead": round(best_val - val_mean, 3), "test_lead": round(its_test - test_mean, 3)}


scores = [[0.80, 0.76], [0.83, 0.77], [0.79, 0.78], [0.81, 0.75]]
gap = selection_gap(scores)
print("validation lead:", gap["val_lead"])
print("test lead:", gap["test_lead"])
