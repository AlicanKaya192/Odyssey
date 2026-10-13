import numpy as np


def top_words(components, vocab, k):
    return []

vocab = ["app", "card", "crash", "refund", "slow"]
components = [[0.9, 0.0, 0.7, 0.0, 0.4],
              [0.0, 0.8, 0.0, 0.6, 0.1]]
print(top_words(components, vocab, 2))
