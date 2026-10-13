from collections import Counter

SENTENCES = [["my", "order", "is", "late"], ["my", "card", "was", "charged"],
             ["my", "order", "never", "came"], ["the", "order", "is", "late"]]


def greedy(sentences, max_len):
    padded = [["<s>"] + s + ["</s>"] for s in sentences]
    pairs = Counter((a, b) for s in padded for a, b in zip(s, s[1:]))
    word, out = "<s>", []
    while len(out) < max_len:
        after = {b: n for (a, b), n in pairs.items() if a == word}
        word = min(after, key=lambda w: (-after[w], w))
        if word == "</s>":
            break
        out.append(word)
    return out

print(greedy(SENTENCES, 10))
print(greedy(SENTENCES, 2))
