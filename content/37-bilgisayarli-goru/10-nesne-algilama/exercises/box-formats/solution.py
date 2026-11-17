def to_xyxy(boxes):
    return [[x, y, x + w, y + h] for x, y, w, h in boxes]


def to_cxcywh(boxes):
    return [[(x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1] for x1, y1, x2, y2 in boxes]

print(to_xyxy([[4, 6, 10, 6], [0, 0, 5, 5]]))
print(to_cxcywh([[4, 6, 14, 12]]))
