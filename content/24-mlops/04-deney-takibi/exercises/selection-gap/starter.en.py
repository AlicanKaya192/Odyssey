def selection_gap(scores):
    # Find the model with the best validation score, compute its leads over both means.
    pass


scores = [[0.80, 0.76], [0.83, 0.77], [0.79, 0.78], [0.81, 0.75]]
gap = selection_gap(scores)
print("validation lead:", gap["val_lead"])
print("test lead:", gap["test_lead"])
