def histogram(values, bins, low, high):
    counts = [0] * bins
    width = (high - low) / bins
    for v in values:
        if v < low or v > high:
            continue
        i = min(int((v - low) / width), bins - 1)
        counts[i] += 1
    return counts

print(histogram([0.5, 1.5, 1.7, 2.0, 3.9, 4.0, -1.0, 4.5], 4, 0, 4))
