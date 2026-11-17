def nms_by_hand(boxes, scores, threshold):
    return []

boxes = [[0, 0, 10, 10], [1, 1, 11, 11], [20, 20, 30, 30], [0, 0, 9, 10]]
scores = [0.9, 0.8, 0.7, 0.95]
print(nms_by_hand(boxes, scores, 0.5))
print(nms_by_hand(boxes, scores, 0.9))
