import math


def perplexity(probs):
    mean_log = sum(math.log(p) for p in probs) / len(probs)
    return round(math.exp(-mean_log), 3)

print(perplexity([0.5, 0.5, 0.5]))
print(perplexity([0.9, 0.1, 0.8, 0.6]))
