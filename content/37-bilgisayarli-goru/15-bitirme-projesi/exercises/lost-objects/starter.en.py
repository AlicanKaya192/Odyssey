def lost_objects(scene, S, size):
    return 0

scene = [[2, 2, 10, 10, 0], [4, 4, 12, 12, 1], [20, 20, 30, 30, 2]]
print(lost_objects(scene, 4, 32))
print(lost_objects(scene, 8, 32))
