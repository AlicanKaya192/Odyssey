MAX_DROP, MAX_DRIFT, MAX_INVALID, MIN_GAIN = 0.05, 0.25, 0.05, 0.003


def decide_month(live, base, drift, invalid, candidate):
    if live >= base - MAX_DROP and drift <= MAX_DRIFT:
        return "keep"
    if invalid > MAX_INVALID:
        return "data rejected"
    if candidate < live + MIN_GAIN:
        return "kept out"
    return "promoted"


print(decide_month(0.813, 0.813, 0.07, 0.0, 0.0))
print(decide_month(0.778, 0.813, 0.578, 0.0, 0.782))
print(decide_month(0.787, 0.782, 0.326, 0.0, 0.784))
print(decide_month(0.691, 0.782, 0.575, 1.0, 0.784))
