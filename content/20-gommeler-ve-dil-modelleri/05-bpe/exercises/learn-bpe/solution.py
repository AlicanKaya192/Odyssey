from collections import Counter


def merge(symbols, pair):
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def learn_bpe(counts, n_merges):
    words = {tuple(w) + ("</w>",): n for w, n in counts.items()}
    merges = []
    for _ in range(n_merges):
        pairs = Counter()
        for symbols, n in words.items():
            for a, b in zip(symbols, symbols[1:]):
                pairs[a, b] += n
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))
        merges.append(list(best))
        new_words = Counter()
        for symbols, n in words.items():
            new_words[merge(symbols, best)] += n
        words = new_words
    return merges

counts = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
for rule in learn_bpe(counts, 5):
    print(rule)
