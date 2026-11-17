def lost_objects(scene, S, size):
    cell = size / S
    taken = set()
    lost = 0
    for x1, y1, x2, y2, label in scene:
        key = (int((y1 + y2) / 2 // cell), int((x1 + x2) / 2 // cell))
        if key in taken:
            lost += 1
        taken.add(key)
    return lost

scene = [[2, 2, 10, 10, 0], [4, 4, 12, 12, 1], [20, 20, 30, 30, 2]]
print(lost_objects(scene, 4, 32))
print(lost_objects(scene, 8, 32))
