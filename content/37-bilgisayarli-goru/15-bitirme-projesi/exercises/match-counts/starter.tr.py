def iou(a, b):
    width = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    common = width * height
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - common
    return common / union


def match_counts(predicted, truth, threshold):
    return [0, 0, 0]

truth = [[0, 0, 10, 10, 0], [20, 20, 30, 30, 1]]
predicted = [[1, 0, 11, 10, 0, 0.9], [20, 20, 30, 30, 0, 0.8], [0, 1, 10, 11, 0, 0.7]]
print(match_counts(predicted, truth, 0.5))
