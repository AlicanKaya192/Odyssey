import math


def perplexity(probs):
    if any(p == 0 for p in probs):
        return math.inf
    mean_log = sum(math.log(p) for p in probs) / len(probs)
    return round(math.exp(-mean_log), 2)

print(perplexity([0.5, 0.5, 0.5]))
print(perplexity([0.9, 0.1, 0.5, 0.25]))
print(perplexity([0.5, 0.0]))
