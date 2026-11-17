from dl_data import make_scenes


def scene_summary(n, seed):
    images, boxes, masks = make_scenes(n, size=32, seed=seed)
    objects = [box for scene in boxes for box in scene]
    per_class = [sum(1 for box in objects if box[4] == c) for c in range(3)]
    areas = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2, label in objects]
    return [len(objects), per_class, round(sum(areas) / len(areas), 1)]

print(scene_summary(100, 7))
print(scene_summary(50, 3))
