words = ["the", "cat", "and", "the", "dog", "and", "the", "bird", "sat", "on", "the", "mat"]

counts = {}
for word in words:
    if word in counts:
        counts[word] = counts[word] + 1
    else:
        counts[word] = 1

chosen = []
for round_number in range(3):
    best = None
    for word in counts:
        if word in chosen:
            continue
        if best is None or counts[word] > counts[best] or (counts[word] == counts[best] and word < best):
            best = word
    chosen.append(best)
    print(best, counts[best])
