from text_data import make_reviews


def shingles(text, n=5):
    text = " ".join(text.lower().split())
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)


def dedupe(n, threshold):
    kept = []
    for review in make_reviews(n):
        s = shingles(review["text"])
        if all(jaccard(s, other) < threshold for other in kept):
            kept.append(s)
    return len(kept)


print(dedupe(600, 1.0))
print(dedupe(600, 0.8))
