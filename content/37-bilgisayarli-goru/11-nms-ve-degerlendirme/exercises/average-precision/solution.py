def average_precision(hits, total_truth):
    precisions, recalls = [], []
    tp = 0
    for k, hit in enumerate(hits, start=1):
        tp += hit
        precisions.append(tp / k)
        recalls.append(tp / total_truth)
    envelope = precisions[:]
    for i in range(len(envelope) - 2, -1, -1):
        envelope[i] = max(envelope[i], envelope[i + 1])
    ap, previous = 0.0, 0.0
    for recall, height in zip(recalls, envelope):
        ap += (recall - previous) * height
        previous = recall
    return round(ap, 3)

print(average_precision([1, 1, 0, 1, 1, 0, 0, 1, 0, 0], 6))
print(average_precision([1, 0, 1, 0], 2))
print(average_precision([0, 0, 1], 1))
