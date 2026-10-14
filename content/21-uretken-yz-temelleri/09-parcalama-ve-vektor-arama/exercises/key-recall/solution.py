def key_recall(results, keys):
    found = sum(any(key in chunk for chunk in chunks) for chunks, key in zip(results, keys))
    return round(found / len(keys), 2)


results = [["valid for 3 years", "x"], ["free shipping"], ["y", "30 days"]]
print(key_recall(results, ["3 years", "4.90", "30 days"]))
