def iou(a, b):
    width = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    common = width * height
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - common
    return common / union


def nms_by_hand(boxes, scores, threshold):
    order = sorted(range(len(boxes)), key=lambda i: -scores[i])
    keep = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= threshold for k in keep):
            keep.append(i)
    return keep

boxes = [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 9, 10]]
scores = [0.9, 0.8, 0.7, 0.95]
print(nms_by_hand(boxes, scores, 0.5))
print(nms_by_hand(boxes, scores, 0.9))
