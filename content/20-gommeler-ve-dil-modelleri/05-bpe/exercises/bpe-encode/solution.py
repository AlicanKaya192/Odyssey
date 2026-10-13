def merge_pair(symbols, pair):
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and [symbols[i], symbols[i + 1]] == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return out


def encode(word, merges):
    symbols = list(word) + ["</w>"]
    for pair in merges:
        symbols = merge_pair(symbols, pair)
    return symbols

merges = [["e", "r"], ["l", "o"], ["lo", "w"], ["er", "</w>"]]
print(encode("lower", merges))
print(encode("slow", merges))
