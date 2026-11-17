def iou(a, b):
    width = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    common = width * height
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - common
    return round(common / union, 3)

truth = [10, 10, 20, 20]
for other in ([10, 10, 20, 20], [15, 10, 25, 20], [12, 12, 22, 22], [30, 30, 40, 40], [0, 0, 10, 10]):
    print(other, iou(truth, other))
