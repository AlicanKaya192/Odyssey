from dl_data import make_scenes


def lost_share(n, seed, S):
    images, boxes, masks = make_scenes(n, size=32, seed=seed)
    cell = 32 / S
    lost = 0
    objects = 0
    for scene in boxes:
        taken = set()
        for x1, y1, x2, y2, label in scene:
            key = (int((y1 + y2) / 2 // cell), int((x1 + x2) / 2 // cell))
            lost += key in taken
            taken.add(key)
            objects += 1
    return round(lost / objects, 3)

for grid in (2, 4, 8):
    print(grid, lost_share(200, 7, grid))
