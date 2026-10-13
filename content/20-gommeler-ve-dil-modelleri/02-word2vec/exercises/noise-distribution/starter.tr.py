def noise_distribution(counts, alpha):
    return {}

counts = {"the": 800, "cat": 100, "throne": 4}
for word, p in noise_distribution(counts, 0.75).items():
    print(word, p)
