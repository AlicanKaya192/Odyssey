from collections import Counter


def build_vocab(sentences, min_count):
    counts = Counter(w for s in sentences for w in s)
    kept = sorted(w for w, c in counts.items() if c >= min_count)
    return ["<pad>", "<unk>"] + kept

data = [["the", "cat", "sat"], ["the", "dog"], ["a", "cat"]]
print(len(build_vocab(data, 1)))
print(build_vocab(data, 2))
