def noise_distribution(counts, alpha):
    weights = {w: n ** alpha for w, n in counts.items()}
    total = sum(weights.values())
    return {w: round(x / total, 3) for w, x in weights.items()}

counts = {"the": 800, "cat": 100, "throne": 4}
for word, p in noise_distribution(counts, 0.75).items():
    print(word, p)
