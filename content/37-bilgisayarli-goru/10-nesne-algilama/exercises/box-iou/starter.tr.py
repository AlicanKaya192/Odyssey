def iou(a, b):
    return 0.0

truth = [10, 10, 20, 20]
for other in ([10, 10, 20, 20], [15, 10, 25, 20], [12, 12, 22, 22], [30, 30, 40, 40], [0, 0, 10, 10]):
    print(other, iou(truth, other))
