points = [
    ((2.0, 1.0), "A"), ((1.5, 2.0), "A"), ((3.0, 1.5), "A"),
    ((7.0, 8.0), "B"), ((8.0, 7.5), "B"), ((6.5, 7.0), "B"),
    ((4.5, 4.0), "A"), ((5.0, 5.5), "B"),
]
new_point = (5.0, 4.5)

nx, ny = new_point
pairs = sorted((round(((x - nx) ** 2 + (y - ny) ** 2) ** 0.5, 2), label)
               for (x, y), label in points)

print([d for d, _ in pairs])

for k in (1, 3, 5):
    nearest = [label for _, label in pairs[:k]]
    winner = "A" if nearest.count("A") > nearest.count("B") else "B"
    print(k, nearest, winner)
