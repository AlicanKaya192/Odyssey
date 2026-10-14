def key_recall(results, keys):
    return 0.0


results = [["valid for 3 years", "x"], ["free shipping"], ["y", "30 days"]]
print(key_recall(results, ["3 years", "4.90", "30 days"]))
