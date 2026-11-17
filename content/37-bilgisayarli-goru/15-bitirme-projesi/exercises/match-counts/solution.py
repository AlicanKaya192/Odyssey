def iou(a, b):
    width = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    common = width * height
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - common
    return common / union


def match_counts(predicted, truth, threshold):
    used = set()
    tp = fp = 0
    for box in sorted(predicted, key=lambda b: -b[5]):
        best, best_j = 0.0, -1
        for j, t in enumerate(truth):
            if j in used or t[4] != box[4]:
                continue
            value = iou(box, t)
            if value > best:
                best, best_j = value, j
        if best >= threshold:
            tp += 1
            used.add(best_j)
        else:
            fp += 1
    return [tp, fp, len(truth) - len(used)]

truth = [[0, 0, 10, 10, 0], [20, 20, 30, 30, 1]]
predicted = [[1, 0, 11, 10, 0, 0.9], [20, 20, 30, 30, 0, 0.8], [0, 1, 10, 11, 0, 0.7]]
print(match_counts(predicted, truth, 0.5))
