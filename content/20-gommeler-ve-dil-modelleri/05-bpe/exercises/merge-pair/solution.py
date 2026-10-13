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

print(merge_pair(["l", "o", "w", "</w>"], ["l", "o"]))
print(merge_pair(["a", "a", "a"], ["a", "a"]))
