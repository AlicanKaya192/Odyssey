points = [
    ((2.0, 3.0), "A"),
    ((3.0, 3.5), "A"),
    ((8.0, 7.0), "B"),
    ((7.5, 8.0), "B"),
    ((2.5, 2.0), "A"),
]
new_point = (7.0, 7.5)

nx, ny = new_point
distances = [
    ((((x - nx) ** 2 + (y - ny) ** 2) ** 0.5), label)
    for (x, y), label in points
]
distances.sort()

print([round(d, 2) for d, _ in distances])
print(distances[0][1])
print([label for _, label in distances[:3]])
